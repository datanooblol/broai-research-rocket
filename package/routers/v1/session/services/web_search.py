from package.database.web_register.model import UrlRecords, UrlRecord, WebStatus
from package.utils.searxng import SearxngSearchOptions, search_searxng
from broai.experiments.chunk import split_overlap
from broai.interface import Context
import json
from package.workers.scrape_worker import scrape_worker
from celery import group
import os
import shutil


class WebSearchService:
    def __init__(self, webDB, sessionDB, knowledgeDB):
        self.webDB = webDB
        self.sessionDB = sessionDB
        self.knowledgeDB = knowledgeDB

    def web_search(self, session_id: str) -> UrlRecords:
        opts = SearxngSearchOptions(
            engines=["google", "bing", "DuckDuckGo"],
            language="en",
            pageno=1
        )
        records = self.sessionDB.get_session(session_id)
        record = records.to_dict(orient="records")[0]
        parsed_outline = record.get("parsed_outline")
        parsed_outline = json.loads(parsed_outline)
        results = []
        for section in parsed_outline:
            questions = section.get("questions", [])
            for question in questions:
                # this will be fixed for whitelist
                results.append(search_searxng(query=question, opts=opts))
        urls_obj = []
        url_list = []
        for urls in results:
            for url in urls.results:
                if url.url not in url_list:
                    url_list.append(url.url)
                    urls_obj.append(UrlRecord(url=url.url, content=url.content))
        return UrlRecords(session_id=session_id, urls=urls_obj)

    def web_register(self, session: UrlRecords) -> UrlRecords:
        urls = [
            UrlRecord(url=url.url, content=url.content) 
            for url in session.urls
        ]
        found_df = self.webDB.check_urls(urls)
        found_urls = found_df['url'].tolist()
        selected_urls = UrlRecords(session_id=session.session_id, urls=[
            UrlRecord(url=url.url, content=url.content)
            for url in urls
            if url.url not in found_urls
        ])
        if len(selected_urls.urls) > 0:
            self.webDB.register(selected_urls)
            
        print("found urls from search engine:", len(urls))
        print("start scraping with selected urls:", len(selected_urls.urls))
        return selected_urls

    def delete_tmp(self, session_id: str):
        dir_path = os.path.join("./tmp", session_id)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
    
    def load_all_json_files(self, session_id: str):
        dir_path = os.path.join("./tmp", session_id)
        data_list = []
    
        if not os.path.exists(dir_path):
            print(f"No folder found for session: {session_id}")
            return data_list
    
        for filename in os.listdir(dir_path):
            if filename.endswith(".json"):
                file_path = os.path.join(dir_path, filename)
                with open(file_path, "r") as f:
                    try:
                        data = json.load(f)
                        data_list.append(data)
                    except json.JSONDecodeError as e:
                        print(f"Skipping {filename}: Invalid JSON - {e}")
    
        return data_list
    
    def web_scrape(self, session: UrlRecords) -> None:
        urls = [uc.url for uc in session.urls]
        session_id = session.session_id
        jobs = group([scrape_worker.s(session_id, url) for url in urls])
        results = jobs.apply_async()
        _ = results.get()
        self.webDB.update_status([
            UrlRecord(url_id=uc.url_id, url=uc.url, content="", remark="", status=WebStatus.DOING)
            for uc in session.urls
        ])
        all_data = self.load_all_json_files(session_id)
        all_contexts = []
        for data in all_data:
            url = list(data.keys())[0]
            context = Context(context=data[url], metadata={"source": url})
            contexts = split_overlap([context])
            all_contexts.extend(contexts)
        self.knowledgeDB.add_contexts(contexts)
        self.webDB.update_status([
            UrlRecord(url_id=uc.url_id, url=uc.url, content="", remark="", status=WebStatus.DONE)
            for uc in session.urls
        ])
        self.delete_tmp(session_id)

    def run(self, session_id):
        results = self.web_search(session_id)
        scrap_urls = self.web_register(results)
        self.web_scrape(scrap_urls)
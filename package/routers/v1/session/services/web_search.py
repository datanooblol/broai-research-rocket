from package.database.web_register.model import UrlRecords, UrlRecord, WebStatus
from package.lib.searxng import SearxngSearchOptions, search_searxng
from broai.experiments.web_scraping import scrape_by_jina_ai
from broai.experiments.cleanup_markdown import clean_up_markdown_link
from broai.experiments.chunk import split_overlap
from broai.interface import Context
import json


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
        return selected_urls

    def web_scrape(self, session: UrlRecords) -> None:
        for uc in session.urls:
            url = uc.url
            self.webDB.update_status([
                UrlRecord(
                    url_id=uc.url_id,
                    url=url,
                    content="",
                    remark="",
                    status=WebStatus.DOING
                )
            ])
            try:
                text = scrape_by_jina_ai(url)
                text = clean_up_markdown_link(text)
                context = Context(context=text, metadata={"source": url})
                contexts = split_overlap([context])
                self.knowledgeDB.add_contexts(contexts)
                self.webDB.update_status([
                    UrlRecord(
                        url_id=uc.url_id,
                        url=url,
                        content="",
                        remark="",
                        status=WebStatus.DONE
                    )
                ])
            except Exception as e:
                self.webDB.update_status([
                    UrlRecord(
                        url_id=uc.url_id,
                        url=url,
                        content="",
                        remark=f"{e}",
                        status=WebStatus.ERROR
                    )
                ])

    def run(self, session_id):
        results = self.web_search(session_id)
        scrap_urls = self.web_register(results)
        self.web_scrape(scrap_urls)
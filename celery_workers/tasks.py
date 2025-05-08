from celery_workers.controller import celery_app
from celery import chord, chain
from time import sleep
from broai.experiments.web_scraping import scrape_by_jina_ai
from broai.experiments.cleanup_markdown import clean_up_markdown_link
from uuid import uuid4

# celery_app = celery_app
# @celery_app.task
# def scrape_worker(url: str):
#     text = scrape_by_jina_ai(url)
#     text = clean_up_markdown_link(text)
#     with open(f"./webpages/{uuid4()}.md", "w") as f:
#         f.write(text)

@celery_app.task
def scrape_worker(url: str):
    # scrape and store in vector DB
    sleep(2)
    return f"stored: {url}"

@celery_app.task
def after_scraping(results):
    # trigger retrieval using vector DB (just return dummy for now)
    return ["retrieved_chunk1", "retrieved_chunk2"]

@celery_app.task
def generate_response(retrieved_chunks):
    # call LLM (return dummy text for now)
    return f"LLM response based on: {retrieved_chunks}"

@celery_app.task
def send_to_chat_app(message):
    print(f"Sending to chat app: {message}")
    return "Delivered"

def start_pipeline(urls: list[str]):
    return chord(
        [scrape_worker.s(url) for url in urls],
        body=chain(
            after_scraping.s(),
            generate_response.s(),
            send_to_chat_app.s()
        )
    ).delay()
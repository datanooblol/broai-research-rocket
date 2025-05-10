from package.workers.controller import celery_app
from broai.experiments.web_scraping import scrape_by_jina_ai
from broai.experiments.cleanup_markdown import clean_up_markdown_link
import os
from uuid import uuid4
import json


@celery_app.task
def scrape_worker(session_id: str, url: str):
    dir_path = os.path.join("./tmp", session_id)
    os.makedirs(dir_path, exist_ok=True)
    # Write the JSON file
    file_path = os.path.join(dir_path, f"{uuid4()}.json")
    text = scrape_by_jina_ai(url)
    text = clean_up_markdown_link(text)
    with open(file_path, "w") as f:
        json.dump({url: text}, f, indent=2)
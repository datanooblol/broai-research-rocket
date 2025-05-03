from fastapi import FastAPI
from pydantic import BaseModel, Field
from package.interfaces.session_record import SessionRecord
from package.lib.parse_outline import parse_outline

app = FastAPI()

@app.get("/")
def health():
    return {"message": "alive"}

@app.post("/start-session")
def start_session(session:SessionRecord):
    """
    Steps:
        - convert outline, save in session_memory: id, tone_of_voice, outline, retrieved_json, summarized_json, publish
        - enrich outline (optional)
        - search with searxng
        - register web
        - scrape web
        - summarize
        - publish
    """
    return {"response": parse_outline(session.outline)}
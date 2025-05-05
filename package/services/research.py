import requests
from dotenv import load_dotenv
import os
from typing import Dict, Any

load_dotenv()  # take environment variables
ENDPOINT = os.getenv("ENDPOINT")


class ResearchService:
    def __init__(
        self,
        ENDPOINT: str = os.getenv("ENDPOINT"),
    ):
        self.ENDPOINT = ENDPOINT

    def post(
        self, session_id: str, user_id: str, endpoint: str
    ) -> Dict[str, Any]:
        headers = {"Content-type": "application/json"}
        payload = {
            "session_id": session_id,
            "user_id": user_id
        }
        response = requests.post(
            f"{self.ENDPOINT}/v1/session/research/{endpoint}",
            headers=headers,
            json=payload
        )
        return response.json()

    def search(self, session_id: str, user_id: str) -> Dict[str, Any]:
        return self.post(session_id, user_id, "search")

    def retrieve(self, session_id: str, user_id: str) -> Dict[str, Any]:
        return self.post(session_id, user_id, "retrieve")

    def enrich(self, session_id: str, user_id: str) -> Dict[str, Any]:
        return self.post(session_id, user_id, "enrich")

    def publish(self, session_id: str, user_id: str) -> Dict[str, Any]:
        return self.post(session_id, user_id, "publish")
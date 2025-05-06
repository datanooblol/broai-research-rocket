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
        self, session_id: str, user_id: str, endpoint: str, **kwargs
    ) -> Dict[str, Any]:
        headers = {"Content-type": "application/json"}
        payload = {
            "session_id": session_id,
            "user_id": user_id
        }
        n_retrieve = kwargs.get("n_retrieve", None)
        n_rerank = kwargs.get("n_rerank", None)
        if isinstance(n_retrieve, int) and isinstance(n_rerank, int):
            payload.update({
                "n_retrieve": n_retrieve,
                "n_rerank": n_rerank
            })
        response = requests.post(
            f"{self.ENDPOINT}/v1/session/research/{endpoint}",
            headers=headers,
            json=payload
        )
        return response.json()

    def search(self, session_id: str, user_id: str) -> Dict[str, Any]:
        return self.post(session_id, user_id, "search")

    def retrieve(self, session_id: str, user_id: str, n_retrieve: int, n_rerank: int) -> Dict[str, Any]:
        return self.post(session_id, user_id, "retrieve", n_retrieve=n_retrieve, n_rerank=n_rerank)

    def enrich(self, session_id: str, user_id: str) -> Dict[str, Any]:
        return self.post(session_id, user_id, "enrich")

    def publish(self, session_id: str, user_id: str) -> Dict[str, Any]:
        return self.post(session_id, user_id, "publish")
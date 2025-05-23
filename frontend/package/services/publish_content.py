import requests
from dotenv import load_dotenv
import os
import json

class PublishService:
    def __init__(
        self,
        ENDPOINT: str = os.getenv("ENDPOINT"),
    ):
        self.ENDPOINT = ENDPOINT

    def post(self, session_id: str, user_id: str, username: str,  endpoint: str):
        headers = {"Content-type": "application/json"}
        payload = {
            "session_id": session_id,
            "user_id": user_id,
            "username": username
        }
        response = requests.post(
            f"{self.ENDPOINT}/v1/session/content/{endpoint}",
            headers=headers,
            json=payload
        )
        return response.json()

    def publish_content(self, session_id: str, user_id: str, username: str):
        return self.post(session_id, user_id, username, "publish")
import requests
from dotenv import load_dotenv
import os
import json


load_dotenv()  # take environment variables
ENDPOINT = os.getenv("ENDPOINT")

class BrainService:
    def __init__(self, ENDPOINT=ENDPOINT):
        self.ENDPOINT = ENDPOINT

    def list_contents(self):
        headers = {"Content-type": "application/json"}

        response = requests.get(f"{ENDPOINT}/v1/brain", headers=headers)
        return response.json()["contents"]

    def get_content(self, session_id: str):
        headers = {"Content-type": "application/json"}
        payload = {"session_id": session_id}
        response = requests.post(f"{ENDPOINT}/v1/brain/get-content", headers=headers, json=payload)
        return response.json()["contents"]
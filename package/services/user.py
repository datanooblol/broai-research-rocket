import requests
from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables

class UserAPI:
    def __init__(self, ENDPOINT=os.getenv("ENDPOINT")):
        self.ENDPOINT = ENDPOINT

    def post(self, username, password, endpoint):
        headers = {"Content-type": "application/json"}
        payload = {
            "username": username,
            "password": password,
        }
        response = requests.post(f"{self.ENDPOINT}/v1/user/{endpoint}", headers=headers, json=payload)
        return response.status_code, response.json()

    def register(self, username, password):
        return self.post(username, password, "register")

    def login(self, username, password):
        return self.post(username, password, "login")
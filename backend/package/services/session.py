import requests
from dotenv import load_dotenv
import os
import json


load_dotenv()  # take environment variables
ENDPOINT = os.getenv("ENDPOINT")


def list_sessions(user_id):
    headers = {"Content-type": "application/json"}
    payload = {
        "user_id": user_id,
    }
    response = requests.post(f"{ENDPOINT}/v1/session/list", headers=headers, json=payload)
    return response.json()["response"]


def get_outline(user_id, session_id):
    headers = {"Content-type": "application/json"}
    payload = {
        "session_id": session_id,
        "user_id": user_id,
    }
    response = requests.post(f"{ENDPOINT}/v1/session/outline", headers=headers, json=payload)
    return response.json()


def generate_outline(instruction):
    headers = {"Content-type": "application/json"}
    payload = {
        "instruction": instruction,
    }
    response = requests.post(f"{ENDPOINT}/v1/session/generate-outline", headers=headers, json=payload)
    return response.json()


def update_outline(session_id, tone_of_voice, outline):
    headers = {"Content-type": "application/json"}
    payload = {
        "session_id": session_id,
        "tone_of_voice": tone_of_voice,
        "outline": outline
    }
    
    response = requests.put(f"{ENDPOINT}/v1/session/update-outline", headers=headers, json=payload)


def get_whitelist(user_id, session_id):
    headers = {"Content-type": "application/json"}
    payload = {
        "session_id": session_id,
        "user_id": user_id,
    }
    response = requests.post(f"{ENDPOINT}/v1/session/whitelist", headers=headers, json=payload)
    return response.json()

def update_whitelist(session_id, whitelist):
    headers = {"Content-type": "application/json"}
    payload = {
        "session_id": session_id,
        "whitelist": whitelist
    }
    
    response = requests.put(f"{ENDPOINT}/v1/session/update-whitelist", headers=headers, json=payload)

class DisplayService:
    def __init__(self, ENDPOINT: str = os.getenv("ENDPOINT")):
        self.ENDPOING = ENDPOINT

    def post(self, session_id: str, user_id: str, endpoint: str):
        headers = {"Content-type": "application/json"}
        payload = {
            "session_id": session_id,
            "user_id": user_id
        }
        response = requests.post(f"{ENDPOINT}/v1/session/{endpoint}", headers=headers, json=payload)
        response = response.json()
        if "error" in response:
            return None
        return response

    def knowledge(self, session_id, user_id):
        return self.post(session_id, user_id, "knowledge")

    def enrich(self, session_id, user_id):
        return self.post(session_id, user_id, "enrich")

    def publish(self, session_id, user_id):
        return self.post(session_id, user_id, "publish")


def create_session(user_id):
    headers = {"Content-type": "application/json"}
    payload = {
        "user_id": user_id,
    }
    response = requests.post(f"{ENDPOINT}/v1/session/create", headers=headers, json=payload)
    return response.json()["session_id"]
        
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

def update_outline(session_id, tone_of_voice, outline):
    headers = {"Content-type": "application/json"}
    payload = {
        "session_id": session_id,
        "tone_of_voice": tone_of_voice,
        "outline": outline
    }
    
    response = requests.put(f"{ENDPOINT}/v1/session/update-outline", headers=headers, json=payload)


def research(session_id, user_id):
    headers = {"Content-type": "application/json"}
    payload = {
        "session_id": session_id,
        "user_id": user_id
    }
    response = requests.post(f"{ENDPOINT}/v1/session/research", headers=headers, json=payload)


def knowledge(session_id, user_id):
    headers = {"Content-type": "application/json"}
    payload = {
        "session_id": session_id,
        "user_id": user_id
    }
    response = requests.post(f"{ENDPOINT}/v1/session/knowledge", headers=headers, json=payload)
    return response.json()


def enrich(session_id, user_id):
    headers = {"Content-type": "application/json"}
    payload = {
        "session_id": session_id,
        "user_id": user_id
    }
    response = requests.post(f"{ENDPOINT}/v1/session/enrich", headers=headers, json=payload)
    return response.json()


def publish(session_id, user_id):
    headers = {"Content-type": "application/json"}
    payload = {
        "session_id": session_id,
        "user_id": user_id
    }
    response = requests.post(f"{ENDPOINT}/v1/session/publish", headers=headers, json=payload)
    return response.json()


def create_session(user_id):
    headers = {"Content-type": "application/json"}
    payload = {
        "user_id": user_id,
    }
    response = requests.post(f"{ENDPOINT}/v1/session/create", headers=headers, json=payload)
    return response.json()["session_id"]
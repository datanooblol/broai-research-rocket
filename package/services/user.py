import requests
from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables
ENDPOINT = os.getenv("ENDPOINT")

def login(username, password):
    headers = {"Content-type": "application/json"}
    payload = {
        "username": username,
        "password": password,
    }
    response = requests.post(f"{ENDPOINT}/v1/user/login", headers=headers, json=payload)
    # if response.status_code == 200:
    return response.status_code, response.json()
    # return None
import requests
BASE_URL = "http://localhost:8080"

def call_api(endpoint, valid=True):
    payload = {"sample": "data"} if valid else {}
    return requests.post(f"{BASE_URL}{endpoint}", json=payload)

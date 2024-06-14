from config import TRANSLATE_TOKEN
import requests

def call_api(url: str, data: dict) -> dict:
    headers = {"Authorization" : f"Api-Key {TRANSLATE_TOKEN}"}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()

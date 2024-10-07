import requests
import json
import base64

UPSTAGE_API_URL = "https://api.upstage.ai/v1/document-ai/ocr"

def upstage_ocr(file_path, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    with open(file_path, "rb") as file:
        files = {"document": file}
        response = requests.post(UPSTAGE_API_URL, headers=headers, files=files)
    
    if response.status_code == 200:
        return response.json()["text"]
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

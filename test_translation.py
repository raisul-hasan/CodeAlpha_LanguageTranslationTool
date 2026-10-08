import os
import requests
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("AZURE_TRANSLATOR_KEY")
region = os.getenv("AZURE_TRANSLATOR_REGION")
endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")

url = endpoint.rstrip("/") + "/translate"

params = {
    "api-version": "3.0",
    "from": "en",
    "to": "bn"
}

headers = {
    "Ocp-Apim-Subscription-Key": key,
    "Ocp-Apim-Subscription-Region": region,
    "Content-Type": "application/json"
}

body = [
    {
        "Text": "Hello, how are you?"
    }
]

response = requests.post(
    url,
    params=params,
    headers=headers,
    json=body,
    timeout=20
)

print("Status:", response.status_code)
print("Response:")
print(response.json())
import requests
import subprocess
import json
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_REPO_OWNER = os.getenv("GITHUB_REPO_OWNER")
GITHUB_REPO_NAME = os.getenv("GITHUB_REPO_NAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
WEBHOOK_ID = os.getenv("WEBHOOK_ID")

def get_ngrok_url():
    try:
        response = subprocess.check_output(['curl', 'http://localhost:4040/api/tunnels'])
        data = json.loads(response)
        return data['tunnels'][0]['public_url']
    except Exception as e:
        print(f"Error getting ngrok URL: {e}")
        return None

def update_github_webhook(ngrok_url):
    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/hooks/{WEBHOOK_ID}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "config": {
            "url": ngrok_url,
            "content_type": "json"
        }
    }
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Webhook updated successfully.")
    else:
        print(f"Failed to update webhook: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    ngrok_url = get_ngrok_url()
    if ngrok_url:
        ngrok_url = ngrok_url + "/github-webhook/"
        update_github_webhook(ngrok_url)

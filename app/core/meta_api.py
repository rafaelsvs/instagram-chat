import os
import httpx

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
GRAPH_URL = "https://graph.facebook.com/v19.0"

def send_message(user_id, message):
    url = f"{GRAPH_URL}/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": user_id},
        "message": {"text": message}
    }
    httpx.post(url, json=payload)

def get_user_info(user_id):
    url = f"{GRAPH_URL}/{user_id}?fields=name,username&access_token={PAGE_ACCESS_TOKEN}"
    r = httpx.get(url)
    if r.status_code == 200:
        return r.json()
    return {}

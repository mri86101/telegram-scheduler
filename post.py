import os
import requests

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
event = os.environ.get("POST_EVENT", "AM")

if event == "AM":
    text = "📌 평일 오전 9시 자동 글입니다."
else:
    text = "📌 평일 오후 3시 30분 자동 글입니다."

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
r = requests.post(url, data={"chat_id": CHAT_ID, "text": text})
r.raise_for_status()
print("Sent!")

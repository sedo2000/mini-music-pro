from db import users
import requests, os

BOT_TOKEN=os.getenv("BOT_TOKEN")
BASE=f"https://api.telegram.org/bot{BOT_TOKEN}"

def broadcast(text):
    for u in users():
        try:
            requests.post(BASE+"/sendMessage",
                data={"chat_id":u,"text":text})
        except:
            pass

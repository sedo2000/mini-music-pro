import os, json, requests
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from db import add_user, add_track, list_tracks
from admin import broadcast

app=FastAPI()

TOKEN=os.getenv("BOT_TOKEN")
BASE=f"https://api.telegram.org/bot{TOKEN}"
DEV=8582402572
WEBAPP=os.getenv("WEBAPP_URL")

# ---------- helpers ----------

def msg(cid,text,kb=None):
    data={"chat_id":cid,"text":text}
    if kb:
        data["reply_markup"]=json.dumps(kb)
    requests.post(BASE+"/sendMessage",data=data)

# ---------- webhook ----------

@app.post("/")
async def hook(req:Request):
    u=await req.json()

    if "message" not in u:
        return {"ok":True}

    m=u["message"]
    cid=m["chat"]["id"]
    add_user(cid)

    text=m.get("text","")

    # start
    if text.startswith("/start"):
        kb={"inline_keyboard":[[
            {"text":"🎵 Open Player",
             "web_app":{"url":WEBAPP}}
        ]]}
        msg(cid,"Welcome to Mini Music 🚀",kb)

    # admin
    elif text.startswith("/admin"):
        if cid!=DEV:
            msg(cid,"No access")
        else:
            msg(cid,"Admin:\n/sendall TEXT\nUpload audio to add")

    # broadcast
    elif text.startswith("/sendall") and cid==DEV:
        broadcast(text.replace("/sendall",""))
        msg(cid,"Sent ✅")

    # audio upload
    elif "audio" in m and cid==DEV:
        file_id=m["audio"]["file_id"]

        file=requests.get(BASE+"/getFile",
            params={"file_id":file_id}).json()

        path=file["result"]["file_path"]

        url=f"https://api.telegram.org/file/bot{TOKEN}/{path}"
        data=requests.get(url).content

        name=path.split("/")[-1]
        save=f"music/{name}"

        with open(save,"wb") as f:
            f.write(data)

        add_track(name,save)
        msg(cid,"Uploaded 🎶")

    return {"ok":True}

# ---------- API ----------

@app.get("/tracks")
def tracks():
    return JSONResponse(list_tracks())

@app.get("/stream/{name}")
def stream(name:str):
    return FileResponse(f"music/{name}")

import logging
import os
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import uvicorn
from integrations import twitch

class TwitchCredentials(BaseModel):
    twitch_token: str
    initial_channels: str

class AuthInfo(BaseModel):
    twitch_auth: TwitchCredentials


# Initialize logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.post("/start_bot")
async def start_bot(body: AuthInfo):
    twitch.start_bot(body.twitch_auth)
    return {"status": "success"}

@app.post("/stop_bot")
async def stop_bot():
    await twitch.stop_bot()
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

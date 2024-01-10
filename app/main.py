import logging
import os
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import uvicorn
from integrations.inputs import twitch_bot

# {
#   "twitch_auth": {
#     "twitch_token": "{{TOKEN}}",
#     "initial_channels": "DuckTapeDevOps, MatisseTec",
#     "emojis": {
#         "computing_emoji": "duckta12Type"
#     }

class TwitchCredentials(BaseModel):
    twitch_token: str
    initial_channels: str
    emojis: dict

class AuthInfo(BaseModel):
    twitch_auth: TwitchCredentials


# Initialize logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.post("/start_bot")
async def start_bot(body: AuthInfo):
    twitch_bot.start_bot(body.twitch_auth)
    print("Started Twitch Bot")
    return {"status": "success"}

@app.post("/stop_bot")
async def stop_bot():
    await twitch_bot.stop_bot()
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

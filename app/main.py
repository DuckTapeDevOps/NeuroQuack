import logging
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import uvicorn
from inputs import twitch_bot


# {
#   "twitch_auth": {
#     "twitch_token": "{{TOKEN}}",
#     "initial_channels": "DuckTapeDevOps, MatisseTec"
#      }
# }

class TwitchCredentials(BaseModel):
    twitch_token: str
    initial_channels: str

class AuthInfo(BaseModel):
    twitch_auth: TwitchCredentials
    replicate_token: str


# Initialize logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()


REPLICATE_API_TOKEN = None


@app.post("/start_bot")
async def start_bot(body: AuthInfo):
    global REPLICATE_API_TOKEN
    REPLICATE_API_TOKEN = body.replicate_token
    print("Started Twitch Bot")
    print(f"Initial Channels: {body.twitch_auth.initial_channels}")
    print("Starting bot...")
    twitch_bot.start_bot(body.twitch_auth)
    print("Started Twitch Bot")
    return {"status": "success"}

@app.post("/stop_bot")
async def stop_bot():
    await twitch_bot.stop_bot()
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

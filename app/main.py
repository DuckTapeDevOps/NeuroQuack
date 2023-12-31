import asyncio
import logging
import os
from mangum import Mangum
from pydantic import BaseModel
from twitchio.ext import commands
from fastapi import FastAPI, HTTPException
import uvicorn


# Initialize logging
logging.basicConfig(level=logging.INFO)

# TWITCH_TOKEN = os.environ.get("TWITCH_TOKEN", "TWITCH_TOKEN not set")
# INITIAL_CHANNELS = os.environ.get("INITIAL_CHANNELS", "INITIAL_CHANNELS not set") # Comma separated list of channels to join

app = FastAPI()

bot = None

class TwitchInfo(BaseModel):
    twitch_token: str
    initial_channels: str

@app.post("/start_bot")
async def start_stream(body: TwitchInfo):
    twitch_token = body.twitch_token
    initial_channels = body.initial_channels
    global bot
    if bot is not None:
        raise HTTPException(status_code=400, detail="Stream already running")

    bot = TwitchBot(twitch_token, initial_channels.split(","))
    asyncio.create_task(bot.start())
    return {"status": "success"}

@app.post("/stop_bot")
async def stop_stream():
    global bot
    if bot is None:
        raise HTTPException(status_code=400, detail="Stream not running")

    await bot.close()
    bot = None
    return {"status": "success"}

class TwitchBot(commands.Bot):
    def __init__(self, token, channels):
        print(f"Initializing TwitchBot with channels {channels}")
        super().__init__(token=token, prefix="!", initial_channels=channels)

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        # Attempt to process the message
        try:
            await self.handle_commands(message)
        except AttributeError as e:
            if "object has no attribute '_ws'" in str(e):
                print(f"Error: Message author is None. Message content: {message.content}")
            else:
                raise e

    @commands.command(name="hello")
    async def hello_command(self, ctx):
        print(f"Received command: {ctx.message.content}")
        await ctx.send(f"Hello {ctx.author.name}!")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


handler = Mangum(app)
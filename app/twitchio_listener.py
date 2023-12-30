import json
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
import os
from twitchio.ext import commands
import functionality.diffusion as diffusion
import functionality.llm as llm
import textwrap  # Add this line to import the textwrap module
# Initialize logging
logging.basicConfig(level=logging.INFO)

TWITCH_TOKEN = os.environ.get("TWITCH_TOKEN", "TWITCH_TOKEN not set")
INITIAL_CHANNELS = os.environ.get("INITIAL_CHANNELS", "INITIAL_CHANNELS not set")

class TwitchBot(commands.Bot):
    def __init__(self):
        channel_list = INITIAL_CHANNELS.split(",")
        print(f"Initializing TwitchBot with channels {channel_list}")
        super().__init__(token=TWITCH_TOKEN, prefix="!", initial_channels=channel_list)

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
        await ctx.send(f"Testing this one {ctx.author.name}!")

    # @commands.command(name="llm")
    # async def llama_command(self, ctx):
    #     await llm.LLM_Query(ctx)

    # @commands.command(name="sdxl")
    # async def sdxl_command(self, ctx):
    #     await diffusion.diffuser_query(ctx)

    
            
if __name__ == "__main__":
    bot = TwitchBot()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.run())

import asyncio
from twitchio.ext import commands
from fastapi import HTTPException
from integrations import llm, diffusers


bot = None

def start_bot(body):
    twitch_token = body.twitch_token
    initial_channels = body.initial_channels
    global bot
    if bot is not None:
        raise HTTPException(status_code=400, detail="Stream already running")

    bot = TwitchBot(twitch_token, initial_channels.split(","))
    asyncio.create_task(bot.start())

async def stop_bot():
    global bot
    if bot is None:
        raise HTTPException(status_code=400, detail="Stream not running")

    await bot.close()
    bot = None

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
            
    @commands.command(name="ping")
    async def ping_command(self, ctx):
        print(f"Received command: {ctx.message.content}")
        await ctx.send(f"Pong! {ctx.author.name}")

    @commands.command(name="hello")
    async def hello_command(self, ctx):
        print(f"Received command: {ctx.message.content}")
        await ctx.send(f"Hello {ctx.author.name}!")

    @commands.command(name="llm")
    async def llm_command(self, ctx):
        # !llm mistral explain my next step 
        split = ctx.message.content.split(" ")
        llm_type = split[1]
        temp_addon = " return the result in under 500 characters as a response to a user in chat"
        prompt = " ".join(split[2:])+temp_addon
        print(f"Received command: {ctx.message.content}")
        print(f"Prompt: {prompt}")
        response = llm.prompt_llm(llm_type, prompt)
        answer = response.split(temp_addon)[-1]
        print(f"Response: {answer}")
        await ctx.send(" @" + ctx.author.name+ ": " + answer)

    @commands.command(name="diffuse")
    async def diffuse_command(self, ctx):
        split = ctx.message.content.split(" ")
        diffuser_type = split[1]
        prompt = " ".join(split[2:])
        print(f"Received command: {ctx.message.content}")
        print(f"Prompt: {prompt}")
        response = await diffusers.prompt_diffuser(diffuser_type, prompt)
        print(f"Response: {response}")
        await ctx.send(" @" + ctx.author.name+ ": " + response)
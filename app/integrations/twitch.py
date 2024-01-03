import asyncio
from twitchio.ext import commands
from fastapi import HTTPException
from integrations import llm, diffusers


bot = None

def start_bot(body):
    '''
    Starts the Twitch bot
    '''
    twitch_token = body.twitch_token
    initial_channels = body.initial_channels
    global bot
    if bot is not None:
        raise HTTPException(status_code=400, detail="Stream already running")

    bot = TwitchBot(twitch_token, initial_channels.split(","))
    asyncio.create_task(bot.start())

async def stop_bot():
    '''
    Stops the Twitch bot
    '''
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
        await self.send(f"Logged in as | {self.nick}")

    async def event_message(self, message):
        # Attempt to process the message
        try:
            await self.handle_commands(message)
        except AttributeError as e:
            # This is a known issue with TwitchIO where messages from the bot itself will throw an error
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
        split = ctx.message.content.split(" ") # ["!llm", "mistral", "explain", "my", "next", "step"]
        llm_type = split[1] # "mistral"

        if llm_type == "help":  # !llm help
            await ctx.send(llm.help_text)
            return
        
        temp_addon = " return the result in under 500 characters as a response to a user in chat" 
        prompt = " ".join(split[2:])+temp_addon # "explain my next step"
        print(f"Received command: {ctx.message.content}") # !llm mistral explain my next step
        print(f"Prompt: {prompt}") # explain my next step

        response = llm.query(llm_type, prompt) # "mistral", "explain my next step"
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
        response = diffusers.prompt_diffuser(diffuser_type, prompt)
        print(f"Response: {response}")
        await ctx.send(" @" + ctx.author.name+ " generated " +prompt + " using " + diffuser_type )

    @commands.command(name="welcome")
    async def welcome_command(self, ctx):
        #Setting up intro variables
        diffuser_type = "sdxl"
        llm_type = "mistral"
        split = ctx.message.content.split(" ")
        welcomee = split[1]
        initial_prompt = " ".join(split[2:]) 
        augmented_prompt = initial_prompt + " using descriptive words in plain english to paint a picture of the scene"


        await ctx.send(f"Welcome to the stream "+ welcomee + "! Use '!commands' to see what I can do!")

        user_profile_img = ctx.author.profile_image_url
        await ctx.send(user_profile_img)

        # diffuser_prompt = llm.query(llm_type, augmented_prompt)
        # print(diffuser_prompt)
        # minimize_prompt = "Summarize the following in under 500 characters to fit in my Twitch chat as a response to a user: " + diffuser_prompt
        # diffuser_prompt = llm.query(llm_type, minimize_prompt)
        # print("Minimized Response: \n" + diffuser_prompt)
        # await ctx.send(diffuser_prompt)
        # diffusers.prompt_diffuser(diffuser_type, diffuser_prompt)
        # await ctx.send(" @" + ctx.author.name + " generated " +initial_prompt + " using " + diffuser_type + " and " + llm_type)

    @commands.command(name="commands")
    async def commands_command(self, ctx):
        print(f"Received command: {ctx.message.content}")
        await ctx.send(f"Available commands: !ping, !hello, !llm, !diffuse, !commands")
import asyncio
from twitchio.ext import commands
from twitchio import Client
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

# def get_user_profile_url(client, username):
#     users = client.fetch_users(names=[username])
#     if users:
#         user = users[0]
#         return user.profile_image
#     else:
#         return None

class TwitchBot(commands.Bot):
    def __init__(self, token, channels):
        print(f"Initializing TwitchBot with channels {channels}")
        super().__init__(token=token, prefix="!", initial_channels=channels)
        self.twitch_client = Client(token=token)

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')

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
        message = ctx.message.content
        prompt_map = {
            "user": ctx.author.name,
            "diffuser_type": message.split(" ")[1], 
            "prompt":  " ".join(message.split(" ")[2:])
        }
        if prompt_map['diffuser_type'] == "help" or prompt_map['prompt'] == "help":
            await ctx.send(diffusers.help_text)
            return
        print(f"Received command: {ctx.message.content}")
        print(f"Prompt: {prompt_map['prompt']}")
        
        response = diffusers.prompt_diffuser(prompt_map)
        print(f"Response: {response}")
        await ctx.send(" @" + prompt_map['user'] + " generated " + prompt_map['prompt'] + " using " + prompt_map['diffuser_type'] )
    
    @commands.command(name="welcome")
    async def welcome_command(self, ctx):
        #Setting up intro variables
        split = ctx.message.content.split(" ")
        welcomee = split[1].strip("@")

        users = await self.twitch_client.fetch_users(names=[welcomee])
        if users:
            user = users[0]
            profile_image_url = user.profile_image
        print(f"{welcomee}'s profile image URL is: {profile_image_url}")
        prompt_map = {
            "user": welcomee,
            "diffuser_type": "sdxl",
            "prompt":  "an astronaut joining the Ducktronaut crew to venture into the Matrix",
            "image_url": profile_image_url,
            "title": "welcome image"
        }
        diffusers.prompt_diffuser_image_to_image(prompt_map)

    @commands.command(name="commands")
    async def commands_command(self, ctx):
        print(f"Received command: {ctx.message.content}")
        await ctx.send(f"Available commands: !ping, !hello, !llm, !diffuse, !commands")
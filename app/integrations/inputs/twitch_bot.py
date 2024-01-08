import asyncio
import io
from jsonschema import ValidationError
from twitchio.ext import commands
from twitchio import Client, PartialUser
from fastapi import HTTPException
from integrations import llm, diffusers, utility, clip
from PIL import Image
import concurrent.futures


from pydantic import BaseModel
from typing import Optional

class Command(BaseModel):
    command: str
    target_user: Optional[str] = None
    extra_param: Optional[str] = None

    @classmethod
    def from_message(cls, message_content: str):
        split = message_content.split(" ")
        command = split[0].lstrip("!")
        target_user = split[1].strip("@") if len(split) > 1 else None
        extra_param = split[2] if len(split) > 2 else None
        return cls(command=command, target_user=target_user, extra_param=extra_param)
    
loading_emoji = "duckta12Type"



bot = None
twitch_token = None
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
            
    # commands
        # !test
        # !llm neural what is foobar
        # !diffuse sdxl foo looking like bar
        # !interrogate @user
        # !welcome @user
        # !manipulate @user into an emoji 
            
    # Example usage in your command method
    @commands.command(name="test")
    async def test_command(self, ctx):
        try:
            command = Command.from_message(ctx.message.content)
            print(f"Received command: {command.command}, Target User: {command.target_user}")
            # Rest of your logic here
            await ctx.send(f"Test successful!")
        except ValidationError as e:
            # Handle validation errors
            print("Invalid command format")

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
        """
        !llm help
        !llm mistral explain my next step
        """
        # !llm mistral explain my next step 
        split = ctx.message.content.split(" ") # ["!llm", "mistral", "explain", "my", "next", "step"]
        llm_type = split[1] # "mistral"

        if llm_type == "help":  # !llm help
            await ctx.send(llm.help_text)
            return
        
        temp_addon = "Respond in less than 500 characters as a chatbot would: " 
        prompt = temp_addon+" ".join(split[2:]) # "explain my next step"
        print(f"Received command: {ctx.message.content}") # !llm mistral explain my next step
        print(f"Prompt: {prompt}") # explain my next step

        response = llm.query(llm_type, prompt) # "mistral", "explain my next step"
        answer = response.split(prompt)[-1]
        print(f"Response: {answer}") 

        # Considering the length of username and additional characters in the message
        max_length = 450 - len(ctx.author.name) - 4 # 4 for " @: "
        if len(answer) > max_length:
            answer = answer[:max_length] + ".."

        await ctx.send(" @" + ctx.author.name+ ": " + answer)
        # Splitting the answer into chunks of 500 characters
        # chunks = [answer[i:i+500] for i in range(0, len(answer), 500)]

        # for chunk in chunks:
        #     await ctx.send(" @" + ctx.author.name+ ": " + chunk)

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
        await ctx.send(" @" + prompt_map['user'] + " generated this image:" + response[0])
    
    @commands.command(name="so")
    async def so_command(self, ctx):
        #Setting up intro variables
        print(f"Received command: {ctx.message.content}")
        split = ctx.message.content.split(" ")
        welcomee = split[1].strip("@")
        users = await self.twitch_client.fetch_users(names=[welcomee])
        if users:
            user = users[0]
            profile_image_url = user.profile_image

        print(f"{welcomee}'s profile image URL is: {profile_image_url}")

        filename, image_bytes = utility.download_image(profile_image_url, "temp/profile_images", f"{welcomee}.png")
        try:
            shoutout_message = await PartialUser.shoutout(self, twitch_token, welcomee, 491187438)
            await ctx.send(shoutout_message)
            await ctx.send(loading_emoji + " @" + ctx.author.name)
            response = clip.clip_interrogate(filename)
            print(f"Interrogation response: {response}")
            await ctx.send(f"Shoutout to {welcomee}! duckta12Cheers")

            # Create a text-to-image rendering
            image_response = await diffusers.text_to_image(welcomee, response)
            await ctx.send(f"Check out this cool image of @{welcomee}: {image_response}")

            # Post the streamer's description to chat
            await ctx.send(f"Here's a bit about {welcomee}: REALLY COOL, I WEAR! ducta12Bang ")
        except Exception as e:
            print(f"Error in !so command: {e}")
            await ctx.send(f"Error: {e}")


    @commands.command(name="welcome")
    async def welcome_command(self, ctx):
        response = await self.interrogate_command(ctx)
        print(response)
        # response ="a close up of a person wearing a plague mask and goggles, plague mask, the plague doctor, plague doctor, plague doctor mask, she wear red eyed gasmask, bladee from drain gang, gothic - cyberpunk, masked, ( ( ( synthwave ) ) ), profile picture 1024px, profile photo, avatar image, gas mask, cyberpunk techwear"

        #Setting up intro variables
        split = ctx.message.content.split(" ")
        welcomee = split[1].strip("@")
        try:
            await ctx.send(" @" + ctx.author.name+ ": welcome to the crew! You look just like " + response)
            await diffusers.text_to_image(welcomee, response)
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")

    @commands.command(name="interrogate")
    async def interrogate_command(self, ctx):
        #Setting up intro variables
        split = ctx.message.content.split(" ")
        welcomee = split[1].strip("@")
        users = await self.twitch_client.fetch_users(names=[welcomee])
        if users:
            user = users[0]
            profile_image_url = user.profile_image

        print(f"{welcomee}'s profile image URL is: {profile_image_url}")

        filename, image_bytes = utility.download_image(profile_image_url, "temp/profile_images", f"{welcomee}.png")
        try:
            await ctx.send(loading_emoji + " @" + ctx.author.name)
            response = clip.clip_interrogate(filename)
            print(f"Interrogation response: {response}")
            
            await ctx.send(" @" + ctx.author.name+ "really looks like... " + response)
            return response
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")

    @commands.command(name="commands")
    async def commands_command(self, ctx):
        print(f"Received command: {ctx.message.content}")
        await ctx.send(f"Available commands: !ping, !hello, !llm, !diffuse, !commands")
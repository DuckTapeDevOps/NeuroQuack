import asyncio
import datetime
import io
import os
from jsonschema import ValidationError
from twitchio.ext import commands
from twitchio import Client, PartialUser
from fastapi import HTTPException
from tasks import diffusers, clip
from utility import input_map, computing, download_image
# from utility.cost import analysis, prediction
from PIL import Image
import concurrent.futures


from pydantic import BaseModel
from typing import Optional

BOT_NAME = os.environ.get("BOT_NAME", "not-set")

help_text = "duckta12Lul"
llm_text = "In order to use an llm, you must choose a model and an inferencing method. For example, !llm sdxl foo looking like bar"



loading_emoji = "duckta12NeuroQuack"
discord_invite = "https://discord.gg/4D5qzdEh"
github_url = "https://github.com/DuckTapeDevOps"
# TTS
pronunciation = {
    "k8s" : "kates",
}




bot = None
emojis = None
twitch_token = None
def start_bot(body):
    '''
    Starts the Twitch bot
    '''
    twitch_token = body.twitch_token
    initial_channels = body.initial_channels
    global bot, emojis
    emojis = body.emojis
    if bot is not None:
        raise HTTPException(status_code=400, detail="Stream already running")

    bot = TwitchBot(twitch_token, initial_channels.split(","))
    asyncio.create_task(bot.start())
    print(f"Started Twitch Bot in channels {initial_channels}")
    
    # bot.get_channel("ducktapedevops").send(f"Cost prediction: $1.00/hr")
    return {"status": "success"}

async def stop_bot():
    '''
    Stops the Twitch bot
    '''
    global bot
    if bot is None:
        raise HTTPException(status_code=400, detail="Stream not running")
    # response = CostAnalysis.get_cost_analysis()
    # print(f"Cost analysis: {response}")
    # await bot.get_channel("neuroquack").send(f"Cost analysis: {response}")
    await bot.close()
    bot = None

class TwitchBot(commands.Bot):
    def __init__(self, token, channels):
        print(f"Initializing TwitchBot with channels {channels}")
        super().__init__(token=token, prefix="@"+ BOT_NAME , initial_channels=channels)
        self.user_interactions = {}
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

    async def _process_input(self, ctx): # First step in processing a command
        """
        Processes the input and fetches profile image URL if needed.
        !

        Args:
            ctx: The context of the command.

        Returns:
            A tuple containing the processed input and user object.
        """
        print(f"Received command: {ctx.message.content}")
        input_map_response = input_map(ctx)
        user = input_map_response["user"]
        print(f"User: {user}")
        input = input_map_response["input"]
        print(f"Input: {input}")

        await ctx.send(computing(user))
        if "@" in input:
            target = input.strip("@")
            target_list = await self.twitch_client.fetch_users(names=[target])
            if target_list:
                target_info = target_list[0]
                profile_image_url = target_info.profile_image
                print(f"profile_image: {profile_image_url}")
                return user, target, profile_image_url

        return user, "no_user", input
            
    async def handle_first_interaction(self, user):
        current_time = datetime.now()
        last_interaction = self.user_interactions.get(user.name)
        print(f"Last interaction: {last_interaction}")

        if not last_interaction or last_interaction.date() < current_time.date():
            # This is the first interaction of the day
            print(f"First interaction of the day for {user.name}")
            # Perform your desired action here

            # Update the record
            self.user_interactions[user.name] = current_time

    @commands.command(name="help")
    async def help_command(self, ctx):
        await ctx.send(help_text)

    @commands.command(name="really?")
    async def really_command(self, ctx):
        await ctx.send("duckta12Cheers")

    @commands.command(name="github")
    async def github_command(self, ctx):
        await ctx.send(f"Check out all the project I'll never finish! {github_url}")

    @commands.command(name="discord")
    async def discord_command(self, ctx):
        await ctx.send(f"Join the Discord! {discord_invite}")

    @commands.command(name="ping")
    async def ping_command(self, ctx):
        await ctx.send(f"Pong! {ctx.author.name}")

    @commands.command(name="llm")
    async def llm_command(self, ctx):
        await ctx.send(f"Try llm-neural or llm-mistral")
    
    @commands.command(name="llm-neural")
    async def llm_neural_command(self, ctx):
        user, target, input = await self._process_input(ctx) # {user of the command}{target}{target_profile_url OR prompt}
        print(f"User: {user}")
        print(f"Target: {target}")
        print(f"Input: {input}")
    
    @commands.command(name="diffuse-sdxl")
    async def diffuse_sdxl_command(self, ctx):
        user, target, prompt = await self._process_input(ctx)
        print(f"User: {user}")
        print(f"Target: {target}")
        print(f"Input: {prompt}")
        response = diffusers.text_to_image_replicate(user, input)
        await ctx.send(" @" + user + " generated this image:" + response[0])

    @commands.command(name="diffuse")
    async def diffuse_command(self, ctx):
        """
        !diffuse help
        !diffuse sdxl foo looking like bar
        """
        await ctx.send(computing(ctx.author.name))
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
        target = split[1].strip("@")
        users = await self.twitch_client.fetch_users(names=[target])
        if users:
            user = users[0]
            profile_image_url = user.profile_image

        print(f"{target}'s profile image URL is: {profile_image_url}")

        filename, image_bytes = download_image(profile_image_url, "temp/profile_images", f"{target}.png")
        try:
            shoutout_message = await PartialUser.shoutout(self, twitch_token, target, 491187438)
            await ctx.send(shoutout_message)
            await ctx.send(loading_emoji + " @" + target)
            response = clip.clip_interrogate(filename)
            print(f"Interrogation response: {response}")
            await ctx.send(f"Shoutout to {target}! duckta12Cheers")

            # Create a text-to-image rendering
            image_response = await diffusers.text_to_image(target, response)
            await ctx.send(f"Check out this cool image of @{target}: {image_response}")

            # Post the streamer's description to chat
            await ctx.send(f"Here's a bit about {target}: REALLY COOL, I WEAR! ducta12Bang ")
        except Exception as e:
            print(f"Error in !so command: {e}")
            await ctx.send(f"Error: {e}")
    
    @commands.command(name="remove_bg")
    async def remove_bg_command(self, ctx):
        user, target, input = await self._process_input(ctx) # {user of the command}{target}{target_profile_url OR prompt}
        response_url = diffusers.background_removal(input)
        print(f"Response: {response_url}")
        await ctx.send(" @" + user + ": " + "Background removed: "+ response_url)


    @commands.command(name="replicate")
    async def replicate_command(self, ctx):
        """
        !replicate help
        Replicate takes in a url and returns a new image based on that image's interrogation response
        """
        #Setting up intro variables
        user, target, input = await self._process_input(ctx) # {user of the command}{target}{target_profile_url OR prompt}
        try:
            print(f"Interrogating: {input}")
            ci_response = clip.clip_interrogate(input)
            print(f"Interrogation response: {ci_response}")
            prompt_map = {
                "user": user,
                "diffuser_type": "sdxl_replicate",
                "prompt":  ci_response
            }
            sdxl_response = diffusers.prompt_diffuser(prompt_map)
            print(f"Response: {sdxl_response}")
            await ctx.send(" @" + target + ": " + sdxl_response[0])
            return sdxl_response
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")

    @commands.command(name="emoji")
    async def emoji_command(self, ctx):
        """
        !emoji help
        !emoji @user
        """
        #Setting up intro variables
        user, target, input = await self._process_input(ctx)
        DEFAULT_THEME = "ducktronaut funko pop"
        try:
            ci_response = clip.clip_interrogate(input)
            print(f"Interrogation response: {ci_response}")
            prompt_map = {
                "user": user,
                "diffuser_type": "emoji",
                "prompt":  ci_response
            }
            sdxl_response = diffusers.prompt_diffuser(prompt_map)
            print(f"Response: {sdxl_response}")
            await ctx.send(" @" + prompt_map['user'] + " looks like: " + sdxl_response[0])
            return sdxl_response
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")

    @commands.command(name="caption")
    async def caption_command(self, ctx):
        """
        !caption help
        !caption @user
        """
        #Setting up intro variables
        user, target, input = await self._process_input(ctx)
        try:
            await ctx.send(loading_emoji + " @" + user)
            caption = clip.image_to_caption(input) # input is the image url
            print(f"Captioning response: {caption}")
            await ctx.send(" @" + user + " captioned: " + caption)
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")

    @commands.command(name="welcome")
    async def welcome_command(self, ctx):
        response = await self.interrogate_command(ctx)
        print(response)
        # response ="a close up of a person wearing a plague mask and goggles, plague mask, the plague doctor, plague doctor, plague doctor mask, she wear red eyed gasmask, bladee from drain gang, gothic - cyberpunk, masked, ( ( ( synthwave ) ) ), profile picture 1024px, profile photo, avatar image, gas mask, cyberpunk techwear"

        #Setting up intro variables
        split = ctx.message.content.split(" ")
        target = split[1].strip("@")
        try:
            await ctx.send(" @" + ctx.author.name+ ": welcome to the crew! You look just like " + response)
            await diffusers.text_to_image(target, response)
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")

    @commands.command(name="interrogate")
    async def interrogate_command(self, ctx):
        user, target, input = await self._process_input(ctx) # {user of the command}{target}{target_profile_url OR prompt}
        print(f"Interrogating: {input} for {user}")
        try:
            print(f"Interrogating: {input}")
            response = clip.clip_interrogate(input)
            print(f"Interrogation response: {response}")
            
            await ctx.send(" @" + user + "really looks like... " + response)
            return response
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")

    @commands.command(name="commands")
    async def commands_command(self, ctx):
        print(f"Received command: {ctx.message.content}")
        await ctx.send(f"Available commands: !ping, !hello, !llm, !diffuse, !commands")
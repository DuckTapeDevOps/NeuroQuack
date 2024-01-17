import asyncio
import datetime
import os
from twitchio.ext import commands
from twitchio import Client
from fastapi import HTTPException
from tasks import diffusers, clip
from utility import computing, download_image
# from utility.cost import analysis, prediction


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
        print(f"Processing input: {ctx.message.content}")
        await ctx.send(loading_emoji)
        bot_name, command, prompt = ctx.message.content.split(" ", 2)
        user = ctx.author.name
        if "@" in prompt:
            target = prompt.strip("@")
            target_list = await self.twitch_client.fetch_users(names=[target])
            if target_list:
                target_info = target_list[0]
                profile_image_url = target_info.profile_image
                print(f"profile_image: {profile_image_url}")
                return user, command, target, profile_image_url

        return user, command, bot_name, prompt
            
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
        user, command, target, prompt = await self._process_input(ctx) # {user of the command}{target}{target_profile_url OR prompt}
        print(f"User: {user}")
        print(f"Command: {command}")
        print(f"Target: {target}")
        print(f"Input: {prompt}")
    
    @commands.command(name="diffuse-sdxl")
    async def diffuse_sdxl_command(self, ctx):
        user, command, target, prompt = await self._process_input(ctx)
        print(f"User: {user}")
        print(f"Target: {target}")
        print(f"Input: {prompt}")
        try:
            response = await diffusers.text_to_image_replicate(user, prompt)
            await ctx.send(" @" + user + " generated this image: " + response[0])
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")

    @commands.command(name="remove-bg")
    async def remove_bg_command(self, ctx):
        user, command, target, prompt = await self._process_input(ctx)
        print(f"User: {user}")
        print(f"Target: {target}")
        print(f"Input: {prompt}")
        response = diffusers.background_removal(prompt)
        await ctx.send(" @" + user + " generated this image: " + response[0])


    
    @commands.command(name="emoji")
    async def emoji_command(self, ctx):
        user, command, target, prompt = await self._process_input(ctx)
        print(f"User: {user}")
        print(f"Target: {target}")
        print(f"Input: {prompt}")
        response = diffusers.emoji_diffuser(prompt)
        await ctx.send(" @" + user + " generated this image: " + response[0])


    @commands.command(name="replicate")
    async def replicate_command(self, ctx):
        """
        !replicate help
        Replicate takes in a url and returns a new image based on that image's interrogation response
        """
        #Setting up intro variables
        user, command, target, pp = await self._process_input(ctx) # {user of the command}{target}{target_profile_url OR prompt}
        try:
            print(f"Interrogating: {pp}")
            ci_response = await clip.clip_interrogate_temp(pp)
            print(f"Interrogation response: {ci_response}")
            diffuser_response = await diffusers.text_to_image_replicate(user, ci_response)
            await ctx.send(" @" + user + " generated this image: " + diffuser_response[0])
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")



    @commands.command(name="interrogate")
    async def interrogate_command(self, ctx):
        user, command, target, pp = await self._process_input(ctx) # {user of the command}{target}{target_profile_url OR prompt}
        print(f"Interrogating: {input} for {user}")
        try:
            print(f"Interrogating: {input}")
            response = await clip.clip_interrogate_temp(pp)
            print(f"Interrogation response: {response}")
            
            await ctx.send(" @" + user + " - " + response)
            return response
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")

    @commands.command(name="commands")
    async def commands_command(self, ctx):
        print(f"Received command: {ctx.message.content}")
        await ctx.send(help_text)

    @commands.command(name="pp")
    async def pp_command(self, ctx):
        user, command, target, pp = await self._process_input(ctx)
        await ctx.send(pp)
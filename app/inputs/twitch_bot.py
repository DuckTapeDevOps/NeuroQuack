import asyncio
import datetime
import os
from twitchio.ext import commands
from twitchio import Client
from fastapi import HTTPException
from tasks import text_to_image, text_generation, video, image_to_text, background_removal, computer_vision
import utility
from flavor import styles
# from utility.cost import analysis, prediction

from pydantic import BaseModel
from typing import Optional

BOT_NAME = os.environ.get("BOT_NAME", "not-set")

help_text = "duckta12Lul"
llm_text = "In order to use an llm, you must choose a model and an inferencing method. For example, !llm sdxl foo looking like bar"
sup_text = "style, llm-neural, sdxl, replicate, photo-maker, emote, emote-url, pp-video, animate-diff, clip, blip, github, discord, commands, ping, really?"
default_style = "Photographic (Default)"
goals_guy = "@SpirodonFL"

loading_emoji = "duckta12Compute"

discord_invite = "https://discord.gg/t5DVy7DdBP"
github_url = "https://github.com/DuckTapeDevOps"


bot = None
twitch_token = None
current_style = default_style
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
    print(f"Started Twitch Bot in channels {initial_channels}")
    
    return {"status": "success"}

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

    async def _get_profile_image_url(self, target):
        """
        Fetches the profile image URL for the given user.
        !

        Args:
            user: The user to fetch the profile image URL for.

        Returns:
            The profile image URL for the given user.
        """
        profile_image_url = None
        print(f"Fetching profile image for {target}")
        # Fetch the user info from Twitch API.
        # If the user is not found, return None.
        # If the user is found, return the profile image URL.
        # If the user is found, but the profile image is not set, return None.
        # If the user is found, but the profile image is set, return the profile image URL.
        # If the user is found, but the profile image is set, but the URL is invalid, return None.
        # If the user is found, but the profile image is set, but the URL is valid, return the profile image URL.
        # If the user is found, but the profile image is set, but the URL is valid, return the profile image URL.
        # If the user is found, but the profile image is set, but the URL is valid, return the profile image URL.
        # If the user is found, but the profile image is set, but the URL is valid, return the profile image URL.
        print(f"Fetching user info for {target}")
        target = target.strip("@")
        target_list = await self.twitch_client.fetch_users(names=[target])
        if target_list:
            target_info = target_list[0]
            print(f"User info: {target_info}")
            profile_image_url = target_info.profile_image
            print(f"profile_image: {profile_image_url}")
        return profile_image_url

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
        if "@" == prompt[0]:
            if " " in prompt:
                target, rest_of_prompt = prompt.split(" ", 1)
            else:
                target = prompt
                rest_of_prompt = ""
            target = target.strip("@")
            profile_image_url = await self._get_profile_image_url(target)
            return user, command, target, profile_image_url, rest_of_prompt

        return user, command, bot_name, prompt, "url, not pp"
    
    
    async def _process_input_url(self, ctx): # First step in processing a command
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
        bot_name, command, url, prompt = ctx.message.content.split(" ", 2)
        user = ctx.author.name

        return user, command, url, prompt or "url, not pp"

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

    @commands.command(name="goals")
    async def goals_command(self, ctx):
        await ctx.send(f"Goals: {goals_guy}")

    @commands.command(name="ping")
    async def ping_command(self, ctx):
        await ctx.send(f"Pong! {ctx.author.name}")

    @commands.command(name="commands")
    async def commands_command(self, ctx):
        print(f"Received command: {ctx.message.content}")
        await ctx.send(help_text)

    @commands.command(name="sup")
    async def sup_command(self, ctx):
        print(f"Received command: {ctx.message.content}")
        await ctx.send(sup_text)

    @commands.command(name="pp")
    async def pp_command(self, ctx):
        user, command, target, pp, prompt = await self._process_input(ctx)
        await ctx.send(pp)

    @commands.command(name="resize-url")
    async def resize_url_command(self, ctx):
        user, command, url, width, height = ctx.message.content.split(" ", 4)
        width = int(width)
        height = int(height)
        print(f"Received command: {ctx.message.content}")
        print(f"Width: {width}")
        print(f"Height: {height}")
        try:
            response = await utility.resize_image(url, width, height)
            await ctx.send(file=response)
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")

    @commands.command(name="get-style")
    async def get_style_command(self, ctx):
        await ctx.send({current_style})


    @commands.command(name="set-style")
    async def style_command(self, ctx):
        print(f"Received command: {ctx.message.content}")
        style = ctx.message.content.split(" ", 1)[1]
        await ctx.send(f"thid dont work, fam")

    @commands.command(name="list-styles")
    async def styles_command(self, ctx):
        print(styles.style_names)
        await ctx.send(', '.join(styles.style_names))  # Join the list items with a comma and space

    ######################
    ## TEXT_GENERATION ###
    ######################

    @commands.command(name="llm-neural")
    async def llm_neural_command(self, ctx):
        user, command, target, prompt, pp = await self._process_input(ctx) # {user of the command}{target}{target_profile_url OR prompt}
        print(f"User: {user}")
        print(f"Command: {command}")
        print(f"Target: {target}")
        print(f"Input: {prompt}")
        try:
            answer = await text_generation.text_generation(prompt)
            answer = utility.sanitize_text(answer, 450)
            await ctx.send(f"@{user} {answer}")
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")
    
    ######################
            
    ######################
    ## TEXT_TO_IMAGE #####
    ######################

    @commands.command(name="sdxl")
    async def sdxl_command(self, ctx):
        user, command, target, prompt, pp = await self._process_input(ctx)
        print(f"User: {user}")
        print(f"Target: {target}")
        print(f"Input: {prompt}")
        try:
            response = await text_to_image.text_to_image_replicate(prompt)
            await ctx.send(" @" + user + " generated this image: " + response[0])
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")

    @commands.command(name="replicate")
    async def replicate_command(self, ctx):
        """
        !replicate help
        Replicate takes in a url and returns a new image based on that image's interrogation response
        """
        user, command, target, pp, prompt = await self._process_input(ctx) # {user of the command}{target}{target_profile_url OR prompt}
        try:
            print(f"Interrogating: {pp}")
            ci_response = await image_to_text.clip(pp)
            print(f"Interrogation response: {ci_response}")
            diffuser_response = await text_to_image.text_to_image_replicate(ci_response)
            await ctx.send("@" + user + " generated this image: " + diffuser_response[0])
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")


    @commands.command(name="pp-photomaker")
    async def photo_maker_command(self, ctx):
        user, command, target, pp, prompt = await self._process_input(ctx)
        print(f"PP: {pp}")
        print(f"Target: {target}")
        print(f"User: {user}")
        print(f"Command: {command}")
        if prompt is None:
            prompt = "img"
        try:
            output = await text_to_image.photomaker(pp, prompt)
            await ctx.send("@" + user + " generated this image: " + output[0])
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")
    
    @commands.command(name="url-photomaker")
    async def photo_maker_url_command(self, ctx):
        print(f"Received command: {ctx.message.content}")
        user, command, url, prompt = await self._process_input_url(ctx)
        print(f"User: {user}")
        print(f"Command: {command}")
        print(f"Prompt: {prompt}")
        try:
            output = await text_to_image.photomaker(url, prompt)
            await ctx.send("@" + user + " generated this image: " + output[0])
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")

    @commands.command(name="emote")
    async def emote_command(self, ctx):
        user, command, target, pp, prompt = await self._process_input(ctx)
        print(f"PP: {pp}")
        print(f"Target: {target}")
        print(f"User: {user}")
        print(f"Command: {command}")
        style= "Photographic (Default)"
        try:
            caption = await image_to_text.blip(pp)
            caption = caption.split(":")[1].strip()  # Extract the text after "Caption:" and remove leading/trailing whitespaces
            prompt = caption + " " + prompt
            image = await text_to_image.photomaker(pp, prompt)
            await ctx.send(f"@{user} '{prompt}' {image[0]}")
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")


    @commands.command(name="emote-url")
    async def emote_url_command(self, ctx):
        user, command, url, prompt = await self._process_input_url(ctx)
        print(f"User: {user}")
        print(f"Command: {command}")
        print(f"Prompt: {prompt}")
        try:
            caption = await image_to_text.blip(url)
            caption = caption.split(":")[1].strip()  # Extract the text after "Caption:" and remove leading/trailing whitespaces
            prompt = caption + " " + prompt
            image = await text_to_image.photomaker(url, prompt)
            await ctx.send(f"@{user} '{prompt}' {image[0]}")
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")

    @commands.command(name="this-is-fine")
    async def this_is_fine_command(self, ctx):
        user, command, target = ctx.message.content.split(" ", 3)
        pp = await self._get_profile_image_url(target)
        prompt = await image_to_text.blip(pp)
        try:
            output = await text_to_image.this_is_fine(pp, prompt)
            await ctx.send("@" + user + " generated this image: " + output[0])
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")

    @commands.command(name="qr-code")
    async def qr_code_command(self, ctx):
        await ctx.send(f"@{ctx.author.name} Generating QR Code... {loading_emoji}")
        user, command, target, webpage = ctx.message.content.split(" ", 4)
        pp = await self._get_profile_image_url(target)
        prompt = await image_to_text.clip(pp)
        try:
            output = await text_to_image.qr_code(prompt, webpage)
            for image in output:
                await ctx.send(f"@{user} generated this image: {image}")
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")

    

    ######################
            
    ######################
    ## BACKGROUND_REMOVAL#
    ######################
            
    # @commands.command(name="remove-bg") toooooo sllooooowwww
    # async def remove_bg_command(self, ctx):
    #     user, command, target, pp, prompt = await self._process_input(ctx)
    #     print(f"PP: {pp}")
    #     print(f"Target: {target}")
    #     print(f"User: {user}")
    #     print(f"Command: {command}")
    #     try:
    #         bg_image = await background_removal.background_removal(pp)
    #         await ctx.send("@" + user + " generated this image: " + bg_image)
    #     except Exception as e:
    #         print(f"Error: {e}")
    #         await ctx.send(f"Error: {e}")


    ######################

    ######################
    ## VIDEO #############
    ######################

    @commands.command(name="pp-video")
    async def pp_video_command(self, ctx):
        user, command, target, pp, prompt = await self._process_input(ctx)
        print(f"PP: {pp}")
        print(f"Target: {target}")
        print(f"User: {user}")
        print(f"Command: {command}")
        try:
            video_url = await video.url_to_video(pp)
            await ctx.send("@" + user + " generated this video: " + video_url)
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")
    
    @commands.command(name="url-video")
    async def animate_command(self, ctx):
        bot_name, command, url = ctx.message.content.split(" ", 2)
        print(f"Command: {command}")
        print(f"URL: {url}")
        user = ctx.author.name
        try:
            await ctx.send("@" + user + " generated this video: " + await video.url_to_video(url))
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")

    
    @commands.command(name="animate-diff")
    async def animate_diff_command(self, ctx):
        user, command, target, prompt = await self._process_input(ctx)
        print(f"PP: {prompt}")
        print(f"Target: {target}")
        print(f"User: {user}")
        print(f"Command: {command}")
        try:
            await ctx.send("@" + user + " generated this video: " + await video.animate_diffusion(prompt))
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")

    @commands.command(name="stylizer")
    async def stylizer_command(self, ctx):
        user, command, target, pp, prompt = await self._process_input(ctx)
        print(f"PP: {pp}")
        print(f"Target: {target}")
        print(f"User: {user}")
        print(f"Command: {command}")
        try:
            video_url = await video.stylizer(pp)
            await ctx.send("@" + user + " generated this video: " + video_url)
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")
        
    ######################
            
    ######################
    ## COMPUTER_VISION ###
    ######################
            
    @commands.command(name="welcome")
    async def welcome_command(self, ctx):
        user, command, target, pp, prompt = await self._process_input(ctx)
        print(f"PP: {pp}")
        print(f"Target: {target}")
        print(f"User: {user}")
        print(f"Command: {command}")

        welcome_prompt = f"This is {target}, tell the story of how he raided into DuckTapeDevOps' channel!"
        try:
            # welcome_story = await computer_vision.minigpt(welcome_prompt, pp)

            asyncio.get_event_loop().run_until_complete(computer_vision.minigpt(prompt, pp))
            await ctx.send(f"@{user} generated this text: {welcome_prompt}")
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")

            
    ######################
    ## IMAGE_TO_TEXT #####
    ######################

    @commands.command(name="clip")
    async def interrogate_command(self, ctx):
        user, command, target, pp, prompt = await self._process_input(ctx) # {user of the command}{target}{target_profile_url OR prompt}
        try:
            print(f"Clipping: {user}")
            response = await image_to_text.clip(pp)
            print(f"Clip response: {response}")
            
            await ctx.send(" @" + user + " - " + response)
            return response
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")

    @commands.command(name="blip")
    async def blip_command(self, ctx):
        user, command, target, pp, prompt = await self._process_input(ctx) # {user of the command}{target}{target_profile_url OR prompt}
        print(f"captioning {user}")
        try:
            response = await image_to_text.blip(pp)
            print(f"Interrogation response: {response}")
            
            await ctx.send(" @" + user + " - " + response)
            return response
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")



    
    ######################
    ## TESTS #############
    ######################

    @commands.command(name="test-yo-self")
    async def test_yo_self_command(self, ctx):
        user, command, target, pp, prompt = await self._process_input(ctx)
        print(f"PP: {pp}")
        print(f"Target: {target}")
        print(f"User: {user}")
        print(f"Command: {command}")
        await ctx.send(pp)
        prompt = await image_to_text.clip(pp)
        print(f"Prompt: {prompt}")
        await ctx.send(prompt)
        image_url = await text_to_image.text_to_image_replicate(prompt)
        print(f"Image URL: {image_url}")
        await ctx.send(image_url)
        chat_reply = utility.sanitize_text(await text_generation.text_generation(f"Tell a story about {target} {prompt}"), 450)
        await ctx.send(chat_reply)
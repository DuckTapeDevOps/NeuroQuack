import json
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from twitchio.ext import commands
from llama_cpp import Llama  # Assuming you have this package installed
import textwrap  # Add this line to import the textwrap module
from inference_interaction import generate_image, init, build_payload

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize twitch_token and initial_channels with default values
twitch_token = None
initial_channels = ["DuckTapeDevOps"]

# Load configuration from config.json
try:
    with open("temp/config.json", "r") as f:
        config = json.load(f)
    twitch_token = config.get("TWITCH_TOKEN")
    initial_channels = config.get("INITIAL_CHANNELS", initial_channels)
except Exception as e:
    logging.error(f"Failed to load config.json: {e}")

# Initialize Llama model
llm = Llama(
  model_path="temp/llama-2-7b-chat.ggmlv3.q8_0.bin",
  n_gpu_layers=-1,
  n_ctx=3900,
)

executor = ThreadPoolExecutor(max_workers=3)

async def run_llm(prompt):
    return await asyncio.get_event_loop().run_in_executor(executor, lambda: llm(prompt, max_tokens=900)['choices'][0]['text'])

class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(token=twitch_token, prefix="!", initial_channels=initial_channels)

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        await self.handle_commands(message)

    @commands.command(name="llama")
    async def llama_command(self, ctx):
        prompt = ctx.message.content.replace("!llama ", "")
        reply = await run_llm(prompt)

        # Split the reply into chunks of 500 characters
        chunks = textwrap.wrap(reply, 500)

        # Send each chunk as a separate message
        for chunk in chunks:
            await ctx.send(chunk)

    @commands.command(name="sdxl")
    async def sdxl_command(self, ctx):
        prompt = ctx.message.content.replace("!sdxl ", "")
        endpoint_name = "neuro-dev-sdxl-w8kx-endpoint"
        model_predictor = init(endpoint_name)
        payload = build_payload(prompt)

        try:
            # Run the generate_image function in an executor to avoid blocking
            filename = await asyncio.get_event_loop().run_in_executor(
                None, generate_image, payload, model_predictor
            )
            # If you have a URL where the image is hosted, you can send it here
            await ctx.send(f"Image generated successfully: [URL to the image]")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
            
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()

    bot = TwitchBot()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.run())

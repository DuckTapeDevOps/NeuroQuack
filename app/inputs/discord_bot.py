import discord
from discord.ext import commands
from pydantic import BaseModel
from typing import Optional

class Command(BaseModel):
    command: str
    target_user: Optional[str] = None
    extra_param: Optional[str] = None

    # Adapt this method for Discord message format
    @classmethod
    def from_message(cls, message_content: str):
        # Your logic here
        pass

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name="test")
async def test_command(ctx):
    try:
        command = Command.from_message(ctx.message.content)
        print(f"Received command: {command.command}, Target User: {command.target_user}")
        await ctx.send(f"Test successful!")
    except ValidationError as e:
        print("Invalid command format")

@bot.command(name="ping")
async def ping_command(ctx):
    print(f"Received command: {ctx.message.content}")
    await ctx.send(f"Pong! {ctx.author.name}")

# Function to start the bot
def start_discord_bot(token):
    bot.run(token)

# Function to stop the bot (Discord.py handles this internally)
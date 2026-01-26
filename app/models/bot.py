from pydantic import BaseModel
from typing import Optional

class APIConfig(BaseModel):
    replicate_token: str
    replicate_org: str

class TwitchConfig(BaseModel):
    twitch_token: str
    initial_channels: str

class DiscordConfig(BaseModel):
    discord_token: str
    guild_id: Optional[str] = None

class BotConfig(BaseModel):
    api: APIConfig
    twitch: Optional[TwitchConfig] = None
    discord: Optional[DiscordConfig] = None

class StartBotRequest(BaseModel):
    twitch_auth: TwitchConfig
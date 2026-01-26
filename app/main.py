import logging
from fastapi import FastAPI, HTTPException
import uvicorn
from routers import images
from models.bot import BotConfig, StartBotRequest
from inputs.twitch_bot import start_bot, stop_bot
import os
import replicate

# Initialize logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()
app.include_router(images.router)

@app.post("/configure")
async def configure_bot(body: BotConfig):
    # Set the tokens first
    os.environ["REPLICATE_API_TOKEN"] = body.api.replicate_token
    os.environ["REPLICATE_ORG"] = body.api.replicate_org
    
    # Test the token by making a simple API call
    try:
        # Test with a simple models list call
        client = replicate.Client(api_token=body.api.replicate_token)
        models = client.models.list()
        print("✅ Replicate token validated successfully")
    except Exception as e:
        print(f"❌ Replicate token validation failed: {e}")
        raise HTTPException(status_code=401, detail=f"Invalid Replicate token: {str(e)}")
    
    print("API configured and ready")
    
    # Optional: Start Twitch bot
    if body.twitch:
        print("Twitch bot configured")
    
    # Optional: Start Discord bot
    if body.discord:
        print("Discord bot configured")
    
    return {
        "status": "success", 
        "message": "API configured and token validated",
        "features": {
            "api": True,
            "twitch": body.twitch is not None,
            "discord": body.discord is not None
        }
    }

@app.post("/start_bot")
async def start_bot_endpoint(body: StartBotRequest):
    """
    Start the Twitch bot with the provided token and channels
    """
    try:
        # Extract the twitch_auth config and create a simple object for start_bot
        class BotStartBody:
            def __init__(self, twitch_token, initial_channels):
                self.twitch_token = twitch_token
                self.initial_channels = initial_channels
        
        bot_body = BotStartBody(
            twitch_token=body.twitch_auth.twitch_token,
            initial_channels=body.twitch_auth.initial_channels
        )
        result = start_bot(bot_body)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start bot: {str(e)}")

@app.post("/stop_bot")
async def stop_bot_endpoint():
    """
    Stop the currently running Twitch bot
    """
    try:
        await stop_bot()
        return {"status": "success", "message": "Bot stopped"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop bot: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

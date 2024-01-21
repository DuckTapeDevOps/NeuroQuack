import os
from dotenv import load_dotenv
import replicate
from outputs import twitch_chat


if not os.getenv("REPLICATE_ORG"):
    load_dotenv()

REPLICATE_ORG = os.environ.get("REPLICATE_ORG", "default-not-set") # "ducktapedevops"

minigpt_deploy = replicate.deployments.get(f"{REPLICATE_ORG}/minigpt-4")

async def minigpt(prompt: str, image_url: str):
    prediction = await minigpt_deploy.predictions.async_create(
        input={
            "image": image_url,
            "top_p": 0.9,
            "prompt": prompt,
            "num_beams": 5,
            "max_length": 4000,
            "temperature": 1.32,
            "max_new_tokens": 3000,
            "repetition_penalty": 1
        }
    )
    
    def handle_prediction(prediction):
        print(prediction.output)
        # twitch_chat.send_message(prediction.output[0])


    prediction.add_done_callback(handle_prediction)

# asyncio.get_event_loop().run_until_complete(minigpt(prompt, image_url))
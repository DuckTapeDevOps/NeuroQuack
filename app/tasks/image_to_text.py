import os
import replicate
from dotenv import load_dotenv

if not os.getenv("REPLICATE_ORG"):
    load_dotenv()

CLIP_ENDPOINT_NAME = os.environ.get("CLIP_ENDPOINT_NAME", "endpoint-name-not-set")
REPLICATE_ORG = os.environ.get("REPLICATE_ORG", "default-not-set") # "ducktapedevops"
blip_deployment = replicate.deployments.get("ducktapedevops/blip")

async def clip(image_path: str):
    output = await replicate.async_run(
        CLIP_ENDPOINT_NAME,
        input={
            "mode": "fast",
            "clip_model_name": "ViT-L-14/openai",
            "image": image_path
            }
    )
    print(output)
    return output


async def blip(image_path: str):
    prediction = await blip_deployment.predictions.async_create(
        input={"image": image_path}
    )
    prediction.wait()
    print(prediction.output)
    return prediction.output
import json
import os
import replicate
from dotenv import load_dotenv

if not os.getenv("REPLICATE_ORG"):
    load_dotenv()

CLIP_ENDPOINT_NAME = os.environ.get("CLIP_ENDPOINT_NAME", "endpoint-name-not-set")
REPLICATE_ORG = os.environ.get("REPLICATE_ORG", "default-not-set") # "ducktapedevops"

ci_deployment = replicate.deployments.get("ducktapedevops/clip-interrogator")

async def clip_interrogate(image_path: str):
        prediction = await ci_deployment.predictions.async_create(
        input={
            "mode": "fast",
            "clip_model_name": "ViT-L-14/openai",
            "image": image_path
            }
        )
        await prediction.wait()
        print(prediction.output)
        return prediction.output


async def clip_interrogate_temp(image_path: str):
    output = await replicate.async_run(
        "pharmapsychotic/clip-interrogator:8151e1c9f47e696fa316146a2e35812ccf79cfc9eba05b11c7f450155102af70",
        input={
            "mode": "best",
            "clip_model_name": "ViT-L-14/openai",
            "image": image_path
            }
    )
    print(output)
    return output
import os
from dotenv import load_dotenv
import replicate



if not os.getenv("DEFAULT_DIFFUSER_TYPE"):
    load_dotenv()

SDXL_ENDPOINT_NAME = os.environ.get("SDXL_ENDPOINT_NAME", "endpoint-name-not-set")
DEFAULT_DIFFUSER_TYPE = os.environ.get("DEFAULT_DIFFUSER_TYPE", "default-not-set")
REPLICATE_ORG = os.environ.get("REPLICATE_ORG", "default-not-set") # "ducktapedevops"
AWS_REGION_NAME = os.environ.get("AWS_REGION_NAME", "default-not-set") # "us-east-1"
SDXL_TURBO_ENDPOINT_NAME = os.environ.get("SDXL_TURBO_ENDPOINT_NAME", "endpoint-name-not-set")


sdxl_deployment = replicate.deployments.get(f"{REPLICATE_ORG}/sdxl")
background_removal_deployment = replicate.deployments.get("{REPLICATE_ORG}/background-removal")
emoji_deployment = replicate.deployments.get("{REPLICATE_ORG}/emoji")
bg_rm_deployment = replicate.deployments.get("{REPLICATE_ORG}/bg-rm")



async def background_removal(img_url):
    prediction = await background_removal_deployment.predictions.async_create(
        input={"file": img_url}
    )
    prediction.wait()
    print(prediction.output)
    return prediction.output
    
async def text_to_image_replicate(user: str, prompt: str):
    prediction = await sdxl_deployment.predictions.async_create(
        input={"prompt": prompt}
    )
    prediction.wait()
    print(prediction.output)
    return prediction.output

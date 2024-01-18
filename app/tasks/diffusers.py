import os
from dotenv import load_dotenv
import replicate

if not os.getenv("REPLICATE_ORG"):
    load_dotenv()

REPLICATE_ORG = os.environ.get("REPLICATE_ORG", "default-not-set") # "ducktapedevops"

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
    
async def text_to_image_replicate(prompt: str):
    prediction = await sdxl_deployment.predictions.async_create(
        input={"prompt": prompt}
    )
    prediction.wait()
    print(prediction.output) #['https://replicate.delivery/pbxt/n5KKU2ii1eXCRiMA0j8Go2WmocappYO70S1En7r5SDPKMwGJA/out-0.png']
    return prediction.output

import os
from dotenv import load_dotenv
import replicate
from config.models import get_model_version
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not os.getenv("REPLICATE_ORG"):
    load_dotenv()

REPLICATE_ORG = os.environ.get("REPLICATE_ORG", "default-not-set") # "ducktapedevops"

# Keep other deployments for now, but we'll use public SDXL
try:
    background_removal_deployment = replicate.deployments.get(f"{REPLICATE_ORG}/background-removal")
    emoji_deployment = replicate.deployments.get(f"{REPLICATE_ORG}/emoji")
    bg_rm_deployment = replicate.deployments.get(f"{REPLICATE_ORG}/bg-rm")
except Exception as e:
    logger.warning(f"Some custom deployments not found: {e}")
    background_removal_deployment = None
    emoji_deployment = None
    bg_rm_deployment = None

async def background_removal(img_url):
    if not background_removal_deployment:
        raise Exception("Background removal deployment not available")
    
    prediction = await background_removal_deployment.predictions.async_create(
        input={"file": img_url}
    )
    prediction.wait()
    logger.info(f"Background removal output: {prediction.output}")
    return prediction.output

async def photomaker(img_url, prompt, style: str = "Photographic (Default)"):
    actual_model = get_model_version("photomaker")
    logger.info(f"Using PhotoMaker model: {actual_model}")
    
    prediction = await replicate.async_run(
        actual_model,
        input={
            "seed": 1143488585,
            "prompt": f"{prompt}",
            "num_steps": 50,
            "style_name": style,
            "input_image": img_url,
            "num_outputs": 4,
            "guidance_scale": 5,
            "negative_prompt": "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry",
            "style_strength_ratio": 20
        }
    )
    logger.info(f"PhotoMaker output: {prediction}")
    return prediction

async def text_to_image_replicate(prompt: str, model: str = None):
    # Use the provided model or fall back to default
    actual_model = get_model_version("sdxl", model)
    logger.info(f"Using SDXL model: {actual_model}")
    
    # Use public SDXL model instead of deployment
    prediction = await replicate.async_run(
        actual_model,
        input={"prompt": prompt}
    )
    logger.info(f"SDXL output: {prediction}")
    return prediction

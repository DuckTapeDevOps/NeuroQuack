import os
import replicate
from dotenv import load_dotenv
from config.models import get_model_version
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not os.getenv("REPLICATE_ORG"):
    load_dotenv()

CLIP_ENDPOINT_NAME = os.environ.get("CLIP_ENDPOINT_NAME", "endpoint-name-not-set")
REPLICATE_ORG = os.environ.get("REPLICATE_ORG", "default-not-set") # "ducktapedevops"

# Try to get custom deployment, fallback to None if it doesn't exist
try:
    blip_deployment = replicate.deployments.get("ducktapedevops/blip")
except:
    blip_deployment = None
    logger.warning("Custom BLIP deployment not found, will use public model")

async def clip_interrogate(image_path: str, model: str = None):
    actual_model = get_model_version("clip_interrogator", model)
    logger.info(f"Using CLIP model: {actual_model}")
    logger.info(f"Image URL: {image_path}")
    
    try:
        output = await replicate.async_run(
            actual_model,
            input={
                "mode": "fast",
                "clip_model_name": "ViT-L-14/openai",
                "image": image_path
            }
        )
        logger.info(f"CLIP output: {output}")
        return output
    except Exception as e:
        logger.error(f"CLIP error: {str(e)}")
        logger.error(f"Model: {actual_model}")
        logger.error(f"Image: {image_path}")
        raise e

async def blip(image_path: str, model: str = None):
    actual_model = get_model_version("blip", model)
    logger.info(f"Using BLIP model: {actual_model}")
    logger.info(f"Image URL: {image_path}")
    
    try:
        if actual_model.startswith("ducktapedevops/") and blip_deployment:
            # Use custom deployment
            logger.info("Using custom BLIP deployment")
            prediction = await blip_deployment.predictions.async_create(
                input={"image": image_path}
            )
        else:
            # Use public model
            logger.info("Using public BLIP model")
            prediction = await replicate.async_run(actual_model, input={"image": image_path})
        
        prediction.wait()
        logger.info(f"BLIP output: {prediction.output}")
        return prediction.output
    except Exception as e:
        logger.error(f"BLIP error: {str(e)}")
        logger.error(f"Model: {actual_model}")
        logger.error(f"Image: {image_path}")
        raise e
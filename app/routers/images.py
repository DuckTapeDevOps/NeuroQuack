from fastapi import APIRouter, HTTPException
from tasks import text_to_image, image_to_text
from models.images import ImageEditRequest, TextToImageRequest, ImageAnalysisRequest, ModelConfig
import logging
import replicate
import os

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/image", tags=["images"])

@router.post("/photomaker")
async def photomaker_endpoint(request: ImageEditRequest):
    """Transform an image using PhotoMaker"""
    try:
        result = await text_to_image.photomaker(request.image_url, request.prompt, request.style)
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"PhotoMaker error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PhotoMaker failed: {str(e)}")

@router.post("/generate")
async def text_to_image_endpoint(request: TextToImageRequest):
    """Generate an image from text prompt"""
    try:
        logger.info(f"Text-to-image request - Prompt: {request.prompt}, Model: {request.model}")
        result = await text_to_image.text_to_image_replicate(request.prompt, request.model)
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Text-to-image error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Text-to-image failed: {str(e)}")

@router.post("/analyze/clip")
async def clip_analyze_endpoint(request: ImageAnalysisRequest):
    """Analyze an image using CLIP"""
    try:
        logger.info(f"CLIP request - Image: {request.image_url}, Model: {request.clip_model}")
        result = await image_to_text.clip_interrogate(request.image_url, request.clip_model)
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"CLIP analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"CLIP analysis failed: {str(e)}")

@router.post("/analyze/blip")
async def blip_analyze_endpoint(request: ImageAnalysisRequest):
    """Generate caption for an image using BLIP"""
    try:
        logger.info(f"BLIP request - Image: {request.image_url}, Model: {request.blip_model}")
        result = await image_to_text.blip(request.image_url, request.blip_model)
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"BLIP analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"BLIP analysis failed: {str(e)}")

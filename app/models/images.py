from pydantic import BaseModel
from typing import Optional
from config.models import get_model_version

class ImageEditRequest(BaseModel):
    image_url: str
    prompt: str
    style: Optional[str] = "Photographic (Default)"

class TextToImageRequest(BaseModel):
    prompt: str
    model: Optional[str] = None  # Allow model override

class ImageAnalysisRequest(BaseModel):
    image_url: str
    clip_model: Optional[str] = None  # Will use get_model_version if None
    blip_model: Optional[str] = None  # Will use get_model_version if None

class ModelConfig(BaseModel):
    sdxl_model: Optional[str] = None  # Will use deployment if not provided
    photomaker_model: Optional[str] = None  # Will use get_model_version if None
    clip_model: Optional[str] = None  # Will use get_model_version if None
    blip_model: Optional[str] = None  # Will use get_model_version if None

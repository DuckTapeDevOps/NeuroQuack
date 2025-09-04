"""
Model configuration for AI services with hierarchical overrides
"""
import os
from typing import Dict, Optional

# Default model versions (app level)
DEFAULT_MODELS = {
    "photomaker": "jd7h/photomaker:latest",
    "clip_interrogator": "pharmapsychotic/clip-interrogator:8151e1c9f47e696fa316146a2e35812ccf79cfc9eba05b11c7f450155102af70",
    "sdxl": "stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc",
    "blip": "ducktapedevops/blip",
    "background_removal": "ducktapedevops/bg-rm",
    "emoji": "ducktapedevops/emoji",
}

def get_model_version(model_name: str, api_override: str = None) -> str:
    """
    Get model version with hierarchical overrides:
    1. API call parameter (highest priority)
    2. ECS Task environment variable
    3. Docker environment variable  
    4. App default (lowest priority)
    """
    if api_override:
        return api_override
    
    # Check for environment variable (works for both ECS and Docker)
    env_key = f"MODEL_{model_name.upper()}"
    env_value = os.environ.get(env_key)
    if env_value:
        return env_value
    
    # Fall back to app default
    return DEFAULT_MODELS.get(model_name, "latest")

# Model configuration (no longer needed since we use the function directly)
# MODELS = { ... }  # Remove this

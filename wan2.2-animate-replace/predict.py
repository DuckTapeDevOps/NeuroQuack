import os
import sys
import torch
import numpy as np
import tempfile
from pathlib import Path
from typing import Optional
import cv2
from PIL import Image
import torchvision.transforms as transforms

# Add Wan2.2 to path
sys.path.append('/src/Wan2.2')
from inference.inference_animate_replace import animate_replace

class Predictor:
    def __init__(self):
        """Load the model into memory to make running multiple predictions efficient"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.checkpoint_path = "/src/checkpoints/wan2.2_animate_replace.ckpt"
        
        # Verify checkpoint exists
        if not os.path.exists(self.checkpoint_path):
            raise FileNotFoundError(f"Checkpoint not found at {self.checkpoint_path}")

    def predict(
        self,
        character_image: str,
        driving_video: str,
        seed: Optional[int] = 42,
        steps: int = 50,
        guidance_scale: float = 3.5,
        width: int = 512,
        height: int = 512,
        num_inference_steps: int = 30,
        fps: int = 30,
    ) -> str:
        """Run a single prediction on the model"""
        # Set random seed for reproducibility
        torch.manual_seed(seed)
        np.random.seed(seed)
        
        # Create temporary directory for outputs
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "output.mp4")
            
            # Run the animation
            try:
                animate_replace(
                    checkpoint_path=self.checkpoint_path,
                    character_image=character_image,
                    driving_video=driving_video,
                    output_path=output_path,
                    steps=steps,
                    guidance_scale=guidance_scale,
                    width=width,
                    height=height,
                    num_inference_steps=num_inference_steps,
                    fps=fps,
                    device=self.device,
                )
                
                # Verify output was created
                if not os.path.exists(output_path):
                    raise Exception("Output video was not generated")
                
                # Return the output file path
                return output_path
                
            except Exception as e:
                print(f"Error during prediction: {str(e)}")
                raise

    def cleanup(self):
        """Cleanup any resources if needed"""
        pass

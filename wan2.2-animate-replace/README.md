# Wan2.2 Animate-Replace Cog Wrapper

This is a Cog wrapper for the [Wan2.2 Animate-Replace](https://github.com/Wan-Video/Wan2.2) model, allowing you to deploy it as a private model on Replicate.

## Prerequisites

- [Cog](https://github.com/replicate/cog) installed (`pip install cog`)
- [Docker](https://docs.docker.com/get-docker/) installed and running
- A [Replicate](https://replicate.com) account

## Building and Pushing to Replicate

1. **Build the Docker image locally (optional, for testing):**
   ```bash
   cog build -t wan2.2-animate-replace
   ```

2. **Push to Replicate:**
   ```bash
   # Log in to Replicate
   cog login
   
   # Push the model
   replicate push your-username/wan2-2-animate-replace
   ```

3. **Use the model:**
   Once pushed, you can use the model via the Replicate API or in ComfyUI with the Replicate node.

## Input Parameters

- `character_image`: Input image of the character to animate
- `driving_video`: Driving video to animate the character with
- `seed`: Random seed (default: 42)
- `steps`: Number of animation steps (default: 50)
- `guidance_scale`: Guidance scale (default: 3.5)
- `width`: Output width (default: 512)
- `height`: Output height (default: 512)
- `num_inference_steps`: Number of denoising steps (default: 30)
- `fps`: Frames per second of the output video (default: 30)

## Example API Usage

```python
import replicate

output = replicate.run(
    "your-username/wan2-2-animate-replace:version",
    input={
        "character_image": "path/to/character.png",
        "driving_video": "path/to/driving.mp4",
        "seed": 42,
        "steps": 50,
        "guidance_scale": 3.5,
        "width": 512,
        "height": 512,
        "num_inference_steps": 30,
        "fps": 30
    }
)
```

## Hardware Requirements

- GPU with at least 16GB VRAM (A100 or similar recommended)
- 16GB+ RAM
- 20GB+ disk space for the model and dependencies

## License

This wrapper is provided under the MIT License. The underlying Wan2.2 model has its own license - please refer to the [original repository](https://github.com/Wan-Video/Wan2.2) for details.

import os
from dotenv import load_dotenv
import replicate


if not os.getenv("REPLICATE_ORG"):
    load_dotenv()

REPLICATE_ORG = os.environ.get("REPLICATE_ORG", "default-not-set") # "ducktapedevops"

stylizer_deployment = replicate.deployments.get(f"{REPLICATE_ORG}/stylizer")
animate_diff_deployment = replicate.deployments.get(f"{REPLICATE_ORG}/animate-diff")

async def pp_to_video(pp):
    output = await replicate.async_run( # Run runs it against an actively deployed model vs create creating a job/task
        "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
        input={
            "input_image": pp
        }
    )
    print(output)
    return output


async def animate_diffusion(prompt):
    prediction = await animate_diff_deployment.predictions.async_create(
        input={
        "path": "toonyou_beta3.safetensors",
        "seed": 0,
        "steps": 25,
        "prompt": prompt,
        "n_prompt": "badhandv4, easynegative, ng_deepnegative_v1_75t, verybadimagenegative_v1.3, bad-artist, bad_prompt_version2-neg, teeth",
        "motion_module": "mm_sd_v15_v2",
        "guidance_scale": 7.5
        }
    )
    prediction.wait()
    print(prediction.output)
    return prediction.output

async def stylizer(img_url):
    prediction = await stylizer_deployment.predictions.async_create(
        input={
            "input": img_url,
            "generate_video": True,
            "video_format": "gif"
        }
    )
    prediction.wait()
    print(prediction.output)
    return prediction.output

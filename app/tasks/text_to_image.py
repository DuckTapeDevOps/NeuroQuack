import os
from dotenv import load_dotenv
import replicate

if not os.getenv("REPLICATE_ORG"):
    load_dotenv()

REPLICATE_ORG = os.environ.get("REPLICATE_ORG", "default-not-set") # "ducktapedevops"

sdxl_deployment = replicate.deployments.get(f"{REPLICATE_ORG}/sdxl")
this_is_fine_deployment = replicate.deployments.get(f"{REPLICATE_ORG}/this-is-fine")
qr_code_deployment = replicate.deployments.get(f"{REPLICATE_ORG}/3d-qr-code")

async def photomaker(img_url, prompt, style: str = "Photographic (Default)"):
    if "img" not in prompt:
        prompt = f"{prompt} img"
    prediction = await replicate.async_run(
        "jd7h/photomaker:b28be690c8a87bcf62002ce5ba77ac534b38998b8c9aaa7ff81d6009db6744b0",
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
    print(prediction)
    return prediction

    
async def text_to_image_replicate(prompt: str):
    prediction = await sdxl_deployment.predictions.async_create(
        input={"prompt": prompt}
    )
    prediction.wait()
    print(prediction.output) #['https://replicate.delivery/pbxt/n5KKU2ii1eXCRiMA0j8Go2WmocappYO70S1En7r5SDPKMwGJA/out-0.png']
    return prediction.output

async def this_is_fine(img_url, prompt):
    prediction = await this_is_fine_deployment.predictions.async_create(
        input={
            "image": img_url,
            "width": 1024,
            "height": 1024,
            "prompt": f"{prompt}in the style of THIS_IS_FINE with fire all around",
            "refine": "no_refiner",
            "scheduler": "K_EULER",
            "lora_scale": 0.6,
            "num_outputs": 1,
            "guidance_scale": 7.5,
            "apply_watermark": False,
            "high_noise_frac": 0.8,
            "negative_prompt": "NSFW",
            "prompt_strength": 0.8,
            "num_inference_steps": 50
        }
    )
    prediction.wait()
    print(prediction.output)
    return prediction.output

async def qr_code(prompt: str, qr_code_content: str):
    prediction = await qr_code_deployment.predictions.async_create(
        input={
            "seed": 7649977186,
            "prompt": prompt,
            "strength": 0.9,
            "batch_size": 4,
            "guidance_scale": 9.5,
            "negative_prompt": "ugly, disfigured, low quality, blurry, nsfw",
            "qr_code_content": qr_code_content,
            "num_inference_steps": 40,
            "controlnet_conditioning_scale": 1.3
        }
    )
    prediction.wait()
    print(prediction.output)
    return prediction.output

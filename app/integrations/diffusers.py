import base64
from datetime import datetime
import hashlib
import io
import json
import os
import re
from tkinter import Image
from typing import Tuple, Union
from fastapi import HTTPException
import requests
from sagemaker.predictor import Predictor
from sagemaker.serializers import JSONSerializer
from sagemaker.deserializers import BytesDeserializer
import sagemaker
from PIL import Image
from dotenv import load_dotenv


if not os.getenv("DEFAULT_DIFFUSER_TYPE"):
    load_dotenv()

SDXL_ENDPOINT_NAME = os.environ.get("SDXL_ENDPOINT_NAME", "endpoint-name-not-set")
DEFAULT_DIFFUSER_TYPE = os.environ.get("DEFAULT_DIFFUSER_TYPE", "default-not-set")

sess = sagemaker.Session()

sdxl_model_predictor = Predictor(
            endpoint_name=SDXL_ENDPOINT_NAME, 
            sagemaker_session=sess,
            serializer=JSONSerializer(),
            deserializer=BytesDeserializer()
        )
diffuser_models = "sdxl"
help_text = f"To use !diffuse, type !diffuse <model> <prompt>. For example, !diffuse sdxl explain my next step. The model can be  {diffuser_models}. The prompt can be any text you want to use to generate a response."

def prompt_diffuser(prompt_map):
    if prompt_map['diffuser_type']  == "sdxl":
        return generate_image(prompt_map['prompt'], sdxl_model_predictor, prompt_map['user'])
    else:
        return generate_image(prompt_map['prompt'], sdxl_model_predictor, prompt_map['user']) # default to sdxl

def generate_image(author: str, prompt: str,diffusion_model_predictor: Predictor = sdxl_model_predictor ):
    try:
        payload = {
            "text_prompts":[{"text": prompt}],
            "width": 1024,
            "height": 1024,
            "sampler": "DPMPP2MSampler",
            "cfg_scale": 7.0,
            "steps": 50,
            "seed": 0,
            "use_refiner": True,
            "refiner_steps": 40,
            "refiner_strength": 0.2
        }
        # Get prediction from SageMaker endpoint
        sdxl_response = diffusion_model_predictor.predict(payload)
        filename = sanitize_filename(author, prompt)
        return decode_and_show(sdxl_response, filename)
    except Exception as e:
        # Handle general exceptions
        raise HTTPException(status_code=500, detail=str(e))

def prompt_diffuser_image_to_image(prompt_map):
    if prompt_map['diffuser_type']  == "sdxl":
        return image_to_image(sdxl_model_predictor,
                              prompt_map['image_url'], 
                              prompt_map['prompt'],
                              prompt_map['user'], 
                              prompt_map.get('title', None))
    else:
        return image_to_image(sdxl_model_predictor,
                              prompt_map['image_url'], 
                              prompt_map['prompt'],
                              prompt_map['user'], 
                              prompt_map['title']) # default to sdxl

def image_to_image(diffusion_model_predictor, image_url: str, prompt: str,  user: str, title: str = None):
    size = (512, 512)
    image_path = download_profile_image(image_url, user)
    encoded_image = encode_image(image_path, size=size)

    payload = {
        "text_prompts":[{"text": prompt}],
        "init_image": encoded_image,
        "cfg_scale": 9,
        "image_strength": 0.8,
        "seed": 42,
        }
    # Get prediction from SageMaker endpoint
    try:
        print(f"Generating image of {prompt} for {user}")
        sdxl_response = diffusion_model_predictor.predict(payload)
        if title is None:
            filename = sanitize_filename(user, prompt)
        else:
            filename = sanitize_filename(user, title)
        return decode_and_show(sdxl_response, filename)
    except Exception as e:
        # Handle general exceptions
        print(f"Error generating image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def download_profile_image(url, username):
    download_image(url, "temp/intermidiary_images", f"{username}_profile.png")
    return f"temp/intermidiary_images/{username}_profile.png"

def encode_image(image_path: str, resize: bool = True, size: Tuple[int, int] = (1024, 1024)) -> Union[str, None]:
    """
    Encode an image as a base64 string, optionally resizing it to a supported resolution.

    Args:
        image_path (str): The path to the image file.
        resize (bool, optional): Whether to resize the image. Defaults to True.

    Returns:
        Union[str, None]: The encoded image as a string, or None if encoding failed.
    """
    assert os.path.exists(image_path)

    if resize:
        image = Image.open(image_path)
        image = image.resize(size)
        image.save("image_path_resized.png")
        image_path = "image_path_resized.png"
    image = Image.open(image_path)
    assert image.size == size
    with open(image_path, "rb") as image_file:
        img_byte_array = image_file.read()
        # Encode the byte array as a Base64 string
        try:
            base64_str = base64.b64encode(img_byte_array).decode("utf-8")
            return base64_str
        except Exception as e:
            print(f"Failed to encode image {image_path} as base64 string.")
            print(e)
            return None
    image.close()
    

def sanitize_filename(user, prompt):
    # Remove non-alphanumeric characters
    prompt = re.sub(r'[^a-zA-Z0-9 ]', '', prompt)
    # Replace spaces with underscores
    prompt = prompt.replace(' ', '_')
    # Shorten the text if it's too long
    safe_prompt = (prompt[:15] + '..') if len(prompt) > 15 else prompt
    # Format the timestamp
    timestamp = datetime.now().strftime('%H%M%S')
    # Create the directory structure
    date_directory = datetime.now().strftime('%Y%m%d')
    # Assemble the filename
    filename = f"{date_directory}/{user}/{safe_prompt}_{timestamp}.png"
    print(filename + " Finished")

    return filename


def decode_and_show(response_bytes, filename):
    # Parse the JSON response to get the base64-encoded string
    response_json = json.loads(response_bytes)
    image_base64 = response_json['generated_image']

    # Decode the base64 string
    image_data = base64.b64decode(image_base64)

    # Create an in-memory bytes buffer for the image data
    img_io = io.BytesIO(image_data)

    # Save the image to a file
    img_io.seek(0)
    img = Image.open(img_io)
    directory = os.path.join("temp", os.path.dirname(filename))

    # Check if the directory exists, and create it if it doesn't
    if not os.path.exists(directory):
        os.makedirs(directory)
    img.save("temp/"+filename)
    img.close()
    return filename
import os
import datetime
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from fastapi.responses import StreamingResponse, PlainTextResponse
from mangum import Mangum
import boto3
from botocore.exceptions import NoCredentialsError
from datetime import datetime
import hashlib
import base64
import io
from PIL import Image
import sys
import re

# Specific imports for SageMaker
from sagemaker.predictor import Predictor
from sagemaker.serializers import JSONSerializer
from sagemaker.deserializers import BytesDeserializer
import sagemaker
import json
from typing import List

class TextPrompt(BaseModel):
    text: str

class ImageGenerationPayload(BaseModel):
    text_prompts: List[TextPrompt]
    width: int = 1024
    height: int = 1024
    sampler: str
    cfg_scale: float
    steps: int
    seed: int
    use_refiner: bool
    refiner_steps: int
    refiner_strength: float



def init(endpoint_name):
    # Initialize SageMaker session and predictor
    sess = sagemaker.Session()
    

    # Define the predictor (this could also be done inside the endpoint call for a fresh setup each time)
    model_predictor = Predictor(
        endpoint_name=endpoint_name, 
        sagemaker_session=sess,
        serializer=JSONSerializer(),
        deserializer=BytesDeserializer()
    )

    return model_predictor

def sanitize_filename(text):
    # Remove non-alphanumeric characters
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    # Replace spaces with underscores
    text = text.replace(' ', '_')
    # Shorten the text if it's too long
    text = (text[:10] + '..') if len(text) > 10 else text
    return text

def generate_image(payload: ImageGenerationPayload, model_predictor):
    try:
        # Convert the Pydantic model to a dictionary
        sdxl_payload = payload.dict(by_alias=True)
        
        # Get prediction from SageMaker endpoint
        sdxl_response = model_predictor.predict(sdxl_payload)
        
        # Generate a safe filename from the prompt
        # Use a hash to ensure uniqueness
        prompt = sdxl_payload.get('text_prompts', [{}])[0].get('text', 'image')
        safe_prompt = sanitize_filename(prompt)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        hash_part = hashlib.md5(prompt.encode()).hexdigest()[:6]
        local_dir = "output"
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        filename = f"{local_dir}/{safe_prompt}_{timestamp}_{hash_part}.png"
        
        # Decode the response and return the image
        return decode_and_save(sdxl_response, filename)
    except Exception as e:
        # Handle general exceptions
        raise e

def build_payload(prompt):
    return ImageGenerationPayload(
        text_prompts=[
            TextPrompt(text=prompt)
        ],
        width=1024,
        height=1024,
        sampler="DPMPP2MSampler",
        cfg_scale=7.0,
        steps=50,
        seed=0,
        use_refiner=True,
        refiner_steps=40,
        refiner_strength=0.2
    )

def decode_and_save(response_bytes, filename):
    # Parse the JSON response to get the base64-encoded string
    response_json = json.loads(response_bytes)
    image_base64 = response_json['generated_image']

    # Decode the base64 string
    image_data = base64.b64decode(image_base64)

    # Create an image from the byte data and save it locally
    image = Image.open(io.BytesIO(image_data))
    image.save(filename)
    image.close()

    return filename

def upload_to_s3(filename, bucket_name, object_name):
    # Create an S3 client
    s3 = boto3.client('s3')

    # Upload the file to S3
    s3.upload_file(filename, bucket_name, object_name)

def main():
    model = sys.argv[1]
    prompt = sys.argv[2]
    if(model=="sdxl"):
        endpoint_name = "neuro-dev-sdxl-w8kx-endpoint"
    model_predictor = init(endpoint_name)
    payload = build_payload(prompt)
    print(generate_image(payload, model_predictor))

# main()
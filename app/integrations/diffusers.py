import base64
import datetime
import hashlib
import io
import json
import os
import re
from tkinter import Image
from fastapi import HTTPException
from sagemaker.predictor import Predictor
from sagemaker.serializers import JSONSerializer
from sagemaker.deserializers import BytesDeserializer
import sagemaker
import boto3
from PIL import Image
from IPython.display import display


sdxl_endpoint_name = os.environ.get("SDXL_ENDPOINT_NAME", "endpoint-name-not-set")



sess = sagemaker.Session()


# sdxl_model_predictor = Predictor(
#     endpoint_name=sdxl_endpoint_name, 
#     sagemaker_session=sess,
#     serializer=JSONSerializer(),
#     deserializer=BytesDeserializer()
# )

# smr = boto3.client('sagemaker-runtime')

# request = {
#         'inputs': prompt,
#         'parameters': DEFAULT_PARAMETERS
#     }

# response = smr.invoke_endpoint(
#             EndpointName=llm_endpoint_name,
#             ContentType=DEFAULT_CONTENT_TYPE,
#             Body=json.dumps(request)
#         )

sdxl_model_predictor = Predictor(
            endpoint_name=sdxl_endpoint_name, 
            sagemaker_session=sess,
            serializer=JSONSerializer(),
            deserializer=BytesDeserializer()
        )

DEFAULT_PARAMETERS = {
    "width": 1024,
    "height": 1024,
    "sampler": "DPMPP2MSampler",
    "cfg_scale": 7.0,
    "steps": 50,
    "seed": 133,
    "use_refiner": True,
    "refiner_steps": 40,
    "refiner_strength": 0.2
}

sample_payload = {
            "text_prompts":[{"text": "jaguar in the Amazon rainforest"}],
            "width": 1024,
            "height": 1024,
            "sampler": "DPMPP2MSampler",
            "cfg_scale": 7.0,
            "steps": 50,
            "seed": 133,
            "use_refiner": True,
            "refiner_steps": 40,
            "refiner_strength": 0.2
        }

def decode_and_show2(model_response) -> None:
    """
    Decodes and displays an image from SDXL output

    Args:
        model_response (GenerationResponse): The response object from the deployed SDXL model.

    Returns:
        None
    """
    image = Image.open(io.BytesIO(base64.b64decode(model_response)))
    display(image)
    image.close()

def test_diffuser():
    response_bytes = sdxl_model_predictor.predict(sample_payload)
    response_json = json.loads(response_bytes.decode('utf-8'))
    print(response_json)
    print(response_json["generated_image"])
    decode_and_show(response_bytes, "test.png")

def prompt_diffuser(diffuser_type, prompt):
    if diffuser_type == "sdxl":
        return generate_image(prompt, sdxl_endpoint_name)
    else:
        return generate_image(prompt, sdxl_endpoint_name)

def generate_image(prompt: str, diffuser_endpoint_name: str):
    try:
        text_prompts= [{"text": prompt}]
        # payload = {
        #     "text_prompts": text_prompts,
        #     **DEFAULT_PARAMETERS
        # }
        payload = {
            "text_prompts":[{"text": prompt}],
            "width": 1024,
            "height": 1024,
            "sampler": "DPMPP2MSampler",
            "cfg_scale": 7.0,
            "steps": 50,
            "seed": 133,
            "use_refiner": True,
            "refiner_steps": 40,
            "refiner_strength": 0.2
        }
        # Get prediction from SageMaker endpoint
        sdxl_response = sdxl_model_predictor.predict(payload)
        # filename = sanitize_filename(payload)
        return decode_and_show(sdxl_response, "test.png")
    except Exception as e:
        # Handle general exceptions
        raise HTTPException(status_code=500, detail=str(e))
    

def sanitize_filename(text):
    # Remove non-alphanumeric characters
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    # Replace spaces with underscores
    text = text.replace(' ', '_')
    # Shorten the text if it's too long
    safe_prompt = (text[:10] + '..') if len(text) > 10 else text
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    hash_part = hashlib.md5(text.encode()).hexdigest()[:6]
    filename = f"{safe_prompt}_{timestamp}_{hash_part}.png"
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
    img.save("temp/"+filename)
    


    return img_io
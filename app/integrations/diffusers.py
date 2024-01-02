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


def prompt_diffuser(diffuser_type, prompt):
    if diffuser_type == "sdxl":
        return generate_image(prompt, sdxl_endpoint_name)
    else:
        return generate_image(prompt, sdxl_endpoint_name)

def generate_image(prompt: str, diffuser_endpoint_name: str):
    try:
        sdxl_model_predictor = Predictor(
            endpoint_name=diffuser_endpoint_name, 
            sagemaker_session=sess,
            serializer=JSONSerializer(),
            deserializer=BytesDeserializer()
        )
        # Get prediction from SageMaker endpoint
        sdxl_response = sdxl_model_predictor.predict(prompt)
        # Decode the response and return the image
        filename = sanitize_filename(prompt)
        return decode_and_show(sdxl_response, filename)
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
    img.save("../temp/"+filename)
    


    return img_io
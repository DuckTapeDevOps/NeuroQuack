import os
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from fastapi.responses import StreamingResponse, PlainTextResponse
from mangum import Mangum
import boto3
from botocore.exceptions import NoCredentialsError

import base64
import io
from PIL import Image

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

# Assume other necessary imports are already done

app = FastAPI()

# Initialize SageMaker session and predictor
sess = sagemaker.Session()
sdxl_endpoint_name = "neuro-dev-sdxl-w8kx-endpoint"

# Define the predictor (this could also be done inside the endpoint call for a fresh setup each time)
sdxl_model_predictor = Predictor(
    endpoint_name=sdxl_endpoint_name, 
    sagemaker_session=sess,
    serializer=JSONSerializer(),
    deserializer=BytesDeserializer()
)


@app.get("/test")
async def test():
    return {"response": "this works!"}

@app.post("/generate-image")
async def generate_image(payload: ImageGenerationPayload):
    try:
        # Convert the Pydantic model to a dictionary
        sdxl_payload = payload.dict(by_alias=True)
        
        # Get prediction from SageMaker endpoint
        sdxl_response = sdxl_model_predictor.predict(sdxl_payload)
        
        # Decode the response and return the image
        return decode_and_show(sdxl_response)
    except Exception as e:
        # Handle general exceptions
        raise HTTPException(status_code=500, detail=str(e))

# The `decode_and_show` function remains the same as previously defined
class DownloadFileBody(BaseModel):
    bucket_name: str
    file_name: str

@app.get("/download")
async def download_file(body: DownloadFileBody):
    bucket_name = body.bucket_name
    file_name = body.file_name
    try:
        s3.download_file(bucket_name, file_name, '/tmp/temp.txt')
        with open('/tmp/temp.txt', 'r') as f:
            file_content = f.read()
        return PlainTextResponse(file_content)
    except FileNotFoundError:
        return {"error": "File not found"}
    except NoCredentialsError:
        return {"error": "Credentials not available"}

def decode_and_show(response_bytes):
    # Parse the JSON response to get the base64-encoded string
    response_json = json.loads(response_bytes)
    image_base64 = response_json['generated_image']

    # Decode the base64 string
    image_data = base64.b64decode(image_base64)

    # Create an image from the byte data
    image = Image.open(io.BytesIO(image_data))
    
    # Prepare the image data for streaming
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    image.close()
    
    return StreamingResponse(img_io, media_type='image/png')
if os.getenv('AWS_EXECUTION_ENV') is not None:
    handler = Mangum(app)
else:
    handler = app
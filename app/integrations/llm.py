import json
import os
from fastapi import HTTPException
import sagemaker
from pydantic import BaseModel
import boto3

mistral_endpoint_name = os.environ.get("MISTRAL_ENDPOINT_NAME", "endpoint-name-not-set")
neural_endpoint_name = os.environ.get("NEURAL_ENDPOINT_NAME", "endpoint-name-not-set")
sess = sagemaker.Session()

# Create a SageMaker client
smr = boto3.client('sagemaker-runtime')


DEFAULT_CONTENT_TYPE = "application/json"
DEFAULT_HISTORY = [
]
DEFAULT_SYSTEM_PROMPT = "You are a twitch bot. All of your responses are responses to chat messages and must be kept under 500 characters."
DEFAULT_PARAMETERS = {
    "do_sample": True,
    "top_p": 0.9,
    "temperature": 0.8,
    "max_new_tokens": 512,
    "repetition_penalty": 1.03,
    "stop": ["###", "</s>"]
}

def prompt_llm(llm_type, prompt):
    if llm_type == "mistral":
        return generate_llm_response(prompt, mistral_endpoint_name)
    else:
        return generate_llm_response(prompt, neural_endpoint_name)

def generate_llm_response(prompt: str, llm_endpoint_name: str):
    print(f"Generating response for prompt: {prompt} on endpoint {llm_endpoint_name}")
    request = {
        'inputs': prompt,
        'parameters': DEFAULT_PARAMETERS
    }

    try:
        response = smr.invoke_endpoint(
            EndpointName=llm_endpoint_name,
            ContentType=DEFAULT_CONTENT_TYPE,
            Body=json.dumps(request)
        )
        response_body = response['Body'].read().decode('utf-8')
        response_data = json.loads(response_body)
        generated_text = response_data[0]['generated_text']
        return generated_text
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")
import json
import os
from fastapi import HTTPException
import sagemaker
from pydantic import BaseModel
import boto3
from dotenv import load_dotenv


if not os.getenv("MISTRAL_ENDPOINT_NAME"):
    load_dotenv()

MISTRAL_ENDPOINT_NAME = os.environ.get("MISTRAL_ENDPOINT_NAME", "endpoint-name-not-set")
NEURAL_ENDPOINT_NAME = os.environ.get("NEURAL_ENDPOINT_NAME", "endpoint-name-not-set")
DEFAULT_LLM_TYPE = os.environ.get("DEFAULT_LLM_TYPE", "mistral")

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

help_text = "To use !llm, type !llm <model> <prompt>. For example, !llm mistral explain my next step. The model can be either mistral or neural. The prompt can be any text you want to use to generate a response. The response will be sent to chat as a message."

def query(llm_type, prompt):
    if llm_type == "mistral":
        return generate_llm_response(prompt, MISTRAL_ENDPOINT_NAME)
    elif llm_type == "neural":
        return generate_llm_response(prompt, NEURAL_ENDPOINT_NAME)
    else:
        return (help_text)

def generate_llm_response(prompt: str, llm_endpoint_name: str):
    print(f"Generating response for prompt: {prompt} on endpoint {llm_endpoint_name}")
    request = {
        'inputs': prompt,
        'parameters': DEFAULT_PARAMETERS
    }

    try:
        response = smr.invoke_endpoint( # smr is the SageMaker runtime client via boto3
            EndpointName=llm_endpoint_name,
            ContentType=DEFAULT_CONTENT_TYPE,
            Body=json.dumps(request)
        )
        response_body = response['Body'].read().decode('utf-8')  # get the response
        response_data = json.loads(response_body) # parse the response into JSON
        generated_text = response_data[0]['generated_text'] # get the generated text from the response
        return generated_text 
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")
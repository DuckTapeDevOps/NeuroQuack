import json
import os
import replicate
import boto3
import sagemaker

sess = sagemaker.Session()

CLIP_ENDPOINT_NAME = os.environ.get("CLIP_ENDPOINT_NAME", "endpoint-name-not-set")

ci_deployment = replicate.deployments.get("ducktapedevops/image-to-prompt")


smr = boto3.client('sagemaker-runtime')

# response = client.invoke_endpoint(
#     EndpointName='string',
#     Body=b'bytes'|file,
#     ContentType='string',
#     Accept='string',
#     CustomAttributes='string',
#     TargetModel='string',
#     TargetVariant='string',
#     TargetContainerHostname='string',
#     InferenceId='string',
#     EnableExplanations='string',
#     InferenceComponentName='string'
# )



def image_to_caption(image_path: str):
    response = smr.invoke_endpoint_async(
        EndpointName='string', # REQUIRED
        ContentType='string', # optional
        Accept='string',    # optional
        CustomAttributes='string', # optional
        InferenceId='string', # optional
        InputLocation='string', # REQUIRED
        RequestTTLSeconds=123, # optional
        InvocationTimeoutSeconds=123 # optional
    )
    # caption = captioner(image_path)[0]['generated_text']
    return caption

def clip_interrogate_deployed(image_path: str):
    prediction = ci_deployment.predictions.create(
    input={
        "mode": "fast",
        "clip_model_name": "ViT-L-14/openai",
        "image": open(image_path, "rb")
        }
    )
    prediction.wait()
    print(prediction.output)
    return prediction.output

def image_to_prompt(image_path: str):
    prediction = ci_deployment.predictions.create(
    input={
        "mode": "fast",
        "clip_model_name": "ViT-L-14/openai",
        "image": open(image_path, "rb")
        }
    )
    prediction.wait()
    print(prediction.output)
    return prediction.output

def clip_interrogate(image_source: str):
    print("clip_interrogate: " + image_source)
    input_data = {
        "mode": "fast",
        "clip_model_name": "ViT-L-14/openai"
    }

    # Check if the source is a URL or a file path
    if image_source.startswith(('http://', 'https://')):
        input_data["image"] = image_source
    else:
        # Assuming it's a file path
        with open(image_source, "rb") as file:
            input_data["image"] = file

    output = replicate.run(
        "pharmapsychotic/clip-interrogator:8151e1c9f47e696fa316146a2e35812ccf79cfc9eba05b11c7f450155102af70",
        input=input_data
    )
    return output
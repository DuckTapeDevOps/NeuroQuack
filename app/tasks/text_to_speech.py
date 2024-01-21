import os
from dotenv import load_dotenv
import replicate


if not os.getenv("REPLICATE_ORG"):
    load_dotenv()

REPLICATE_ORG = os.environ.get("REPLICATE_ORG", "default-not-set") # "ducktapedevops"

tortoise_deployment = replicate.deployments.get(f"{REPLICATE_ORG}/tortoise-tts")

def tts(prompt: str):
    

    prediction = deployment.predictions.create(
        input={"text": prompt}
    )
    prediction.wait()
    print(prediction.output)
    return prediction.output

deployment = replicate.deployments.get(f"{REPLICATE_ORG}/tortoise-tts")

prediction = deployment.predictions.create(
  input={"text": "The expressiveness of autoregressive transformers is literally nuts! I absolutely adore them."}
)
prediction.wait()
print(prediction.output)
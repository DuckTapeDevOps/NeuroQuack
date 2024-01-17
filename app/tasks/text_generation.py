import os
from dotenv import load_dotenv
import replicate


if not os.getenv("REPLICATE_ORG"):
    load_dotenv()

REPLICATE_ORG = os.environ.get("REPLICATE_ORG", "default-not-set") # "ducktapedevops"

deployment = replicate.deployments.get(f"{REPLICATE_ORG}/neural-chat")

async def text_generation(prompt):
    prediction = await deployment.predictions.async_create(
        input={"prompt": prompt}
    )
    prediction.wait()
    print(prediction.output)
    return prediction.output
import replicate


deployment = replicate.deployments.get("ducktapedevops/neural-chat")

async def text_generation(prompt):
    prediction = await deployment.predictions.async_create(
        input={"prompt": prompt}
    )
    print("lazy debug")
    prediction.wait()
    print(prediction.output)
    print("lazy debug 2")
    return prediction.output
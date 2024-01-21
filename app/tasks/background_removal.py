import replicate


background_removal_deployment = replicate.deployments.get("ducktapedevops/bg-rm")


async def background_removal(img_url):
    prediction = await background_removal_deployment.predictions.async_create(
        input={"file": img_url}
    )
    prediction.wait()
    print(prediction.output)
    return prediction.output
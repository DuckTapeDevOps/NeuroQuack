import replicate

ci_deployment = replicate.deployments.get("nonpareilnic/clip-interrogator")

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


def clip_interrogate(image_path: str):
    output = replicate.run(
        "pharmapsychotic/clip-interrogator:8151e1c9f47e696fa316146a2e35812ccf79cfc9eba05b11c7f450155102af70",
            input={
                "mode": "fast",
                "clip_model_name": "ViT-L-14/openai",
                "image": open(image_path, "rb")
            }
        )
    return output
import asyncio
from inference_interaction import generate_image, init, build_payload


async def diffuser_query(self, ctx):
    prompt = ctx.message.content.replace("!sdxl ", "")
    endpoint_name = "neuro-dev-sdxl-w8kx-endpoint"
    model_predictor = init(endpoint_name)
    payload = build_payload(prompt)

    try:
        # Run the generate_image function in an executor to avoid blocking
        filename = await asyncio.get_event_loop().run_in_executor(
            None, generate_image, payload, model_predictor
        )
        # If you have a URL where the image is hosted, you can send it here
        await ctx.send(f"Image generated successfully: [URL to the image]")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
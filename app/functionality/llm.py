import textwrap
from inference_interaction import generate_image, init, build_payload


async def LLM_Query(ctx):
    prompt = ctx.message.content.replace("!llama ", "")
    reply = await run_llm(prompt)

    # Split the reply into chunks of 500 characters
    chunks = textwrap.wrap(reply, 500)

    # Send each chunk as a separate message
    for chunk in chunks:
        await ctx.send(chunk)
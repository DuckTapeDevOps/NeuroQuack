import os
import requests


def download_image(url, directory, filename):
    """Download an image and save it to the `images` directory.
    """
    # The path to save the image
    file_path = os.path.join(directory, filename)

    # Fetch the image
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Write the image to a file
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Image saved as {file_path}")
        return file_path, response.content
    else:
        print("Failed to download image")
        return None, None
    

def list_inference_endpoints():
    """List all inference endpoints.
    """
    return [
        "mistral",
        "neural"
    ]
def computing(user: str, emoji="duckta12Type"):
    """Computing
    """
    return f" {emoji} @{user}"

def input_map(ctx):
    print(f"Received command: {ctx.message.content}")
    try:
        user = ctx.author.name
        split = ctx.message.content.split(" ")
        command = split[1]
        return {
            "user": user,
            "command": command,
            "input": ctx.message.content.replace(f"{command} ", "").replace(f"{user}", "")
        }
    except Exception as e:
        print(f"Error parsing command: {e}")
        return None
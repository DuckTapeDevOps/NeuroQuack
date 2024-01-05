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
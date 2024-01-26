from PIL import Image
import io



def sanitize_text(text, max_length):
    text = text.lstrip()
    if len(text) > max_length:
        text = text[:max_length] + ".."
    return text 

def resize_image(image_data, width, height):
    # Open the image from the image_data object
    image = Image.open(io.BytesIO(image_data))

    # Resize the image
    resized_image = image.resize((width, height), Image.ANTIALIAS)

    # Save the resized image as a BytesIO object
    output_buffer = io.BytesIO()
    resized_image.save(output_buffer, format="PNG")
    output_buffer.seek(0)
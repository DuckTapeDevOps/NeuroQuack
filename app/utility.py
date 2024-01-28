from PIL import Image
import io
from stl import mesh
import numpy as np
import pywavefront


def obj_to_stl(obj_file_path, stl_file_path):
    """
    Convert a .obj file to .stl
    :param obj_file_path: Path to the .obj file
    :param stl_file_path: Path to the .stl file
    """
    # Load .obj file
    scene = pywavefront.Wavefront(obj_file_path, collect_faces=True)

    # Create numpy array to hold mesh data
    data = np.zeros(len(scene.mesh_list[0].faces), dtype=mesh.Mesh.dtype)

    # Fill numpy array with mesh data
    for i, face in enumerate(scene.mesh_list[0].faces):
        for j in range(3):
            data['vectors'][i][j] = scene.vertices[face[j]]

    # Create mesh object
    obj_mesh = mesh.Mesh(data)

    # Save as .stl
    obj_mesh.save(stl_file_path)

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
from rembg import remove
from PIL import Image

def remove_background(input_path, output_path):
    with open(input_path, "rb") as i:
        input_image = i.read()
        output_image = remove(input_image)
    with open(output_path, "wb") as o:
        o.write(output_image)

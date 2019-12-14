import os
from PIL import Image

## Creating square image based on puzzle size (3/4/5). 
## Note - Each puzzle block size must be 100x100
def setup_image_requirements(image_path, puzzle_shape):
    image_obj = Image.open(image_path)
    base_sq_size = 100 * puzzle_shape
    wpercent = (base_sq_size/float(image_obj.size[0]))
    new_size = int((float(image_obj.size[0])*float(wpercent)))
    image_obj = image_obj.resize((base_sq_size,new_size), Image.ANTIALIAS)
    new_file_name = "{}_temp.jpg".format(os.path.splitext(image_path)[0])
    image_obj.save(new_file_name)
    return new_file_name
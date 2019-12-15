import os
import numpy as np
from skimage.util.shape import view_as_blocks
from PIL import Image
import image_slicer
import skimage.io


main_dir_home = 'data'

image_knn_name = "data/temp_image.jpg"


test_dir_home = 'tempdata/test'
test_image_prefix = 'test_img'

train_dir_home = 'tempdata/train'
train_image_prefix = 'train_img'

all_image_format = "jpeg"

def create_dir_if_not_exisit(dir_name):
    outDir = os.path.join(os.getcwd(), dir_name)
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    return outDir

## Shuffle image
def generate_training_data(image_np, row_col):
    image_url = save_image_to_disk_from_np_array(image_np)
    ## check if "train_dir_home" folder exist otherwise exception
    return generate_train_n_test_data_from_image(image_url, row_col, train_dir_home, train_image_prefix)

## Original Image
def generate_test_data(image_url, row_col):
    ## check if "test_dir_home" folder exist otherwise exception
    return generate_train_n_test_data_from_image(image_url, row_col, test_dir_home, test_image_prefix)

def save_image_to_disk_from_np_array(passed_image_np):
    pill_image = Image.fromarray(passed_image_np.astype('uint8'), 'RGB')
    pill_image.save(image_knn_name)
    return image_knn_name

def generate_train_n_test_data_from_image(image_url, row_col, data_dir, img_prefix):
    create_dir_if_not_exisit(data_dir)
    ## Generating Test Images -> From shuffled Image
    ## Removing previous files (if found)
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            os.remove(os.path.join(root, file))
    ## Slicing square images from the sourc image
    tiles = image_slicer.slice(image_url, row_col * row_col, save = False)
    ## Saving square images to the disk
    test_images_list = image_slicer.save_tiles(tiles, directory=data_dir, prefix=img_prefix, format=all_image_format)
    ## return the list of images
    return test_images_list

def load_images_into_memory(file_list, img_prefix, img_file_type):
    imgs = []
    for file in file_list:
        start = str(file).find(img_prefix)
        end = len(str(file))
        fname = str(file)[start:end-1]
        fname = os.path.join(os.getcwd(), main_dir_home, img_file_type , fname)
        img = skimage.io.imread(fname, as_gray=False)
        imgs.append(img)
    return imgs
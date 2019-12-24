from skimage import data
from skimage.color import rgb2gray, rgb2hsv, rgb2hed

def convert_color_to_grayscale(img_orig):
    grayscale = rgb2gray(img_orig)
    return grayscale

def convert_color_to_rgb2hsv(img_orig):
    grayscale = rgb2hsv(img_orig)
    return grayscale

def convert_color_to_rgb2hsl(img_orig):
    grayscale = rgb2hed(img_orig)
    return grayscale

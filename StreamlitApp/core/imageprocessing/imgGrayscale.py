from skimage import data
from skimage.color import rgb2gray, rgb2hsv, rgb2hed, gray2rgb

import streamlit as st

def convert_color_to_grayscale(img_orig):
    grayscale = rgb2gray(img_orig)
    return grayscale

def convert_color_to_rgb2hsv(img_orig):
    try:
        img_orig = gray2rgb(img_orig, alpha=None)
        result_image = rgb2hsv(img_orig)
    except:
        st.empty()
        result_image = img_orig
         
    return result_image

def convert_color_to_rgb2hsl(img_orig):
    ## TODO: Need work
    grayscale = rgb2hed(img_orig)
    return grayscale

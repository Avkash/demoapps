from skimage import data
from skimage.transform import resize
import streamlit as st


def process_resize(img_orig):
    height = img_orig.shape[0]
    size = 50
    size = st.slider("Select image height between 25 to {}:".format(height), 25,height,50,25)
    img_resized = resize(img_orig, (size, size))
    return img_resized

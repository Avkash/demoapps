from skimage import data
from skimage.transform import rotate
import streamlit as st


def process_rotation(img_orig):
    max_angle = 360
    angle = 70
    angle = st.slider("Select image rotation angle between 0 to {}:".format(max_angle), 0,max_angle,70,5)
    image_rotated = rotate(img_orig, angle=angle, resize=True)
    return image_rotated

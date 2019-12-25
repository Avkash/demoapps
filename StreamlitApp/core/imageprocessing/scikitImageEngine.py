import streamlit as st
from datetime import datetime
from skimage.io import imread, imshow
from skimage import data

import numpy as np

import utils.globalDefine as globalDefine
import core.imageprocessing.imgSelection as imgSelection
import core.imageprocessing.imgGrayscale as imgGrayscale
import core.imageprocessing.imgResize as imgResize
import core.imageprocessing.imgRotation as imgRotation
import core.imageprocessing.imgFlip as imgFlip
import core.imageprocessing.imgBrightness as imgBrightness
import core.imageprocessing.imgFliters as imgFliters
import core.imageprocessing.imgSegmentation as imgSegmentation


def calc_main(title, subtitle):
    st.write("Scikit Image Demo")    

    st.sidebar.title(title)
    st.sidebar.info(
        subtitle
    )

    img_keys = globalDefine.IMAGE_LIST.keys()    
    img_id = st.sidebar.selectbox("Select Image: ", list(img_keys))
    img_selected = globalDefine.IMAGE_LIST.get(img_id)

    image = imgSelection.process_selection(img_selected)
    st.image(image,  width=400)

    op_keys = globalDefine.IMGPROC_TYPES.keys()    
    op_id = st.selectbox("Select choice: ", list(op_keys))
    op_selected = globalDefine.IMGPROC_TYPES.get(op_id)

    if op_selected == "GRAYSCALE":
        img = imgGrayscale.convert_color_to_grayscale(image)
        st.image(img, width=400)
    if op_selected == 'RGB2HSV':
        img = imgGrayscale.convert_color_to_rgb2hsv(image)
        st.image(img, width=400)
    if op_selected == 'RGB2HSL':
        img = imgGrayscale.convert_color_to_rgb2hsl(image)
        st.image(img, width=400)
    if op_selected == 'RESIZE':
        img = imgResize.process_resize(image)
        st.image(img)
        if st.checkbox("Show code? "):
            st.write("Show code")
    if op_selected == 'ROTATION':
        img = imgRotation.process_rotation(image)
        st.image(img)
        if st.checkbox("Show code? "):
            st.write("Show code")
    if op_selected == 'FLIP':
        img = imgFlip.process_flip(image)
        st.image(img)
        if st.checkbox("Show code? "):
            st.write("Show code")
    if op_selected == 'BRIGHTNESS':
        img = imgBrightness.process_brightness(image)
        st.image(img)
        if st.checkbox("Show code? "):
            st.write("Show code")
    if op_selected == 'FILTER':
        img = imgFliters.process_filters(image)
        st.image(img, width=300)
        if st.checkbox("Show code? "):
            st.write("Show code")
    if op_selected == "SEGMENTATION":
        img = imgSegmentation.process_segmentation(image)
        st.image(img, width=300)
        if st.checkbox("Show code? "):
            st.write("Show code")
    else:
        st.write("Thanks!!")
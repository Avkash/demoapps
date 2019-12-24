import streamlit as st
from datetime import datetime
from skimage.io import imread, imshow
from skimage import data

import numpy as np

import utils.globalDefine as globalDefine
import core.imageprocessing.imgGrayscale as imgGrayscale

def calc_main(title, subtitle):
    st.write("Scikit Image Demo")    

    st.sidebar.title(title)
    st.sidebar.info(
        subtitle
    )

    image = data.astronaut()
    st.image(image,  width=400)

    op_keys = globalDefine.IMGPROC_TYPES.keys()    
    op_id = st.selectbox("Select choice: ", list(op_keys))
    op_selected = globalDefine.IMGPROC_TYPES.get(op_id)

    if op_selected == "GRAYSCALE":
        img = imgGrayscale.convert_color_to_grayscale(image)
        st.image(img, width=400)
    if op_selected == 'RGB2HSV':
        img = imgGrayscale.convert_color_to_grayscale(image)
        st.image(img, width=400)
    if op_selected == 'RGB2HSL':
        img = imgGrayscale.convert_color_to_grayscale(image)
        st.image(img, width=400)
    else:
        st.write("Thanks!!")
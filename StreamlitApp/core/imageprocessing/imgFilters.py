from skimage import data
from skimage import filters, restoration
from skimage.color import rgb2gray
import streamlit as st
import numpy as np

import utils.globalDefine as globalDefine

def process_filters(img_orig):
    filter_keys = globalDefine.FILTER_CHOICE.keys()    
    filter_id = st.selectbox("Select filter choice: ", list(filter_keys))
    filter_choice = globalDefine.FILTER_CHOICE.get(filter_id)

    try:
        ## If image is color it will change to gray
        img_orig = rgb2gray(img_orig)
    except:
        ## Do nothing
        st.empty()

    if filter_choice == "MEDIAN":
        max_val = 30
        val = 10
        val = st.slider("Select mask between 0 to {}:".format(max_val), 0,max_val,val,1)
        return filters.median(img_orig, np.ones((val, val)))
    if filter_choice == "GAUSSIAN":
        max_val = 20
        val = 5
        val = st.slider("Select sigma value between 0 to {}:".format(max_val), 0,max_val,val,1)
        return filters.gaussian(img_orig, sigma=(0.1, float(val)), truncate=3.5, multichannel=True)
    if filter_choice == 'RESTORATION':
        max_val = 10
        val = 5
        val = st.slider("Select weight between 1 to {}:".format(max_val), 1,max_val,val,1)
        return restoration.denoise_tv_chambolle(img_orig, weight=float(val/10))
    if filter_choice == "SOBEL":
        return filters.sobel(img_orig, mask=None)
    else:
        image_final = img_orig
        return image_final

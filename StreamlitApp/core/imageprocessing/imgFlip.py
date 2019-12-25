from skimage import data
from skimage.transform import rotate
import streamlit as st
from numpy import fliplr, flipud

import utils.globalDefine as globalDefine

def process_flip(img_orig):
    flip_keys = globalDefine.FLIP_CHOICE.keys()    
    flip_id = st.selectbox("Select flip choice: ", list(flip_keys))
    flip_choice = globalDefine.FLIP_CHOICE.get(flip_id)

    if flip_choice == "ORIG":
        image_flipped = img_orig
    if flip_choice == "FLIP_LR":
        image_flipped = fliplr(img_orig)
    elif flip_choice == "FLIP_VR":
        image_flipped = flipud(img_orig)
    else:
        image_flipped = img_orig
    return image_flipped

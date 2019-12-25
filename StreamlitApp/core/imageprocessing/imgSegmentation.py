from skimage import segmentation
from skimage import filters, restoration
from skimage.color import rgb2gray
import numpy as np
import streamlit as st


def process_segmentation(img_orig):
    try:
        ## If image is color it will change to gray
        img_orig = rgb2gray(img_orig)
    except:
        ## Do nothing
        st.empty()

    mask = img_orig > filters.threshold_otsu(img_orig)
    img_border = segmentation.clear_border(mask).astype(np.int)
    img_edges = segmentation.mark_boundaries(img_orig, img_border)
    return img_edges

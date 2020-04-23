import streamlit as st
from datetime import datetime

import random

import numpy as np
import os
from PIL import Image
from scipy import stats
from imageio import imsave
import matplotlib.pyplot as plt
from skimage.util.shape import view_as_blocks
import core.ImageFormater as ImageFormatter
import cv2
# import image_slicer

import skimage.io


import utils.globalDefine as globalDefine


@st.cache(allow_output_mutation=True)
def load_image_from_upload(file):
    tmp = np.fromstring(file.read(), np.uint8)
    return cv2.imdecode(tmp, 1)


def run_main(title, subtitle):
    st.write("[Quick Demo]")
    frameST = st.empty()

    st.sidebar.title(title)
    st.sidebar.info(
        subtitle
    )

    cpu_gpu_keys = globalDefine.CPU_GPU_OPTIONS.keys()
    cpu_gpu_id = st.selectbox("Select CPU or GPU: ", list(cpu_gpu_keys))
    cpu_gpu_choice = globalDefine.PUZZLE_SIZE.get(cpu_gpu_id)

    file_ready = False
    uploaded_file = st.file_uploader("Choose a file", type=['jpg'])
    if uploaded_file is not None:
        image_path = load_image_from_upload(uploaded_file)
        cv2.imwrite("3d-photo-inpainting/image/3dimage.jpg", image_path)
        st.image(uploaded_file, use_column_width=True)
        if os.path.isfile('3d-photo-inpainting/image/3dimage.jpg'):
            file_ready = True

    if file_ready:
        st.button('Start 3D Photo Rendering')
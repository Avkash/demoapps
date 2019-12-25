from skimage import exposure
import streamlit as st


def process_brightness(img_orig):
    max_gamma = 50
    gamma_value = 5
    gamma_value = st.slider("Select brightness value between 0 to {}:".format(max_gamma), 0,max_gamma,5, 1)
    image_final = exposure.adjust_gamma(img_orig, gamma=gamma_value/10,gain=1)
    return image_final

import pathlib
import utils.display as udisp
import streamlit as st
import utils.globalDefine as globalDefine


def write():
    udisp.title_awesome("3D Photo Creator")

    video_keys = globalDefine.SAMPLE_VIDEO_LIST.keys()
    video_id = st.selectbox("Select a sample 3D video output ", list(video_keys))
    video_choice = globalDefine.SAMPLE_VIDEO_LIST.get(video_id)
    st.video(video_choice, format='video/mp4', start_time=0)
    udisp.render_md("resources/home_info.md")


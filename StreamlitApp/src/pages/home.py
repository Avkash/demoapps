import pathlib
import utils.display as udisp

import streamlit as st


def write():
    udisp.title_awesome("Puzzle Solver Home")
    udisp.render_md("resources/home_info.md")


import pathlib
import utils.display as udisp

import streamlit as st
import core.calculator.CalcEngine as CalcEngine

def write():
    udisp.title_awesome("Calculator")
    CalcEngine.calc_main("Calculator", "A simple calclator to operator two digits")

    st.write("@avkashchauhan")
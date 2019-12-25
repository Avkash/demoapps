import streamlit as st
from datetime import datetime

import numpy as np

import utils.display as display
import utils.globalDefine as globalDefine

def calc_main(title, subtitle):
    st.write("A Simple Calculator")    

    st.sidebar.title(title)
    st.sidebar.info(
        subtitle
    )

    show_operator = False
    num1 = 0
    num2 = 0
    num1_in = st.text_input('Please input first number: ')
    '''
    if not num1_in.isnumeric():
        st.write("The input number must be numeric")
    else:
        num1 = int(num1_in)
    '''

    num2_in = st.text_input('Please input second number: ')
    '''
    if not num2_in.isnumeric():
        st.write("The input number must be numeric")
    else:
        num2 = int(num2_in)
    '''

    if not num1_in.isnumeric() and not num2_in.isnumeric():
        st.write("Both input must be numeric")
    else:
        num1 = int(num1_in)
        num2 = int(num2_in)
        show_operator = True

    if show_operator:
        op_keys = globalDefine.OPERATOR_LIST.keys()    
        op_id = st.selectbox("Select Operator: ", list(op_keys))
        op_selected = globalDefine.OPERATOR_LIST.get(op_id)

        if op_selected == "PLUS":
            st.write("The sum is ", num1 + num2)
        elif op_selected == "MINUS":
            st.write("The substrction is ", num1 - num2)
        elif op_selected == "TIMES":
            st.write("The multiplication is ", num1 * num2)
        elif op_selected == "DIVISION":
            st.write("The division is ", num1 / num2)

    if st.checkbox("Show source code? "):
        st.code(display.show_code("core/calculator/CalcEngine.py"))

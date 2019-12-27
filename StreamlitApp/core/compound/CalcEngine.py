import streamlit as st
from datetime import datetime

import numpy as np

import utils.display as display
import utils.globalDefine as globalDefine

'''
    https://www.thecalculatorsite.com/finance/calculators/compoundinterestcalculator.php
'''

def yearly_compound_interest(P, R, T):   
    CI = P * (pow((1 + R / 100), T)) 
    return CI

def monthly_compound_interest(P, R, T):   
    CI = P * ((1 + R / 12) ** (12 * T))
    return CI

def calc_main(title, subtitle):
    st.sidebar.title(title)
    st.sidebar.info(
        subtitle
    )

    if st.checkbox("Show help document? "):
        display.render_md("resources/compound.md")

    show_operator = False
    principal_float = st.text_input('Please input principal amound: ')
    rate_float = st.text_input('Please input annual interest rate (float): ')
    years_float = st.text_input('Please input years (float): ')

    m_y_keys = globalDefine.CI_CHOICE.keys()    
    m_y_id = st.selectbox("Select Compound Option (Monthly/Yearly): ", list(m_y_keys))
    monthly_yearly = globalDefine.CI_CHOICE.get(m_y_id)

    if not principal_float.isnumeric() and not rate_float.isnumeric() and not years_float.isnumeric():
        st.write("Principal, rate & years must be numeric")
    else:
        P = float(principal_float)
        R = float(rate_float)
        N = float(years_float)
        show_operator = True

    if show_operator:
        if (monthly_yearly == "YEARLY"):
            st.write("Formula: " + "CI = P * (pow((1 + R / 100), N)) ")
            CI = yearly_compound_interest(P,R,N)
            st.write('At the end of ', N, 'year(s) your principal plus compound interest will be $',format(CI, '.2f'))
        else:
            st.write("Formula: " + "CI = P * (1 + R / 12) ** (12 * T)")
            st.write("Note: For montly compound interst the rate is divided by 100 means R = R/100")
            CI = monthly_compound_interest(P,R/100,N)
            st.write('At the end of ', N, 'year(s) your principal plus compound interest will be $',format(CI, '.2f'))

    
    if st.checkbox("Show source code? "):
        st.code(display.show_code("core/compound/CalcEngine.py"))

    st.write("Forumla Source: https://www.thecalculatorsite.com/finance/calculators/compoundinterestcalculator.php")


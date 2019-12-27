import streamlit as st

import utils.display as udisp

import src.pages.home
import src.pages.about
import src.pages.calculator
import src.pages.compound
import src.pages.scikit_image

MENU = {
    "Home" : src.pages.home,
    "Simple Calculator" : src.pages.calculator,
    "Calculate Compound Interest" : src.pages.compound,
    "Scikit Image Demo" : src.pages.scikit_image,
    "Credits" : src.pages.about
}

def main():
    st.sidebar.title("Navigate yourself...")
    menu_selection = st.sidebar.radio("Choice your option...", list(MENU.keys()))

    menu = MENU[menu_selection]

    with st.spinner(f"Loading {menu_selection} ..."):
        udisp.render_page(menu)

    st.sidebar.info(
        "https://github.com/Avkash/demoapps"
    )
    st.sidebar.info(
        "demoapps/StreamlitApp"
    )

if __name__ == "__main__":
    main()
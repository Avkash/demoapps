import streamlit as st

import utils.display as udisp

import src.pages.home
import src.pages.CreatorDemo
import src.pages.about
import src.pages.codereview


MENU = {
    "Home": src.pages.home,
    "3D Photo Creator (Quick Demo)": src.pages.CreatorDemo,
    "Credits": src.pages.about
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


if __name__ == "__main__":
    main()

import streamlit as st

import utils.display as udisp

import src.pages.home
import src.pages.solver
import src.pages.solverc
import src.pages.solverdemo
import src.pages.about
import src.pages.codereview


MENU = {
    "Home" : src.pages.home,
    "Puzzle Solver (Quick Demo)" : src.pages.solverdemo,
    "Puzzle Solver (Walkthrough Demo)" : src.pages.solver,
    "Solve puzzle (Bring your images)" : src.pages.solverc,
    "How it works (Review)?" : src.pages.codereview,
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

if __name__ == "__main__":
    main()
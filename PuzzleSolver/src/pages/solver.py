import pathlib
import utils.display as udisp

import core.CoreSolver as CoreSolver

import streamlit as st

def write():
    udisp.title_awesome("Step by Step Walkthrough")
    CoreSolver.run_main("Title", "Subtitle")
    
def solve_custom():
    udisp.title_awesome("Step by Step Walkthrough")
    CoreSolver.run_main("Title", "Subtitle")

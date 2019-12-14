import pathlib
import utils.display as udisp

import core.SolverQuickDemo as SolverQuickDemo

import streamlit as st

def write():
    udisp.title_awesome("Puzzle Solver")    
    SolverQuickDemo.run_main("Title", "Subtitle")
    
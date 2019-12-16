import pathlib
import utils.display as udisp

import core.CoreSolver as CoreSolver

import streamlit as st

def write():
    udisp.title_awesome("Step by Step Walkthrough")
    CoreSolver.run_main("Configration", "Just select the image, model type and puzzle size, and GO")
    

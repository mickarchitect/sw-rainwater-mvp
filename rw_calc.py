import numpy as np
import pandas as pd
import time
import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk

def data_view_main() :
    st.markdown("## data view main")
    return

def display_view_about() :
    st.markdown("## About")
    return


######################################################################
# Main
#
# Later
######################################################################

drvg_dctnry = {'Data View Main' : data_view_main,
               'About' : display_view_about}
page_list = list(drvg_dctnry.keys())
page = st.sidebar.radio('Select page:', page_list)

drvg_dctnry[page]()

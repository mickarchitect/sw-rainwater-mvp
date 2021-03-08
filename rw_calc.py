"""
This module contains the main program and all functions to perform
rainwater harvesting calculations and view rainwater data.
"""

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import streamlit as st


def rf_data_view() :
    """Rainfall Data - view selected historical data by selected location."""
    hdr_cntnr, crit_cntnr1, crit_cntnr2, crit_cntnr3 = st.beta_columns([1, 1, 1, 1])
    hdr_cntnr.markdown('## Historical Rainfall by Location')
    loc = crit_cntnr1.selectbox('Location: ', ['Kathmandu, Nepal', 'Fairplay, US'])
    beg_year = crit_cntnr2.selectbox('Begin Year: ', [2003, 2004, 2005])
    end_year = crit_cntnr3.selectbox('End Year: ', [2003, 2004, 2005])
    yr_plot_cntnr, mth_plot_cntnr = st.beta_columns(2)
    rainfall_raw_df = pd.read_csv("rainfall_data/Nepal/kathmandu-20042013.csv")
    df_tmp1 = rainfall_raw_df['date'].str.split('-')
    df_tmp2 = df_tmp1.tolist()
    df_tmp3 = pd.DataFrame(df_tmp2, columns=['year', 'mth', 'day', ])
    rainfall_df = rainfall_raw_df.join(df_tmp3)
    rf_yr_df = rainfall_df.groupby('year', as_index = False)['rainfall'].sum()
    fig, ax = plt.subplots()
    ax.set_title('Kathmandu Rainfall Average by Year')
    ax.set_ylabel('Rainfall Amount')
    ax.set_xlabel('Year')
    x = rf_yr_df['year']
    y = rf_yr_df['rainfall']
    ax.plot(x, y)
    yr_plot_cntnr.pyplot(fig)
    mgb = rainfall_df.groupby(['mth'], as_index=False)
    mgb_df = mgb.agg(np.mean).rename(columns={'rainfall' : 'rf_avg'})
    mgb_df2 = mgb_df.reset_index()
    fig2, ax2 = plt.subplots()
    ax2.set_title('Kathmandu Rainfall Average by Month')
    ax2.set_ylabel('Rainfall Amount')
    ax2.set_xlabel('Month')
    x2 = mgb_df2['mth']
    y2 = mgb_df2['rf_avg']
    ax2.plot(x2,y2)
    mth_plot_cntnr.pyplot(fig2)
    mth_yr_cntnr, df_mth_cntnr, df_yr_cntnr, df_mthyr_cntnr = st.beta_columns([3,1,1,1])
    df_mth_cntnr.dataframe(mgb_df2)
    df_yr_cntnr.dataframe(rf_yr_df)
    rf_mthyr_df = rainfall_df.groupby(['year', 'mth'],as_index=False)['rainfall'].sum()
    rf_mthyr_df['mth_num'] = pd.to_numeric(rf_mthyr_df['mth'])
    rf_mthyr_sorted_df = rf_mthyr_df.sort_values(['year', 'mth_num'])
    graph_df = rf_mthyr_sorted_df.pivot(index='mth_num', columns='year', values='rainfall')
    fig3, ax3 = plt.subplots()
    ax3.set_title('Kathmandu Rainfall by Month and Year - 2004-2013')
    ax3.set_ylabel('Rainfall Amount')
    ax3.set_xlabel('Month')
    x3 = graph_df.index
    for f in (range(2004, 2013)) :
        ax3.plot(x3, graph_df[str(f)], label=str(f))
    ax3.legend(loc='upper left')
    mth_yr_cntnr.pyplot(fig3)
    df_mthyr_cntnr.dataframe(rf_mthyr_df)
    return


def scenario_input() :
    """Input main data and parameters to run a rainwater collection scenario"""
    st.markdown('## Rainwater Collection - Scenario Input')
    return


def scenario_view() :
    """Allow user to analyze rainwater collection scenario"""
    st.markdown('## Rainwater Collection - Scenario Analysis View')
    return


def about_view() :
    """ About """
    st.markdown('## About')
    return


########################################################################
# Main
#
# Later
########################################################################

drvg_dct = {
            'Historical Rainfall by Location' : rf_data_view,
            'Rainwater Collection Scenario Input' : scenario_input,
            'Rainwater Collection Scenario Analysis' : scenario_view,
            'About' : about_view
           }
page_lst = list(drvg_dct.keys())
page = st.sidebar.radio('Select page:', page_lst)
drvg_dct[page]()

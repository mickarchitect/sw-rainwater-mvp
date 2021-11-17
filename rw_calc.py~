"""
This module contains the main program and all functions to perform
rainwater harvesting calculations and view rainwater data.
"""

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st


def rf_dv_get_criteria() :
    """ Get all criteria for the data view """
    hdr_cntnr, crit_cntnr1, crit_cntnr2, crit_cntnr3 = st.beta_columns([1, 1, 1, 1])
    hdr_cntnr.markdown('## Historical Rainfall by Location')
    loc = crit_cntnr1.selectbox('Location: ', ['Kathmandu, Nepal', 'Fairplay, US'])
    beg_year = crit_cntnr2.selectbox('Begin Year: ', [2004, 2005, 2006, 2007, 2008, 
                                                      2009, 2010, 2011, 2012, 2013],
                                                      index=0)
    end_year = crit_cntnr3.selectbox('End Year: ', [2004, 2005, 2006, 2007, 2008,
                                                    2009, 2010, 2011, 2012, 2013],
                                                    index=9)
    return loc, beg_year, end_year

def rf_dv_get_rainfall(loc, beg_year, end_year) :
    """ Get the rainfall data for the given location and year range """
    # Need logic for locations
    # Need to deal with dates more naturally - low priority
    # Need to validate end_year >= beg_year, or just make it so.
    rainfall_raw_df = pd.read_csv("kathmandu-20042013.csv")
    df_tmp1 = rainfall_raw_df['date'].str.split('/')
    df_tmp2 = df_tmp1.tolist()
    df_tmp3 = pd.DataFrame(df_tmp2, columns=['year', 'mth', 'day', ])
    df_tmp3['year'] = df_tmp3['year'].astype(int)
    df_tmp3['mth'] = df_tmp3['mth'].astype(int)
    df_tmp3['day'] = df_tmp3['day'].astype(int)
    filter = (df_tmp3['year'] >= beg_year) & (df_tmp3['year'] <= end_year)
    df_tmp4 = df_tmp3.loc[filter]
    rainfall_df = rainfall_raw_df.join(df_tmp4)
    return rainfall_df

def rf_dv_draw_year_avg(rainfall_df, cntnr) :
    """ Plot the rainfall total by year """
    # Need to take location into account - on title at least
    rf_yr_df = rainfall_df.groupby('year', as_index = False)['rainfall'].sum()
    fig, ax = plt.subplots()
    ax.set_title('Kathmandu Rainfall Average by Year')
    ax.set_ylabel('Rainfall Amount')
    ax.set_xlabel('Year')
    x = rf_yr_df['year']
    y = rf_yr_df['rainfall']
    ax.plot(x, y)
    cntnr.pyplot(fig)
    cntnr.dataframe(rf_yr_df)
    return

def rf_dv_draw_mth_avg(rainfall_df, cntnr) :
    """ Plot the rainfall average by month over all the years """
    mgb = rainfall_df.groupby(['mth'], as_index=False)
    mgb_df = mgb.agg(np.mean).rename(columns={'rainfall' : 'rf_avg'})
    mgb_df2 = mgb_df.reset_index()
    fig, ax = plt.subplots()
    ax.set_title('Kathmandu Rainfall Average by Month')
    ax.set_ylabel('Rainfall Amount')
    ax.set_xlabel('Month')
    x = mgb_df2['mth']
    y = mgb_df2['rf_avg']
    ax.plot(x,y)
    cntnr.pyplot(fig)
    cntnr.dataframe(mgb_df2)
    return

def rf_dv_draw_mthyr(rainfall_df, beg_year, end_year, cntnr) :
    """ Plot the months for each year """
    rf_mthyr_df = rainfall_df.groupby(['year', 'mth'],as_index=False)['rainfall'].sum()
    rf_mthyr_sorted_df = rf_mthyr_df.sort_values(['year', 'mth'])
    graph_df = rf_mthyr_sorted_df.pivot(index='mth', columns='year', values='rainfall')
    fig, ax = plt.subplots()
    ax.set_title('Kathmandu Rainfall by Month and Year')
    ax.set_ylabel('Rainfall Amount')
    ax.set_xlabel('Month')
    x = graph_df.index
    for f in (range(beg_year, end_year)) :
        ax.plot(x, graph_df[f], label=str(f))
    ax.legend(loc='upper left')
    cntnr.pyplot(fig)
    #cntnr.write('By Year and Month')
    cntnr.dataframe(rf_mthyr_df)
    return

def rf_data_view() :
    """Rainfall Data - view selected historical data by selected location."""
    loc, beg_year, end_year = rf_dv_get_criteria()
    rainfall_df = rf_dv_get_rainfall(loc, beg_year, end_year)
    yr_plot_cntnr, mth_plot_cntnr = st.beta_columns(2)
    mth_yr_cntnr = st.beta_container()
    rf_dv_draw_year_avg(rainfall_df, yr_plot_cntnr)
    rf_dv_draw_mth_avg(rainfall_df, mth_plot_cntnr)
    rf_dv_draw_mthyr(rainfall_df, beg_year, end_year, mth_yr_cntnr)
    return

def get_month_abbr(input_month_number) :
    if input_month_number == 1 :
        return 'Jan'
    elif input_month_number == 2 :
        return 'Feb'
    elif input_month_number == 3 :
        return 'Mar'
    elif input_month_number == 4 :
        return 'Apr'
    elif input_month_number == 5 :
        return 'May'
    elif input_month_number == 6 :
        return 'Jun'
    elif input_month_number == 7 :
        return 'Jul'
    elif input_month_number == 8 :
        return 'Aug'
    elif input_month_number == 9 :
        return 'Sep'
    elif input_month_number == 10 :
        return 'Oct'
    elif input_month_number == 11 :
        return 'Nov'
    elif input_month_number == 12 :
        return 'Dec'

def sv_get_criteria() :
    """ Get all criteria for the scenario view """
    hdr_cntnr, crit_cntnr1 = st.beta_columns([1, 1])
    crit_cntnr2, crit_cntnr3, crit_cntnr4 = st.beta_columns([1, 1, 1])
    hdr_cntnr.markdown('## Scenario Analysis View')
    loc = crit_cntnr1.selectbox('Location: ', ['Kathmandu, Nepal', 'Fairplay, US'])
    roof_sz = crit_cntnr2.number_input('Roof Size: ', value=100)
    tank_cap = crit_cntnr3.number_input('Tank Capacity: ', value=10000)
    daily_usage = crit_cntnr4.number_input('Daily Usage: ', value=500)
    crit_cntnr5, crit_cntnr6, crit_cntnr7 = st.beta_columns([1, 1, 1])
    roof_eff = crit_cntnr5.selectbox('Roof Efficiency: ', [80, 90], index=0)
    water_level_pct = crit_cntnr6.number_input('Water Level Pct: ', value=50)
    tank_reorder_pct = crit_cntnr7.number_input('Tank Reorder Pct: ', value=30)
    crit_cntnr8 = st.beta_container()
    agg_method = crit_cntnr8.selectbox('Data to View: ', [
                                       'Average'
                                      ,'Worst Year'
                                      ,'Best Year'
                                      ,'Lots of others'
                                      ])
    crit_cntnr9, crit_cntnr10 = st.beta_columns(2)
    beg_year = crit_cntnr9.selectbox('Begin Year: ', [2004, 2005, 2006, 2007, 2008, 
                                                      2009, 2010, 2011, 2012, 2013],
                                                      index=0)
    end_year = crit_cntnr10.selectbox('End Year: ', [2004, 2005, 2006, 2007, 2008,
                                                    2009, 2010, 2011, 2012, 2013],
                                                    index=9)
    dct = {
            'Location' : loc
           ,'Roof Size' : roof_sz
           ,'Tank Capacity' : tank_cap
           ,'Daily Usage' : daily_usage
           ,'Roof Efficiency' : roof_eff
           ,'Water Level Pct' : water_level_pct
           ,'Tank Reorder Pct' : tank_reorder_pct
           ,'Aggregation Method' : agg_method
           ,'Begin Year' : beg_year
           ,'End Year' : end_year
          }
    return dct

#def sv_get_daily_data(crit_dct) :
#    """ Given a location, get the daily rainfall data for beg_year through end_year """
    #loc = crit_dct[
#    return rainfall_dly_df

def sv_derive_daily_data(crit_dct) :
    """ Given criteria and rainfall data, derive the daily scenario data """
    # Need to derive it, just reading some old stuff for now
    dly_df = pd.read_csv("scenario_data/scenario2_daily.csv")
#    rainfall_dly_df = sv_get_daily_data(crit_dct)
#    rainfall_df = rainfall_raw_df.filtered to beg/end year
#    returndf = aggregate_function(rainfall_df)
    return dly_df

def sv_derive_mth_data(dly_df) :
    """ Given daily data, derive the monthly scenario data """
    # Need to derive it, just reading some old stuff for now
    mth_df = pd.read_csv("scenario_data/scenario2_monthly.csv")
    return mth_df

def sv_draw_mth_wf(mth_df, cntnr) :
    f2004 = mth_df['year'] == 2004
    viz_df = mth_df.loc[f2004]
    tgt_ctr = 0
    wf_x = []
    wf_y = []
    wf_measure = []

    for row in viz_df.iterrows() :
        mth_abbv = get_month_abbr(row[1].mth)
        wf_y.append(f"Beg Water Level {mth_abbv}")
        if tgt_ctr == 0 :
            wf_measure.append("absolute")
            wf_x.append(row[1].beg_of_mth_lvl)
        else :
            wf_measure.append("total")
            wf_x.append(0)
        wf_y.append(f"RF Collected {mth_abbv}")
        wf_measure.append("Relative")
        wf_x.append(int(row[1].mth_rain_coll))
        wf_y.append(f"Tanker Delivered {mth_abbv}")
        wf_measure.append("Relative")
        wf_x.append(row[1].tnkr_amt)
        wf_y.append(f"Monthly Usage {mth_abbv}")
        wf_measure.append("Relative")
        wf_x.append(int(-1*row[1].mth_usage))
        tgt_ctr += 1

    fig = go.Figure(go.Waterfall(
        name = "2018", 
        orientation = "h", 
        measure = wf_measure,   
        y = wf_y,
        x = wf_x,
        connector = {"mode":"between", "line":{"width":4, "color":"rgb(0, 0, 0)", "dash":"solid"}}
    ))
    #fig.update_layout(title = "Rainfall Collected", width=1000, height=1200)
    fig.update_layout(height=1000)
    cntnr.markdown('### Rainfall and Tanker Collected vs Usage Over Time')
    cntnr.plotly_chart(fig)
    cntnr.markdown('### Monthly Rainfall and Tanker Collected vs Usage - Data')
    cntnr.dataframe(viz_df)
    return

def sv_draw_mth_cb(mth_df, cntnr) :
    cntnr.markdown('### Monthly Rainfall and Tanker Collected vs Usage - Chart')
    f2004 = mth_df['year'] == 2004
    viz_df = mth_df.loc[f2004]
    fig, ax = plt.subplots(figsize=(12, 8))
    #x = viz_df['mth']
    x = viz_df.index
    bar_width = 0.3
    b1 = ax.bar(x, viz_df['mth_rain_coll'], width=bar_width, label='Rainfall Coll.')
    b2 = ax.bar(x+bar_width, viz_df['tnkr_amt'], width=bar_width, label='Tanker Amt')
    b3 = ax.bar(x+(2*bar_width), viz_df['mth_usage'], width=bar_width, label='Usage')
    ax.set_xticks(x + (3*bar_width))
    ax.set_xticklabels(viz_df['mth'])
    ax.legend()
    cntnr.pyplot(fig)
    return

def sv_draw_yr_sum(mth_df, cntnr) :
    cntnr.markdown('### Annual Summary')
    f2004 = mth_df['year'] == 2004
    viz_df = mth_df.loc[f2004]
    totals = mth_df.agg({
                          'mth_rain_coll' : np.sum
                         ,'tnkr_amt' : np.sum
                         ,'mth_usage' : np.sum
                         })
    cntnr.write(totals)
    return

def scenario_view() :
    """Allow user to analyze rainwater collection scenario"""
    crit_dct = sv_get_criteria()
    dly_df = sv_derive_daily_data(crit_dct)
    mth_df = sv_derive_mth_data(dly_df)
    wf_cntnr = st.beta_container()
    sv_draw_mth_wf(mth_df, wf_cntnr)
    cb_cntnr = st.beta_container()
    sv_draw_mth_cb(mth_df, cb_cntnr)
    yr_sum_cntnr = st.beta_container()
    sv_draw_yr_sum(mth_df, yr_sum_cntnr)
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
            'Rainwater Collection Scenarios' : scenario_view,
            'About' : about_view
           }
page_lst = list(drvg_dct.keys())
page = st.sidebar.radio('Select page:', page_lst)
drvg_dct[page]()

# delete below here once safe
#def scenario_input() :
#    """Input main data and parameters to run a rainwater collection scenario"""
#    def_roof_sz = 80
#    def_tank_cap = 10000
#    def_daily_usage = 500
#    def_roof_eff = 80
#    def_water_level_pct = 50
#    def_tank_reorder_pct = 30
#    input_cntnr, parm_cntnr = st.beta_columns([2, 1])
#    input_cntnr.markdown('## Rainwater Collection - Scenario Input')
#    scn_roof_sz = input_cntnr.number_input('Roof Size: ', value=def_roof_sz)
#    scn_tank_cap = input_cntnr.number_input('Tank Capacity: ', value=def_tank_cap)
#    scn_daily_usage = input_cntnr.number_input('Daily Usage: ', value=def_daily_usage)
#    parm_cntnr.markdown('## Parameters, Change Less Frequently')
#    scn_roof_eff = parm_cntnr.number_input('Roof Efficiency: ', value=def_roof_eff)
#    scn_water_level_pct = parm_cntnr.number_input('Water Level Percent in Tank: ', value=def_water_level_pct)
#    scn_reorder_pct = parm_cntnr.number_input('Reorder Level Percent in Tank: ', value=def_tank_reorder_pct)
#    return


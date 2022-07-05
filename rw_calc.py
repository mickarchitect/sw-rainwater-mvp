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
    hdr_cntnr, crit_cntnr1, crit_cntnr2, crit_cntnr3 = st.columns([1, 1, 1, 1])
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
    df_tmp3 = pd.DataFrame(df_tmp2, columns=['mth', 'day', 'year', ])
    df_tmp3['year'] = df_tmp3['year'].astype(int)
    df_tmp3['mth'] = df_tmp3['mth'].astype(int)
    df_tmp3['day'] = df_tmp3['day'].astype(int)
    filter = (df_tmp3['year'] >= beg_year) & (df_tmp3['year'] <= end_year)
    df_tmp4 = df_tmp3.loc[filter]
    rainfall_df = df_tmp4.join(rainfall_raw_df)
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
    return

def rf_dv_draw_mthyr(rainfall_df, beg_year, end_year, cntnr) :
    """ Plot the months for each year """
    rf_mthyr_df = rainfall_df.groupby(['year', 'mth'],as_index=False)['rainfall'].sum()
    rf_mthyr_sorted_df = rf_mthyr_df.sort_values(['year', 'mth'])
    graph_df = rf_mthyr_sorted_df.pivot(index='mth', columns='year', values='rainfall')
    fig, ax = plt.subplots()
    ax.set_title('Kathmandu Change this Rainfall by Month and Year')
    ax.set_ylabel('Rainfall Amount')
    ax.set_xlabel('Month')
    x = graph_df.index
    for f in (range(beg_year, end_year)) :
        ax.plot(x, graph_df[f], label=str(f))
    ax.legend(loc='upper left')
    cntnr.pyplot(fig)
    #cntnr.write('By Year and Month')
    return

def rf_data_view() :
    """Rainfall Data - view selected historical data by selected location."""
    loc, beg_year, end_year = rf_dv_get_criteria()
    rainfall_df = rf_dv_get_rainfall(loc, beg_year, end_year)
    yr_plot_cntnr, mth_plot_cntnr = st.columns(2)
    mth_yr_cntnr = st.container()
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
    #hdr_cntnr, crit_cntnr1 = st.columns([1, 1])
    #crit_cntnr2, crit_cntnr3, crit_cntnr4 = st.columns([1, 1, 1])
    #hdr_cntnr.markdown('## Scenario Analysis View')
    #loc = crit_cntnr1.selectbox('Location: ', ['Kathmandu, Nepal', 'Fairplay, US'])
    #roof_sz = crit_cntnr2.number_input('Roof Size: ', value=100)
    #tank_cap = crit_cntnr3.number_input('Tank Capacity: ', value=10000)
    #daily_usage = crit_cntnr4.number_input('Daily Usage: ', value=500)
    #crit_cntnr5, crit_cntnr6, crit_cntnr7 = st.columns([1, 1, 1])
    #roof_eff = crit_cntnr5.selectbox('Roof Efficiency: ', [80, 90], index=0)
    #water_level_pct = crit_cntnr6.number_input('Water Level Pct: ', value=50)
    #tank_reorder_pct = crit_cntnr7.number_input('Tank Reorder Pct: ', value=30)
    #crit_cntnr8 = st.container()
    #agg_method = crit_cntnr8.selectbox('Data to View: ', [
                                       #'Average'
                                      #,'Worst Year'
                                      #,'Best Year'
                                      #,'Lots of others'
                                      #])
    #crit_cntnr9, crit_cntnr10 = st.columns(2)
    #beg_year = crit_cntnr9.selectbox('Begin Year: ', [2004, 2005, 2006, 2007, 2008, 
                                                      #2009, 2010, 2011, 2012, 2013],
                                                      #index=0)
    #end_year = crit_cntnr10.selectbox('End Year: ', [2004, 2005, 2006, 2007, 2008,
                                                    #2009, 2010, 2011, 2012, 2013],
                                                    #index=9)
    agg_method = 'Average'
    beg_year = 2006
    end_year = 2012
    
    scn_form = st.form('scnro_form')
    scn_form.markdown("""
        ## Scenario Analysis View
        - Enter information about your (proposed) rainwater collection and usage.
        - Get back daily, monthly and annual summaries of rainwater collected and tankers used.
        ### First - Basics
        - Enter simple information about your proposed rainwater system and household
        """)
    basic_col1, basic_col2, basic_col3 = scn_form.columns(3)
    roof_sz = basic_col1.number_input('Roof Size (square meters): ', value=100)
    tank_cap = basic_col2.number_input('Tank Capacity (liters): ', value=10000)
    daily_usage = basic_col3.number_input('Daily Usage (liters): ', value=500)
    scn_form.markdown("""
        ### Second - Advanced, skip if unsure
        """)
    adv_col1, adv_col2, adv_col3 = scn_form.columns(3)
    roof_eff = adv_col1.selectbox('Roof Efficiency: ', [80, 90], index=0)
    water_level_pct = adv_col2.number_input('Water Level Pct: ', value=50)
    tank_reorder_pct = adv_col3.number_input('Tank Reorder Pct: ', value=30)
    scn_form.markdown("""
        ### Finally - what scenario would you like to forecast against
        """)
    scn_col1, scn_col2 = scn_form.columns(2)
    beg_year = scn_col1.selectbox('Begin Year: ', [2004, 2005, 2006, 2007, 2008, 
                                             2009, 2010, 2011, 2012, 2013],
                                             index=3)
    end_year = scn_col2.selectbox('End Year: ', [2004, 2005, 2006, 2007, 2008,
                                           2009, 2010, 2011, 2012, 2013],
                                           index=3)
    loc = scn_col1.selectbox('Location: ', ['Kathmandu, Nepal', 'Fairplay, US'])
    agg_method = scn_col2.selectbox('Scenario: ', [
                                       'Average'
                                      ,'Worst Day of All Years'
                                      ,'Best Day of All Years'
                                      ,'One Year'
                                      ,'Lots of others'
                                      ], index=3)
    submitted = scn_form.form_submit_button('Calculate')

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

def sv_average_filter(tmp_df, crit_dct) :
    """ Given criteria and rainfall data, derive the daily scenario data for rainfall=one year"""
    # display it for debugging
    #st.dataframe(oy_df)

    # Preserve the mid-year year to add back to the dataframe later
    mid_year = round(crit_dct['Begin Year'] + ((crit_dct['End Year'] - crit_dct['Begin Year']) / 2))

    # leap year causes issues, get rid of it, not working, so skip for now
    fltr3 = tmp_df['date'].dt.month == 2
    fltr4 = tmp_df['date'].dt.day == 29

    # Filter to the beg/end year given by the user
    end_dt = '12/31/' + str(crit_dct['End Year'])
    beg_dt = '01/01/' + str(crit_dct['Begin Year'])
    fltr1 = tmp_df['date'] <= end_dt
    fltr2 = tmp_df['date'] >= beg_dt
    #tmp2_df = tmp_df[fltr1&fltr2& (not (fltr3&fltr4))]
    tmp2_df = tmp_df[fltr1&fltr2]

    tmp2_df['month'] = tmp2_df['date'].dt.month
    tmp2_df['day'] = tmp2_df['date'].dt.day
    tmp3_df = tmp2_df.groupby(['month', 'day'], as_index=False).mean()
    #fltr3 = tmp3_df['month'] == 2
    #fltr4 = tmp3_df['day'] == 29
    #tmp4_df = tmp3_df[not (fltr3&fltr4)]
    tmp3_df['year'] = mid_year
    #tmp3_df['date'] = str(tmp3_df['month'])+str(tmp3_df['day'])+str(tmp3_df['year'])
    st.dataframe(tmp3_df)
    tmp3_df['date'] = pd.to_datetime(tmp3_df[['month', 'day', 'year']])

    return tmp3_df

def sv_one_year_filter(tmp_df, crit_dct) :
    """ Given criteria and rainfall data, derive the daily scenario data for rainfall=one year"""
    # display it for debugging
    #st.dataframe(oy_df)

    # Filter to the beg/end year given by the user
    end_dt = '12/31/' + str(crit_dct['End Year'])
    beg_dt = '01/01/' + str(crit_dct['Begin Year'])
    fltr1 = tmp_df['date'] <= end_dt
    fltr2 = tmp_df['date'] >= beg_dt
    tmp2_df = tmp_df[fltr1&fltr2]
    return tmp2_df

def sv_one_year_calc(tmp_df, crit_dct) :
    """ Given criteria and rainfall data, derive the daily scenario data for rainfall=one year"""
    # display it for debugging
    #st.dataframe(oy_df)

    # get the starting index #
    ctr = 1
    for my_row in tmp_df.iterrows() :
        if ctr == 1 :
            st_index = my_row[0]
            ctr += 1
        else :
            break

    dt_s = pd.Series([], name='dt', dtype='datetime64[ns]')
    rainfall_s = pd.Series([], name='rainfall', dtype='float')
    ystrdy_lvl_s = pd.Series([], name='ystrdy_lvl', dtype='float')
    usg_amt_s = pd.Series([], name='usg_amt', dtype='float')
    tdy_rain_ptntl_s = pd.Series([], name='tdy_rain_ptntl', dtype='float')
    tdy_rain_coll_s = pd.Series([], name='tdy_rain_coll', dtype='float')
    tdy_rain_ovflw_s = pd.Series([], name='tdy_rain_ovflw', dtype='float')
    tnkr_amt_s = pd.Series([], name='tnkr_amt', dtype='int')
    tdy_lvl_s = pd.Series([], name='tdy_lvl', dtype='float')
    
    tank_capacity = crit_dct['Tank Capacity']
    current_water_level_percent = crit_dct['Water Level Pct']
    roof_size = crit_dct['Roof Size']
    roof_efficiency = crit_dct['Roof Efficiency']
    daily_usage = crit_dct['Daily Usage']
    tank_reorder_pct = crit_dct['Tank Reorder Pct']

    for dnum in range(1,364) :
        didx = dnum - 1
        if dnum == 1 :
            yesterday_level = tank_capacity * (current_water_level_percent / 100)
        else :
            yesterday_level = tdy_lvl_s.at[didx-1]
        dt = tmp_df.at[(didx+st_index), 'date']
        today_rainfall = tmp_df.at[(didx+st_index), 'rainfall']
        today_rain_pot = today_rainfall * roof_size * (roof_efficiency / 100)
        if ((yesterday_level - daily_usage) + today_rain_pot) < tank_capacity :
            today_rain_coll = today_rain_pot
            today_rain_overflow = 0
        else :
            today_rain_coll = tank_capacity - (yesterday_level - daily_usage)
            today_rain_overflow = today_rain_pot - today_rain_coll
        tanker_amt = 0
        if yesterday_level < (tank_capacity * (tank_reorder_pct / 100)) :
            refill_max = tank_capacity - yesterday_level
            num_tankers = refill_max // 6000
            tanker_amt = 6000 * num_tankers
            #tanker_amt = 6
        today_level = (yesterday_level - daily_usage) + today_rain_coll + tanker_amt

        ystrdy_lvl_s.at[didx] = round(yesterday_level)
        usg_amt_s.at[didx] = round(daily_usage)
        tdy_rain_ptntl_s.at[didx] = round(today_rain_pot)
        tdy_rain_coll_s.at[didx] = round(today_rain_coll)
        tdy_rain_ovflw_s.at[didx] = round(today_rain_overflow)
        tnkr_amt_s.at[didx] = round(tanker_amt)
        tdy_lvl_s.at[didx] = round(today_level)
        dt_s[didx] = dt
        rainfall_s[didx] = today_rainfall

    new_df = dt_s.to_frame().join(rainfall_s).join(ystrdy_lvl_s).join(usg_amt_s).join(tdy_rain_ptntl_s).join(tdy_rain_coll_s).\
                              join(tnkr_amt_s).join(tdy_lvl_s).join(tdy_rain_ovflw_s)
    return new_df

def sv_derive_daily_data(crit_dct) :
    """ Given criteria and rainfall data, derive the daily scenario data """
    # Read the raw data file
    tmp_df = pd.read_csv('kathmandu-20042013.csv', parse_dates=[0])

    # if/elif for the scenario
    scenario = crit_dct['Aggregation Method']
    if scenario == 'One Year' :
        tmp2_df = sv_one_year_filter(tmp_df, crit_dct)
        ret_df = sv_one_year_calc(tmp2_df, crit_dct)
    elif scenario == 'Average' :
        tmp2_df = sv_average_filter(tmp_df, crit_dct)
        ret_df = sv_one_year_calc(tmp2_df, crit_dct)
    elif scenario == 'Worst Day of All Years' :
        ret_df = sv_one_year_calc(tmp_df, crit_dct)
    elif scenario == 'Best Day of All Years' :
        ret_df = sv_one_year_calc(tmp_df, crit_dct)


    # Need to do calculations for Average and Worst/Best Day of All Years, 
    # for right now, implement One Year

    # need to reindex the dataframe - this is having no effect, built a workaround in sv_one_year_calc
    #tmp3_df = tmp2_df.reindex()

    # need to handle if more than one year is in our input, ignore for now
    #tmp4_df = sv_one_year_calc(tmp3_df, crit_dct)
    return ret_df

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

    cntnr.markdown('### Monthly Rainfall and Tanker Collected vs Usage - Data')
    cntnr.dataframe(viz_df)
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

    st.markdown("""
        ## Results 
        ### Daily - Tabular Results
        """)
    st.dataframe(dly_df)
    mth_df = sv_derive_mth_data(dly_df)
    wf_cntnr = st.container()
    sv_draw_mth_wf(mth_df, wf_cntnr)
    #cb_cntnr = st.container()
    #sv_draw_mth_cb(mth_df, cb_cntnr)
    #yr_sum_cntnr = st.container()
    #sv_draw_yr_sum(mth_df, yr_sum_cntnr)
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

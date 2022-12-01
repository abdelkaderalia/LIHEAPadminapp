#importing packages
import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from mpl_toolkits.axes_grid1 import make_axes_locatable
import mapclassify
import plotly.express as px
import webbrowser
import openpyxl


@st.cache
#define function to get geo data
def get_geo():
    geo = gpd.read_file('/vsicurl/https://github.com/abdelkaderalia/LIHEAPadminapp/raw/main/Data/tl_2021_us_state.shp')
    #save shapefile to dataframe
    geo = geo.to_crs("EPSG:4326")
    geo = geo.rename(columns = {'STUSPS':'State'})

    df = pd.read_excel('https://github.com/abdelkaderalia/LIHEAPadminapp/raw/main/Data/admin_data.xlsx')

    df = df.merge(geo,on='NAME',how='left')

    return df


#### App starts here
if __name__ == "__main__":
    #st.markdown('<h2 align="left">How much money does the federal government spend?</h2>', unsafe_allow_html=True) # Add app title
    st.set_page_config(page_icon="📑",page_title="Administrative Burdens - LIHEAP",layout="wide")
    st.title('Administrative Burdens by State')
    st.header('Low Income Home Energy Assistance Program (LIHEAP)')
    st.subheader('')

    url1 = 'https://www.acf.hhs.gov/ocs/low-income-home-energy-assistance-program-liheap'
    url2 = 'https://crsreports.congress.gov/product/pdf/R/R40486'

    part1 = f"""[The Low Income Home Energy Assistance Program (LIHEAP)]({url1}) has been administered by the Department of Health and Human Services (HHS) since 1981
            to provide low-income households with financial assistance to cover energy bills (heating, cooling) and weatherization of their homes.
            This [block grant]({url2}) allocates federal funds to grantees, each of which is a U.S. state, territory, or tribe."""

    part2 = """Due to the block grant structure, each grantee independently administers funds to households in its jurisdiction.
            As such, each grantee has its own application (or multiple applications, if they utilize a subgrantee) and these applications
            can differ widely in terms of the administrative burden imposed on the applicant. Below is visualization of the estimated burden for a LIHEAP applicant in each state."""

    st.write(part1)

    st.write(part2)

    metrics = {'Application time (min)':'App_time','Number of pages':'Num_pages','Number of questions':'Num_q'}
    var = st.selectbox("Choose a burden metric:", metrics.keys())
    var_name = metrics[var]

    df = get_geo()

    fig = px.choropleth(df,locations='State', color=var_name,
                               color_continuous_scale="darkmint",
                               range_color=(df[var_name].min(), df[var_name].max()),
                               hover_name='NAME',
                               locationmode='USA-states',
                               scope="usa",
                               labels={var_name:var},
                               width=1300, height=700)

    fig.update_layout(autosize=True)

    st.plotly_chart(fig)

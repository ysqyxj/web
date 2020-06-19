# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import pandas as pd  
import plotly_express as px
import plotly.graph_objs as go 
import time 
import datetime as dt
import pydeck as pdk
import numpy as np 

st.title('Where to go in LA')


def load_data():
    da=pd.read_csv('~/Desktop/Covid/COVID19_by_Neighborhood.csv')
    da=da[['COUNTY_NAME','cases','case_rate','deaths','death_rate','Date']]
    da.columns=['County_name','cases','case_rate','deaths','death_rate','date']
    da=da.sort_values('case_rate')
    return da


da= load_data()

st.write("Check the location you wanna go:") 
st.table(da.head())


county=da['County_name']


county_name=st.sidebar.selectbox(
    "Which area do you want to go to?",
    county
    )
part=da[(da['County_name']==county_name)]

place=['Gym','Resturant','Park','Outdoor','School','Workplace']
place=st.sidebar.selectbox(
    "Which place do you want to go to?",
    place
    )  


map_data=pd.read_csv('~/Desktop/Covid/Covid challenge/COVID19_by_Neighborhood.csv')
map_data=pd.concat([da,map_data['geometry'].str.split('[',expand=True).iloc[:,3]],axis=1)


map_data=pd.concat([da,map_data.iloc[:,6].str.split(',',expand=True)],axis=1)

map_data.columns=['County_name','cases','case_rate','deaths','death_rate','date','lat','lon','p']
map_data=map_data.drop(columns=['p'])
map_data=map_data[map_data['lat'].notnull()]
map_data=map_data[map_data['lon'].notnull()] 
map_data=map_data[map_data['County_name'].notnull()]   
map_data=map_data[map_data['cases'].notnull()]
map_data=map_data[map_data['case_rate'].notnull()]
map_data=map_data[map_data['death_rate'].notnull()]

map_data=pd.concat([map_data.drop(columns=['lon']),map_data.iloc[:,7].str.split(']',expand=True)],axis=1)
map_data.columns=['County_name','cases','case_rate','deaths','death_rate','date','lat','lon','p']
map_data=map_data.drop(columns=['p'])

map_data['lat']=pd.to_numeric(map_data['lat'])
map_data['lon']=pd.to_numeric(map_data['lon']) 



INITIAL_VIEW_STATE = pdk.ViewState(
  latitude=34.5,
  longitude=-118.2,
  zoom=11,
  max_zoom=16,
  pitch=45,
  bearing=0
)

polygon = pdk.Layer(
    'PolygonLayer',
    data=map_data,
    stroked=False,
    get_polygon='-',
    get_fill_color=[0, 0, 0, 20]
)

geojson = pdk.Layer(
    'ScatterplotLayer',
    data=map_data,
    opacity=0.8,
    stroked=False,
    filled=True,
    extruded=True,
    get_line_color=[255, 255, 255],
    pickable=True
)

r = pdk.Deck(
    layers=[polygon, geojson],
    initial_view_state=INITIAL_VIEW_STATE)

st.write(r)



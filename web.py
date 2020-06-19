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

@st.cache 

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
# map_dat['date']=dt.strptime(map_data['date'],'%Y/%m/%d')

# fig=go.Figure(go.Choroplethmapbox(
#                              data_frame=map_data,
#                              lat=map_data.lat,
#                              lon=map_data.lon,
#                              z=map_data.cases,
#                              test=map_data.County_name,
#                              showscale=True,
#               ))

# fig.update_layout(mapbox_style="carto-darkmatter",
#                   mapbox_zoom=3,
#                   mapbox_center={"lat":34.2,"lon":118.3},
#                   )

def plot_world_data(County_name,lat,lon,cases):
  data = [go.Choropleth(
      lat=map_data.lat,
      lon=map_data.lon,
      z=map_data.cases,
      test=map_data.County_name,
      colorscale = [
          [0, "rgb(103,0,13)"],
          [0.35, "rgb(165,15,21)"],
          [0.5, "rgb(203,24,29)"],
          [0.6, "rgb(239,59,44)"],
          [0.7, "rgb(251,106,74)"],
          [1, "rgb(254,229,217)"]
      ],
      autocolorscale = False,
      reversescale = True,
      marker = go.choropleth.Marker(
          line = go.choropleth.marker.Line(
              color = 'rgb(180,180,180)',
              width = 0.5
          )),
      colorbar = go.choropleth.ColorBar(
          #tickprefix = '$',
          title = 'Cases'),
  )]

  layout = go.Layout(
      title = go.layout.Title(
          text = 'Covid19 LA Map'
      ),
      geo = go.layout.Geo(
          showframe = False,
          showcoastlines = False,
          projection = go.layout.geo.Projection(
              type = 'equirectangular'
          )
      ),
      annotations = [go.layout.Annotation(
          x = 0.55,
          y = 0.1,
          xref = 'paper',
          yref = 'paper',
          text = 'Source: <a href="https://covid.ourworldindata.org">\
              Our World In Data</a>',
          showarrow = False
      )]
  )

  fig = go.Figure(data = map_data, layout = layout)
  #fig.show()
  # show global cases on a map
  st.plotly_chart(fig)
    
# INITIAL_VIEW_STATE = pdk.ViewState(
#   latitude=34.5,
#   longitude=-118.2,
#   zoom=11,
#   max_zoom=16,
#   pitch=45,
#   bearing=0
# )

# polygon = pdk.Layer(
#     'PolygonLayer',
#     data=da,
#     stroked=False,
#     # processes the data as a flat longitude-latitude pair
#     get_polygon='-',
#     get_fill_color=[0, 0, 0, 20]
# )

# geojson = pdk.Layer(
#     'ScatterplotLayer',
#     data=da,
#     opacity=0.8,
#     stroked=False,
#     filled=True,
#     extruded=True,
#     get_line_color=[255, 255, 255],
#     pickable=True
# )

# r = pdk.Deck(
#     layers=[polygon, geojson],
#     initial_view_state=INITIAL_VIEW_STATE)





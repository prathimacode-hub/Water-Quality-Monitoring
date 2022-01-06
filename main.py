import datetime
import folium
import geopandas as gpd
import geopy
import networkx as nx
import joblib
import osmnx as ox
import shapely.wkt
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
import time
import base64
from branca.element import Figure
from folium.features import DivIcon
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(
    page_title="Water Quality Monitoring Dashboard for Kutch Region",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.set_option('deprecation.showPyplotGlobalUse', False)

st.sidebar.markdown('<h1 style="margin-left:8%; color:	#FA8072 ">Kutch Water Quality Monitoring Dashboard </h1>',
                    unsafe_allow_html=True)

add_selectbox = st.sidebar.radio(
    "",
    ("Home", "About", "Features", "Select AOI Data Parameters", "Our Result", "Visualizations", "Conclusion", "Team")
)

if add_selectbox == 'Home':
    
    LOGO_IMAGE = "omdena_india_logo.png"
    
    st.markdown(
          """
          <style>
          .container {
          display: flex;
        }
        .logo-text {
             font-weight:700 !important;
             font-size:50px !important;
             color: #f9a01b !important;
             padding-top: 75px !important;
        }
        .logo-img {
             float:right;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
          f"""
          <div class="container">
               <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
          </div>
          """,
          unsafe_allow_html=True
    )
    
    st.subheader('PROBLEM STATEMENT')
    
    st.markdown('', unsafe_allow_html=True)

    
elif add_selectbox == 'About':
    
    st.subheader('ABOUT THE PROJECT')

    st.markdown('<h4>Project Goals</h4>', unsafe_allow_html=True)
    st.markdown('• ', unsafe_allow_html=True) 
    st.markdown('• ', unsafe_allow_html=True) 
    st.markdown('• ', unsafe_allow_html=True) 
    st.markdown('• ', unsafe_allow_html=True) 
    st.markdown('• ', unsafe_allow_html=True) 
    st.markdown('• ', unsafe_allow_html=True) 
    
    st.markdown('<h4>Location Choosen</h4>', unsafe_allow_html=True)
    st.markdown('',
                unsafe_allow_html=True)
    
    st.markdown('<h4>Developments Made</h4>', unsafe_allow_html=True)
    st.markdown(' \
        ',
                unsafe_allow_html=True)
    st.markdown(' \
         \
            '
                , unsafe_allow_html=True)
 

elif add_selectbox == 'Features':

    st.subheader('PROJECT ENDORSEMENTS')

    st.markdown('• ', unsafe_allow_html=True)
    st.markdown('• ', unsafe_allow_html=True)
    st.markdown('• ', unsafe_allow_html=True)
    
    
elif add_selectbox == 'Select AOI Data Parameters':
    
    st.subheader('Select for AOI Data Parameters')    
    
    col1, col2 = st.columns(2)

    aoi_type = col1.selectbox(
        "Select Area of Interest (AOI)",
        ("Topansar Lake","Shakoor Lake","Hamirsar Lake")
    )
    
    d = st.date_input("Select Date")

    prm_type = col2.selectbox(
        "Data Selection Parameters",
        ("pH","Salinity","Turbidity","Sea Surface Temperature","Chlorophyll","Suspended matter",
     "Dissolved Organic Matter","Dissolved Oxygen","Sulphates","Calcium Carbonate")
    )
    
    if st.button('Submit'):

        if aoi_type == 'Topansar Lake':
            aoi_data = pd.read_csv('https://perso.telecom-paristech.fr/eagan/class/igr204/data/cars.csv')
        elif aoi_type == 'Shakoor Lake':
            aoi_data = pd.read_csv('https://perso.telecom-paristech.fr/eagan/class/igr204/data/cars.csv')
        elif aoi_type == 'Hamirsar Lake':
            aoi_data = pd.read_csv('https://perso.telecom-paristech.fr/eagan/class/igr204/data/cars.csv')

        prm = prm_type.split(" ")

        details = aoi_data[aoi_data['prm']==prm[0]]

        coordinates = {
            'Kutch Region': [23.7337,69.8597]
        }

        m = folium.Map(location=coordinates[prm_type], zoom_start=10)
        folium.TileLayer('Stamen Terrain').add_to(m)
        folium.TileLayer('Stamen Toner').add_to(m)
        folium.TileLayer('Stamen Water Color').add_to(m)
        folium.TileLayer('cartodbpositron').add_to(m)
        folium.TileLayer('cartodbdark_matter').add_to(m)
        folium.LayerControl().add_to(m)
        m
        for index, row in details.iterrows():
            if row['geometry'].startswith("POINT"):
                geometry = shapely.wkt.loads(row['geometry'])
            else:
                p = shapely.wkt.loads(row['geometry'])
                geometry = p.centroid

            folium.Marker(
                [geometry.y, geometry.x], popup=row['display_name'],
            ).add_to(m)

        folium_static(m, width=900)


elif add_selectbox == 'Result':
    
    st.subheader('Our Result')
        
        
elif add_selectbox == 'Visualizations':
    
    st.subheader('PROJECT VISUALIZATIONS')
    st.markdown('<h4></h4>', unsafe_allow_html=True)
    st.image("", width=500)
    st.markdown('<h4></h4>', unsafe_allow_html=True)
    st.image("", width=500)
    st.markdown('<h4></h4>', unsafe_allow_html=True)
    st.image("", width=500)
    st.markdown('<h4></h4>', unsafe_allow_html=True)
    st.image("", width=500)
   
    
elif add_selectbox == 'Conclusion':
    
    st.subheader('PROJECT SUMMARY')

    st.markdown('Write Project Summary here', unsafe_allow_html=True) 
    
    st.subheader('CONCLUSION')
    
    st.markdown('Write Conclusion here', unsafe_allow_html=True)
    
    
elif add_selectbox == 'Team':
    
    st.subheader('COLLABORATORS')

    st.markdown('<a href="https://www.linkedin.com/in/tanisha-banik-04b511173/">Tanisha Banik</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="https://www.linkedin.com/in/renju-zachariah-30982247/">Renju Zacharaiah</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="">Sai Villiers</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="">Ishita Kheria</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="https://www.linkedin.com/in/prathima-kadari/">Prathima Kadari</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="https://www.linkedin.com/in/deepali-bidwai/">Deepali Bidwai</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="">Himanshu Mishra</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="">Bharati Panigrahi</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="">Kiran Ryakala</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="https://www.linkedin.com/in/drij-chudasama-2a112a168/">Drij Chudasama</a>',
                unsafe_allow_html=True)

    st.subheader('PROJECT MANAGER')

    st.markdown('<a href="https://www.linkedin.com/in/chancy-shah-671787119/">Chancy Shah</a>', unsafe_allow_html=True)
                

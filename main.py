import datetime
import folium
import geopandas as gpd
import geopy
import networkx as nx
import joblib
import osmnx as ox
import shapely.wkt
import pandas as pd
#import plotly.express as px
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

st.sidebar.markdown('<h1 style="margin-left:8%; color:	#FF9933 ">Kutch Water Quality Monitoring Dashboard </h1>',
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
    
    st.markdown('Our problem statement is to develop a centralized dashboard with different water quality parameters for analyzing, interpretation, and visualization in near real-time using Remote Sensing and AI for better decision making. This will identify if any parameter is not within standard limits for taking up an immediate action and reinforce the abilities to monitor water quality more effectively & efficiently.', 
         unsafe_allow_html=True)

    
elif add_selectbox == 'About':
    
    st.subheader('ABOUT THE PROJECT')

    st.markdown('<h4>Project Goals</h4>', unsafe_allow_html=True)
    st.markdown('• Water Quality Indicator Dashboard for Analysis, Interpretation and Visualization near Real Time', unsafe_allow_html=True) 
    st.markdown('• Compare Real Water Quality Parameters with Standard Water Quality Limits', unsafe_allow_html=True) 
    
    st.markdown('<h4>Location Choosen</h4>', unsafe_allow_html=True)
    st.markdown('Harmisar Lake, Shinai Lake, Tappar Lake',
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
    
    st.subheader('SELECT FOR AOI DATA PARAMETERS')    
    
    col1, col2 = st.columns(2)

    aoi_type = col1.selectbox(
        "Select Area of Interest (AOI)",
        ("Shinai Lake","Harmirsar Lake", "Tappar Reservoir Lake")
    )
    
    prm_type = col2.selectbox(
        "Data Selection Parameters",
        ("pH","Salinity","Turbidity","Land Surface Temperature","Chlorophyll","Suspended matter",
     "Dissolved Organic Matter","Dissolved Oxygen")
    )
    
    col3, col4 = st.columns(2)
    
    d1 = st.date_input("Start Date")
    
    d2 = st.date_input("End Date")
    
    
    if st.button('Submit'):

#        if aoi_type == 'Shinai Lake':
#            aoi_data = pd.read_csv('https://github.com/prathimacode-hub/Water-Quality-Monitoring/blob/main/Dataset/Shinai%20Lake/Data_Shinai_Lake_2019')
#            aoi_data = pd.read_csv('https://github.com/prathimacode-hub/Water-Quality-Monitoring/blob/main/Dataset/Shinai%20Lake/Data_2020_Shinai_Lake')
#            aoi_data = pd.read_csv('https://github.com/prathimacode-hub/Water-Quality-Monitoring/blob/main/Dataset/Shinai%20Lake/Data_2021_Shinai_Lake')
#        elif aoi_type == 'Harmirsar Lake':
#            aoi_data = pd.read_csv('https://github.com/prathimacode-hub/Water-Quality-Monitoring/blob/main/Dataset/Harmisar%20Lake/Data_2019_Harmisar_Lake')
#            aoi_data = pd.read_csv('https://github.com/prathimacode-hub/Water-Quality-Monitoring/blob/main/Dataset/Harmisar%20Lake/Data_2020_Harmisar_Lake')
#            aoi_data = pd.read_csv('https://github.com/prathimacode-hub/Water-Quality-Monitoring/blob/main/Dataset/Harmisar%20Lake/Data_2021_Harmisar_Lake')
#        elif aoi_type == 'Tappar Lake':
#            aoi_data = pd.read_csv('https://github.com/prathimacode-hub/Water-Quality-Monitoring/blob/main/Dataset/Tappar%20Lake/Data_2019_Tappar_Lake')
#            aoi_data = pd.read_csv('https://github.com/prathimacode-hub/Water-Quality-Monitoring/blob/main/Dataset/Tappar%20Lake/Data_2020_Tappar_Lake')
#            aoi_data = pd.read_csv('https://github.com/prathimacode-hub/Water-Quality-Monitoring/blob/main/Dataset/Tappar%20Lake/Data_2021_Tappar_Lake')

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
        # m
        
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
    
    st.subheader('OUR RESULT')
    st.markdown('<h4></h4>', unsafe_allow_html=True)
    st.image("", width=500)
        
        
elif add_selectbox == 'Visualizations':
    
    st.subheader('PROJECT VISUALIZATIONS')
    st.markdown('<h4>Harmisar Lake</h4>', unsafe_allow_html=True)
    st.image("https://github.com/prathimacode-hub/Water-Quality-Monitoring/blob/main/Visualization/Harmisar%20Lake.png", width=500)
    st.markdown('<h4>Shinai Lake</h4>', unsafe_allow_html=True)
    st.image("https://github.com/prathimacode-hub/Water-Quality-Monitoring/blob/main/Visualization/Shinai%20Lake.png", width=500)
    st.markdown('<h4>Tappar Lake</h4>', unsafe_allow_html=True)
    st.image("https://github.com/prathimacode-hub/Water-Quality-Monitoring/blob/main/Visualization/Tappar%20Lake.png", width=500)
    #st.markdown('<h4></h4>', unsafe_allow_html=True)
    #st.image("", width=500)
   
    
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
    st.markdown('<a href="https://www.linkedin.com/in/bharati-panigrahi-10a9461a0/">Bharati Panigrahi</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="">Kiran Ryakala</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="https://www.linkedin.com/in/drij-chudasama-2a112a168/">Drij Chudasama</a>',
                unsafe_allow_html=True)

    st.subheader('PROJECT MANAGER')

    st.markdown('<a href="https://www.linkedin.com/in/chancy-shah-671787119/">Chancy Shah</a>', unsafe_allow_html=True)
                

import datetime
import folium
import geopandas as gpd
import geopy
import networkx as nx
import joblib
import osmnx as ox
import shapely.wkt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import time
import base64
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
    st.subheader('Find Safest Path')

    sentence = st.text_input('Input your current location:')

    # G_walk = ox.graph_from_place('Manhattan Island, New York City, New York, USA',
    #                          network_type='walk')

   # G_walk = joblib.load('G_walk.sav')

   # orig_node = ox.get_nearest_node(G_walk,
   #                                (40.748441, -73.985664))

   # dest_node = ox.get_nearest_node(G_walk,
   #                                (40.748441, -73.4))

   # route = nx.shortest_path(G_walk,
   #                         orig_node,
   #                          dest_node,
   #                          weight='length')

   # route_map = ox.plot_route_folium(G_walk, route)

   # folium_static(route_map, width=900)

elif add_selectbox == 'Result':
    st.subheader('Our Result')

    col1, col2 = st.columns(2)

    map_type = col1.selectbox(
        "Shelters",
        ('横手市 (Earthquakes)', '湯沢市 (Tsunamis)', '湯沢市 (Floods)')
    )

    ward_type = col2.selectbox(
        "Ward",
        ( '横手市 (Nakagawa Ward)', '横手市 (Midori Ward)'
        )
    )
    
    if st.button('Search'):

        if map_type == 'Earthquakes':
            map_data = pd.read_csv('nakagawa_earthquake_shelters.csv')
        elif map_type == 'Tsunamis':
            map_data = pd.read_csv('nakagawa_tsunami_shelters.csv')
        elif map_type == 'Floods':
            map_data = pd.read_csv('nakagawa_flood_shelters.csv')

        ward = ward_type.split(" ")

        details = map_data[map_data['ward']==ward[0]]

        coordinates = {
            #'中川区 (Nakagawa Ward)': [35.1332, 136.8350],
            #'中川区 (Nakagawa Ward)': [35.139288, 136.8128218]
            '中川区 (Nakagawa Ward)': [35.1392027, 136.7778013],
            '緑区 (Midori Ward)': [35.0852, 136.9708]
        }

        m = folium.Map(location=coordinates[ward_type], zoom_start=10)
        for index, row in details.iterrows():
            if row['geometry'].startswith("POINT"):
                geometry = shapely.wkt.loads(row['geometry'])
            else:
                p = shapely.wkt.loads(row['geometry'])
                geometry = p.centroid

            folium.Marker(
                [geometry.y, geometry.x], popup=row['display_name'],
            ).add_to(m)

        # london_location = [35.183334,136.899994]

        # m = folium.Map(location=london_location, zoom_start=15)
        folium_static(m, width=900)
        
        
elif add_selectbox == 'Visualizations':
    
    
    st.subheader('PROJECT VISUALIZATIONS')
    st.markdown('<h4></h4>', unsafe_allow_html=True)
    st.image("Japan_Earthquakes_Zoning.png", width=500)
    st.markdown('<h4></h4>', unsafe_allow_html=True)
    st.image("Nakagawa_Shelter_Maps.png", width=500)
    st.markdown('<h4></h4>', unsafe_allow_html=True)
    st.image("Nakagawa_Building_Density_Score.png", width=500)
    st.markdown('<h4></h4>', unsafe_allow_html=True)
    st.image("Nakagawa_Distance_Risk_Score.png", width=500)
   
    
elif add_selectbox == 'Conclusion':
    
    st.subheader('PROJECT SUMMARY')

    st.markdown('Write Project Summary here', unsafe_allow_html=True) 
    
    st.subheader('CONCLUSION')
    
    st.markdown('Write Conclusion here', unsafe_allow_html=True)
    
    
elif add_selectbox == 'Team':
    
    st.subheader('COLLABORATORS')

    st.markdown('<a href="">Tanisha Banik</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="">Renju Zacharaiah</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="">Sai Villiers</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="">Ishita Kheria</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="https://www.linkedin.com/in/prathima-kadari/">Prathima Kadari</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="">Deepali Bidwai</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="">Himanshu Mishra</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="">Bharati Panigrahi</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="">Kiran Ryakala</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="">Drij Chudasama</a>',
                unsafe_allow_html=True)

    st.subheader('PROJECT MANAGER')

    st.markdown('<a href="">Chancy Shah</a>', unsafe_allow_html=True)
                

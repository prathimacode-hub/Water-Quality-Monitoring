import datetime
import math
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
from dateutil.relativedelta import relativedelta
from data_collection import *
from predict import *
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import time
from matplotlib.backends.backend_agg import RendererAgg
from bokeh.plotting import figure

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
        "Data Visualization Parameters",
        ("All","pH","Salinity","Turbidity","Land Surface Temperature","Chlorophyll","Suspended matter",
     "Dissolved Organic Matter","Dissolved Oxygen")
    )

    long = st.number_input('Longitude', format="%.4f")

    lat = st.number_input('Latitude', format="%.4f")
    
    col3,_ = st.columns((1,2)) # To make it narrower
    
    format = 'MMM DD, YYYY'  # format output
        
    start1 = datetime.date(year=2024,month=1,day=1)-relativedelta(years=5) #  I need some range in the past

    start2 = datetime.date(year=2024,month=11,day=1)
    
    # end1 = datetime.datetime.now().date()+relativedelta(years=2)
    
    max_days = start2-start1
        
    slider1 = col3.slider('Select Start Date', min_value=start1, value=start2 ,max_value=start2, format=format)
        ## Sanity check
    st.table(pd.DataFrame([[start1, slider1,start2]],
                      columns=['start1',
                               'start_selected',
                               'start2'],
                      index=['date']))

    end1 = datetime.date(year=2024,month=2,day=1)-relativedelta(years=5) #  I need some range in the past
    
    end2 = datetime.date(year=2024,month=12,day=1)
    
    max_days = end2-end1
        
    slider2 = col3.slider('Select End Date', min_value=end1, value=end2, max_value=end2, format=format)
        ## Sanity check
    st.table(pd.DataFrame([[end1, slider2, end2]],
                      columns=['end1',
                               'end_selected',
                               'end2'],
                      index=['date']))
    
    # df_all = send_df()
    # st.write(df_all)
    
    def plot_do(df_all):
        mpl.rcParams.update({"axes.grid" : True, "grid.color": "black"})
        sns.set(font_scale = 2)
        fig = plt.figure(figsize=(25,10))
        ax = sns.histplot(df_all['Dissolved Oxygen'], kde=True, stat="density")
        ax.tick_params(axis='y', colors='black') 
        ax.tick_params(axis='x', colors='black') 
        ax.set_xticks(np.arange(math.floor(df_all['Dissolved Oxygen'].min()), df_all['Dissolved Oxygen'].max() + 1, 0.5))
        plt.setp(ax.get_xticklabels(), rotation=-10)
        st.pyplot(fig, clear_figure = True)

    def plot_dom(df_all):
        mpl.rcParams.update({"axes.grid" : True, "grid.color": "black"})
        sns.set(font_scale = 2)
        fig = plt.figure(figsize=(30,8))
        ax = sns.histplot(df_all['Dissolved Organic Matter'], kde=True, stat="density")
        ax.tick_params(axis='y', colors='black') 
        ax.tick_params(axis='x', colors='black') 
        ax.set_xticks(np.arange(math.floor(df_all['Dissolved Organic Matter'].min()),df_all['Dissolved Organic Matter'].max() + 2, 20))
        plt.setp(ax.get_xticklabels(), rotation=-10)
        st.pyplot(fig, clear_figure = True) 
    
    def plot_salinity(df_all):
        mpl.rcParams.update({"axes.grid" : True, "grid.color": "black"})
        sns.set(font_scale = 2)
        fig = plt.figure(figsize=(20,6))
        ax = sns.histplot(df_all['Salinity'], kde=True, stat="density")
        ax.tick_params(axis='y', colors='black') 
        ax.tick_params(axis='x', colors='black') 
        ax.set_xticks(np.arange(math.floor(df_all['Salinity'].min()),df_all['Salinity'].max() + 0.1, 0.01))
        plt.setp(ax.get_xticklabels(), rotation=-10)
        st.pyplot(fig, clear_figure = True)

    def plot_turbidity(df_all):
        mpl.rcParams.update({"axes.grid" : True, "grid.color": "black"})
        sns.set(font_scale = 2)
        fig = plt.figure(figsize=(30,6))
        ax = sns.histplot(df_all['Turbidity'], kde=True, stat="density")
        ax.tick_params(axis='y', colors='black') 
        ax.tick_params(axis='x', colors='black') 
        ax.set_xticks(np.arange(math.floor(df_all['Turbidity'].min()),df_all['Turbidity'].max() + 0.01, 0.3))
        plt.setp(ax.get_xticklabels(), rotation=-10)
        st.pyplot(fig, clear_figure = True)

    def plot_temperature(df_all):
        mpl.rcParams.update({"axes.grid" : True, "grid.color": "black"})
        sns.set(font_scale = 2)
        fig = plt.figure(figsize=(30,6))
        ax = sns.histplot(df_all['Temperature'], kde=True, stat="density")
        ax.tick_params(axis='y', colors='black') 
        ax.tick_params(axis='x', colors='black') 
        ax.set_xticks(np.arange(math.floor(df_all['Temperature'].min()),df_all['Temperature'].max() + 1, 0.5))
        plt.setp(ax.get_xticklabels(), rotation=-10)
        st.pyplot(fig, clear_figure = True)

    def plot_chlorophyll(df_all):
        mpl.rcParams.update({"axes.grid" : True, "grid.color": "black"})
        sns.set(font_scale = 2)
        fig = plt.figure(figsize=(30,6))
        ax = sns.histplot(df_all['Chlorophyll'], kde=True, stat="density")
        ax.tick_params(axis='y', colors='black') 
        ax.tick_params(axis='x', colors='black') 
        ax.set_xticks(np.arange(math.floor(df_all['Chlorophyll'].min()),df_all['Chlorophyll'].max() + 0.1, 0.01))
        plt.setp(ax.get_xticklabels(), rotation=-10)
        st.pyplot(fig, clear_figure = True)

    def plot_pH(df_all):
        mpl.rcParams.update({"axes.grid" : True, "grid.color": "black"})
        sns.set(font_scale = 2)
        fig = plt.figure(figsize=(18,6))
        ax = sns.histplot(df_all['pH'], kde=True, stat="density")
        ax.tick_params(axis='y', colors='black') 
        ax.tick_params(axis='x', colors='black') 
        ax.set_xticks(np.arange(math.floor(df_all['pH'].min()), df_all['pH'].max() + 1, 0.1))
        plt.setp(ax.get_xticklabels(), rotation=-10)
        st.pyplot(fig, clear_figure = True)

    def plot_sm(df_all):
        mpl.rcParams.update({"axes.grid" : True, "grid.color": "black"})
        sns.set(font_scale = 2)
        fig = plt.figure(figsize=(20,9))
        ax = sns.histplot(df_all['Suspended Matter'], kde=True, stat="density")
        ax.tick_params(axis='y', colors='black') 
        ax.tick_params(axis='x', colors='black') 
        ax.set_xticks(np.arange(math.floor(df_all['Suspended Matter'].min()),df_all['Suspended Matter'].max() + 100, 20))
        plt.setp(ax.get_xticklabels(), rotation=-10)
        st.pyplot(fig, clear_figure = True)



    

        
    if st.button('Submit'):
        

        df2 = get_data(long, lat, slider1, slider2) 
        # st.write(mess)
        df_all, test = send_df(df2)
        st.write(df_all)

        if prm_type == 'Dissolved Oxygen':
            plot_do(df_all)
        elif prm_type == 'Salinity':
            plot_salinity(df_all)
        elif prm_type == 'Land Surface Temperature':
            plot_temperature(df_all)
        elif prm_type == 'Turbidity':
            plot_turbidity(df_all)
        elif prm_type == 'pH':
            plot_pH(df_all)
        elif prm_type == 'Chlorophyll':
            plot_chlorophyll(df_all)
        elif prm_type == 'Suspended Matter':
            plot_sm(df_all)
        elif prm_type == 'Dissolved Organic Matter':
            plot_dom(df_all)
        else:
            plot_dom(df_all)
            plot_pH(df_all)
            plot_sm(df_all)
            plot_chlorophyll(df_all)
            plot_turbidity(df_all)
            plot_temperature(df_all)
            plot_salinity(df_all)
            plot_do(df_all)


        if aoi_type == 'Shinai Lake':
            aoi_data = pd.read_csv('Data_Shinai_Lake_2019')
            aoi_data = pd.read_csv('Data_2020_Shinai_Lake')
            aoi_data = pd.read_csv('Data_2021_Shinai_Lake')
        elif aoi_type == 'Harmirsar Lake':
            aoi_data = pd.read_csv('Data_2019_Harmisar_Lake')
            aoi_data = pd.read_csv('Data_2020_Harmisar_Lake')
            aoi_data = pd.read_csv('Data_2021_Harmisar_Lake')
        elif aoi_type == 'Tappar Lake':
            aoi_data = pd.read_csv('Data_2019_Tappar_Lake')
            aoi_data = pd.read_csv('Data_2020_Tappar_Lake')
            aoi_data = pd.read_csv('Data_2021_Tappar_Lake')

        prm = prm_type.split(" ")

        # st.write(prm)
        
        # details = aoi_data[aoi_data['prm']==prm[0]]

        # coordinates = {
        #     'Kutch Region': [23.7337,69.8597]
        # }

        # m = folium.Map(location=coordinates[prm_type], zoom_start=10)
        # folium.TileLayer('Stamen Terrain').add_to(m)
        # folium.TileLayer('Stamen Toner').add_to(m)
        # folium.TileLayer('Stamen Water Color').add_to(m)
        # folium.TileLayer('cartodbpositron').add_to(m)
        # folium.TileLayer('cartodbdark_matter').add_to(m)
        # folium.LayerControl().add_to(m)
        # # m
        
        # for index, row in details.iterrows():
        #     if row['geometry'].startswith("POINT"):
        #         geometry = shapely.wkt.loads(row['geometry'])
        #     else:
        #         p = shapely.wkt.loads(row['geometry'])
        #         geometry = p.centroid

        #     folium.Marker(
        #         [geometry.y, geometry.x], popup=row['display_name'],
        #     ).add_to(m)

        # folium_static(m, width=900)


elif add_selectbox == 'Result':
    
    st.subheader('OUR RESULT')
    st.markdown('<h4></h4>', unsafe_allow_html=True)
    st.image("", width=500)
    # if st.button('Submit'):
    #     st.write(predict_quality(df2, test))

        
        
elif add_selectbox == 'Visualizations':
    
    st.subheader('PROJECT VISUALIZATIONS')
    st.markdown('<h4>Harmisar Lake</h4>', unsafe_allow_html=True)
    st.image("harmisar_lake.png", width=400)
    st.markdown('<h4>Shinai Lake</h4>', unsafe_allow_html=True)
    st.image("shinai_lake.png", width=400)
    st.markdown('<h4>Tappar Lake</h4>', unsafe_allow_html=True)
    st.image("tappar_lake.png", width=400)
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
    st.markdown('<a href="https://www.linkedin.com/in/sairam-kannan-8648a0138/">Sai Villiers</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="https://www.linkedin.com/in/ishita-kheria-20b1b31ab/">Ishita Kheria</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="https://www.linkedin.com/in/prathima-kadari/">Prathima Kadari</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="https://www.linkedin.com/in/himanshu-mishra-851459b5/">Himanshu Mishra</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="https://www.linkedin.com/in/bharati-panigrahi-10a9461a0/">Bharati Panigrahi</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="https://www.linkedin.com/in/deepali-bidwai/">Deepali Bidwai</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="">Kiran Ryakala</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="https://www.linkedin.com/in/drij-chudasama-2a112a168/">Drij Chudasama</a>',
                unsafe_allow_html=True)

    st.subheader('PROJECT MANAGER')

    st.markdown('<a href="https://www.linkedin.com/in/chancy-shah-671787119/">Chancy Shah</a>', unsafe_allow_html=True)
                

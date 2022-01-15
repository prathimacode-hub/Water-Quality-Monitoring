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
from dateutil.relativedelta import relativedelta
from data_collection import *
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import time

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
    
    col3,_ = st.columns((1,2)) # To make it narrower
    
    format = 'MMM DD, YYYY'  # format output
        
    start1 = datetime.date(year=2024,month=7,day=1)-relativedelta(years=5) #  I need some range in the past
    
    end1 = datetime.datetime.now().date()+relativedelta(years=2)
    
    max_days = end1-start1
        
    slider1 = col3.slider('Select date', min_value=start1, value=end1 ,max_value=end1, format=format)
        ## Sanity check
    st.table(pd.DataFrame([[start1, slider1, end1]],
                      columns=['start_selected',
                               'end_selected',
                               'end'],
                      index=['date']))

    start2 = datetime.date(year=2024,month=1,day=1)-relativedelta(years=5) #  I need some range in the past
    
    end2 = datetime.datetime.now().date()+relativedelta(years=2)
    
    max_days = end2-start2
        
    slider2 = col3.slider('Select date', min_value=start2, value=end2, max_value=end2, format=format)
        ## Sanity check
    st.table(pd.DataFrame([[start2, slider2, end2]],
                      columns=['start_selected',
                               'end_selected',
                               'end'],
                      index=['date']))
    #col3, col4 = st.columns(2)
    
    #d1 = st.sidebar.date_input('start date', datetime.date(2022,1,1))
    
    #st.write(d1)
    
    #d2 = st.sidebar.date_input('end date', datetime.date(2022,1,15))
    
    #st.write(d2)
    
    #d1 = st.date_input("Start Date")
    
    #d2 = st.date_input("End Date")
    df_all = send_df()
    st.write(df_all)

    mpl.rcParams.update({"axes.grid" : True, "grid.color": "black"})
    sns.set(font_scale = 1)

    fig = plt.figure(figsize=(25,10))
    ax = sns.histplot(df_all['Dissolved Oxygen'], kde=True, stat="density")
    ax.tick_params(axis='y', colors='black') 
    ax.tick_params(axis='x', colors='black') 
    ax.set_xticks(np.arange(-7, df_all['Dissolved Oxygen'].max() + 1, 1))
    plt.setp(ax.get_xticklabels(), rotation=-10)
    plt.show() 
    plt.savefig('do.png', bbox_inches='tight')
    st.pyplot(fig, clear_figure = True) 
    # st.image('do.png')
    time.sleep(5)
    
    # plt.show()    
    if st.button('Submit'):

        # mess = get_data(start_date, slider) 
        # st.write(mess)


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

        st.write(prm)
        
        # details = aoi_data[aoi_data['prm']==prm[0]]

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
    st.markdown('<a href="">Sai Villiers</a>',
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
                

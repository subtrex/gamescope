import requests
import streamlit as st
import folium
from folium import plugins
from streamlit_folium import folium_static
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from folium import Choropleth, GeoJson
import json
import numpy as np
from io import BytesIO
import base64
from folium import IFrame, plugins

st.set_page_config(page_title="GameScope", page_icon=":trident:", layout="wide")

# Custom CSS for text justification
text_justification_css = """
    p {
        text-align: center;
    }
"""
# Combined custom CSS
mystyle = f'''
    <style>
        {text_justification_css}
    </style>
'''
st.markdown(mystyle, unsafe_allow_html=True)
st.markdown('<span style="font-size:60px; font-weight: bold; font-family: Calibri;"> GameScope </span>', unsafe_allow_html=True)
st.markdown('<span style="font-size:20px; font-style: italic;"> Navigating Game Sales </span>', unsafe_allow_html=True)

st.write("---")

st.write("Welcome to GameScope, a web platform to navigate game sales from 1996-2016. To get started, please choose the desired year range and genre. You can track the total game sales, and also the region wise best-sellers for your chosen categories.")

with st.container():
    col_1, col_2= st.columns([1, 1], gap="large")

    with col_1:
        year_option = st.selectbox('Year',('All', '1996-2000', '2001-2005', '2006-2010', '2011-2016'))

    with col_2:
        genre_option = st.selectbox('Genre',('All', 'Role-Playing',
    'Racing',
    'Action',
    'Misc',
    'Adventure',
    'Simulation',
    'Sports',
    'Shooter',
    'Puzzle',
    'Platform',
    'Strategy',
    'Fighting'))

st.write("\n")

df = pd.read_csv('video_games_sales_data.csv')

# Pre-processing

# Dropping extra columns
columns_to_drop = ['Critic_Count', 'User_Score', 'User_Count', 'Developer', 'Rating']
df = df.drop(columns=columns_to_drop)

# Merging similar rows by the Name, Genre, Publisher column
df['Year_of_Release'] = df['Year_of_Release'].astype(int)
df = df.groupby(['Name', 'Genre', 'Publisher'], as_index=False).agg({
    'Year_of_Release': 'max',
    'NA_Sales': 'sum',
    'EU_Sales': 'sum',
    'JP_Sales': 'sum',
    'Other_Sales': 'sum',
    'Global_Sales': 'sum',
    'Critic_Score': 'mean'
})

st.write('<div style="text-align: left;">Note: {}</div>'.format("Sales are in millions"), unsafe_allow_html=True)

# Making bins for the year of release
df['Year_Bin'] = pd.cut(df['Year_of_Release'], bins=[1995, 2000, 2005, 2010, 2016], labels=['1996-2000', '2001-2005', '2006-2010', '2011-2016'])
df = df.dropna()

# Calculations

if(year_option == "All" and genre_option == "All"):
    cumulative_sales = [df['NA_Sales'].sum(),df['EU_Sales'].sum(),df['JP_Sales'].sum(),df['Other_Sales'].sum()]

    sorted_df_NA = df.sort_values(by='NA_Sales', ascending=False)
    NA_top_game = [sorted_df_NA.iloc[0]['Name'], sorted_df_NA.iloc[0]['Publisher'], sorted_df_NA.iloc[0]['Genre'], sorted_df_NA.iloc[0]['Year_of_Release'], sorted_df_NA.iloc[0]['NA_Sales']]
    NA_second_top_game = [sorted_df_NA.iloc[1]['Name'], sorted_df_NA.iloc[1]['Publisher'], sorted_df_NA.iloc[1]['Genre'], sorted_df_NA.iloc[1]['Year_of_Release'], sorted_df_NA.iloc[1]['NA_Sales']]
    NA_third_top_game = [sorted_df_NA.iloc[2]['Name'], sorted_df_NA.iloc[2]['Publisher'], sorted_df_NA.iloc[2]['Genre'], sorted_df_NA.iloc[2]['Year_of_Release'], sorted_df_NA.iloc[2]['NA_Sales']]

    sorted_df_EU = df.sort_values(by='EU_Sales', ascending=False)
    EU_top_game = [sorted_df_EU.iloc[0]['Name'], sorted_df_EU.iloc[0]['Publisher'], sorted_df_EU.iloc[0]['Genre'], sorted_df_EU.iloc[0]['Year_of_Release'], sorted_df_EU.iloc[0]['EU_Sales']]
    EU_second_top_game = [sorted_df_EU.iloc[1]['Name'], sorted_df_EU.iloc[1]['Publisher'], sorted_df_EU.iloc[1]['Genre'], sorted_df_EU.iloc[1]['Year_of_Release'], sorted_df_EU.iloc[1]['EU_Sales']]
    EU_third_top_game = [sorted_df_EU.iloc[2]['Name'], sorted_df_EU.iloc[2]['Publisher'], sorted_df_EU.iloc[2]['Genre'], sorted_df_EU.iloc[2]['Year_of_Release'], sorted_df_EU.iloc[2]['EU_Sales']]

    sorted_df_JP = df.sort_values(by='JP_Sales', ascending=False)
    JP_top_game = [sorted_df_JP.iloc[0]['Name'], sorted_df_JP.iloc[0]['Publisher'], sorted_df_JP.iloc[0]['Genre'], sorted_df_JP.iloc[0]['Year_of_Release'], sorted_df_JP.iloc[0]['JP_Sales']]
    JP_second_top_game = [sorted_df_JP.iloc[1]['Name'], sorted_df_JP.iloc[1]['Publisher'], sorted_df_JP.iloc[1]['Genre'], sorted_df_JP.iloc[1]['Year_of_Release'], sorted_df_JP.iloc[1]['JP_Sales']]
    JP_third_top_game = [sorted_df_JP.iloc[2]['Name'], sorted_df_JP.iloc[2]['Publisher'], sorted_df_JP.iloc[2]['Genre'], sorted_df_JP.iloc[2]['Year_of_Release'], sorted_df_JP.iloc[2]['JP_Sales']]

    sorted_df_Other = df.sort_values(by='Other_Sales', ascending=False)
    Other_top_game = [sorted_df_Other.iloc[0]['Name'], sorted_df_Other.iloc[0]['Publisher'], sorted_df_Other.iloc[0]['Genre'], sorted_df_Other.iloc[0]['Year_of_Release'], sorted_df_Other.iloc[0]['Other_Sales']]
    Other_second_top_game = [sorted_df_Other.iloc[1]['Name'], sorted_df_Other.iloc[1]['Publisher'], sorted_df_Other.iloc[1]['Genre'], sorted_df_Other.iloc[1]['Year_of_Release'], sorted_df_Other.iloc[1]['Other_Sales']]
    Other_third_top_game = [sorted_df_Other.iloc[2]['Name'], sorted_df_Other.iloc[2]['Publisher'], sorted_df_Other.iloc[2]['Genre'], sorted_df_Other.iloc[2]['Year_of_Release'], sorted_df_Other.iloc[2]['Other_Sales']]

    top_game_result = [NA_top_game, EU_top_game, JP_top_game, Other_top_game]
    second_top_game_result = [NA_second_top_game, EU_second_top_game, JP_second_top_game, Other_second_top_game]
    third_top_game_result = [NA_third_top_game, EU_third_top_game, JP_third_top_game, Other_third_top_game]
    
elif(year_option == "All" and genre_option != "All"):
    filtered_df = df[(df['Genre'] == genre_option)]
    cumulative_sales = [filtered_df['NA_Sales'].sum(),filtered_df['EU_Sales'].sum(),filtered_df['JP_Sales'].sum(),filtered_df['Other_Sales'].sum()]
    
    sorted_df_NA = filtered_df.sort_values(by='NA_Sales', ascending=False)
    NA_top_game = [sorted_df_NA.iloc[0]['Name'], sorted_df_NA.iloc[0]['Publisher'], sorted_df_NA.iloc[0]['Genre'], sorted_df_NA.iloc[0]['Year_of_Release'], sorted_df_NA.iloc[0]['NA_Sales']]
    NA_second_top_game = [sorted_df_NA.iloc[1]['Name'], sorted_df_NA.iloc[1]['Publisher'], sorted_df_NA.iloc[1]['Genre'], sorted_df_NA.iloc[1]['Year_of_Release'], sorted_df_NA.iloc[1]['NA_Sales']]
    NA_third_top_game = [sorted_df_NA.iloc[2]['Name'], sorted_df_NA.iloc[2]['Publisher'], sorted_df_NA.iloc[2]['Genre'], sorted_df_NA.iloc[2]['Year_of_Release'], sorted_df_NA.iloc[2]['NA_Sales']]

    sorted_df_EU = filtered_df.sort_values(by='EU_Sales', ascending=False)
    EU_top_game = [sorted_df_EU.iloc[0]['Name'], sorted_df_EU.iloc[0]['Publisher'], sorted_df_EU.iloc[0]['Genre'], sorted_df_EU.iloc[0]['Year_of_Release'], sorted_df_EU.iloc[0]['EU_Sales']]
    EU_second_top_game = [sorted_df_EU.iloc[1]['Name'], sorted_df_EU.iloc[1]['Publisher'], sorted_df_EU.iloc[1]['Genre'], sorted_df_EU.iloc[1]['Year_of_Release'], sorted_df_EU.iloc[1]['EU_Sales']]
    EU_third_top_game = [sorted_df_EU.iloc[2]['Name'], sorted_df_EU.iloc[2]['Publisher'], sorted_df_EU.iloc[2]['Genre'], sorted_df_EU.iloc[2]['Year_of_Release'], sorted_df_EU.iloc[2]['EU_Sales']]

    sorted_df_JP = filtered_df.sort_values(by='JP_Sales', ascending=False)
    JP_top_game = [sorted_df_JP.iloc[0]['Name'], sorted_df_JP.iloc[0]['Publisher'], sorted_df_JP.iloc[0]['Genre'], sorted_df_JP.iloc[0]['Year_of_Release'], sorted_df_JP.iloc[0]['JP_Sales']]
    JP_second_top_game = [sorted_df_JP.iloc[1]['Name'], sorted_df_JP.iloc[1]['Publisher'], sorted_df_JP.iloc[1]['Genre'], sorted_df_JP.iloc[1]['Year_of_Release'], sorted_df_JP.iloc[1]['JP_Sales']]
    JP_third_top_game = [sorted_df_JP.iloc[2]['Name'], sorted_df_JP.iloc[2]['Publisher'], sorted_df_JP.iloc[2]['Genre'], sorted_df_JP.iloc[2]['Year_of_Release'], sorted_df_JP.iloc[2]['JP_Sales']]

    sorted_df_Other = filtered_df.sort_values(by='Other_Sales', ascending=False)
    Other_top_game = [sorted_df_Other.iloc[0]['Name'], sorted_df_Other.iloc[0]['Publisher'], sorted_df_Other.iloc[0]['Genre'], sorted_df_Other.iloc[0]['Year_of_Release'], sorted_df_Other.iloc[0]['Other_Sales']]
    Other_second_top_game = [sorted_df_Other.iloc[1]['Name'], sorted_df_Other.iloc[1]['Publisher'], sorted_df_Other.iloc[1]['Genre'], sorted_df_Other.iloc[1]['Year_of_Release'], sorted_df_Other.iloc[1]['Other_Sales']]
    Other_third_top_game = [sorted_df_Other.iloc[2]['Name'], sorted_df_Other.iloc[2]['Publisher'], sorted_df_Other.iloc[2]['Genre'], sorted_df_Other.iloc[2]['Year_of_Release'], sorted_df_Other.iloc[2]['Other_Sales']]

    top_game_result = [NA_top_game, EU_top_game, JP_top_game, Other_top_game]
    second_top_game_result = [NA_second_top_game, EU_second_top_game, JP_second_top_game, Other_second_top_game]
    third_top_game_result = [NA_third_top_game, EU_third_top_game, JP_third_top_game, Other_third_top_game]

elif(year_option != "All" and genre_option == "All"):
    filtered_df = df[(df['Year_Bin'] == year_option)]
    cumulative_sales = [filtered_df['NA_Sales'].sum(),filtered_df['EU_Sales'].sum(),filtered_df['JP_Sales'].sum(),filtered_df['Other_Sales'].sum()]    

    sorted_df_NA = filtered_df.sort_values(by='NA_Sales', ascending=False)
    NA_top_game = [sorted_df_NA.iloc[0]['Name'], sorted_df_NA.iloc[0]['Publisher'], sorted_df_NA.iloc[0]['Genre'], sorted_df_NA.iloc[0]['Year_of_Release'], sorted_df_NA.iloc[0]['NA_Sales']]
    NA_second_top_game = [sorted_df_NA.iloc[1]['Name'], sorted_df_NA.iloc[1]['Publisher'], sorted_df_NA.iloc[1]['Genre'], sorted_df_NA.iloc[1]['Year_of_Release'], sorted_df_NA.iloc[1]['NA_Sales']]
    NA_third_top_game = [sorted_df_NA.iloc[2]['Name'], sorted_df_NA.iloc[2]['Publisher'], sorted_df_NA.iloc[2]['Genre'], sorted_df_NA.iloc[2]['Year_of_Release'], sorted_df_NA.iloc[2]['NA_Sales']]

    sorted_df_EU = filtered_df.sort_values(by='EU_Sales', ascending=False)
    EU_top_game = [sorted_df_EU.iloc[0]['Name'], sorted_df_EU.iloc[0]['Publisher'], sorted_df_EU.iloc[0]['Genre'], sorted_df_EU.iloc[0]['Year_of_Release'], sorted_df_EU.iloc[0]['EU_Sales']]
    EU_second_top_game = [sorted_df_EU.iloc[1]['Name'], sorted_df_EU.iloc[1]['Publisher'], sorted_df_EU.iloc[1]['Genre'], sorted_df_EU.iloc[1]['Year_of_Release'], sorted_df_EU.iloc[1]['EU_Sales']]
    EU_third_top_game = [sorted_df_EU.iloc[2]['Name'], sorted_df_EU.iloc[2]['Publisher'], sorted_df_EU.iloc[2]['Genre'], sorted_df_EU.iloc[2]['Year_of_Release'], sorted_df_EU.iloc[2]['EU_Sales']]

    sorted_df_JP = filtered_df.sort_values(by='JP_Sales', ascending=False)
    JP_top_game = [sorted_df_JP.iloc[0]['Name'], sorted_df_JP.iloc[0]['Publisher'], sorted_df_JP.iloc[0]['Genre'], sorted_df_JP.iloc[0]['Year_of_Release'], sorted_df_JP.iloc[0]['JP_Sales']]
    JP_second_top_game = [sorted_df_JP.iloc[1]['Name'], sorted_df_JP.iloc[1]['Publisher'], sorted_df_JP.iloc[1]['Genre'], sorted_df_JP.iloc[1]['Year_of_Release'], sorted_df_JP.iloc[1]['JP_Sales']]
    JP_third_top_game = [sorted_df_JP.iloc[2]['Name'], sorted_df_JP.iloc[2]['Publisher'], sorted_df_JP.iloc[2]['Genre'], sorted_df_JP.iloc[2]['Year_of_Release'], sorted_df_JP.iloc[2]['JP_Sales']]

    sorted_df_Other = filtered_df.sort_values(by='Other_Sales', ascending=False)
    Other_top_game = [sorted_df_Other.iloc[0]['Name'], sorted_df_Other.iloc[0]['Publisher'], sorted_df_Other.iloc[0]['Genre'], sorted_df_Other.iloc[0]['Year_of_Release'], sorted_df_Other.iloc[0]['Other_Sales']]
    Other_second_top_game = [sorted_df_Other.iloc[1]['Name'], sorted_df_Other.iloc[1]['Publisher'], sorted_df_Other.iloc[1]['Genre'], sorted_df_Other.iloc[1]['Year_of_Release'], sorted_df_Other.iloc[1]['Other_Sales']]
    Other_third_top_game = [sorted_df_Other.iloc[2]['Name'], sorted_df_Other.iloc[2]['Publisher'], sorted_df_Other.iloc[2]['Genre'], sorted_df_Other.iloc[2]['Year_of_Release'], sorted_df_Other.iloc[2]['Other_Sales']]

    top_game_result = [NA_top_game, EU_top_game, JP_top_game, Other_top_game]
    second_top_game_result = [NA_second_top_game, EU_second_top_game, JP_second_top_game, Other_second_top_game]
    third_top_game_result = [NA_third_top_game, EU_third_top_game, JP_third_top_game, Other_third_top_game]

else:
    filtered_df = df[(df['Year_Bin'] == year_option) & (df['Genre'] == genre_option)]
    cumulative_sales = [filtered_df['NA_Sales'].sum(),filtered_df['EU_Sales'].sum(),filtered_df['JP_Sales'].sum(),filtered_df['Other_Sales'].sum()] 

    sorted_df_NA = filtered_df.sort_values(by='NA_Sales', ascending=False)
    NA_top_game = [sorted_df_NA.iloc[0]['Name'], sorted_df_NA.iloc[0]['Publisher'], sorted_df_NA.iloc[0]['Genre'], sorted_df_NA.iloc[0]['Year_of_Release'], sorted_df_NA.iloc[0]['NA_Sales']]
    NA_second_top_game = [sorted_df_NA.iloc[1]['Name'], sorted_df_NA.iloc[1]['Publisher'], sorted_df_NA.iloc[1]['Genre'], sorted_df_NA.iloc[1]['Year_of_Release'], sorted_df_NA.iloc[1]['NA_Sales']]
    NA_third_top_game = [sorted_df_NA.iloc[2]['Name'], sorted_df_NA.iloc[2]['Publisher'], sorted_df_NA.iloc[2]['Genre'], sorted_df_NA.iloc[2]['Year_of_Release'], sorted_df_NA.iloc[2]['NA_Sales']]

    sorted_df_EU = filtered_df.sort_values(by='EU_Sales', ascending=False)
    EU_top_game = [sorted_df_EU.iloc[0]['Name'], sorted_df_EU.iloc[0]['Publisher'], sorted_df_EU.iloc[0]['Genre'], sorted_df_EU.iloc[0]['Year_of_Release'], sorted_df_EU.iloc[0]['EU_Sales']]
    EU_second_top_game = [sorted_df_EU.iloc[1]['Name'], sorted_df_EU.iloc[1]['Publisher'], sorted_df_EU.iloc[1]['Genre'], sorted_df_EU.iloc[1]['Year_of_Release'], sorted_df_EU.iloc[1]['EU_Sales']]
    EU_third_top_game = [sorted_df_EU.iloc[2]['Name'], sorted_df_EU.iloc[2]['Publisher'], sorted_df_EU.iloc[2]['Genre'], sorted_df_EU.iloc[2]['Year_of_Release'], sorted_df_EU.iloc[2]['EU_Sales']]

    sorted_df_JP = filtered_df.sort_values(by='JP_Sales', ascending=False)
    JP_top_game = [sorted_df_JP.iloc[0]['Name'], sorted_df_JP.iloc[0]['Publisher'], sorted_df_JP.iloc[0]['Genre'], sorted_df_JP.iloc[0]['Year_of_Release'], sorted_df_JP.iloc[0]['JP_Sales']]
    JP_second_top_game = [sorted_df_JP.iloc[1]['Name'], sorted_df_JP.iloc[1]['Publisher'], sorted_df_JP.iloc[1]['Genre'], sorted_df_JP.iloc[1]['Year_of_Release'], sorted_df_JP.iloc[1]['JP_Sales']]
    JP_third_top_game = [sorted_df_JP.iloc[2]['Name'], sorted_df_JP.iloc[2]['Publisher'], sorted_df_JP.iloc[2]['Genre'], sorted_df_JP.iloc[2]['Year_of_Release'], sorted_df_JP.iloc[2]['JP_Sales']]

    sorted_df_Other = filtered_df.sort_values(by='Other_Sales', ascending=False)
    Other_top_game = [sorted_df_Other.iloc[0]['Name'], sorted_df_Other.iloc[0]['Publisher'], sorted_df_Other.iloc[0]['Genre'], sorted_df_Other.iloc[0]['Year_of_Release'], sorted_df_Other.iloc[0]['Other_Sales']]
    Other_second_top_game = [sorted_df_Other.iloc[1]['Name'], sorted_df_Other.iloc[1]['Publisher'], sorted_df_Other.iloc[1]['Genre'], sorted_df_Other.iloc[1]['Year_of_Release'], sorted_df_Other.iloc[1]['Other_Sales']]
    Other_third_top_game = [sorted_df_Other.iloc[2]['Name'], sorted_df_Other.iloc[2]['Publisher'], sorted_df_Other.iloc[2]['Genre'], sorted_df_Other.iloc[2]['Year_of_Release'], sorted_df_Other.iloc[2]['Other_Sales']]

    top_game_result = [NA_top_game, EU_top_game, JP_top_game, Other_top_game]
    second_top_game_result = [NA_second_top_game, EU_second_top_game, JP_second_top_game, Other_second_top_game]
    third_top_game_result = [NA_third_top_game, EU_third_top_game, JP_third_top_game, Other_third_top_game]

cumulative_sales = [round(value, 2) for value in cumulative_sales]

# Mapping

# Load GeoJSON data for North American countries
#north_america_geojson_url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json"
#north_america_data = requests.get(north_america_geojson_url).json()

#world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = gpd.read_file("geoData/ne_110m_admin_0_countries.shp")
north_america_data = world[world['CONTINENT'] == 'North America']
europe_data = world[world['CONTINENT'] == 'Europe']
japan_data = world[world['NAME'] == 'Japan']
exclude_countries_continents = ['North America', 'Europe', 'Japan']
rest_of_world_data = world[~(world['NAME'].isin(exclude_countries_continents) | world['CONTINENT'].isin(exclude_countries_continents))]

# Create a Folium map centered around North America
m = folium.Map(location=[30.4168, -3.7038], zoom_start=2.3)

# Create a GeoJson object with North American countries
folium.GeoJson(north_america_data, name="North America", style_function=lambda x: {'fillColor': 'red', 'color': 'transparent'}).add_to(m)
folium.GeoJson(europe_data, name="Europe", style_function=lambda x: {'fillColor': 'blue', 'color': 'transparent'}).add_to(m)
folium.GeoJson(japan_data, name="Japan", style_function=lambda x: {'fillColor': 'yellow', 'color': 'transparent'}).add_to(m)
folium.GeoJson(rest_of_world_data, name="Others", style_function=lambda x: {'fillColor': 'purple', 'color': 'transparent'}).add_to(m)

# Add LayerControl to toggle layers on/off
folium.LayerControl().add_to(m)

# Custom Marker


marker_data = pd.DataFrame({
   'lon':[-100, 80, 135, 30.32],
   'lat':[70, 70, 40, 30],
   'name':['North America', 'Europe', 'Japan', 'Others'],
   'sale_info':cumulative_sales,
   'top_game_name': [top_game_result[0][0], top_game_result[1][0], top_game_result[2][0], top_game_result[3][0]],
   'top_game_publisher': [top_game_result[0][1], top_game_result[1][1], top_game_result[2][1], top_game_result[3][1]],
   'top_game_genre': [top_game_result[0][2], top_game_result[1][2], top_game_result[2][2], top_game_result[3][2]],
   'top_game_year': [top_game_result[0][3], top_game_result[1][3], top_game_result[2][3], top_game_result[3][3]],
   'top_game_sales': [top_game_result[0][4], top_game_result[1][4], top_game_result[2][4], top_game_result[3][4]],
   'second_top_game_name': [second_top_game_result[0][0], second_top_game_result[1][0], second_top_game_result[2][0], second_top_game_result[3][0]],
   'second_top_game_publisher': [second_top_game_result[0][1], second_top_game_result[1][1], second_top_game_result[2][1], second_top_game_result[3][1]],
   'second_top_game_genre': [second_top_game_result[0][2], second_top_game_result[1][2], second_top_game_result[2][2], second_top_game_result[3][2]],
   'second_top_game_year': [second_top_game_result[0][3], second_top_game_result[1][3], second_top_game_result[2][3], second_top_game_result[3][3]],
   'second_top_game_sales': [second_top_game_result[0][4], second_top_game_result[1][4], second_top_game_result[2][4], second_top_game_result[3][4]],
   'third_top_game_name': [third_top_game_result[0][0], third_top_game_result[1][0], third_top_game_result[2][0], third_top_game_result[3][0]],
   'third_top_game_publisher': [third_top_game_result[0][1], third_top_game_result[1][1], third_top_game_result[2][1], third_top_game_result[3][1]],
   'third_top_game_genre': [third_top_game_result[0][2], third_top_game_result[1][2], third_top_game_result[2][2], third_top_game_result[3][2]],
   'third_top_game_year': [third_top_game_result[0][3], third_top_game_result[1][3], third_top_game_result[2][3], third_top_game_result[3][3]],
   'third_top_game_sales': [third_top_game_result[0][4], third_top_game_result[1][4], third_top_game_result[2][4], third_top_game_result[3][4]],
}, dtype=str)

for i in range(0,len(marker_data)):
    html=f"""
        <h1> {marker_data.iloc[i]['name']}</h1>
        <p><b>Best Seller:</b></p>
        <p><i>{marker_data['top_game_name'][i]}</i></p>
        <p>Publisher: {marker_data['top_game_publisher'][i]}</p>
        <p>Genre: {marker_data['top_game_genre'][i]}</p>
        <p>Year Released: {marker_data['top_game_year'][i]}</p>
        <p>Sales: {round(float(marker_data['top_game_sales'][i]),2)}</p>
        <br>
        <p><b>Second Best Seller:</b></p>
        <p><i>{marker_data['second_top_game_name'][i]}</i></p>
        <p>Publisher: {marker_data['second_top_game_publisher'][i]}</p>
        <p>Genre: {marker_data['second_top_game_genre'][i]}</p>
        <p>Year Released: {marker_data['second_top_game_year'][i]}</p>
        <p>Sales: {round(float(marker_data['second_top_game_sales'][i]),2)}</p>
        <br>
        <p><b>Third Best Seller:</b></p>
        <p><i>{marker_data['third_top_game_name'][i]}</i></p>
        <p>Publisher: {marker_data['third_top_game_publisher'][i]}</p>
        <p>Genre: {marker_data['third_top_game_genre'][i]}</p>
        <p>Year Released: {marker_data['third_top_game_year'][i]}</p>
        <p>Sales: {round(float(marker_data['third_top_game_sales'][i]),2)}</p>
        """
    iframe = folium.IFrame(html=html, width=300, height=300)
    popup = folium.Popup(iframe, max_width=2650, auto_open=True)
    folium.Marker(
        location=[marker_data.iloc[i]['lat'], marker_data.iloc[i]['lon']],
        popup=popup,
        icon=folium.DivIcon(html=f"""
            <div>
                <span style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 14px; font-weight: bold;">
                    {marker_data['name'][i]}
                    <i style="font-style: italic; font-size: 12px; white-space: nowrap;">Total Sales: {marker_data['sale_info'][i]}</i>
                </span>
                <svg>
                    <circle cx="50" cy="50" r="40" fill="#69b3a2" opacity=".4"/>
                    <circle cx="50" cy="50" r="20" fill="#ff0000" opacity=".5"/>
                </svg>
            </div>""")
    ).add_to(m)

# Pie chart
region_labels = ['NA Sales', 'EU Sales', 'JP Sales', 'Other Sales']
region_sizes = [cumulative_sales[0], cumulative_sales[1], cumulative_sales[2], cumulative_sales[3]]
colors = ['#ffbfba', '#dbacfc', '#fdffba', '#fcb8e9']

fig, ax = plt.subplots(figsize=(10, 10))
plt.title('Sales Volume %', fontsize=30)
ax.pie(region_sizes, colors=colors, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.7, edgecolor='w', linewidth=2), textprops={'fontsize': 20})
fig.patch.set_alpha(0.0)
ax.patch.set_alpha(0.0)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

# Convert the Matplotlib figure to HTML
image_stream = BytesIO()
fig.savefig(image_stream, format='png')
image_stream.seek(0)
base64_image = base64.b64encode(image_stream.read()).decode('utf-8')

# Embed the HTML with the pie chart
html = f"""
    <div style="position: fixed; top: 10px; left: 10px; z-index: 1000;">
        <img src="data:image/png;base64,{base64_image}" alt="Pie Chart" width="250" height="250"/>
    </div>
"""

# Embed the HTML with the pie chart directly on the Folium map
m.get_root().html.add_child(folium.Element(html))

# Vertical bar Chart

regions = ['NA', 'EU', 'JP', 'Others']
top_game_sales = [top_game_result[0][4], top_game_result[1][4], top_game_result[2][4], top_game_result[3][4]]
second_top_game_sales = [second_top_game_result[0][4], second_top_game_result[1][4], second_top_game_result[2][4], second_top_game_result[3][4]]
third_top_game_sales = [third_top_game_result[0][4], third_top_game_result[1][4], third_top_game_result[2][4], third_top_game_result[3][4]]

bar_width = 0.25
index = np.arange(len(regions))

fig, ax = plt.subplots(figsize=(10, 10))
plt.title('Sales Volume %', fontsize=30)
bar1 = ax.bar(index, top_game_sales, bar_width, label='1st', color='#fcd568')
bar2 = ax.bar(index + bar_width, second_top_game_sales, bar_width, label='2nd', color='#e070ff')
bar3 = ax.bar(index + 2 * bar_width, third_top_game_sales, bar_width, label='3rd', color='#68fcf5')

ax.set_xlabel('Regions', fontsize=20)
ax.set_ylabel('Sales (in millions)', fontsize=20)
ax.set_title('Sales Difference of Top Sellers', fontsize=30)
ax.set_xticks(index + bar_width)
ax.set_xticklabels(regions, fontsize=15)
fig.patch.set_alpha(0.0)
ax.patch.set_alpha(0.0)
ax.legend(loc='upper center', fancybox=True, shadow=True, ncol=3, fontsize=15)

image_stream = BytesIO()
fig.savefig(image_stream, format='png')
image_stream.seek(0)
base64_image = base64.b64encode(image_stream.read()).decode('utf-8')

# Embed the HTML with the pie chart
html = f"""
    <div style="position: fixed; top: 300px; left: 10px; z-index: 1000;">
        <img src="data:image/png;base64,{base64_image}" alt="Pie Chart" width="250" height="250"/>
    </div>
"""

# Embed the HTML with the pie chart directly on the Folium map
m.get_root().html.add_child(folium.Element(html))

# Display the map
folium_static(m)

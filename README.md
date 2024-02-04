# GameScope

GameScope is a macroscope designed for enthusiasts, and researchers interested in exploring the intricate landscape of video game sales spanning from 1996 to 2016. Tailored to meet the diverse needs of the gaming community, this tool empowers users to dive into the vast realm of gaming data, providing insights into sale numbers, genre preferences, and regional best-sellers.

Link: https://gamescope.streamlit.app/

## Tech

Python | pandas | Matplotlib | Folium | Plotly Express | Streamlit 

## Data

We have used the "Global Video Game Sales & Ratings" dataset from Kaggle (https://www.kaggle.com/datasets/thedevastator/global-video-game-sales-ratings). The dataset consists of records from Metacritic providing insight into global video game ratings and sales. It contains data such as publisher, genre, year of release, and sales information.

## Methodology

1 - Preprocessing: We dropped the unnecessary columns, normalized the values in the sales columns, merged rows that showed data for the same video game and their corresponding data.

2 - Visualization: We used folium to create a world map to make it visually appealing and interesting to navigate the data. We used plotly express to generate bar and pie charts to analyze the sales data.

3 - Dashboard: We created the dashboard using Streamlit and hosted using Streamlit Cloud.

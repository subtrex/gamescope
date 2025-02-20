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

## About

A dashboard to navigate video game sales.

![gs-1](https://github.com/user-attachments/assets/df3e3378-a24b-4057-99a4-3089760b5688)

Filter based on published year.

![gs-2](https://github.com/user-attachments/assets/700ac0bd-5b39-4b50-902e-51840a7f4540)

Filter based on region.

![gs-3](https://github.com/user-attachments/assets/4a7c0ae6-5287-408d-9837-0139ddb34a23)

Click on region to get further data on top selling games.

![gs-4](https://github.com/user-attachments/assets/e4a32748-1607-444f-a560-d843022589f3)

![gs-5](https://github.com/user-attachments/assets/694743ce-3038-4075-b6ec-631a204357af)

![gs-6](https://github.com/user-attachments/assets/543c4125-a26f-43d3-b671-ec9b6b7b7270)




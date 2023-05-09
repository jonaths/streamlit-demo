import seaborn as sns
import folium
from h3 import h3

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


def get_data(route, truck_type, n_rows=1000):
    np.random.seed(42)
    date_range = pd.date_range(end=datetime.today(), periods=n_rows, freq='D')
    route_list = [route] * n_rows
    truck_type_list = [truck_type] * n_rows
    category_list = np.random.choice(['Plaza', 'Zona', 'Region'], n_rows)
    value_list = np.random.randint(0, 201, n_rows)

    data = pd.DataFrame({
        'date': date_range,
        'route': route_list,
        'truck_type': truck_type_list,
        'category': category_list,
        'value': value_list
    })

    return data


# Title of the app
# Function to create a 'time_range' column based on the date
def assign_time_range(row):
    if row['date'] > datetime.today() - timedelta(days=30):
        return 'Last Month'
    elif row['date'] > datetime.today() - timedelta(days=90):
        return 'Last 3 Months'
    elif row['date'] > datetime.today() - timedelta(days=180):
        return 'Last 6 Months'
    else:
        return 'Older'


# Functions to generate a seaborn histogram and folium map
def create_histogram(data, bins=10):
    fig, ax = plt.subplots()
    sns.histplot(data, bins=bins, kde=True, ax=ax)
    return fig


def create_map(hexagons, map_center: tuple = (37.7749, -122.4194)):
    folium_map = folium.Map(location=map_center, zoom_start=12, control_scale=True)

    for hex_id in hexagons:
        points = h3.h3_to_geo_boundary(hex_id)
        folium.Polygon(locations=points, color="blue", fill=True, fill_opacity=0.4).add_to(folium_map)

    return folium_map


def get_histogram_data(df):
    # TODO: aquí debería ir la lógica para el histograma.
    return df['value']

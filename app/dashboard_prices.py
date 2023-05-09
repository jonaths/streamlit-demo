import streamlit as st
import streamlit.components.v1 as components

from modules.prices.tools import get_data, assign_time_range, create_histogram, create_map, get_histogram_data

# Inputs ======================================================================

# Plaza, Region, Zona
current_reference_prices = [10, 11, 25]
# Lat, Long
map_center = (37.7749, -122.4194)
# To plot N hexagons
hexagon_ids_to_plot = ['882830829bfffff', '8828308299fffff', '88283082c3fffff']

# =============================================================================

st.set_page_config(layout="wide")

# Title of the app
st.title("Historic Prices Dashboard")

# User input: route and truck_type (in the sidebar)
with st.sidebar:
    route = st.text_input("Enter the route:")
    truck_type = st.text_input("Enter the truck type:")

# Fetch data and filter by date ranges
if route and truck_type:
    df = get_data(route, truck_type)

    # Add a 'time_range' column to the DataFrame
    df['time_range'] = df.apply(assign_time_range, axis=1)

    # Group and aggregate the data
    grouped_data_df = df.groupby(['time_range', 'category']).agg({'value': 'mean'}).reset_index()

    # Display grid of indicators
    st.subheader("Value Averages")

    table_data_df = grouped_data_df.pivot_table(index='category', columns='time_range', values='value')

    # Add current reference price
    table_data_df['Current price'] = current_reference_prices

    # Reorder columns
    table_data_df = table_data_df[['Current price', 'Last Month', 'Last 3 Months', 'Last 6 Months']]

    st.table(table_data_df.style.format("{:.2f}"))

    # Build histogram
    histogram_data = get_histogram_data(df)

    # Create two columns below the table
    col1, col2 = st.columns(2)

    with col1:
        # Display seaborn histogram in the left column
        st.subheader("Histogram")
        st.pyplot(create_histogram(histogram_data))

    with col2:
        # Display folium map with Uber H3 hexagons in the right column
        st.subheader("Map")
        folium_map = create_map(hexagon_ids_to_plot, map_center)
        components.html(folium_map._repr_html_(), height=800, scrolling=True)

else:
    st.write("Please enter both the route and truck type.")

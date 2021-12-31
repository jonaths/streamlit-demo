import matplotlib.pyplot as plt
import streamlit as st

import pandas as pd
import numpy as np
import seaborn as sns

np.random.seed(1)


def build_dataframe():
    """
    Creates columns with random data.
    """
    data = {
        'impressions': np.random.randint(low=111, high=10000, size=100),
        'clicks': np.random.randint(low=0, high=1000, size=100)
    }

    df = pd.DataFrame(data)
    # add a date column and calculate the weekday of each row
    df['date'] = pd.date_range(start='1/1/2018', periods=100)
    df['weekday'] = df['date'].dt.dayofweek

    return df


def build_weekly_bar_plot(df: pd.DataFrame, kpi: str):
    """
    Builds a weekly plot figure with one ax.
    """
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    sns.barplot(x='weekday', y=kpi, data=df, ax=ax)
    return fig, ax


st.title('Streamlit dashboard')

selected_kpi = st.selectbox(
    'Select a KPI: ',
    ['clicks', 'impressions']
)

df = build_dataframe()

weekday_df = df.groupby('weekday').sum()
# required to get a column called weekday from the index
weekday_df.reset_index(inplace=True)
weekday_df['weekday'] = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sat', 'Sun']

weekday_fig, weekday_ax = build_weekly_bar_plot(weekday_df, kpi=selected_kpi)

st.pyplot(weekday_fig)

with st.expander("Show weekday values table"):
    st.dataframe(weekday_df)

with st.expander("Show full stats"):
    st.dataframe(df.describe())

#!/usr/bin/env python
# coding: utf-8

# In[4]:
import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows=10000):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Load data
data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

# Raw data section
st.subheader('Raw data')
st.write(data)

# Visualization 1: Number of pickups by hour using Plotly
st.subheader('Number of pickups by hour')
hist_values = pd.DataFrame({'Hour': data[DATE_COLUMN].dt.hour, 'Count': 1})
fig = px.bar(hist_values, x='Hour', y='Count', title='Number of Pickups by Hour')
st.plotly_chart(fig)

# Visualization 2: Map of all pickups using Plotly
st.subheader('Map of all pickups')
fig = px.scatter_mapbox(data, lat='lat', lon='lon', hover_name=DATE_COLUMN,
                        title='Map of All Pickups',
                        mapbox_style="carto-positron", zoom=10)
st.plotly_chart(fig)

# Interactive Feature 1: Map of pickups at a specific hour using Plotly
hour_to_filter = st.slider('Select an hour:', 0, 23, 17)  # Slider to choose the hour (default: 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
fig = px.scatter_mapbox(filtered_data, lat='lat', lon='lon', hover_name=DATE_COLUMN,
                        title=f'Map of Pickups at {hour_to_filter}:00',
                        mapbox_style="carto-positron", zoom=10)
st.plotly_chart(fig)

# Interactive Feature 2: Show/hide raw data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# Interactive Feature 3: Create another visualization (for example, a scatter plot)
st.subheader('Interactive Feature 3: Scatter Plot')
x_values = st.selectbox('Select x-axis data:', data.columns)
y_values = st.selectbox('Select y-axis data:', data.columns)
scatter_fig = px.scatter(data, x=x_values, y=y_values, title='Scatter Plot')
st.plotly_chart(scatter_fig)




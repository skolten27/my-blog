import pandas as pd
import zipfile
import plotly.express as px
import matplotlib.pyplot as plt
import requests
from io import BytesIO
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from my_plots import *
import streamlit as st

@st.cache_data
def load_name_data():
    file = 'combined_data.csv'
    with open(file) as f:
        data =pd.read_csv(f)
        data = data.drop(columns=["Unnamed: 0"])
    return data

data = load_name_data()

st.title("Kolten's First Streamlit app!")

with st.sidebar:
    stock_ticker = st.radio('Ticker Symbol', ['WEN', 'TSLA', 'AAPL', 'GOOG'])
    year_input = st.slider("Year", min_value=1880, max_value=2023, value=2000)
    n_names = st.text_input('Enter a name:', 'Mary')
    sex_input = st.selectbox("Sex for One Hit Wonders", ["M", "F"])


tab1, tab2, tab3 = st.tabs(['Names', 'Year', 'Trends'])

with tab1: 
    stock_data = data[data['symbol']==stock_ticker].copy()
    fig = plot_trading_volume_around_earnings(stock_data, stock = stock_ticker)
    st.plotly_chart(fig)

with tab2:
    fig2 = top_names_plot(data, year=year_input, n=n_names)
    st.plotly_chart(fig2)

    st.write('Unique Names Table')
    output_table = unique_names_summary(data, 2000)
    st.dataframe(output_table)

with tab3:
    fig3 = name_trend_plot(data, name=input_name)
    st.plotly_chart(fig3)

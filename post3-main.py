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
    year_input = st.slider("Year", min_value=1999, max_value=2024, value=2024)


tab1, tab2, tab3 = st.tabs(['Trading Volume', 'Surprise by Year', 'Surprise vs Stock Price Change'])

with tab1: 
    stock_data = data[data['symbol']==stock_ticker].copy()
    fig = plot_average_trading_volume(stock_data, stock = stock_ticker)
    st.plotly_chart(fig)

with tab2:
    fig2 = plot_density_surprise_percentage_by_year(data,year = year_input)
    st.plotly_chart(fig2)

with tab3:
    min_surprise = st.number_input('Minimum Surprise Percentage', value=-1000)
    max_surprise = st.number_input('Maximum Surprise Percentage', value=5000)
    fig3 = plot_surprise_vs_price_change(data, symbol=stock_ticker, min_surprise=min_surprise, max_surprise=max_surprise)
    st.plotly_chart(fig3)

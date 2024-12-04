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


st.markdown("""
# Analyzing Earnings and Market Trends
Welcome to the earnings and market trends analysis app! 
Select a stock ticker and adjust the filters to explore trading volume, earnings surprises, and stock price changes.
""")

with st.sidebar:
    st.header("Filter Options")
    st.write("Customize the filters below to analyze specific trends.")
    stock_ticker = st.radio('Ticker Symbol', ['WEN', 'TSLA', 'AAPL', 'GOOG'])
    year_input = st.slider("Year", min_value=1999, max_value=2024, value=2024)


tab1, tab2, tab3 = st.tabs(['Trading Volume', 'Surprise by Year', 'Surprise vs Stock Price Change'])

with tab1: 
    st.subheader("📈 Trading Volume Analysis")
    st.markdown("#### Key Question: How does trading volume change as earnings release date is approached across selected stocks?")
    st.write("Analyze the average trading volume for your selected stock. You can change the selected stock using the Ticker Symbol radio on the left")
    stock_data = data[data['symbol']==stock_ticker].copy()
    fig = plot_average_trading_volume(stock_data, stock = stock_ticker)
    st.plotly_chart(fig)

with tab2:
    st.subheader("📊 Surprise Percentage Anlysis")
    st.markdown("#### Key Question: How accurate are the analyst at predicting earnings?")
    st.write("Analyze the density of surprise in earnings reports. You can change the selected year using the Year slider on the left")
    fig2 = plot_density_surprise_percentage_by_year(data,year = year_input)
    st.plotly_chart(fig2)

with tab3:   
    st.subheader("📉 Surprise vs. Stock Price Change Analysis")
    st.markdown("#### Key Question: How does suprise affect stock prices if it affects it at all?")
    st.write("Analyze the stock price change percentage and earnings suprise percentage for your selected stock. You can change the selected stock using the Ticker Symbol radio on the left. You can adjust the minimum and maximum earnings surprise percentage using the text boxes below to be able to focus on smaller portions and identify trends.")
    min_surprise = st.number_input('Minimum Surprise Percentage', value=-1000)
    max_surprise = st.number_input('Maximum Surprise Percentage', value=5000)
    fig3 = plot_surprise_vs_price_change(data, symbol=stock_ticker, min_surprise=min_surprise, max_surprise=max_surprise)
    st.plotly_chart(fig3)

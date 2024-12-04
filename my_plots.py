import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import pandas as pd

def plot_average_trading_volume(df, stock='WEN', width=800, height=600):
    # Filter the data for the specified stock
    stock_data = df[df['symbol'] == stock].copy()
    # Ensure date types and calculate the relative days
    stock_data['price_date'] = pd.to_datetime(stock_data['price_date'])
    stock_data['earnings_release_date'] = pd.to_datetime(stock_data['earnings_release_date'])
    stock_data['days_before_earnings'] = (stock_data['price_date'] - stock_data['earnings_release_date']).dt.days
    
    # Filter the data for the desired window
    earnings_window = stock_data[
        (stock_data['days_before_earnings'] >= -7) &
        (stock_data['days_before_earnings'] <= 7)
    ]
    
    # Group by the relative day and calculate the average trading volume
    avg_volume = (
        earnings_window
        .groupby('days_before_earnings')['5. volume']
        .mean()
        .reset_index()
    )
    
    # Create the Plotly line chart with an area fill
    fig = px.line(
        avg_volume,
        x='days_before_earnings',
        y='5. volume',
        title=f'Average Trading Volume Around Earnings Release for {stock}',
        markers=True,
    )
    
    # Add the fill effect and customize traces
    fig.update_traces(
        line_color='orange',
        mode='lines+markers',
        fill='tozeroy',  # Fills the area below the line
        fillcolor='rgba(255,165,0,0.2)'  # Light orange transparency
    )
    # Customize the layout
    fig.update_layout(
        xaxis_title='Days Before/After Earnings Release',
        yaxis_title='Average Trading Volume',
        width=width,
        height=height,
        plot_bgcolor='#1C1C1E',
        font=dict(size=12)
    )
    return fig

def plot_density_surprise_percentage_by_year(df, year=None, width=800, height=600):
    # Ensure the 'earning_release_date' column is datetime type
    df['earnings_release_date'] = pd.to_datetime(df['earnings_release_date'])
    
    # Filter the data for the selected year if provided
    if year:
        df = df[df['earnings_release_date'].dt.year == year]
    
    # Ensure the 'surprisePercentage' column is numeric
    df['surprisePercentage'] = pd.to_numeric(df['surprisePercentage'], errors='coerce')
    
    # Remove NaN values for plotting
    df_clean = df[df['surprisePercentage'].notna()]
    
    # Create the density plot using Plotly
    fig = px.density_contour(
        df_clean,
        x='surprisePercentage',
        title=f'Density Plot of Earnings Surprise Percentage for {year}' if year else 'Density Plot of Earnings Surprise Percentage'
    )
    
    # Update the layout for better styling
    fig.update_layout(
        xaxis_title='Earnings Surprise Percentage',
        yaxis_title='Density',
        width=width,
        height=height,
        plot_bgcolor='#1C1C1E',
        font=dict(size=12)
    )
    
    # Optional: Add styling to the contour plot
    fig.update_traces(contours_coloring="fill", colorscale="Blues", line_smoothing=1.3)

    return fig

def plot_surprise_vs_price_change(df, symbol, min_surprise=-1000, max_surprise=5000, exclude_large_changes=False, width=800, height=600):
    # Filter data for the selected symbol
    df_filtered = df[df['symbol'] == symbol].copy()  # Use a copy to avoid modifying the original dataframe

    # Ensure the necessary columns are numeric
    df_filtered['price_change'] = pd.to_numeric(df_filtered['price_change'], errors='coerce')

    # Apply the exclusion for large stock price changes if the checkbox is checked
    if exclude_large_changes:
        df_filtered = df_filtered[df_filtered['price_change'] <= 100]

    # Apply filtering based on min/max surprise percentage
    df_filtered = df_filtered[
        (df_filtered['surprisePercentage'] >= min_surprise) &
        (df_filtered['surprisePercentage'] <= max_surprise)
    ]

    # Check if there's data to plot
    if df_filtered.empty:
        raise ValueError(f"No data available for the selected filters: Min Surprise = {min_surprise}, Max Surprise = {max_surprise}")

    # Create the scatter plot
    fig = px.scatter(
        df_filtered,
        x='surprisePercentage',
        y='price_change',
        color_discrete_sequence=['orange'],
        title=f"Earnings Surprise vs. Stock Price Change for {symbol}",
        labels={
            'surprisePercentage': 'Earnings Surprise Percentage',
            'price_change': 'Stock Price Percentage Change'
        }
    )

    # Update layout for better styling
    fig.update_layout(
        width=width,
        height=height,
        plot_bgcolor='#1C1C1E',  # Transparent background
        paper_bgcolor='#1C1C1E',  # Transparent figure background
        font=dict(color='#EAEAEA')  # Light font for dark themes
    )

    return fig

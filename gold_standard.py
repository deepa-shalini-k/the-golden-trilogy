import pandas as pd
import plotly.graph_objects as go

# Read the CSV file
df = pd.read_csv('Gold_Price_2025.csv')

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Sort by date in ascending order (oldest to newest)
df = df.sort_values('Date')

# Add a ticker column (as mentioned it's missing)
df['Ticker'] = 'GOLD'

# Create the candlestick chart
fig = go.Figure(data=[go.Candlestick(
    x=df['Date'],
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Price'],
    name='Gold Price'
)])

# Update layout
fig.update_layout(
    title=dict(
        text='Gold Standard Candlestick Chart 2025<br><sub>Rupees per 10g of 24K Gold | Green = Price Up | Red = Price Down</sub>',
    ),
    xaxis_title='Date',
    yaxis_title='Price (₹ per 10g)',
    xaxis_rangeslider_visible=True,
    template='plotly_white',
    height=600
)

# Show the chart
fig.show()
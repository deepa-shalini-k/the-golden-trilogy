import pandas as pd
import plotly.graph_objects as go

# Read the CSV file
df = pd.read_csv('Gold_Price_2025.csv')

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Sort by date to ensure chronological order
df = df.sort_values('Date')

# Extract month and day for organizing the data
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df['DayOfYear'] = df['Date'].dt.dayofyear

# Calculate angles for each data point
# Map day of year to angle (0-360), with rotation and direction handled by layout
total_days = 365
angles = (df['DayOfYear'] - 1) / total_days * 360

# Create hover text
hover_text = [
    f"<b>Date:</b> {row['Date'].strftime('%d %b %Y')}<br>" +
    f"<b>Price:</b> ₹{row['Price']:,.0f}<br>" +
    f"<b>Change:</b> {row['Chg%']:+.2f}%<br>" +
    f"<b>Day:</b> {row['Date'].strftime('%A')}"
    for _, row in df.iterrows()
]

# Create the polar bar chart
fig = go.Figure()

fig.add_trace(go.Barpolar(
    r=df['Price'],
    theta=angles,
    width=360/total_days,  # Bar width to fill the circle
    marker=dict(
        color='#FFDB58',  # Mustard color
        line=dict(color='#FFDB58', width=0.5)
    ),
    text=hover_text,
    hovertemplate='%{text}<extra></extra>',
))

# Update layout
fig.update_layout(
    title=dict(
        text='Gold Rosette - Closing Price Chart 2025 (Rupees per 10g of 24K Gold)<br><sub>Each bar = one trading day | Longer bars = higher prices | Read clockwise from January</sub>',
    ),
    polar=dict(
        bgcolor='white',
        radialaxis=dict(
            visible=True,
            range=[0, df['Price'].max() * 1.1],
            showticklabels=True,
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1,
            title='Closing Price (₹ per 10g)'
        ),
        angularaxis=dict(
            visible=True,
            direction='clockwise',
            rotation=90,  # Start at top
            tickmode='array',
            tickvals=[0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330],
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            showgrid=False,
            showline=False
        )
    ),
    showlegend=False,
    height=800,
    width=800,
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# Show the chart
fig.show()
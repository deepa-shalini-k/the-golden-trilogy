import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Read the CSV file
df = pd.read_csv('Gold_Price_2025.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# Calculate volatility (using daily change percentage)
df['Volatility'] = abs(df['Chg%'])

# Normalize values for visualization
price_normalized = (df['Price'] - df['Price'].min()) / (df['Price'].max() - df['Price'].min())
volume_normalized = (df['Volume'] - df['Volume'].min()) / (df['Volume'].max() - df['Volume'].min())
volatility_normalized = (df['Volatility'] - df['Volatility'].min()) / (df['Volatility'].max() - df['Volatility'].min())

# Add artistic jitter
np.random.seed(42)
jitter_x = pd.Series(np.random.normal(0, 0.8, len(df)), index=df.index)
jitter_y = pd.Series(np.random.normal(0, 200, len(df)), index=df.index)

# Create jittered positions
df['x_pos'] = df['Date'] + pd.to_timedelta(jitter_x, unit='D')
df['y_pos'] = df['Price'] + jitter_y

# Size based on volume, opacity based on volatility
df['star_size'] = 8 + volume_normalized * 30
df['star_opacity'] = 0.3 + volatility_normalized * 0.7

# Identify significant price events (top 20% price changes)
threshold = df['Volatility'].quantile(0.80)
significant_events = df[df['Volatility'] >= threshold]

# Create the figure
fig = go.Figure()

# Add cosmic dust effect (small background stars)
np.random.seed(123)
cosmic_count = 300
cosmic_dates = pd.date_range(df['Date'].min(), df['Date'].max(), periods=cosmic_count)
cosmic_y = np.random.uniform(df['Price'].min() - 500, df['Price'].max() + 500, cosmic_count)
cosmic_sizes = np.random.uniform(1, 3, cosmic_count)
cosmic_alpha = np.random.uniform(0.1, 0.3, cosmic_count)

fig.add_trace(go.Scatter(
    x=cosmic_dates,
    y=cosmic_y,
    mode='markers',
    marker=dict(
        size=cosmic_sizes,
        color='white',
        opacity=cosmic_alpha,
    ),
    hoverinfo='skip',
    showlegend=False,
    name='Cosmic Dust'
))

# Draw constellation lines connecting significant events
for i in range(len(significant_events) - 1):
    event1 = significant_events.iloc[i]
    event2 = significant_events.iloc[i + 1]
    
    fig.add_trace(go.Scatter(
        x=[event1['x_pos'], event2['x_pos']],
        y=[event1['y_pos'], event2['y_pos']],
        mode='lines',
        line=dict(color='gold', width=0.8, dash='solid'),
        opacity=0.25,
        hoverinfo='skip',
        showlegend=False,
        name='Constellation Line'
    ))

# Add glow effect for significant events
fig.add_trace(go.Scatter(
    x=significant_events['x_pos'],
    y=significant_events['y_pos'],
    mode='markers',
    marker=dict(
        size=significant_events['star_size'] * 3,
        color='gold',
        opacity=0.15,
        symbol='circle',
    ),
    hoverinfo='skip',
    showlegend=False,
    name='Event Glow'
))

# Create the main star scatter plot
hover_text = [
    f"<b>Date:</b> {row['Date'].strftime('%d %b %Y')}<br>" +
    f"<b>Price:</b> ₹{row['Price']:,.0f}<br>" +
    f"<b>Volume:</b> {row['Volume']:,.0f} contracts<br>" + 
    f"<b>Change:</b> {row['Chg%']:+.2f}%<br>" + 
    f"<b>Volatility:</b> {row['Volatility']:.2f}%"
    for _, row in df.iterrows()
]

fig.add_trace(go.Scatter(
    x=df['x_pos'],
    y=df['y_pos'],
    mode='markers',
    marker=dict(
        size=df['star_size'],
        color='gold',
        opacity=df['star_opacity'],
        line=dict(color='#FFD700', width=0.5),
        symbol='star',
    ),
    text=hover_text,
    hovertemplate='%{text}<extra></extra>',
    name='Trading days',
    showlegend=True
))

# Update layout with dark theme
fig.update_layout(
    title=dict(
        text='<b>THE GOLD RUSH 2025</b><br><sub>Closing Price in Rupees per 10g of 24K Gold</sub><br><span style="font-size:14px; font-weight:300; font-family:Arial; margin-top:-5px; display:block;">Star size = Trading volume | Brightness = Volatility | Halos = Top 20% Volatile days</span>',
        font=dict(size=24, color='gold', family='Arial Black'),
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        gridcolor='rgba(255, 215, 0, 0.1)',
        showgrid=True,
        zeroline=False,
        tickfont=dict(color='#888888'),
        showline=False
    ),
    yaxis=dict(
        title=dict(text='<b>Closing Price (₹ per 10g)</b>', font=dict(size=14, color='gold')),
        gridcolor='rgba(255, 215, 0, 0.1)',
        showgrid=True,
        zeroline=False,
        tickfont=dict(color='#888888'),
        showline=False
    ),
    plot_bgcolor='#0a0a0a',
    paper_bgcolor='#0a0a0a',
    hovermode='closest',
    showlegend=True,
    legend=dict(
        bgcolor='rgba(26, 26, 26, 0.8)',
        bordercolor='gold',
        borderwidth=1,
        font=dict(color='gold', size=11),
        x=0.02,
        y=0.98,
        xanchor='left',
        yanchor='top'
    ),
    width=1600,
    height=900,
    margin=dict(l=80, r=80, t=100, b=80)
)

# Show the chart
fig.show()
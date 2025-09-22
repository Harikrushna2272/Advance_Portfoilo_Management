# Dashboard page component
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time

def render_dashboard():
    """Render the main dashboard page."""
    st.subheader("📊 Trading Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🎯 Total Decisions",
            "1,234",
            delta="12"
        )
    
    with col2:
        st.metric(
            "💼 Trades Executed",
            "89",
            delta="5"
        )
    
    with col3:
        st.metric(
            "📈 Success Rate",
            "73.2%",
            delta="2.1%"
        )
    
    with col4:
        st.metric(
            "💰 P&L Today",
            "$1,234.56",
            delta="$123.45"
        )
    
    st.divider()
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        render_portfolio_chart()
    
    with col2:
        render_performance_chart()
    
    # Recent decisions
    render_recent_decisions()

def render_portfolio_chart():
    """Render portfolio composition chart."""
    st.subheader("📊 Portfolio Composition")
    
    # Sample data - in real implementation, this would come from the portfolio
    portfolio_data = {
        "AAPL": {"shares": 50, "value": 7500, "percentage": 35},
        "TSLA": {"shares": 25, "value": 5000, "percentage": 23},
        "GOOGL": {"shares": 15, "value": 4000, "percentage": 19},
        "Cash": {"shares": 0, "value": 5000, "percentage": 23}
    }
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=list(portfolio_data.keys()),
        values=[data["value"] for data in portfolio_data.values()],
        hole=0.3
    )])
    
    fig.update_layout(
        title="Portfolio Allocation",
        showlegend=True,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_performance_chart():
    """Render performance chart."""
    st.subheader("📈 Performance Over Time")
    
    # Sample data - in real implementation, this would come from historical data
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    performance = [100000 + i * 100 + (i % 7) * 50 for i in range(len(dates))]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=performance,
        mode='lines',
        name='Portfolio Value',
        line=dict(color='#1f77b4', width=2)
    ))
    
    fig.update_layout(
        title="Portfolio Performance (30 Days)",
        xaxis_title="Date",
        yaxis_title="Portfolio Value ($)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_recent_decisions():
    """Render recent trading decisions."""
    st.subheader("🔄 Recent Trading Decisions")
    
    # Sample data - in real implementation, this would come from the decision engine
    decisions_data = {
        "Timestamp": [
            datetime.now() - timedelta(minutes=5),
            datetime.now() - timedelta(minutes=10),
            datetime.now() - timedelta(minutes=15),
            datetime.now() - timedelta(minutes=20),
            datetime.now() - timedelta(minutes=25)
        ],
        "Symbol": ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN"],
        "Signal": ["BUY", "SELL", "HOLD", "BUY", "HOLD"],
        "Confidence": [85, 72, 45, 91, 38],
        "Quantity": [50, 25, 0, 30, 0],
        "Price": [150.25, 245.80, 2800.50, 320.15, 3100.75]
    }
    
    df = pd.DataFrame(decisions_data)
    
    # Color code the signals
    def color_signal(val):
        if val == "BUY":
            return "background-color: #d4edda; color: #155724"
        elif val == "SELL":
            return "background-color: #f8d7da; color: #721c24"
        else:
            return "background-color: #fff3cd; color: #856404"
    
    styled_df = df.style.applymap(color_signal, subset=['Signal'])
    st.dataframe(styled_df, use_container_width=True)

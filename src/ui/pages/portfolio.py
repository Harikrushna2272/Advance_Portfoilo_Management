# Portfolio management page component
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render_portfolio_page():
    """Render the portfolio management page."""
    st.subheader("💼 Portfolio Management")
    
    # Portfolio overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Value", "$21,500.00", delta="$1,234.56")
    
    with col2:
        st.metric("Total Return", "7.5%", delta="2.1%")
    
    with col3:
        st.metric("Sharpe Ratio", "1.23", delta="0.15")
    
    st.divider()
    
    # Positions table
    render_positions_table()
    
    # Trade execution
    render_trade_execution()
    
    # Portfolio allocation chart
    render_allocation_chart()

def render_positions_table():
    """Render current positions table."""
    st.subheader("📊 Current Positions")
    
    positions_data = {
        "Symbol": ["AAPL", "TSLA", "GOOGL"],
        "Shares": [50, 25, 15],
        "Avg Price": [145.50, 240.00, 2750.00],
        "Current Price": [150.25, 245.80, 2800.50],
        "Market Value": [7512.50, 6145.00, 42007.50],
        "Unrealized P&L": [237.50, 145.00, 757.50],
        "P&L %": [3.26, 2.42, 1.80]
    }
    
    df = pd.DataFrame(positions_data)
    
    # Color code P&L
    def color_pnl(val):
        if val > 0:
            return "background-color: #d4edda; color: #155724"
        else:
            return "background-color: #f8d7da; color: #721c24"
    
    styled_df = df.style.applymap(color_pnl, subset=['Unrealized P&L', 'P&L %'])
    st.dataframe(styled_df, use_container_width=True)

def render_trade_execution():
    """Render trade execution interface."""
    st.subheader("💼 Execute Trade")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        trade_symbol = st.selectbox("Symbol", ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN"])
    
    with col2:
        trade_action = st.selectbox("Action", ["BUY", "SELL"])
    
    with col3:
        trade_quantity = st.number_input("Quantity", min_value=1, max_value=1000, value=10)
    
    # Additional trade options
    col1, col2 = st.columns(2)
    
    with col1:
        order_type = st.selectbox("Order Type", ["Market", "Limit", "Stop"])
    
    with col2:
        if order_type == "Limit":
            limit_price = st.number_input("Limit Price", min_value=0.01, value=150.00, step=0.01)
        elif order_type == "Stop":
            stop_price = st.number_input("Stop Price", min_value=0.01, value=145.00, step=0.01)
    
    # Risk management
    st.subheader("⚠️ Risk Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_position_size = st.slider("Max Position Size (%)", 1, 20, 10)
    
    with col2:
        stop_loss = st.number_input("Stop Loss (%)", min_value=0.1, max_value=20.0, value=5.0, step=0.1)
    
    # Execute trade button
    if st.button("🚀 Execute Trade", type="primary"):
        # Calculate estimated cost
        estimated_cost = trade_quantity * 150.00  # Sample price
        
        st.success(f"Trade executed: {trade_action} {trade_quantity} shares of {trade_symbol}")
        st.info(f"Estimated cost: ${estimated_cost:,.2f}")

def render_allocation_chart():
    """Render portfolio allocation chart."""
    st.subheader("📊 Portfolio Allocation")
    
    # Sample allocation data
    allocation_data = {
        "Technology": 45,
        "Healthcare": 20,
        "Finance": 15,
        "Energy": 10,
        "Consumer": 10
    }
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=list(allocation_data.keys()),
        values=list(allocation_data.values()),
        hole=0.3
    )])
    
    fig.update_layout(
        title="Portfolio Allocation by Sector",
        showlegend=True,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance by sector
    st.subheader("📈 Performance by Sector")
    
    sector_performance = {
        "Technology": 8.5,
        "Healthcare": 5.2,
        "Finance": 3.8,
        "Energy": -2.1,
        "Consumer": 4.3
    }
    
    fig_bar = go.Figure(data=[
        go.Bar(
            x=list(sector_performance.keys()),
            y=list(sector_performance.values()),
            marker_color=['green' if x > 0 else 'red' for x in sector_performance.values()]
        )
    ])
    
    fig_bar.update_layout(
        title="Sector Performance (%)",
        xaxis_title="Sector",
        yaxis_title="Performance (%)",
        height=400
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)

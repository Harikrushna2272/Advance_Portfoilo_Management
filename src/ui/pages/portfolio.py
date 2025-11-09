"""
Portfolio management page component - Enhanced with risk analytics and position management
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np


def render_portfolio_page():
    """Render the comprehensive portfolio management page."""
    st.markdown("## 💼 Portfolio Management & Risk Analytics")
    st.markdown("Advanced portfolio tracking, position management, and risk analysis")

    # Portfolio summary metrics
    render_portfolio_summary()

    st.markdown("---")

    # Two-column layout
    col1, col2 = st.columns([2, 1])

    with col1:
        render_positions_table()
        render_trade_history()

    with col2:
        render_allocation_charts()
        render_risk_metrics()

    st.markdown("---")

    # Risk analysis section
    render_risk_analysis()

    st.markdown("---")

    # Manual trade execution
    render_trade_execution()


def render_portfolio_summary():
    """Render portfolio summary metrics."""
    portfolio = st.session_state.portfolio

    total_value = portfolio.get("total_value", 100000.0)
    cash = portfolio.get("cash", 100000.0)
    initial_value = 100000.0

    # Calculate metrics
    invested = total_value - cash
    total_return = total_value - initial_value
    total_return_pct = (total_return / initial_value) * 100

    # Simulate additional metrics
    day_return = np.random.uniform(-500, 1000)
    day_return_pct = (day_return / total_value) * 100

    # Display metrics
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "💰 Total Value",
            f"${total_value:,.2f}",
            delta=f"${total_return:+,.2f}",
            help="Total portfolio value including cash and positions",
        )

    with col2:
        st.metric(
            "💵 Cash Available",
            f"${cash:,.2f}",
            delta=f"{(cash / total_value * 100):.1f}% of total",
            help="Available cash for new positions",
        )

    with col3:
        st.metric(
            "📊 Invested Amount",
            f"${invested:,.2f}",
            delta=f"{(invested / total_value * 100):.1f}% allocated",
            help="Total value of all positions",
        )

    with col4:
        delta_color = "normal" if total_return >= 0 else "inverse"
        st.metric(
            "📈 Total Return",
            f"{total_return_pct:+.2f}%",
            delta=f"${total_return:+,.2f}",
            delta_color=delta_color,
            help="Total return since inception",
        )

    with col5:
        delta_color = "normal" if day_return >= 0 else "inverse"
        st.metric(
            "📅 Today's Return",
            f"{day_return_pct:+.2f}%",
            delta=f"${day_return:+,.2f}",
            delta_color=delta_color,
            help="Return for today",
        )


def render_positions_table():
    """Render current positions table with detailed information."""
    st.markdown("### 📊 Current Positions")

    portfolio = st.session_state.portfolio
    positions = portfolio.get("positions", {})

    # If no positions, show sample data
    if not positions:
        positions = {
            "AAPL": {
                "shares": 50,
                "avg_cost": 175.50,
                "current_price": 182.50,
                "market_value": 9125.00,
                "cost_basis": 8775.00,
                "unrealized_pnl": 350.00,
                "unrealized_pnl_pct": 3.99,
                "day_change": 125.00,
                "day_change_pct": 1.39,
            },
            "TSLA": {
                "shares": 25,
                "avg_cost": 248.00,
                "current_price": 245.80,
                "market_value": 6145.00,
                "cost_basis": 6200.00,
                "unrealized_pnl": -55.00,
                "unrealized_pnl_pct": -0.89,
                "day_change": -78.50,
                "day_change_pct": -1.28,
            },
            "GOOGL": {
                "shares": 30,
                "avg_cost": 138.25,
                "current_price": 140.50,
                "market_value": 4215.00,
                "cost_basis": 4147.50,
                "unrealized_pnl": 67.50,
                "unrealized_pnl_pct": 1.63,
                "day_change": 37.50,
                "day_change_pct": 0.90,
            },
        }

    # Convert to DataFrame
    rows = []
    for symbol, pos in positions.items():
        rows.append(
            {
                "Symbol": symbol,
                "Shares": pos["shares"],
                "Avg Cost": f"${pos['avg_cost']:.2f}",
                "Current Price": f"${pos['current_price']:.2f}",
                "Market Value": f"${pos['market_value']:,.2f}",
                "Cost Basis": f"${pos['cost_basis']:,.2f}",
                "Unrealized P&L": f"${pos['unrealized_pnl']:+,.2f}",
                "P&L %": f"{pos['unrealized_pnl_pct']:+.2f}%",
                "Day Change": f"${pos['day_change']:+,.2f}",
                "Day %": f"{pos['day_change_pct']:+.2f}%",
            }
        )

    df = pd.DataFrame(rows)

    # Add totals row
    if rows:
        total_market_value = sum([pos["market_value"] for pos in positions.values()])
        total_cost_basis = sum([pos["cost_basis"] for pos in positions.values()])
        total_unrealized_pnl = sum(
            [pos["unrealized_pnl"] for pos in positions.values()]
        )
        total_unrealized_pnl_pct = (
            (total_unrealized_pnl / total_cost_basis * 100)
            if total_cost_basis > 0
            else 0
        )
        total_day_change = sum([pos["day_change"] for pos in positions.values()])
        total_day_change_pct = (
            (total_day_change / total_market_value * 100)
            if total_market_value > 0
            else 0
        )

        totals_row = {
            "Symbol": "TOTAL",
            "Shares": "-",
            "Avg Cost": "-",
            "Current Price": "-",
            "Market Value": f"${total_market_value:,.2f}",
            "Cost Basis": f"${total_cost_basis:,.2f}",
            "Unrealized P&L": f"${total_unrealized_pnl:+,.2f}",
            "P&L %": f"{total_unrealized_pnl_pct:+.2f}%",
            "Day Change": f"${total_day_change:+,.2f}",
            "Day %": f"{total_day_change_pct:+.2f}%",
        }
        df = pd.concat([df, pd.DataFrame([totals_row])], ignore_index=True)

    # Style the dataframe
    def highlight_row(row):
        if row["Symbol"] == "TOTAL":
            return ["background-color: #e9ecef; font-weight: bold"] * len(row)
        return [""] * len(row)

    styled_df = df.style.apply(highlight_row, axis=1)

    st.dataframe(styled_df, use_container_width=True, hide_index=True, height=250)

    # Position actions
    if positions:
        st.markdown("**Quick Actions:**")
        cols = st.columns(len(positions))
        for idx, symbol in enumerate(positions.keys()):
            with cols[idx]:
                if st.button(
                    f"📊 Analyze {symbol}",
                    key=f"analyze_btn_{symbol}",
                    use_container_width=True,
                ):
                    st.session_state.selected_stock = symbol
                    st.session_state.run_analysis = True
                    st.info(f"Switch to Analysis tab to view {symbol} analysis")


def render_trade_history():
    """Render trade history table."""
    st.markdown("### 📜 Recent Trade History")

    # Sample trade history
    trades = [
        {
            "timestamp": datetime.now() - timedelta(hours=2),
            "symbol": "AAPL",
            "action": "BUY",
            "quantity": 50,
            "price": 175.50,
            "total": 8775.00,
            "status": "Filled",
        },
        {
            "timestamp": datetime.now() - timedelta(hours=5),
            "symbol": "TSLA",
            "action": "BUY",
            "quantity": 25,
            "price": 248.00,
            "total": 6200.00,
            "status": "Filled",
        },
        {
            "timestamp": datetime.now() - timedelta(days=1),
            "symbol": "GOOGL",
            "action": "BUY",
            "quantity": 30,
            "price": 138.25,
            "total": 4147.50,
            "status": "Filled",
        },
        {
            "timestamp": datetime.now() - timedelta(days=2),
            "symbol": "MSFT",
            "action": "SELL",
            "quantity": 20,
            "price": 415.00,
            "total": 8300.00,
            "status": "Filled",
        },
        {
            "timestamp": datetime.now() - timedelta(days=3),
            "symbol": "AMZN",
            "action": "BUY",
            "quantity": 15,
            "price": 178.50,
            "total": 2677.50,
            "status": "Cancelled",
        },
    ]

    # Convert to DataFrame
    df = pd.DataFrame(trades)
    df["Time"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
    df["Symbol"] = df["symbol"]
    df["Action"] = df["action"]
    df["Qty"] = df["quantity"]
    df["Price"] = df["price"].apply(lambda x: f"${x:.2f}")
    df["Total"] = df["total"].apply(lambda x: f"${x:,.2f}")
    df["Status"] = df["status"]

    display_df = df[["Time", "Symbol", "Action", "Qty", "Price", "Total", "Status"]]

    # Style based on action
    def highlight_action(row):
        if row["Action"] == "BUY":
            return ["background-color: #d4edda"] * len(row)
        elif row["Action"] == "SELL":
            return ["background-color: #f8d7da"] * len(row)
        return [""] * len(row)

    styled_df = display_df.style.apply(highlight_action, axis=1)

    st.dataframe(styled_df, use_container_width=True, hide_index=True, height=250)


def render_allocation_charts():
    """Render portfolio allocation visualizations."""
    st.markdown("### 🥧 Portfolio Allocation")

    portfolio = st.session_state.portfolio
    positions = portfolio.get("positions", {})
    cash = portfolio.get("cash", 100000.0)

    # Prepare data
    labels = ["Cash"]
    values = [cash]
    colors = ["#28a745"]

    # Add positions
    stock_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    for idx, (symbol, pos) in enumerate(positions.items()):
        labels.append(symbol)
        values.append(pos.get("market_value", 0))
        colors.append(stock_colors[idx % len(stock_colors)])

    # If no data, use sample
    if sum(values) == 0 or len(values) == 1:
        labels = ["Cash", "AAPL", "TSLA", "GOOGL"]
        values = [80515.00, 9125.00, 6145.00, 4215.00]
        colors = ["#28a745", "#1f77b4", "#ff7f0e", "#2ca02c"]

    # Create donut chart
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.5,
                marker=dict(colors=colors),
                textinfo="label+percent",
                textposition="auto",
                hovertemplate="<b>%{label}</b><br>Value: $%{value:,.2f}<br>%{percent}<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title="Current Allocation",
        height=300,
        showlegend=True,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=30, b=0),
    )

    st.plotly_chart(fig, use_container_width=True)

    # Sector allocation
    st.markdown("### 🏭 Sector Allocation")

    sectors = {"Technology": 65, "Consumer": 20, "Other": 15}

    fig_sector = go.Figure(
        data=[
            go.Pie(
                labels=list(sectors.keys()),
                values=list(sectors.values()),
                hole=0.4,
                marker=dict(colors=["#1f77b4", "#ff7f0e", "#2ca02c"]),
                textinfo="label+percent",
            )
        ]
    )

    fig_sector.update_layout(
        title="Sector Distribution",
        height=250,
        showlegend=True,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=30, b=0),
    )

    st.plotly_chart(fig_sector, use_container_width=True)


def render_risk_metrics():
    """Render risk metrics panel."""
    st.markdown("### ⚠️ Risk Metrics")

    # Calculate or simulate risk metrics
    total_value = st.session_state.portfolio.get("total_value", 100000.0)
    positions = st.session_state.portfolio.get("positions", {})

    # Portfolio concentration
    if positions:
        largest_position = max(
            [pos.get("market_value", 0) for pos in positions.values()]
        )
        concentration = (largest_position / total_value) * 100
    else:
        concentration = 9.1

    # Display metrics
    st.metric(
        "📊 Largest Position",
        f"{concentration:.1f}%",
        delta="Within 20% limit" if concentration < 20 else "Exceeds limit",
        delta_color="normal" if concentration < 20 else "inverse",
        help="Percentage of portfolio in largest single position",
    )

    st.metric(
        "📉 Max Drawdown",
        "-3.2%",
        delta="Low risk",
        help="Maximum observed loss from peak",
    )

    st.metric(
        "📊 Beta",
        "1.15",
        delta="+0.15 vs market",
        help="Portfolio volatility vs market",
    )

    st.metric(
        "⚡ Sharpe Ratio", "1.23", delta="Good", help="Risk-adjusted return metric"
    )

    st.metric(
        "🎯 Win Rate", "73.2%", delta="+23.2%", help="Percentage of profitable trades"
    )

    st.markdown("---")

    # Risk level indicator
    risk_score = 35  # Low risk

    if risk_score < 40:
        risk_level = "LOW"
        risk_color = "#28a745"
    elif risk_score < 70:
        risk_level = "MODERATE"
        risk_color = "#ffc107"
    else:
        risk_level = "HIGH"
        risk_color = "#dc3545"

    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, {risk_color}22 0%, {risk_color}11 100%);
                    padding: 1rem; border-radius: 12px; border-left: 5px solid {risk_color}; text-align: center;">
            <h4 style="margin: 0; color: {risk_color};">Risk Level: {risk_level}</h4>
            <p style="margin: 0.5rem 0 0 0;">Score: {risk_score}/100</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.progress(risk_score / 100)


def render_risk_analysis():
    """Render comprehensive risk analysis."""
    st.markdown("### 📊 Risk Analysis Dashboard")

    tab1, tab2, tab3 = st.tabs(
        ["Position Risk", "Portfolio Correlation", "Stress Testing"]
    )

    with tab1:
        render_position_risk()

    with tab2:
        render_correlation_matrix()

    with tab3:
        render_stress_tests()


def render_position_risk():
    """Render position-level risk analysis."""
    st.markdown("#### Position Risk Breakdown")

    # Sample position risk data
    risk_data = {
        "Symbol": ["AAPL", "TSLA", "GOOGL"],
        "Position Size": ["$9,125", "$6,145", "$4,215"],
        "% of Portfolio": ["9.1%", "6.1%", "4.2%"],
        "Volatility (30d)": ["22%", "45%", "28%"],
        "Beta": ["1.2", "1.8", "1.1"],
        "VaR (95%)": ["-$182", "-$276", "-$118"],
        "Risk Score": [35, 68, 42],
    }

    df = pd.DataFrame(risk_data)

    st.dataframe(df, use_container_width=True, hide_index=True)

    # Risk score visualization
    fig = go.Figure(
        data=[
            go.Bar(
                x=risk_data["Symbol"],
                y=risk_data["Risk Score"],
                marker_color=["#28a745", "#ffc107", "#ff7f0e"],
                text=risk_data["Risk Score"],
                textposition="auto",
            )
        ]
    )

    fig.add_hline(
        y=50,
        line_dash="dash",
        line_color="orange",
        annotation_text="Moderate Risk Threshold",
    )
    fig.add_hline(
        y=70, line_dash="dash", line_color="red", annotation_text="High Risk Threshold"
    )

    fig.update_layout(
        title="Position Risk Scores",
        xaxis_title="Symbol",
        yaxis_title="Risk Score",
        height=350,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)


def render_correlation_matrix():
    """Render correlation matrix."""
    st.markdown("#### Portfolio Correlation Matrix")

    # Sample correlation data
    symbols = ["AAPL", "TSLA", "GOOGL"]
    correlation_matrix = np.array(
        [[1.00, 0.65, 0.75], [0.65, 1.00, 0.58], [0.75, 0.58, 1.00]]
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=correlation_matrix,
            x=symbols,
            y=symbols,
            colorscale="RdYlGn",
            zmid=0,
            text=correlation_matrix,
            texttemplate="%{text:.2f}",
            textfont={"size": 14},
            colorbar=dict(title="Correlation"),
        )
    )

    fig.update_layout(
        title="Asset Correlation Heatmap",
        height=400,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "💡 **Insight**: Diversification score: 72/100 - Portfolio shows moderate diversification"
    )


def render_stress_tests():
    """Render stress test scenarios."""
    st.markdown("#### Stress Test Scenarios")

    scenarios = {
        "Scenario": [
            "Market Crash (-20%)",
            "Tech Selloff (-30%)",
            "Volatility Spike (+50%)",
            "Interest Rate Hike",
            "Black Swan Event",
        ],
        "Impact on Portfolio": [
            "-$20,000 (-20%)",
            "-$18,500 (-18.5%)",
            "-$12,000 (-12%)",
            "-$8,500 (-8.5%)",
            "-$35,000 (-35%)",
        ],
        "Probability": ["5%", "10%", "15%", "20%", "1%"],
        "Recovery Time": [
            "6-12 months",
            "4-8 months",
            "2-4 months",
            "3-6 months",
            "12+ months",
        ],
    }

    df = pd.DataFrame(scenarios)

    st.dataframe(df, use_container_width=True, hide_index=True)

    # Visualize scenario impacts
    impacts = [-20000, -18500, -12000, -8500, -35000]

    fig = go.Figure(
        data=[
            go.Bar(
                x=scenarios["Scenario"],
                y=impacts,
                marker_color=["#dc3545" if x < -15000 else "#ffc107" for x in impacts],
                text=[f"${x:,}" for x in impacts],
                textposition="auto",
            )
        ]
    )

    fig.update_layout(
        title="Stress Test Impact Analysis",
        xaxis_title="Scenario",
        yaxis_title="Portfolio Impact ($)",
        height=350,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)


def render_trade_execution():
    """Render manual trade execution interface."""
    st.markdown("### 💼 Manual Trade Execution")

    with st.expander("🔧 Execute Manual Trade", expanded=False):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            trade_symbol = st.selectbox(
                "Symbol",
                options=st.session_state.settings.get(
                    "stock_list", ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN"]
                ),
            )

        with col2:
            trade_action = st.selectbox("Action", ["BUY", "SELL"])

        with col3:
            trade_quantity = st.number_input(
                "Quantity", min_value=1, max_value=1000, value=10, step=1
            )

        with col4:
            order_type = st.selectbox("Order Type", ["Market", "Limit", "Stop"])

        # Additional parameters
        col1, col2 = st.columns(2)

        with col1:
            if order_type == "Limit":
                limit_price = st.number_input(
                    "Limit Price ($)", min_value=0.01, value=100.00, step=0.01
                )
            elif order_type == "Stop":
                stop_price = st.number_input(
                    "Stop Price ($)", min_value=0.01, value=95.00, step=0.01
                )

        with col2:
            time_in_force = st.selectbox("Time in Force", ["DAY", "GTC", "IOC", "FOK"])

        # Risk controls
        st.markdown("**⚠️ Risk Controls:**")
        col1, col2, col3 = st.columns(3)

        with col1:
            enable_stop_loss = st.checkbox("Enable Stop Loss", value=True)
            if enable_stop_loss:
                stop_loss_pct = st.slider("Stop Loss %", 1, 20, 5)

        with col2:
            enable_take_profit = st.checkbox("Enable Take Profit", value=False)
            if enable_take_profit:
                take_profit_pct = st.slider("Take Profit %", 1, 50, 10)

        with col3:
            position_limit_check = st.checkbox("Check Position Limit", value=True)
            if position_limit_check:
                st.info("20% limit will be enforced")

        # Execution summary
        st.markdown("---")
        st.markdown("**📋 Order Summary:**")

        estimated_price = 182.50  # Sample price
        estimated_cost = trade_quantity * estimated_price
        estimated_fee = estimated_cost * 0.001  # 0.1% fee
        total_cost = estimated_cost + estimated_fee

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Estimated Price", f"${estimated_price:.2f}")
        with col2:
            st.metric("Estimated Cost", f"${estimated_cost:,.2f}")
        with col3:
            st.metric("Estimated Fee", f"${estimated_fee:.2f}")
        with col4:
            st.metric("Total", f"${total_cost:,.2f}")

        # Execute button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button(
                f"🚀 Execute {trade_action} Order",
                key="execute_manual_trade_button",
                type="primary",
                use_container_width=True,
            ):
                with st.spinner("Executing trade..."):
                    import time

                    time.sleep(1)
                st.success(
                    f"✅ Successfully executed {trade_action} {trade_quantity} shares of {trade_symbol}!"
                )
                st.balloons()

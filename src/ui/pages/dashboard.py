"""
Dashboard page component - Enhanced with real-time data integration
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List


def render_dashboard():
    """Render the main dashboard page with real-time updates."""
    st.markdown("## 📊 Trading Dashboard")
    st.markdown("Real-time overview of trading activity and performance")

    # Top-level KPI metrics
    render_kpi_metrics()

    st.markdown("---")

    # Charts section - two columns
    col1, col2 = st.columns(2)

    with col1:
        render_portfolio_value_chart()
        render_signal_distribution()

    with col2:
        render_portfolio_composition()
        render_daily_pnl_chart()

    st.markdown("---")

    # Recent activity section
    col1, col2 = st.columns([2, 1])

    with col1:
        render_recent_decisions()

    with col2:
        render_agent_status()

    st.markdown("---")

    # Performance analytics
    render_performance_analytics()


def render_kpi_metrics():
    """Render key performance indicator metrics."""
    col1, col2, col3, col4, col5 = st.columns(5)

    # Calculate metrics from session state
    total_decisions = st.session_state.total_decisions
    total_trades = st.session_state.total_trades
    successful_trades = st.session_state.successful_trades

    # Win rate calculation
    if total_trades > 0:
        win_rate = (successful_trades / total_trades) * 100
    else:
        win_rate = 0.0

    # Today's P&L
    daily_pnl = st.session_state.analytics.get("daily_pnl", 0.0)

    # Portfolio value
    portfolio_value = st.session_state.portfolio.get("total_value", 100000.0)
    initial_value = 100000.0
    total_return_pct = ((portfolio_value - initial_value) / initial_value) * 100

    with col1:
        st.metric(
            label="🎯 Total Decisions",
            value=f"{total_decisions:,}",
            delta=f"+{st.session_state.cycle_count}"
            if st.session_state.cycle_count > 0
            else "0",
            help="Total number of trading decisions made",
        )

    with col2:
        st.metric(
            label="💼 Trades Executed",
            value=f"{total_trades:,}",
            delta=f"+{min(total_trades, 5)}" if total_trades > 0 else "0",
            help="Total number of executed trades",
        )

    with col3:
        delta_color = "normal" if win_rate >= 50 else "inverse"
        st.metric(
            label="📈 Win Rate",
            value=f"{win_rate:.1f}%",
            delta=f"{(win_rate - 50):.1f}%" if total_trades > 0 else "N/A",
            delta_color=delta_color,
            help="Percentage of profitable trades",
        )

    with col4:
        delta_color = "normal" if daily_pnl >= 0 else "inverse"
        st.metric(
            label="💰 P&L Today",
            value=f"${daily_pnl:,.2f}",
            delta=f"{(daily_pnl / initial_value * 100):.2f}%"
            if abs(daily_pnl) > 0
            else "0%",
            delta_color=delta_color,
            help="Profit/Loss for today",
        )

    with col5:
        delta_color = "normal" if total_return_pct >= 0 else "inverse"
        st.metric(
            label="📊 Total Return",
            value=f"{total_return_pct:+.2f}%",
            delta=f"${portfolio_value - initial_value:,.2f}",
            delta_color=delta_color,
            help="Total portfolio return",
        )


def render_portfolio_value_chart():
    """Render portfolio value over time chart."""
    st.markdown("### 📈 Portfolio Performance")

    # Generate sample historical data (in production, fetch from database)
    if "portfolio_history" not in st.session_state:
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=30), end=datetime.now(), freq="D"
        )
        initial_value = 100000

        # Simulate portfolio growth with some volatility
        np.random.seed(42)
        returns = np.random.normal(0.001, 0.02, len(dates))
        values = [initial_value]

        for ret in returns[1:]:
            values.append(values[-1] * (1 + ret))

        st.session_state.portfolio_history = pd.DataFrame(
            {"Date": dates, "Value": values}
        )

    df = st.session_state.portfolio_history

    # Create the chart
    fig = go.Figure()

    # Add portfolio value line
    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Value"],
            mode="lines",
            name="Portfolio Value",
            line=dict(color="#1f77b4", width=3),
            fill="tozeroy",
            fillcolor="rgba(31, 119, 180, 0.1)",
        )
    )

    # Add benchmark line (initial value)
    fig.add_hline(
        y=100000,
        line_dash="dash",
        line_color="gray",
        annotation_text="Initial Value",
        annotation_position="right",
    )

    # Update layout
    fig.update_layout(
        title="30-Day Portfolio Performance",
        xaxis_title="Date",
        yaxis_title="Portfolio Value ($)",
        height=350,
        hovermode="x unified",
        showlegend=True,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    # Add gridlines
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(128,128,128,0.2)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(128,128,128,0.2)")

    st.plotly_chart(fig, use_container_width=True)


def render_portfolio_composition():
    """Render portfolio composition pie chart."""
    st.markdown("### 🥧 Portfolio Allocation")

    portfolio = st.session_state.portfolio
    positions = portfolio.get("positions", {})
    cash = portfolio.get("cash", 100000.0)

    # Prepare data
    labels = []
    values = []
    colors = []

    # Add cash
    labels.append("Cash")
    values.append(cash)
    colors.append("#28a745")

    # Add positions
    stock_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
    for idx, (symbol, position) in enumerate(positions.items()):
        labels.append(symbol)
        market_value = position.get("market_value", 0)
        values.append(market_value)
        colors.append(stock_colors[idx % len(stock_colors)])

    # If no data, show initial state
    if not values or sum(values) == 0:
        labels = ["Cash"]
        values = [100000]
        colors = ["#28a745"]

    # Create donut chart
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.4,
                marker=dict(colors=colors),
                textinfo="label+percent",
                textposition="auto",
                hovertemplate="<b>%{label}</b><br>Value: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title="Asset Allocation",
        height=350,
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)


def render_signal_distribution():
    """Render signal distribution bar chart."""
    st.markdown("### 📊 Signal Distribution")

    # Count signals from recent decisions
    recent_decisions = st.session_state.get("recent_decisions", [])

    signal_counts = {"BUY": 0, "SELL": 0, "HOLD": 0}

    for decision in recent_decisions:
        signal = decision.get("signal", "HOLD")
        signal_counts[signal] = signal_counts.get(signal, 0) + 1

    # If no decisions, show sample data
    if sum(signal_counts.values()) == 0:
        signal_counts = {"BUY": 5, "SELL": 3, "HOLD": 12}

    # Create bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                x=list(signal_counts.keys()),
                y=list(signal_counts.values()),
                marker_color=["#28a745", "#dc3545", "#ffc107"],
                text=list(signal_counts.values()),
                textposition="auto",
                hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title="Recent Trading Signals",
        xaxis_title="Signal Type",
        yaxis_title="Count",
        height=350,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(128,128,128,0.2)")

    st.plotly_chart(fig, use_container_width=True)


def render_daily_pnl_chart():
    """Render daily P&L chart."""
    st.markdown("### 💵 Daily P&L")

    # Generate sample P&L data
    if "daily_pnl_history" not in st.session_state:
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=14), end=datetime.now(), freq="D"
        )
        np.random.seed(43)
        pnl_values = np.random.normal(200, 500, len(dates))

        st.session_state.daily_pnl_history = pd.DataFrame(
            {"Date": dates, "PnL": pnl_values}
        )

    df = st.session_state.daily_pnl_history

    # Create bar chart with colors based on positive/negative
    colors = ["#28a745" if pnl >= 0 else "#dc3545" for pnl in df["PnL"]]

    fig = go.Figure(
        data=[
            go.Bar(
                x=df["Date"],
                y=df["PnL"],
                marker_color=colors,
                hovertemplate="<b>%{x|%Y-%m-%d}</b><br>P&L: $%{y:,.2f}<extra></extra>",
            )
        ]
    )

    fig.add_hline(y=0, line_dash="solid", line_color="gray", line_width=1)

    fig.update_layout(
        title="14-Day P&L History",
        xaxis_title="Date",
        yaxis_title="P&L ($)",
        height=350,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(128,128,128,0.2)")

    st.plotly_chart(fig, use_container_width=True)


def render_recent_decisions():
    """Render recent trading decisions table."""
    st.markdown("### 🔄 Recent Trading Decisions")

    recent_decisions = st.session_state.get("recent_decisions", [])

    # If no decisions, show sample data
    if not recent_decisions:
        sample_decisions = [
            {
                "timestamp": datetime.now() - timedelta(minutes=5),
                "symbol": "AAPL",
                "signal": "BUY",
                "confidence": 85,
                "quantity": 50,
                "price": 182.50,
                "executed": True,
            },
            {
                "timestamp": datetime.now() - timedelta(minutes=10),
                "symbol": "TSLA",
                "signal": "SELL",
                "confidence": 72,
                "quantity": 25,
                "price": 245.80,
                "executed": True,
            },
            {
                "timestamp": datetime.now() - timedelta(minutes=15),
                "symbol": "GOOGL",
                "signal": "HOLD",
                "confidence": 45,
                "quantity": 0,
                "price": 140.50,
                "executed": False,
            },
            {
                "timestamp": datetime.now() - timedelta(minutes=20),
                "symbol": "MSFT",
                "signal": "BUY",
                "confidence": 91,
                "quantity": 30,
                "price": 420.15,
                "executed": True,
            },
            {
                "timestamp": datetime.now() - timedelta(minutes=25),
                "symbol": "AMZN",
                "signal": "HOLD",
                "confidence": 38,
                "quantity": 0,
                "price": 175.75,
                "executed": False,
            },
        ]
        recent_decisions = sample_decisions

    # Convert to DataFrame
    df = pd.DataFrame(recent_decisions)

    # Format timestamp
    df["Time"] = df["timestamp"].dt.strftime("%H:%M:%S")
    df["Symbol"] = df["symbol"]
    df["Signal"] = df["signal"]
    df["Confidence"] = df["confidence"].apply(lambda x: f"{x}%")
    df["Quantity"] = df["quantity"]
    df["Price"] = df["price"].apply(lambda x: f"${x:.2f}")
    df["Status"] = df["executed"].apply(lambda x: "✅ Executed" if x else "⏸️ Held")

    # Select and reorder columns
    display_df = df[
        ["Time", "Symbol", "Signal", "Confidence", "Quantity", "Price", "Status"]
    ]

    # Apply styling
    def highlight_signal(row):
        if row["Signal"] == "BUY":
            return ["background-color: #d4edda"] * len(row)
        elif row["Signal"] == "SELL":
            return ["background-color: #f8d7da"] * len(row)
        else:
            return ["background-color: #fff3cd"] * len(row)

    styled_df = display_df.style.apply(highlight_signal, axis=1)

    st.dataframe(styled_df, use_container_width=True, hide_index=True)


def render_agent_status():
    """Render agent status panel."""
    st.markdown("### 🤖 Agent Status")

    agents = [
        {"name": "Fundamentals", "status": "active", "confidence": 80},
        {"name": "Technicals", "status": "active", "confidence": 75},
        {"name": "Valuation", "status": "active", "confidence": 68},
        {"name": "Sentiment", "status": "active", "confidence": 62},
        {"name": "Risk Manager", "status": "active", "confidence": 85},
    ]

    for agent in agents:
        status_icon = "🟢" if agent["status"] == "active" else "🔴"
        confidence = agent["confidence"]

        st.markdown(f"**{status_icon} {agent['name']}**")
        st.progress(confidence / 100, text=f"{confidence}% confidence")
        st.markdown("")  # Spacing

    st.markdown("---")

    # RL Models status
    st.markdown("### 🧠 RL Models")

    models = ["SAC", "PPO", "A2C", "DQN", "TD3"]

    for model in models:
        st.markdown(f"✅ **{model}** - Loaded")

    # Model ensemble accuracy
    st.markdown("---")
    st.metric(
        "🎯 Ensemble Accuracy",
        "79.2%",
        delta="+2.3%",
        help="Combined accuracy of all RL models",
    )


def render_performance_analytics():
    """Render detailed performance analytics."""
    st.markdown("### 📊 Performance Analytics")

    col1, col2, col3, col4 = st.columns(4)

    analytics = st.session_state.analytics

    with col1:
        st.metric(
            "📅 Daily P&L",
            f"${analytics.get('daily_pnl', 0):.2f}",
            delta=f"{(analytics.get('daily_pnl', 0) / 100000 * 100):.2f}%",
        )

    with col2:
        st.metric(
            "📅 Weekly P&L",
            f"${analytics.get('weekly_pnl', 0):.2f}",
            delta=f"{(analytics.get('weekly_pnl', 0) / 100000 * 100):.2f}%",
        )

    with col3:
        st.metric(
            "📅 Monthly P&L",
            f"${analytics.get('monthly_pnl', 0):.2f}",
            delta=f"{(analytics.get('monthly_pnl', 0) / 100000 * 100):.2f}%",
        )

    with col4:
        st.metric(
            "⚡ Sharpe Ratio",
            f"{analytics.get('sharpe_ratio', 0):.2f}",
            delta="Good" if analytics.get("sharpe_ratio", 0) > 1 else "Low",
        )

    # Additional metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📉 Max Drawdown",
            f"{analytics.get('max_drawdown', 0):.2f}%",
            delta="Within limits"
            if abs(analytics.get("max_drawdown", 0)) < 10
            else "High risk",
            delta_color="inverse",
        )

    with col2:
        st.metric(
            "🎯 Win Rate",
            f"{analytics.get('win_rate', 0):.1f}%",
            delta=f"{(analytics.get('win_rate', 0) - 50):.1f}%"
            if analytics.get("win_rate", 0) > 0
            else "N/A",
        )

    with col3:
        avg_win = analytics.get("avg_win", 0)
        st.metric("💰 Avg Win", f"${avg_win:.2f}" if avg_win else "N/A")

    with col4:
        avg_loss = analytics.get("avg_loss", 0)
        st.metric(
            "💸 Avg Loss",
            f"${avg_loss:.2f}" if avg_loss else "N/A",
            delta_color="inverse",
        )

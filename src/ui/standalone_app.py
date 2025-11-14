"""
StockAI - STANDALONE Trading System UI
100% Self-Contained - NO external file dependencies
Everything works in-memory with session state only
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import time

# Configure page
st.set_page_config(
    page_title="StockAI - Trading System",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================== DUMMY DATA & HELPERS ====================

DUMMY_PRICES = {
    "AAPL": 182.50,
    "TSLA": 245.80,
    "GOOGL": 140.50,
    "MSFT": 420.15,
    "AMZN": 175.75,
    "NVDA": 495.50,
    "META": 485.30,
    "NFLX": 625.40,
    "AMD": 155.20,
    "INTC": 42.80,
}


def get_price(symbol):
    """Get dummy price for a symbol."""
    return DUMMY_PRICES.get(symbol, 100.0)


# ==================== SESSION STATE INITIALIZATION ====================


def init_session_state():
    """Initialize all session state variables."""
    if "initialized" not in st.session_state:
        # Portfolio
        st.session_state.cash = 100000.0
        st.session_state.positions = {}  # {symbol: {'shares': X, 'avg_cost': Y}}
        st.session_state.trade_history = []

        # Stats
        st.session_state.total_trades = 0
        st.session_state.total_value = 100000.0

        # System
        st.session_state.trading_active = False
        st.session_state.auto_refresh = True
        st.session_state.last_update = datetime.now()

        st.session_state.initialized = True


# ==================== TRADING FUNCTIONS ====================


def execute_trade(symbol, action, quantity):
    """Execute a trade and update portfolio."""
    price = get_price(symbol)

    if action == "BUY":
        cost = quantity * price
        if st.session_state.cash >= cost:
            st.session_state.cash -= cost

            if symbol in st.session_state.positions:
                pos = st.session_state.positions[symbol]
                old_shares = pos["shares"]
                old_cost = pos["avg_cost"]
                new_shares = old_shares + quantity
                new_avg_cost = ((old_shares * old_cost) + cost) / new_shares

                st.session_state.positions[symbol] = {
                    "shares": new_shares,
                    "avg_cost": new_avg_cost,
                }
            else:
                st.session_state.positions[symbol] = {
                    "shares": quantity,
                    "avg_cost": price,
                }

            # Add to history
            st.session_state.trade_history.insert(
                0,
                {
                    "timestamp": datetime.now(),
                    "symbol": symbol,
                    "action": "BUY",
                    "quantity": quantity,
                    "price": price,
                    "total": cost,
                },
            )

            st.session_state.total_trades += 1
            update_total_value()
            return True, f"✅ Bought {quantity} {symbol} @ ${price:.2f} = ${cost:,.2f}"
        else:
            return (
                False,
                f"❌ Insufficient cash. Need ${cost:,.2f}, have ${st.session_state.cash:,.2f}",
            )

    elif action == "SELL":
        if symbol in st.session_state.positions:
            pos = st.session_state.positions[symbol]
            if pos["shares"] >= quantity:
                proceeds = quantity * price
                st.session_state.cash += proceeds

                pos["shares"] -= quantity
                if pos["shares"] == 0:
                    del st.session_state.positions[symbol]

                # Add to history
                st.session_state.trade_history.insert(
                    0,
                    {
                        "timestamp": datetime.now(),
                        "symbol": symbol,
                        "action": "SELL",
                        "quantity": quantity,
                        "price": price,
                        "total": proceeds,
                    },
                )

                st.session_state.total_trades += 1
                update_total_value()
                return (
                    True,
                    f"✅ Sold {quantity} {symbol} @ ${price:.2f} = ${proceeds:,.2f}",
                )
            else:
                return (
                    False,
                    f"❌ Not enough shares. Have {pos['shares']}, trying to sell {quantity}",
                )
        else:
            return False, f"❌ No position in {symbol}"


def update_total_value():
    """Calculate total portfolio value."""
    positions_value = sum(
        pos["shares"] * get_price(symbol)
        for symbol, pos in st.session_state.positions.items()
    )
    st.session_state.total_value = st.session_state.cash + positions_value


# ==================== UI COMPONENTS ====================


def render_header():
    """Render header."""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(
            '<h1 style="text-align: center;">📈 StockAI Trading System</h1>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="text-align: center; color: #666;">Simple, Dynamic, Self-Contained</p>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Stats bar
    col1, col2, col3, col4 = st.columns(4)

    total_return = st.session_state.total_value - 100000
    total_return_pct = (total_return / 100000) * 100

    with col1:
        status = "🟢 ACTIVE" if st.session_state.trading_active else "🟡 STANDBY"
        st.markdown(
            f'<div style="text-align: center; padding: 10px; background: #f0f2f6; border-radius: 5px;"><b>{status}</b></div>',
            unsafe_allow_html=True,
        )

    with col2:
        st.metric(
            "💰 Total Value",
            f"${st.session_state.total_value:,.2f}",
            f"{total_return_pct:+.2f}%",
        )

    with col3:
        st.metric("💵 Cash", f"${st.session_state.cash:,.2f}")

    with col4:
        st.metric("📊 Positions", len(st.session_state.positions))


def render_sidebar():
    """Render sidebar controls."""
    with st.sidebar:
        st.title("🎛️ Control Panel")

        st.markdown("### 🚀 Trading Controls")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Start", type="primary", use_container_width=True):
                st.session_state.trading_active = True
                st.success("✅ Started!")
                st.rerun()

        with col2:
            if st.button("⏹️ Stop", use_container_width=True):
                st.session_state.trading_active = False
                st.warning("⏸️ Stopped!")
                st.rerun()

        if st.button("🔄 Reset All", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("Reset!")
            st.rerun()

        st.markdown("---")

        # Portfolio summary
        st.markdown("### 💼 Portfolio Summary")

        total_return = st.session_state.total_value - 100000
        total_return_pct = (total_return / 100000) * 100

        st.metric(
            "Total Value",
            f"${st.session_state.total_value:,.2f}",
            f"{total_return_pct:+.2f}%",
        )
        st.metric("Cash", f"${st.session_state.cash:,.2f}")
        st.metric("Positions", len(st.session_state.positions))
        st.metric("Total Trades", st.session_state.total_trades)

        # Allocation
        if st.session_state.positions:
            invested = st.session_state.total_value - st.session_state.cash
            invested_pct = (invested / st.session_state.total_value) * 100
            st.progress(invested_pct / 100, text=f"Invested: {invested_pct:.1f}%")

        st.markdown("---")
        st.caption(f"Last updated: {st.session_state.last_update.strftime('%H:%M:%S')}")


def render_positions_table():
    """Render current positions."""
    st.markdown("### 📊 Current Positions")

    if not st.session_state.positions:
        st.info(
            "💡 No positions currently held. Execute a BUY trade below to open a position."
        )
        return

    rows = []
    for symbol, pos in st.session_state.positions.items():
        current_price = get_price(symbol)
        market_value = pos["shares"] * current_price
        cost_basis = pos["shares"] * pos["avg_cost"]
        pnl = market_value - cost_basis
        pnl_pct = (pnl / cost_basis) * 100 if cost_basis > 0 else 0

        rows.append(
            {
                "Symbol": symbol,
                "Shares": pos["shares"],
                "Avg Cost": f"${pos['avg_cost']:.2f}",
                "Current Price": f"${current_price:.2f}",
                "Market Value": f"${market_value:,.2f}",
                "Cost Basis": f"${cost_basis:,.2f}",
                "P&L": f"${pnl:+,.2f}",
                "P&L %": f"{pnl_pct:+.2f}%",
            }
        )

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_trade_history():
    """Render trade history."""
    st.markdown("### 📜 Trade History")

    if not st.session_state.trade_history:
        st.info("💡 No trades yet. Execute trades below to see them here.")
        return

    df = pd.DataFrame(st.session_state.trade_history[:20])
    df["Time"] = df["timestamp"].dt.strftime("%H:%M:%S")
    df["Symbol"] = df["symbol"]
    df["Action"] = df["action"]
    df["Qty"] = df["quantity"]
    df["Price"] = df["price"].apply(lambda x: f"${x:.2f}")
    df["Total"] = df["total"].apply(lambda x: f"${x:,.2f}")

    display_df = df[["Time", "Symbol", "Action", "Qty", "Price", "Total"]]
    st.dataframe(display_df, use_container_width=True, hide_index=True)


def render_allocation_chart():
    """Render portfolio allocation pie chart."""
    st.markdown("### 🥧 Portfolio Allocation")

    labels = []
    values = []
    colors = []

    # Cash
    if st.session_state.cash > 0:
        labels.append("Cash")
        values.append(st.session_state.cash)
        colors.append("#28a745")

    # Positions
    stock_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
    for idx, (symbol, pos) in enumerate(st.session_state.positions.items()):
        market_value = pos["shares"] * get_price(symbol)
        labels.append(symbol)
        values.append(market_value)
        colors.append(stock_colors[idx % len(stock_colors)])

    if not values:
        st.info("💡 No data to display yet.")
        return

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.4,
                marker=dict(colors=colors),
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>$%{value:,.2f}<br>%{percent}<extra></extra>",
            )
        ]
    )

    fig.update_layout(height=350, showlegend=True, margin=dict(l=0, r=0, t=30, b=0))

    st.plotly_chart(fig, use_container_width=True)


def render_manual_trading():
    """Render manual trading interface."""
    st.markdown("### 💼 Manual Trading")

    with st.expander("🔧 Execute Trade", expanded=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            symbol = st.selectbox("Symbol", options=list(DUMMY_PRICES.keys()))

        with col2:
            action = st.selectbox("Action", ["BUY", "SELL"])

        with col3:
            quantity = st.number_input(
                "Quantity", min_value=1, max_value=1000, value=10, step=1
            )

        # Show estimate
        price = get_price(symbol)
        total = quantity * price

        st.markdown("**📋 Order Summary:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Price", f"${price:.2f}")
        with col2:
            st.metric("Total", f"${total:,.2f}")
        with col3:
            if action == "BUY":
                st.metric("Cash After", f"${st.session_state.cash - total:,.2f}")
            else:
                st.metric("Cash After", f"${st.session_state.cash + total:,.2f}")

        # Execute button
        if st.button(f"🚀 Execute {action}", type="primary", use_container_width=True):
            success, message = execute_trade(symbol, action, quantity)
            if success:
                st.success(message)
                st.balloons()
                time.sleep(0.5)
                st.rerun()
            else:
                st.error(message)


# ==================== MAIN APP ====================


def main():
    """Main app."""
    # Initialize
    init_session_state()

    # Update timestamp
    st.session_state.last_update = datetime.now()

    # Render
    render_header()
    render_sidebar()

    # Main content tabs
    tab1, tab2 = st.tabs(["📊 Portfolio", "📈 Trading"])

    with tab1:
        col1, col2 = st.columns([2, 1])

        with col1:
            render_positions_table()
            st.markdown("---")
            render_trade_history()

        with col2:
            render_allocation_chart()

    with tab2:
        render_manual_trading()

        st.markdown("---")

        # Quick trade buttons
        st.markdown("### ⚡ Quick Trades")

        cols = st.columns(5)
        for idx, symbol in enumerate(["AAPL", "TSLA", "GOOGL", "MSFT", "NVDA"]):
            with cols[idx]:
                if st.button(
                    f"📈 BUY 10\n{symbol}",
                    key=f"buy_{symbol}",
                    use_container_width=True,
                ):
                    success, message = execute_trade(symbol, "BUY", 10)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

        cols = st.columns(5)
        for idx, symbol in enumerate(["AAPL", "TSLA", "GOOGL", "MSFT", "NVDA"]):
            with cols[idx]:
                if st.button(
                    f"📉 SELL 5\n{symbol}",
                    key=f"sell_{symbol}",
                    use_container_width=True,
                ):
                    success, message = execute_trade(symbol, "SELL", 5)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)


if __name__ == "__main__":
    main()

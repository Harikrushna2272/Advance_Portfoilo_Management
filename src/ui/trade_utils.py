"""
Trade utility functions - shared between pages
No streamlit imports here to avoid set_page_config conflicts
"""

from datetime import datetime

# Dummy prices for realistic feel
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


def get_stock_price(symbol):
    """Get price for a symbol with realistic fluctuation."""
    import random

    base_price = DUMMY_PRICES.get(symbol, 100.0)

    # Add small random fluctuation (±0.5%) to make it feel dynamic
    # Use a seed based on current minute to keep price stable within same minute
    current_minute = datetime.now().minute
    random.seed(hash(symbol + str(current_minute)))

    fluctuation = random.uniform(-0.005, 0.005)  # ±0.5%
    current_price = base_price * (1 + fluctuation)

    return round(current_price, 2)


def execute_trade(st, symbol, action, quantity):
    """
    Execute a trade and update portfolio - WORKING VERSION.

    Args:
        st: Streamlit module (passed in to avoid import issues)
        symbol: Stock symbol
        action: "BUY" or "SELL"
        quantity: Number of shares

    Returns:
        tuple: (success: bool, message: str)
    """
    price = get_stock_price(symbol)

    if action == "BUY":
        cost = quantity * price
        if st.session_state.cash >= cost:
            st.session_state.cash -= cost

            # Update positions
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

            # Add to trade history
            st.session_state.trade_history.insert(
                0,
                {
                    "timestamp": datetime.now(),
                    "symbol": symbol,
                    "signal": "BUY",
                    "action": "BUY",
                    "quantity": quantity,
                    "price": price,
                    "total": cost,
                    "confidence": 100.0,
                    "executed": True,
                    "reasoning": "Manual trade from UI",
                },
            )

            # Add to recent decisions
            st.session_state.recent_decisions.insert(
                0,
                {
                    "timestamp": datetime.now(),
                    "symbol": symbol,
                    "signal": "BUY",
                    "confidence": 100.0,
                    "quantity": quantity,
                    "price": price,
                    "executed": True,
                    "reasoning": "Manual trade execution",
                },
            )

            st.session_state.total_trades += 1
            st.session_state.successful_trades += 1
            st.session_state.total_decisions += 1

            update_portfolio_value(st, symbol)
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

                # Add to trade history
                st.session_state.trade_history.insert(
                    0,
                    {
                        "timestamp": datetime.now(),
                        "symbol": symbol,
                        "signal": "SELL",
                        "action": "SELL",
                        "quantity": quantity,
                        "price": price,
                        "total": proceeds,
                        "confidence": 100.0,
                        "executed": True,
                        "reasoning": "Manual trade from UI",
                    },
                )

                # Add to recent decisions
                st.session_state.recent_decisions.insert(
                    0,
                    {
                        "timestamp": datetime.now(),
                        "symbol": symbol,
                        "signal": "SELL",
                        "confidence": 100.0,
                        "quantity": quantity,
                        "price": price,
                        "executed": True,
                        "reasoning": "Manual trade execution",
                    },
                )

                st.session_state.total_trades += 1
                st.session_state.successful_trades += 1
                st.session_state.total_decisions += 1

                update_portfolio_value(st, symbol)
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


def update_portfolio_value(st, symbol=None):
    """Update total portfolio value and sync with legacy portfolio dict."""
    # Calculate positions value
    positions_value = sum(
        pos["shares"] * get_stock_price(sym)
        for sym, pos in st.session_state.positions.items()
    )

    # Update legacy portfolio dict for UI compatibility
    st.session_state.portfolio["cash"] = st.session_state.cash
    st.session_state.portfolio["total_value"] = st.session_state.cash + positions_value

    # Sync positions to legacy format
    st.session_state.portfolio["positions"] = {}
    for sym, pos in st.session_state.positions.items():
        current_price = get_stock_price(sym)
        market_value = pos["shares"] * current_price
        cost_basis = pos["shares"] * pos["avg_cost"]
        unrealized_pnl = market_value - cost_basis
        unrealized_pnl_pct = (
            (unrealized_pnl / cost_basis * 100) if cost_basis > 0 else 0
        )

        st.session_state.portfolio["positions"][sym] = {
            "shares": pos["shares"],
            "avg_cost": pos["avg_cost"],
            "current_price": current_price,
            "market_value": market_value,
            "cost_basis": cost_basis,
            "unrealized_pnl": unrealized_pnl,
            "unrealized_pnl_pct": unrealized_pnl_pct,
            "day_change": 0.0,  # Dummy value
            "day_change_pct": 0.0,  # Dummy value
        }
        st.session_state.portfolio["cost_basis"][sym] = cost_basis

    # Calculate return
    initial = 100000.0
    st.session_state.portfolio["total_return"] = (
        st.session_state.portfolio["total_value"] - initial
    )
    st.session_state.portfolio["total_return_pct"] = (
        st.session_state.portfolio["total_return"] / initial
    ) * 100

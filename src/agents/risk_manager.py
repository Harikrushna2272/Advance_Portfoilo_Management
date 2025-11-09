import pandas as pd
import numpy as np
from datetime import datetime

# Import the API functions from ai-hedge-fund
from src.tools import api as hedge_api

def analyze_risk(stock, start_date, end_date, portfolio):
    """Run risk management analysis for a single stock."""
    try:
        # Get price data for risk analysis
        prices = hedge_api.get_prices(
            ticker=stock,
            start_date=start_date,
            end_date=end_date,
        )

        if not prices:
            return {"signal": "neutral", "confidence": 0}

        prices_df = hedge_api.prices_to_df(prices)

        # Calculate current price
        current_price = prices_df["close"].iloc[-1]

        # Calculate current position value for this ticker
        current_position_value = portfolio.get("cost_basis", {}).get(stock, 0)

        # Calculate total portfolio value
        total_portfolio_value = portfolio.get("cash", 0) + sum(portfolio.get("cost_basis", {}).get(t, 0) for t in portfolio.get("cost_basis", {}))

        # Base limit is 20% of portfolio for any single position
        position_limit = total_portfolio_value * 0.20

        # For existing positions, subtract current position value from limit
        remaining_position_limit = position_limit - current_position_value

        # Ensure we don't exceed available cash
        max_position_size = min(remaining_position_limit, portfolio.get("cash", 0))

        # Risk assessment based on position size
        if max_position_size > total_portfolio_value * 0.15:  # High risk
            signal = "bearish"
            confidence = 80
        elif max_position_size > total_portfolio_value * 0.10:  # Medium risk
            signal = "neutral"
            confidence = 60
        else:  # Low risk
            signal = "bullish"
            confidence = 70

        reasoning = {
            "portfolio_value": float(total_portfolio_value),
            "current_position": float(current_position_value),
            "position_limit": float(position_limit),
            "remaining_limit": float(remaining_position_limit),
            "available_cash": float(portfolio.get("cash", 0)),
            "max_position_size": float(max_position_size),
        }

        return {
            "signal": signal,
            "confidence": confidence,
            "reasoning": reasoning,
            "remaining_position_limit": float(max_position_size),
            "current_price": float(current_price),
        }
    
    except Exception as e:
        print(f"Error in risk analysis for {stock}: {e}")
        return {"signal": "neutral", "confidence": 0}

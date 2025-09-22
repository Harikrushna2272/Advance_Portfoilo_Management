import pandas as pd
import numpy as np
from datetime import datetime

def analyze_portfolio(analyst_signals, portfolio, tickers):
    """Run portfolio management analysis to make final trading decisions."""
    try:
        decisions = {}
        
        for ticker in tickers:
            # Get position limits and current prices for the ticker
            risk_data = analyst_signals.get("risk_manager", {}).get(ticker, {})
            position_limits = risk_data.get("remaining_position_limit", 0)
            current_prices = risk_data.get("current_price", 0)

            # Calculate maximum shares allowed based on position limit and price
            if current_prices > 0:
                max_shares = int(position_limits / current_prices)
            else:
                max_shares = 0

            # Get signals for the ticker
            ticker_signals = {}
            for agent, signals in analyst_signals.items():
                if agent != "risk_manager" and ticker in signals:
                    ticker_signals[agent] = {
                        "signal": signals[ticker]["signal"], 
                        "confidence": signals[ticker]["confidence"]
                    }

            # Make decision based on signals
            decision = make_trading_decision(ticker_signals, max_shares, portfolio, ticker)
            decisions[ticker] = decision

        return decisions
    
    except Exception as e:
        print(f"Error in portfolio analysis: {e}")
        return {ticker: {"action": "hold", "quantity": 0, "confidence": 0.0, "reasoning": "Error in portfolio management"} for ticker in tickers}


def make_trading_decision(ticker_signals, max_shares, portfolio, ticker):
    """Make individual trading decision for a ticker based on signals."""
    try:
        # Count bullish vs bearish signals
        bullish_count = 0
        bearish_count = 0
        total_confidence = 0
        signal_count = 0

        for agent, signal_data in ticker_signals.items():
            signal = signal_data["signal"]
            confidence = signal_data["confidence"]
            
            if signal == "bullish":
                bullish_count += 1
            elif signal == "bearish":
                bearish_count += 1
            
            total_confidence += confidence
            signal_count += 1

        # Calculate average confidence
        avg_confidence = total_confidence / signal_count if signal_count > 0 else 0

        # Make decision based on signal majority
        if bullish_count > bearish_count and avg_confidence > 60:
            action = "buy"
            quantity = min(max_shares, 10)  # Limit to 10 shares max
            reasoning = f"Bullish signals: {bullish_count}, Bearish: {bearish_count}, Confidence: {avg_confidence:.1f}%"
        elif bearish_count > bullish_count and avg_confidence > 60:
            action = "sell"
            # Get current position
            current_position = portfolio.get("positions", {}).get(ticker, {}).get("shares", 0)
            quantity = min(current_position, 10)  # Limit to 10 shares max
            reasoning = f"Bearish signals: {bearish_count}, Bullish: {bullish_count}, Confidence: {avg_confidence:.1f}%"
        else:
            action = "hold"
            quantity = 0
            reasoning = f"Mixed signals or low confidence. Bullish: {bullish_count}, Bearish: {bearish_count}, Confidence: {avg_confidence:.1f}%"

        return {
            "action": action,
            "quantity": quantity,
            "confidence": avg_confidence,
            "reasoning": reasoning
        }
    
    except Exception as e:
        print(f"Error making trading decision for {ticker}: {e}")
        return {
            "action": "hold",
            "quantity": 0,
            "confidence": 0.0,
            "reasoning": "Error in decision making"
        }

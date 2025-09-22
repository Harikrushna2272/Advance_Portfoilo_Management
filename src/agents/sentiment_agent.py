import pandas as pd
import numpy as np
from datetime import datetime

# Import the API functions from ai-hedge-fund
from utils import api as hedge_api

def analyze_sentiment(stock, end_date):
    """Run sentiment analysis for a single stock using insider trading data."""
    try:
        # Get the insider trades
        insider_trades = hedge_api.get_insider_trades(
            ticker=stock,
            end_date=end_date,
            limit=1000,
        )

        if not insider_trades:
            return {"signal": "neutral", "confidence": 0}

        # Get the signals from the insider trades
        transaction_shares = pd.Series([t.transaction_shares for t in insider_trades]).dropna()
        bearish_condition = transaction_shares < 0
        signals = np.where(bearish_condition, "bearish", "bullish").tolist()

        # Determine overall signal
        bullish_signals = signals.count("bullish")
        bearish_signals = signals.count("bearish")
        if bullish_signals > bearish_signals:
            overall_signal = "bullish"
        elif bearish_signals > bullish_signals:
            overall_signal = "bearish"
        else:
            overall_signal = "neutral"

        # Calculate confidence level based on the proportion of indicators agreeing
        total_signals = len(signals)
        confidence = 0  # Default confidence when there are no signals
        if total_signals > 0:
            confidence = round(max(bullish_signals, bearish_signals) / total_signals, 2) * 100
        
        reasoning = f"Bullish signals: {bullish_signals}, Bearish signals: {bearish_signals}"

        return {
            "signal": overall_signal,
            "confidence": confidence,
            "reasoning": reasoning,
        }
    
    except Exception as e:
        print(f"Error in sentiment analysis for {stock}: {e}")
        return {"signal": "neutral", "confidence": 0}
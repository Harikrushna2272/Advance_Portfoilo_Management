import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any

# Import the API functions from tools.api module
from src.tools import api as hedge_api


def analyze_sentiment(stock: str, end_date: str) -> Dict[str, Any]:
    """Run sentiment analysis for a single stock using insider trading data."""
    try:
        # Get the insider trades
        insider_trades = hedge_api.get_insider_trades(
            ticker=stock,
            end_date=end_date,
            limit=1000,
        )

        # Process insider trading signals
        if insider_trades:
            transaction_shares = pd.Series(
                [t.transaction_shares for t in insider_trades]
            ).dropna()
            bearish_condition = transaction_shares < 0
            signals = np.where(bearish_condition, "bearish", "bullish").tolist()

            # Calculate insider trading sentiment
            bullish_signals = signals.count("bullish")
            bearish_signals = signals.count("bearish")

            if bullish_signals > bearish_signals:
                insider_signal = "bullish"
            elif bearish_signals > bullish_signals:
                insider_signal = "bearish"
            else:
                insider_signal = "neutral"

            # Calculate insider confidence
            total_signals = len(signals)
            insider_confidence = (
                round(max(bullish_signals, bearish_signals) / total_signals, 2) * 100
                if total_signals > 0
                else 0
            )
        else:
            insider_signal = "neutral"
            insider_confidence = 0
            bullish_signals = 0
            bearish_signals = 0

        # Use insider trading signal as the final signal
        final_signal = insider_signal
        final_confidence = insider_confidence

        reasoning = (
            f"Insider Trading: {insider_signal} ({insider_confidence:.1f}% confidence) "
            f"[Bullish: {bullish_signals}, Bearish: {bearish_signals}]"
        )

        return {
            "signal": final_signal,
            "confidence": final_confidence,
            "reasoning": reasoning,
        }

    except Exception as e:
        print(f"Error in sentiment analysis for {stock}: {e}")
        return {"signal": "neutral", "confidence": 0, "reasoning": f"Error: {str(e)}"}

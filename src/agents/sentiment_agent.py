import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any

# Import the API functions from ai-hedge-fund
from utils import api as hedge_api
from utils.knowledge_graph import CompanyKnowledgeGraph

def analyze_sentiment(stock: str, end_date: datetime) -> Dict[str, Any]:
    """Run sentiment analysis for a single stock using insider trading data and knowledge graph."""
    try:
        # Initialize knowledge graph
        kg = CompanyKnowledgeGraph()
        
        # Get company data
        company_data = hedge_api.get_company_data(stock)
        
        # Get news data
        news_data = hedge_api.get_news(
            ticker=stock,
            end_date=end_date,
            limit=50  # Last 50 news items
        )
        
        # Get company relationships
        relationships = hedge_api.get_company_relationships(stock)
        
        # Build knowledge graph
        kg.build_graph(company_data, news_data, relationships)
        
        # Get knowledge graph-based sentiment
        kg_signal, kg_confidence = kg.get_sentiment_score()
        
        # Get the insider trades
        insider_trades = hedge_api.get_insider_trades(
            ticker=stock,
            end_date=end_date,
            limit=1000,
        )

        # Process insider trading signals
        if insider_trades:
            transaction_shares = pd.Series([t.transaction_shares for t in insider_trades]).dropna()
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
            insider_confidence = round(max(bullish_signals, bearish_signals) / total_signals, 2) * 100 if total_signals > 0 else 0
        else:
            insider_signal = "neutral"
            insider_confidence = 0
            bullish_signals = 0
            bearish_signals = 0

        # Combine signals with weights
        # Knowledge graph: 60%, Insider trading: 40%
        if kg_signal == insider_signal:
            final_signal = kg_signal
            final_confidence = (kg_confidence * 0.6 + insider_confidence * 0.4)
        else:
            # If signals disagree, use the one with higher confidence
            if kg_confidence * 0.6 > insider_confidence * 0.4:
                final_signal = kg_signal
                final_confidence = kg_confidence * 0.6
            else:
                final_signal = insider_signal
                final_confidence = insider_confidence * 0.4

        reasoning = (
            f"Knowledge Graph Signal: {kg_signal} ({kg_confidence:.1f}% confidence), "
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
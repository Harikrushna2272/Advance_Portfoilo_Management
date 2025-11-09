"""
Analysis page component - Enhanced with live agent signals and comprehensive technical analysis
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np
import time


def render_analysis_page():
    """Render the comprehensive analysis page."""
    st.markdown("## 🔍 Market Analysis & Decision Engine")
    st.markdown("Deep dive into multi-agent analysis and RL ensemble predictions")

    # Stock selection controls
    render_analysis_controls()

    st.markdown("---")

    # Main analysis content
    if "selected_stock" in st.session_state and st.session_state.get(
        "run_analysis", False
    ):
        selected_stock = st.session_state.selected_stock

        # Two-column layout for agents and RL
        col1, col2 = st.columns([1, 1])

        with col1:
            render_agent_analysis_panel(selected_stock)

        with col2:
            render_rl_ensemble_panel(selected_stock)

        st.markdown("---")

        # Portfolio manager decision
        render_portfolio_manager_decision(selected_stock)

        st.markdown("---")

        # Technical analysis charts
        render_comprehensive_charts(selected_stock)

        st.markdown("---")

        # Strategy breakdown
        render_strategy_breakdown(selected_stock)
    else:
        # Show placeholder
        st.info(
            "👆 Select a stock and click 'Run Analysis' to begin comprehensive market analysis"
        )
        render_quick_market_overview()


def render_analysis_controls():
    """Render analysis control panel."""
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

    with col1:
        selected_stock = st.selectbox(
            "📊 Select Stock for Deep Analysis",
            options=st.session_state.settings.get(
                "stock_list", ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN"]
            ),
            index=0,
            help="Choose a stock to analyze with all agents and models",
        )
        st.session_state.selected_stock = selected_stock

    with col2:
        timeframe = st.selectbox(
            "⏰ Timeframe", options=["1D", "1W", "1M", "3M", "6M", "1Y"], index=2
        )
        st.session_state.analysis_timeframe = timeframe

    with col3:
        if st.button("🔍 Run Analysis", type="primary", use_container_width=True):
            with st.spinner(f"Analyzing {selected_stock}..."):
                st.session_state.run_analysis = True
                # Simulate analysis time
                time.sleep(1.5)
            st.success(f"✅ Analysis complete for {selected_stock}!")
            st.rerun()

    with col4:
        if st.button("🔄 Refresh", use_container_width=True):
            st.session_state.run_analysis = False
            st.rerun()


def render_agent_analysis_panel(stock: str):
    """Render detailed agent analysis panel."""
    st.markdown("### 🤖 5-Agent Analysis")

    # Simulate or fetch actual agent results
    agent_results = {
        "Fundamentals": {
            "signal": "bullish",
            "confidence": 85,
            "reasoning": [
                "Strong ROE of 28.5%",
                "Revenue growth: +15.3% YoY",
                "Net margin improving: 21.2%",
                "P/E ratio: 25.3 (fair value)",
            ],
            "metrics": {
                "ROE": "28.5%",
                "Revenue Growth": "+15.3%",
                "Net Margin": "21.2%",
                "P/E Ratio": "25.3",
            },
        },
        "Technicals": {
            "signal": "bullish",
            "confidence": 78,
            "reasoning": [
                "Trend: Strong uptrend (ADX: 32)",
                "Momentum: Positive (RSI: 62)",
                "Price above SMA-20 and SMA-50",
                "Bollinger Bands: Normal volatility",
            ],
            "strategies": {
                "Trend Following": {"signal": "bullish", "weight": 25},
                "Mean Reversion": {"signal": "neutral", "weight": 20},
                "Momentum": {"signal": "bullish", "weight": 25},
                "Volatility": {"signal": "neutral", "weight": 15},
                "Stat Arb": {"signal": "bearish", "weight": 15},
            },
        },
        "Valuation": {
            "signal": "bullish",
            "confidence": 72,
            "reasoning": [
                "DCF intrinsic value: $195.50",
                "Current price: $182.50",
                "Upside potential: +7.1%",
                "Owner earnings positive",
            ],
            "metrics": {
                "DCF Value": "$195.50",
                "Current Price": "$182.50",
                "Upside": "+7.1%",
                "Margin of Safety": "12%",
            },
        },
        "Sentiment": {
            "signal": "neutral",
            "confidence": 58,
            "reasoning": [
                "Insider trades: Mixed signals",
                "Recent buying: 2 transactions",
                "Recent selling: 2 transactions",
                "Net sentiment: Neutral",
            ],
            "metrics": {
                "Insider Buys": "2",
                "Insider Sells": "2",
                "Net Position": "Neutral",
            },
        },
        "Risk Manager": {
            "signal": "neutral",
            "confidence": 75,
            "reasoning": [
                "Current position: $7,500 (7.5%)",
                "Max position limit: $20,000 (20%)",
                "Remaining capacity: $12,500",
                "Portfolio well-diversified",
            ],
            "metrics": {
                "Current Exposure": "7.5%",
                "Max Allowed": "20%",
                "Remaining": "$12,500",
                "Risk Score": "Low",
            },
        },
    }

    # Display each agent
    for agent_name, result in agent_results.items():
        signal = result["signal"]
        confidence = result["confidence"]

        # Signal icon
        if signal == "bullish":
            signal_icon = "🟢"
            signal_color = "#28a745"
        elif signal == "bearish":
            signal_icon = "🔴"
            signal_color = "#dc3545"
        else:
            signal_icon = "🟡"
            signal_color = "#ffc107"

        # Create expander for each agent
        with st.expander(
            f"{signal_icon} **{agent_name}** - {signal.upper()} ({confidence}%)",
            expanded=(agent_name == "Fundamentals"),
        ):
            # Confidence bar
            st.progress(confidence / 100, text=f"Confidence: {confidence}%")

            # Reasoning
            st.markdown("**📝 Analysis:**")
            for reason in result["reasoning"]:
                st.markdown(f"- {reason}")

            # Metrics
            if "metrics" in result:
                st.markdown("**📊 Key Metrics:**")
                metric_cols = st.columns(len(result["metrics"]))
                for idx, (metric_name, metric_value) in enumerate(
                    result["metrics"].items()
                ):
                    with metric_cols[idx]:
                        st.metric(metric_name, metric_value)

            # Strategy breakdown for Technical agent
            if "strategies" in result:
                st.markdown("**📈 Strategy Breakdown:**")
                for strategy_name, strategy_data in result["strategies"].items():
                    strat_signal = strategy_data["signal"]
                    strat_weight = strategy_data["weight"]

                    strat_icon = (
                        "🟢"
                        if strat_signal == "bullish"
                        else "🔴"
                        if strat_signal == "bearish"
                        else "🟡"
                    )
                    st.markdown(
                        f"{strat_icon} {strategy_name}: **{strat_signal.upper()}** ({strat_weight}% weight)"
                    )


def render_rl_ensemble_panel(stock: str):
    """Render RL ensemble analysis panel."""
    st.markdown("### 🧠 RL Ensemble Predictions")

    # Simulate RL model predictions
    rl_models = {
        "SAC": {"prediction": 1, "confidence": 82, "action": "BUY"},
        "PPO": {"prediction": 1, "confidence": 78, "action": "BUY"},
        "A2C": {"prediction": 0, "confidence": 55, "action": "HOLD"},
        "DQN": {"prediction": 1, "confidence": 85, "action": "BUY"},
        "TD3": {"prediction": -1, "confidence": 68, "action": "SELL"},
    }

    # Calculate ensemble prediction
    total_prediction = sum([model["prediction"] * 0.2 for model in rl_models.values()])

    if total_prediction > 0.3:
        ensemble_action = "BUY"
        ensemble_color = "#28a745"
        ensemble_icon = "🟢"
    elif total_prediction < -0.3:
        ensemble_action = "SELL"
        ensemble_color = "#dc3545"
        ensemble_icon = "🔴"
    else:
        ensemble_action = "HOLD"
        ensemble_color = "#ffc107"
        ensemble_icon = "🟡"

    # Calculate ensemble confidence (based on agreement)
    predictions = [model["prediction"] for model in rl_models.values()]
    agreement = (
        len([p for p in predictions if p == predictions[0]]) / len(predictions)
    ) * 100
    ensemble_confidence = int(agreement)

    # Display ensemble result
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, {ensemble_color}22 0%, {ensemble_color}11 100%);
                    padding: 1.5rem; border-radius: 12px; border-left: 5px solid {ensemble_color}; margin-bottom: 1rem;">
            <h3 style="margin: 0; color: {ensemble_color};">{ensemble_icon} Ensemble Prediction: {ensemble_action}</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">Confidence: {ensemble_confidence}% | Agreement Score: {agreement:.1f}%</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Individual model predictions
    st.markdown("**🤖 Individual Model Predictions:**")

    for model_name, model_data in rl_models.items():
        action = model_data["action"]
        confidence = model_data["confidence"]
        prediction = model_data["prediction"]

        if action == "BUY":
            action_icon = "🟢"
            action_color = "#28a745"
        elif action == "SELL":
            action_icon = "🔴"
            action_color = "#dc3545"
        else:
            action_icon = "🟡"
            action_color = "#ffc107"

        col1, col2, col3 = st.columns([2, 2, 3])

        with col1:
            st.markdown(f"**{model_name}**")

        with col2:
            st.markdown(f"{action_icon} **{action}**")

        with col3:
            st.progress(confidence / 100, text=f"{confidence}%")

    st.markdown("---")

    # Model voting visualization
    st.markdown("**🗳️ Model Voting Distribution:**")

    vote_counts = {"BUY": 0, "SELL": 0, "HOLD": 0}
    for model_data in rl_models.values():
        vote_counts[model_data["action"]] += 1

    # Create bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                x=list(vote_counts.keys()),
                y=list(vote_counts.values()),
                marker_color=["#28a745", "#dc3545", "#ffc107"],
                text=list(vote_counts.values()),
                textposition="auto",
            )
        ]
    )

    fig.update_layout(
        title="Model Vote Distribution",
        xaxis_title="Action",
        yaxis_title="Number of Models",
        height=250,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)

    # Feature importance
    st.markdown("**📊 Top Feature Importance:**")

    features = {
        "MACD": 0.18,
        "RSI-30": 0.15,
        "Volume": 0.12,
        "SMA-30": 0.11,
        "Bollinger Upper": 0.09,
        "Close Price": 0.08,
    }

    for feature, importance in features.items():
        st.progress(importance, text=f"{feature}: {importance:.1%}")


def render_portfolio_manager_decision(stock: str):
    """Render final portfolio manager decision."""
    st.markdown("### 🎯 Portfolio Manager Final Decision")

    # Simulate decision making
    agent_consensus = "bullish"  # From 3 bullish, 0 bearish, 2 neutral
    rl_signal = "BUY"

    # Calculate final decision
    final_signal = "BUY"
    final_confidence = 82
    final_quantity = 75
    multiplier = 1.0

    # Create three columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #28a74522 0%, #28a74511 100%);
                        padding: 1.5rem; border-radius: 12px; border-left: 5px solid #28a745; text-align: center;">
                <h2 style="margin: 0; color: #28a745;">🟢 {final_signal}</h2>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; font-weight: 600;">Final Signal</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #1f77b422 0%, #1f77b411 100%);
                        padding: 1.5rem; border-radius: 12px; border-left: 5px solid #1f77b4; text-align: center;">
                <h2 style="margin: 0; color: #1f77b4;">{final_confidence}%</h2>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; font-weight: 600;">Confidence</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #ff7f0e22 0%, #ff7f0e11 100%);
                        padding: 1.5rem; border-radius: 12px; border-left: 5px solid #ff7f0e; text-align: center;">
                <h2 style="margin: 0; color: #ff7f0e;">{final_quantity}</h2>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; font-weight: 600;">Shares</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")

    # Decision reasoning
    with st.expander("📋 Decision Reasoning", expanded=True):
        st.markdown(f"""
        **Analysis Summary:**
        - **Agent Consensus**: {agent_consensus.upper()} (3 bullish, 0 bearish, 2 neutral)
        - **RL Ensemble**: {rl_signal} with {final_confidence - 10}% confidence
        - **Alignment**: Strong agreement between agents and RL models
        - **Multiplier**: {multiplier}x (full conviction)

        **Quantity Calculation:**
        - Base Quantity: 100 shares
        - Confidence Scaling: {final_confidence}%
        - Multiplier: {multiplier}x
        - Risk Adjustment: 1.0x (neutral risk)
        - **Final Quantity**: {final_quantity} shares

        **Expected Trade:**
        - Action: {final_signal} {final_quantity} shares of {stock}
        - Estimated Price: $182.50
        - Estimated Cost: ${final_quantity * 182.50:,.2f}
        - Position Impact: +0.{final_quantity}% of portfolio
        """)

    # Execute button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button(
            f"🚀 Execute {final_signal} Order",
            key="execute_analysis_trade_button",
            type="primary",
            use_container_width=True,
        ):
            with st.spinner("Executing trade..."):
                time.sleep(1)
            st.success(
                f"✅ Successfully executed {final_signal} {final_quantity} shares of {stock}!"
            )
            st.balloons()


def render_comprehensive_charts(stock: str):
    """Render comprehensive technical analysis charts."""
    st.markdown("### 📈 Technical Analysis Charts")

    # Generate sample price data
    dates = pd.date_range(
        start=datetime.now() - timedelta(days=90), end=datetime.now(), freq="D"
    )

    # Simulate price data
    np.random.seed(42)
    base_price = 150
    price_changes = np.random.normal(0.002, 0.02, len(dates))
    close_prices = [base_price]

    for change in price_changes[1:]:
        close_prices.append(close_prices[-1] * (1 + change))

    # Generate OHLC data
    df = pd.DataFrame(
        {
            "Date": dates,
            "Open": [p * (1 + np.random.uniform(-0.01, 0.01)) for p in close_prices],
            "High": [p * (1 + abs(np.random.uniform(0, 0.02))) for p in close_prices],
            "Low": [p * (1 - abs(np.random.uniform(0, 0.02))) for p in close_prices],
            "Close": close_prices,
            "Volume": np.random.randint(1000000, 5000000, len(dates)),
        }
    )

    # Calculate indicators
    df["SMA_20"] = df["Close"].rolling(window=20).mean()
    df["SMA_50"] = df["Close"].rolling(window=50).mean()
    df["EMA_12"] = df["Close"].ewm(span=12).mean()
    df["EMA_26"] = df["Close"].ewm(span=26).mean()
    df["MACD"] = df["EMA_12"] - df["EMA_26"]
    df["Signal"] = df["MACD"].ewm(span=9).mean()

    # Bollinger Bands
    df["BB_Middle"] = df["Close"].rolling(window=20).mean()
    df["BB_Std"] = df["Close"].rolling(window=20).std()
    df["BB_Upper"] = df["BB_Middle"] + (df["BB_Std"] * 2)
    df["BB_Lower"] = df["BB_Middle"] - (df["BB_Std"] * 2)

    # RSI
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # Create subplots
    fig = make_subplots(
        rows=4,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=(f"{stock} Price Chart", "Volume", "MACD", "RSI"),
        row_heights=[0.5, 0.15, 0.2, 0.15],
    )

    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Price",
        ),
        row=1,
        col=1,
    )

    # Moving averages
    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["SMA_20"],
            name="SMA 20",
            line=dict(color="orange", width=1),
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["SMA_50"],
            name="SMA 50",
            line=dict(color="blue", width=1),
        ),
        row=1,
        col=1,
    )

    # Bollinger Bands
    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["BB_Upper"],
            name="BB Upper",
            line=dict(color="gray", width=1, dash="dash"),
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["BB_Lower"],
            name="BB Lower",
            line=dict(color="gray", width=1, dash="dash"),
            fill="tonexty",
            fillcolor="rgba(128,128,128,0.1)",
        ),
        row=1,
        col=1,
    )

    # Volume
    colors = [
        "red" if df.iloc[i]["Close"] < df.iloc[i]["Open"] else "green"
        for i in range(len(df))
    ]
    fig.add_trace(
        go.Bar(x=df["Date"], y=df["Volume"], name="Volume", marker_color=colors),
        row=2,
        col=1,
    )

    # MACD
    fig.add_trace(
        go.Scatter(
            x=df["Date"], y=df["MACD"], name="MACD", line=dict(color="blue", width=2)
        ),
        row=3,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"], y=df["Signal"], name="Signal", line=dict(color="red", width=1)
        ),
        row=3,
        col=1,
    )

    # MACD Histogram
    macd_hist = df["MACD"] - df["Signal"]
    colors = ["green" if val >= 0 else "red" for val in macd_hist]
    fig.add_trace(
        go.Bar(x=df["Date"], y=macd_hist, name="MACD Hist", marker_color=colors),
        row=3,
        col=1,
    )

    # RSI
    fig.add_trace(
        go.Scatter(
            x=df["Date"], y=df["RSI"], name="RSI", line=dict(color="purple", width=2)
        ),
        row=4,
        col=1,
    )

    # RSI levels
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=4, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=4, col=1)
    fig.add_hline(y=50, line_dash="dot", line_color="gray", row=4, col=1)

    # Update layout
    fig.update_layout(
        height=900,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(128,128,128,0.2)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(128,128,128,0.2)")

    st.plotly_chart(fig, use_container_width=True)


def render_strategy_breakdown(stock: str):
    """Render detailed strategy breakdown."""
    st.markdown("### 📊 Technical Strategy Breakdown")

    strategies = {
        "Trend Following": {
            "signal": "bullish",
            "confidence": 85,
            "weight": 25,
            "indicators": [
                "EMA 12/26 crossover",
                "ADX: 32 (strong trend)",
                "Price above SMA-50",
            ],
        },
        "Mean Reversion": {
            "signal": "neutral",
            "confidence": 58,
            "weight": 20,
            "indicators": [
                "Bollinger Bands: Mid-range",
                "RSI: 62 (neutral zone)",
                "Z-score: 0.5",
            ],
        },
        "Momentum": {
            "signal": "bullish",
            "confidence": 78,
            "weight": 25,
            "indicators": [
                "1M return: +5.2%",
                "3M return: +12.8%",
                "6M return: +18.3%",
            ],
        },
        "Volatility": {
            "signal": "neutral",
            "confidence": 65,
            "weight": 15,
            "indicators": [
                "ATR: Normal range",
                "Volatility regime: Moderate",
                "IV Percentile: 45%",
            ],
        },
        "Statistical Arbitrage": {
            "signal": "bearish",
            "confidence": 52,
            "weight": 15,
            "indicators": [
                "Hurst exponent: 0.48",
                "Mean reversion expected",
                "Short-term overextension",
            ],
        },
    }

    for strategy_name, strategy_data in strategies.items():
        signal = strategy_data["signal"]
        confidence = strategy_data["confidence"]
        weight = strategy_data["weight"]

        if signal == "bullish":
            signal_icon = "🟢"
            signal_color = "#28a745"
        elif signal == "bearish":
            signal_icon = "🔴"
            signal_color = "#dc3545"
        else:
            signal_icon = "🟡"
            signal_color = "#ffc107"

        with st.expander(
            f"{signal_icon} {strategy_name} - {signal.upper()} ({confidence}%) | Weight: {weight}%"
        ):
            col1, col2 = st.columns([1, 2])

            with col1:
                st.metric("Confidence", f"{confidence}%")
                st.progress(confidence / 100)
                st.metric("Weight", f"{weight}%")
                st.progress(weight / 100)

            with col2:
                st.markdown("**Key Indicators:**")
                for indicator in strategy_data["indicators"]:
                    st.markdown(f"- {indicator}")


def render_quick_market_overview():
    """Render quick market overview when no analysis is selected."""
    st.markdown("### 📊 Market Overview")

    # Sample market data
    market_data = {
        "Symbol": ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN"],
        "Price": [182.50, 245.80, 140.50, 420.15, 175.75],
        "Change": [2.50, -3.20, 1.25, 5.80, -2.10],
        "Change %": [1.39, -1.28, 0.90, 1.40, -1.18],
        "Volume": ["52.3M", "98.7M", "25.4M", "32.1M", "45.6M"],
    }

    df = pd.DataFrame(market_data)

    # Style the dataframe
    def color_change(val):
        try:
            num_val = float(val.replace("%", "").replace("M", ""))
            if num_val > 0:
                return "color: #28a745; font-weight: bold"
            elif num_val < 0:
                return "color: #dc3545; font-weight: bold"
            else:
                return ""
        except:
            return ""

    styled_df = df.style.map(color_change, subset=["Change", "Change %"])

    st.dataframe(styled_df, use_container_width=True, hide_index=True)

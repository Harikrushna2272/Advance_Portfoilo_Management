# Streamlit UI for StockAI Trading System
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import asyncio
import json
import time
from typing import Dict, List, Any
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.settings import get_settings
from utils.logger import setup_logger
from core.decision_engine import DecisionEngine
from agents.execution_agent import ExecutionAgent

# Configure page
st.set_page_config(
    page_title="StockAI Trading System",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-card {
        border-left-color: #28a745;
    }
    .warning-card {
        border-left-color: #ffc107;
    }
    .danger-card {
        border-left-color: #dc3545;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.decision_engine = None
    st.session_state.execution_agent = None
    st.session_state.portfolio = {
        "cash": 100000.0,
        "positions": {},
        "cost_basis": {}
    }
    st.session_state.trading_active = False
    st.session_state.last_update = None

# Initialize logger
logger = setup_logger("stockai.ui")

class StockAIUI:
    """Main UI class for StockAI Trading System."""
    
    def __init__(self):
        self.settings = get_settings()
        self.initialize_services()
    
    def initialize_services(self):
        """Initialize trading services."""
        try:
            if not st.session_state.initialized:
                with st.spinner("Initializing StockAI services..."):
                    # Initialize decision engine
                    st.session_state.decision_engine = DecisionEngine()
                    
                    # Initialize execution agent
                    st.session_state.execution_agent = ExecutionAgent()
                    
                    st.session_state.initialized = True
                    st.success("✅ Services initialized successfully!")
        except Exception as e:
            st.error(f"❌ Failed to initialize services: {e}")
            logger.error(f"Service initialization failed: {e}")
    
    def render_header(self):
        """Render the main header."""
        st.markdown('<h1 class="main-header">📈 StockAI Trading System</h1>', unsafe_allow_html=True)
        
        # Status indicator
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.session_state.trading_active:
                st.success("🟢 Trading System: ACTIVE")
            else:
                st.warning("🟡 Trading System: INACTIVE")
    
    def render_sidebar(self):
        """Render the sidebar with controls."""
        st.sidebar.title("🎛️ Control Panel")
        
        # Trading Controls
        st.sidebar.subheader("Trading Controls")
        
        if st.sidebar.button("🚀 Start Trading", type="primary"):
            st.session_state.trading_active = True
            st.success("Trading system started!")
        
        if st.sidebar.button("⏹️ Stop Trading"):
            st.session_state.trading_active = False
            st.warning("Trading system stopped!")
        
        st.sidebar.divider()
        
        # Configuration
        st.sidebar.subheader("⚙️ Configuration")
        
        # Stock list
        stock_list = st.sidebar.multiselect(
            "📊 Select Stocks",
            options=["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN", "NVDA", "META", "NFLX"],
            default=["AAPL", "TSLA", "GOOGL"]
        )
        
        # Confidence threshold
        confidence_threshold = st.sidebar.slider(
            "🎯 Confidence Threshold (%)",
            min_value=50,
            max_value=95,
            value=60,
            step=5
        )
        
        # Base quantity
        base_quantity = st.sidebar.number_input(
            "📦 Base Quantity",
            min_value=1,
            max_value=1000,
            value=100,
            step=10
        )
        
        st.sidebar.divider()
        
        # System Status
        st.sidebar.subheader("📊 System Status")
        
        # Portfolio value
        total_value = st.session_state.portfolio["cash"]
        for symbol, position in st.session_state.portfolio["positions"].items():
            # This would be calculated with current prices
            total_value += position.get("market_value", 0)
        
        st.sidebar.metric("💰 Portfolio Value", f"${total_value:,.2f}")
        st.sidebar.metric("💵 Available Cash", f"${st.session_state.portfolio['cash']:,.2f}")
        st.sidebar.metric("📈 Active Positions", len(st.session_state.portfolio["positions"]))
        
        return {
            "stock_list": stock_list,
            "confidence_threshold": confidence_threshold,
            "base_quantity": base_quantity
        }
    
    def render_dashboard(self):
        """Render the main dashboard."""
        st.subheader("📊 Trading Dashboard")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🎯 Total Decisions",
                "1,234",
                delta="12"
            )
        
        with col2:
            st.metric(
                "💼 Trades Executed",
                "89",
                delta="5"
            )
        
        with col3:
            st.metric(
                "📈 Success Rate",
                "73.2%",
                delta="2.1%"
            )
        
        with col4:
            st.metric(
                "💰 P&L Today",
                "$1,234.56",
                delta="$123.45"
            )
        
        st.divider()
        
        # Charts section
        col1, col2 = st.columns(2)
        
        with col1:
            self.render_portfolio_chart()
        
        with col2:
            self.render_performance_chart()
        
        # Recent decisions
        self.render_recent_decisions()
    
    def render_portfolio_chart(self):
        """Render portfolio composition chart."""
        st.subheader("📊 Portfolio Composition")
        
        # Sample data - in real implementation, this would come from the portfolio
        portfolio_data = {
            "AAPL": {"shares": 50, "value": 7500, "percentage": 35},
            "TSLA": {"shares": 25, "value": 5000, "percentage": 23},
            "GOOGL": {"shares": 15, "value": 4000, "percentage": 19},
            "Cash": {"shares": 0, "value": 5000, "percentage": 23}
        }
        
        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=list(portfolio_data.keys()),
            values=[data["value"] for data in portfolio_data.values()],
            hole=0.3
        )])
        
        fig.update_layout(
            title="Portfolio Allocation",
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_performance_chart(self):
        """Render performance chart."""
        st.subheader("📈 Performance Over Time")
        
        # Sample data - in real implementation, this would come from historical data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
        performance = [100000 + i * 100 + (i % 7) * 50 for i in range(len(dates))]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=performance,
            mode='lines',
            name='Portfolio Value',
            line=dict(color='#1f77b4', width=2)
        ))
        
        fig.update_layout(
            title="Portfolio Performance (30 Days)",
            xaxis_title="Date",
            yaxis_title="Portfolio Value ($)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_recent_decisions(self):
        """Render recent trading decisions."""
        st.subheader("🔄 Recent Trading Decisions")
        
        # Sample data - in real implementation, this would come from the decision engine
        decisions_data = {
            "Timestamp": [
                datetime.now() - timedelta(minutes=5),
                datetime.now() - timedelta(minutes=10),
                datetime.now() - timedelta(minutes=15),
                datetime.now() - timedelta(minutes=20),
                datetime.now() - timedelta(minutes=25)
            ],
            "Symbol": ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN"],
            "Signal": ["BUY", "SELL", "HOLD", "BUY", "HOLD"],
            "Confidence": [85, 72, 45, 91, 38],
            "Quantity": [50, 25, 0, 30, 0],
            "Price": [150.25, 245.80, 2800.50, 320.15, 3100.75]
        }
        
        df = pd.DataFrame(decisions_data)
        
        # Color code the signals
        def color_signal(val):
            if val == "BUY":
                return "background-color: #d4edda; color: #155724"
            elif val == "SELL":
                return "background-color: #f8d7da; color: #721c24"
            else:
                return "background-color: #fff3cd; color: #856404"
        
        styled_df = df.style.applymap(color_signal, subset=['Signal'])
        st.dataframe(styled_df, use_container_width=True)
    
    def render_analysis_page(self):
        """Render the analysis page."""
        st.subheader("🔍 Market Analysis")
        
        # Stock selection
        selected_stock = st.selectbox(
            "Select Stock for Analysis",
            ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN"]
        )
        
        if st.button("🔍 Run Analysis"):
            with st.spinner(f"Analyzing {selected_stock}..."):
                # Simulate analysis
                time.sleep(2)
                
                # Display analysis results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Agent Analysis")
                    
                    analysis_results = {
                        "Fundamentals": {"signal": "bullish", "confidence": 80},
                        "Technicals": {"signal": "neutral", "confidence": 65},
                        "Valuation": {"signal": "bullish", "confidence": 75},
                        "Sentiment": {"signal": "bearish", "confidence": 60},
                        "Risk": {"signal": "neutral", "confidence": 70}
                    }
                    
                    for agent, result in analysis_results.items():
                        signal_color = "🟢" if result["signal"] == "bullish" else "🔴" if result["signal"] == "bearish" else "🟡"
                        st.write(f"{signal_color} **{agent}**: {result['signal'].title()} ({result['confidence']}%)")
                
                with col2:
                    st.subheader("🤖 RL Ensemble")
                    
                    rl_results = {
                        "SAC": "BUY",
                        "PPO": "BUY", 
                        "A2C": "HOLD",
                        "DQN": "BUY",
                        "TD3": "SELL"
                    }
                    
                    for model, signal in rl_results.items():
                        signal_color = "🟢" if signal == "BUY" else "🔴" if signal == "SELL" else "🟡"
                        st.write(f"{signal_color} **{model}**: {signal}")
                    
                    st.divider()
                    st.subheader("🎯 Final Decision")
                    st.success("**BUY** - Confidence: 78% - Quantity: 45 shares")
    
    def render_portfolio_page(self):
        """Render the portfolio management page."""
        st.subheader("💼 Portfolio Management")
        
        # Portfolio overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Value", "$21,500.00", delta="$1,234.56")
        
        with col2:
            st.metric("Total Return", "7.5%", delta="2.1%")
        
        with col3:
            st.metric("Sharpe Ratio", "1.23", delta="0.15")
        
        st.divider()
        
        # Positions table
        st.subheader("📊 Current Positions")
        
        positions_data = {
            "Symbol": ["AAPL", "TSLA", "GOOGL"],
            "Shares": [50, 25, 15],
            "Avg Price": [145.50, 240.00, 2750.00],
            "Current Price": [150.25, 245.80, 2800.50],
            "Market Value": [7512.50, 6145.00, 42007.50],
            "Unrealized P&L": [237.50, 145.00, 757.50],
            "P&L %": [3.26, 2.42, 1.80]
        }
        
        df = pd.DataFrame(positions_data)
        st.dataframe(df, use_container_width=True)
        
        # Trade execution
        st.subheader("💼 Execute Trade")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            trade_symbol = st.selectbox("Symbol", ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN"])
        
        with col2:
            trade_action = st.selectbox("Action", ["BUY", "SELL"])
        
        with col3:
            trade_quantity = st.number_input("Quantity", min_value=1, max_value=1000, value=10)
        
        if st.button("🚀 Execute Trade", type="primary"):
            st.success(f"Trade executed: {trade_action} {trade_quantity} shares of {trade_symbol}")
    
    def render_monitoring_page(self):
        """Render the system monitoring page."""
        st.subheader("📊 System Monitoring")
        
        # System health
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🟢 API Status", "Connected")
        
        with col2:
            st.metric("🟢 Database", "Healthy")
        
        with col3:
            st.metric("🟢 Models", "Loaded")
        
        with col4:
            st.metric("🟡 Memory", "78%")
        
        st.divider()
        
        # Logs viewer
        st.subheader("📝 System Logs")
        
        # Sample logs
        logs_data = {
            "Timestamp": [
                datetime.now() - timedelta(minutes=1),
                datetime.now() - timedelta(minutes=2),
                datetime.now() - timedelta(minutes=3),
                datetime.now() - timedelta(minutes=4),
                datetime.now() - timedelta(minutes=5)
            ],
            "Level": ["INFO", "INFO", "WARNING", "INFO", "ERROR"],
            "Message": [
                "Trade executed: BUY 50 AAPL",
                "Analysis completed for TSLA",
                "Low confidence signal for GOOGL",
                "Portfolio updated successfully",
                "API connection timeout"
            ]
        }
        
        df = pd.DataFrame(logs_data)
        st.dataframe(df, use_container_width=True)
        
        # Auto-refresh
        if st.checkbox("🔄 Auto-refresh logs"):
            st.rerun()

def main():
    """Main Streamlit application."""
    ui = StockAIUI()
    
    # Render header
    ui.render_header()
    
    # Render sidebar
    config = ui.render_sidebar()
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🔍 Analysis", "💼 Portfolio", "📊 Monitoring"])
    
    with tab1:
        ui.render_dashboard()
    
    with tab2:
        ui.render_analysis_page()
    
    with tab3:
        ui.render_portfolio_page()
    
    with tab4:
        ui.render_monitoring_page()
    
    # Footer
    st.divider()
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "StockAI Trading System v1.0.0 | "
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

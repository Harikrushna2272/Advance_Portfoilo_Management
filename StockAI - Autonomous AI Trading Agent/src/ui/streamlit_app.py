# Simplified Streamlit app for StockAI
import streamlit as st
import sys
import os
from datetime import datetime

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pages.dashboard import render_dashboard
from pages.analysis import render_analysis_page
from pages.portfolio import render_portfolio_page
from pages.monitoring import render_monitoring_page

# Configure page
st.set_page_config(
    page_title="Advance AI Trading System",
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'trading_active' not in st.session_state:
    st.session_state.trading_active = False
    st.session_state.portfolio = {
        "cash": 100000.0,
        "positions": {},
        "cost_basis": {}
    }

def render_header():
    """Render the main header."""
    st.markdown('<h1 class="main-header">📈 StockAI Trading System</h1>', unsafe_allow_html=True)
    
    # Status indicator
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.trading_active:
            st.success("🟢 Trading System: ACTIVE")
        else:
            st.warning("🟡 Trading System: INACTIVE")

def render_sidebar():
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
        total_value += position.get("market_value", 0)
    
    st.sidebar.metric("💰 Portfolio Value", f"${total_value:,.2f}")
    st.sidebar.metric("💵 Available Cash", f"${st.session_state.portfolio['cash']:,.2f}")
    st.sidebar.metric("📈 Active Positions", len(st.session_state.portfolio["positions"]))
    
    return {
        "stock_list": stock_list,
        "confidence_threshold": confidence_threshold,
        "base_quantity": base_quantity
    }

def main():
    """Main Streamlit application."""
    # Render header
    render_header()
    
    # Render sidebar
    config = render_sidebar()
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🔍 Analysis", "💼 Portfolio", "📊 Monitoring"])
    
    with tab1:
        render_dashboard()
    
    with tab2:
        render_analysis_page()
    
    with tab3:
        render_portfolio_page()
    
    with tab4:
        render_monitoring_page()
    
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

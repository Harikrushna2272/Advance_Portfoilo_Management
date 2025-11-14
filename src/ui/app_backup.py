"""
StockAI - Advanced Multi-Agent Trading System UI
Sophisticated Streamlit Interface with Real-time Monitoring
"""

import streamlit as st

# Configure page FIRST - must be the very first Streamlit command
st.set_page_config(
    page_title="StockAI - Advanced Trading System",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/yourusername/stockai",
        "Report a bug": "https://github.com/yourusername/stockai/issues",
        "About": "# StockAI Trading System v1.0.0\n\nAI-powered algorithmic trading with multi-agent decision making.",
    },
)

# Now import everything else
import sys
import os
from datetime import datetime
import asyncio
from pathlib import Path

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from pages.dashboard import render_dashboard
from pages.analysis import render_analysis_page
from pages.portfolio import render_portfolio_page
from pages.monitoring import render_monitoring_page

# Import simple state manager (no external dependencies)
try:
    from ui import simple_state

    STATE_MANAGER = simple_state
    SYSTEM_AVAILABLE = True
except Exception as e:
    print(f"Warning: Could not initialize state manager: {e}")
    STATE_MANAGER = None
    SYSTEM_AVAILABLE = False

# Custom CSS for professional look
st.markdown(
    """
<style>
    /* Main theme colors */
    :root {
        --primary-color: #1f77b4;
        --success-color: #28a745;
        --warning-color: #ffc107;
        --danger-color: #dc3545;
        --info-color: #17a2b8;
        --dark-bg: #0e1117;
        --light-bg: #f0f2f6;
    }

    /* Header styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1f77b4 0%, #17a2b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        padding: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #f0f2f6 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

    .metric-card.success {
        border-left-color: #28a745;
    }

    .metric-card.warning {
        border-left-color: #ffc107;
    }

    .metric-card.danger {
        border-left-color: #dc3545;
    }

    .metric-card.info {
        border-left-color: #17a2b8;
    }

    /* Status indicators */
    .status-active {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1.5rem;
        background-color: #d4edda;
        color: #155724;
        border-radius: 20px;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(40, 167, 69, 0.2);
    }

    .status-inactive {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1.5rem;
        background-color: #fff3cd;
        color: #856404;
        border-radius: 20px;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(255, 193, 7, 0.2);
    }

    .status-error {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1.5rem;
        background-color: #f8d7da;
        color: #721c24;
        border-radius: 20px;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(220, 53, 69, 0.2);
    }

    /* Signal badges */
    .signal-buy {
        background-color: #d4edda;
        color: #155724;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.9rem;
    }

    .signal-sell {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.9rem;
    }

    .signal-hold {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.9rem;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }

    /* Button styling */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 2rem;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
        font-size: 1.1rem;
    }

    /* Alert boxes */
    .alert-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }

    .alert-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }

    .alert-danger {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }

    /* Loading animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    .loading {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    /* Footer styling */
    .footer {
        text-align: center;
        color: #999;
        padding: 2rem 0;
        border-top: 1px solid #e0e0e0;
        margin-top: 3rem;
    }

    /* Data table styling */
    .dataframe {
        font-size: 0.9rem;
    }

    .dataframe thead th {
        background-color: #1f77b4 !important;
        color: white !important;
        font-weight: 600;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
</style>
""",
    unsafe_allow_html=True,
)


# Initialize session state
def initialize_session_state():
    """Initialize session state variables - now loads from state manager."""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True

    # Load real-time state from simple state manager
    if STATE_MANAGER is not None:
        try:
            # Get current state from state manager
            current_state = STATE_MANAGER.load_state()

            # Update session state with real data
            st.session_state.trading_active = current_state.get("trading_active", False)
            st.session_state.last_update = datetime.fromisoformat(
                current_state.get("timestamp", datetime.now().isoformat())
            )
            st.session_state.cycle_count = current_state.get("cycle_count", 0)
            st.session_state.total_decisions = current_state.get("total_decisions", 0)
            st.session_state.total_trades = current_state.get("total_trades", 0)
            st.session_state.successful_trades = current_state.get(
                "successful_trades", 0
            )

            # Portfolio state
            st.session_state.portfolio = current_state.get("portfolio", {})

            # System state
            st.session_state.system_health = current_state.get("system_health", {})

            # Recent decisions
            st.session_state.recent_decisions = current_state.get(
                "recent_decisions", []
            )

            # Analytics
            st.session_state.analytics = current_state.get("analytics", {})

            # Settings
            st.session_state.settings = current_state.get("settings", {})

            # Portfolio history
            st.session_state.portfolio_history = None  # Will be loaded on demand
            st.session_state.daily_pnl_history = None  # Will be loaded on demand

        except Exception as e:
            st.error(f"Error loading state from state manager: {e}")
            # Fall back to default values
            _initialize_default_state()
    else:
        # No state manager available, use defaults
        _initialize_default_state()


def update_portfolio_value():
    """Update total portfolio value."""
    positions_value = sum(
        pos["shares"] * get_stock_price(symbol)
        for symbol, pos in st.session_state.positions.items()
    )
    st.session_state.portfolio["total_value"] = st.session_state.cash + positions_value
    st.session_state.portfolio["cash"] = st.session_state.cash

    # Calculate return
    initial = 100000.0
    st.session_state.portfolio["total_return"] = (
        st.session_state.portfolio["total_value"] - initial
    )
    st.session_state.portfolio["total_return_pct"] = (
        st.session_state.portfolio["total_return"] / initial
    ) * 100


def _initialize_default_state():
    """Initialize default state when state manager is not available."""
    st.session_state.trading_active = False
    st.session_state.last_update = datetime.now()
    st.session_state.cycle_count = 0
    st.session_state.total_decisions = 0
    st.session_state.total_trades = 0
    st.session_state.successful_trades = 0

    # Portfolio state
    st.session_state.portfolio = {
        "cash": 100000.0,
        "positions": {},
        "cost_basis": {},
        "total_value": 100000.0,
        "total_return": 0.0,
        "total_return_pct": 0.0,
    }

    # System state
    st.session_state.system_health = {
        "api_status": "Disconnected",
        "database_status": "Offline",
        "models_loaded": 0,
        "total_models": 5,
        "memory_usage": 0,
        "cpu_usage": 0,
    }

    # Recent decisions
    st.session_state.recent_decisions = []

    # Analytics
    st.session_state.analytics = {
        "daily_pnl": 0.0,
        "weekly_pnl": 0.0,
        "monthly_pnl": 0.0,
        "sharpe_ratio": 0.0,
        "max_drawdown": 0.0,
        "win_rate": 0.0,
    }

    # Settings
    st.session_state.settings = {
        "stock_list": ["AAPL", "TSLA", "GOOGL"],
        "confidence_threshold": 60,
        "base_quantity": 100,
        "max_quantity": 500,
        "cycle_interval": 60,
        "auto_refresh": True,
        "refresh_interval": 5,
    }


def render_header():
    """Render the main header with status."""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(
            '<h1 class="main-header">📈 StockAI Trading System</h1>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="sub-header">AI-Powered Multi-Agent Algorithmic Trading Platform</p>',
            unsafe_allow_html=True,
        )

    # Real-time status bar
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.session_state.trading_active:
            st.markdown(
                '<div class="status-active">🟢 SYSTEM ACTIVE</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="status-inactive">🟡 SYSTEM STANDBY</div>',
                unsafe_allow_html=True,
            )

    with col2:
        api_status = st.session_state.system_health.get("api_status", "Disconnected")
        if api_status == "Connected":
            st.markdown(
                '<div class="status-active">📡 API Connected</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="status-inactive">📡 API Offline</div>',
                unsafe_allow_html=True,
            )

    with col3:
        models_loaded = st.session_state.system_health.get("models_loaded", 0)
        total_models = st.session_state.system_health.get("total_models", 5)
        if models_loaded == total_models:
            st.markdown(
                f'<div class="status-active">🤖 Models {models_loaded}/{total_models}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="status-inactive">🤖 Models {models_loaded}/{total_models}</div>',
                unsafe_allow_html=True,
            )

    with col4:
        st.markdown(
            f'<div class="status-active">⏱️ Cycle #{st.session_state.cycle_count}</div>',
            unsafe_allow_html=True,
        )


def render_sidebar():
    """Render the advanced control sidebar."""
    with st.sidebar:
        st.title("🎛️ Control Panel")

        # Trading Controls Section
        st.markdown("### 🚀 Trading Controls")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Start", type="primary", use_container_width=True):
                st.session_state.trading_active = True
                st.session_state.system_health["api_status"] = "Connected"
                st.session_state.system_health["models_loaded"] = 5
                st.success("✅ Trading system started!")
                st.rerun()

        with col2:
            if st.button("⏹️ Stop", type="secondary", use_container_width=True):
                st.session_state.trading_active = False
                st.session_state.system_health["api_status"] = "Disconnected"
                st.warning("⏸️ Trading system stopped!")
                st.rerun()

        if st.button("🔄 Reset System", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("🔄 System reset complete!")
            st.rerun()

        st.markdown("---")

        # Configuration Section
        st.markdown("### ⚙️ Configuration")

        # Stock selection
        stock_list = st.multiselect(
            "📊 Trading Universe",
            options=[
                "AAPL",
                "TSLA",
                "GOOGL",
                "MSFT",
                "AMZN",
                "NVDA",
                "META",
                "NFLX",
                "AMD",
                "INTC",
            ],
            default=st.session_state.settings["stock_list"],
            help="Select stocks to monitor and trade",
        )
        st.session_state.settings["stock_list"] = stock_list

        # Confidence threshold
        confidence_threshold = st.slider(
            "🎯 Confidence Threshold (%)",
            min_value=50,
            max_value=95,
            value=st.session_state.settings["confidence_threshold"],
            step=5,
            help="Minimum confidence required to execute trades",
        )
        st.session_state.settings["confidence_threshold"] = confidence_threshold

        # Quantity settings
        col1, col2 = st.columns(2)
        with col1:
            base_qty = st.number_input(
                "📦 Base Qty",
                min_value=1,
                max_value=1000,
                value=st.session_state.settings["base_quantity"],
                step=10,
            )
            st.session_state.settings["base_quantity"] = base_qty

        with col2:
            max_qty = st.number_input(
                "📦 Max Qty",
                min_value=1,
                max_value=5000,
                value=st.session_state.settings["max_quantity"],
                step=50,
            )
            st.session_state.settings["max_quantity"] = max_qty

        # Cycle interval
        cycle_interval = st.slider(
            "⏱️ Cycle Interval (sec)",
            min_value=10,
            max_value=300,
            value=st.session_state.settings["cycle_interval"],
            step=10,
            help="Time between trading cycles",
        )
        st.session_state.settings["cycle_interval"] = cycle_interval

        st.markdown("---")

        # Portfolio Overview
        st.markdown("### 💼 Portfolio Overview")

        total_value = st.session_state.portfolio["total_value"]
        cash = st.session_state.portfolio["cash"]
        positions_count = len(st.session_state.portfolio["positions"])
        total_return_pct = st.session_state.portfolio["total_return_pct"]

        st.metric(
            "💰 Total Value", f"${total_value:,.2f}", delta=f"{total_return_pct:+.2f}%"
        )

        st.metric("💵 Cash Available", f"${cash:,.2f}")

        st.metric("📊 Active Positions", f"{positions_count}")

        # Calculate invested amount
        invested = total_value - cash
        if total_value > 0:
            invested_pct = (invested / total_value) * 100
        else:
            invested_pct = 0

        st.progress(invested_pct / 100, text=f"Invested: {invested_pct:.1f}%")

        st.markdown("---")

        # Performance Metrics
        st.markdown("### 📊 Performance")

        st.metric("📈 Win Rate", f"{st.session_state.analytics['win_rate']:.1f}%")

        st.metric(
            "📉 Max Drawdown", f"{st.session_state.analytics['max_drawdown']:.2f}%"
        )

        st.metric(
            "⚡ Sharpe Ratio", f"{st.session_state.analytics['sharpe_ratio']:.2f}"
        )

        st.markdown("---")

        # System Status
        st.markdown("### 🏥 System Health")

        mem_usage = st.session_state.system_health.get("memory_usage", 0)
        cpu_usage = st.session_state.system_health.get("cpu_usage", 0)

        st.metric("💾 Memory", f"{mem_usage}%")
        st.progress(mem_usage / 100)

        st.metric("🖥️ CPU", f"{cpu_usage}%")
        st.progress(cpu_usage / 100)

        st.markdown("---")

        # Display Settings
        st.markdown("### 🎨 Display Settings")

        auto_refresh = st.checkbox(
            "🔄 Auto-refresh",
            value=st.session_state.settings["auto_refresh"],
            help="Automatically refresh data",
        )
        st.session_state.settings["auto_refresh"] = auto_refresh

        if auto_refresh:
            refresh_interval = st.slider(
                "Refresh interval (sec)",
                min_value=1,
                max_value=60,
                value=st.session_state.settings["refresh_interval"],
            )
            st.session_state.settings["refresh_interval"] = refresh_interval

        # Footer
        st.markdown("---")
        st.caption(f"Last updated: {st.session_state.last_update.strftime('%H:%M:%S')}")
        st.caption("StockAI v1.0.0")


def main():
    """Main application entry point."""
    # Initialize session state
    initialize_session_state()

    # Render header
    render_header()

    # Render sidebar
    render_sidebar()

    # Main content area with tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Dashboard", "🔍 Analysis", "💼 Portfolio", "📈 Monitoring"]
    )

    with tab1:
        render_dashboard()

    with tab2:
        render_analysis_page()

    with tab3:
        render_portfolio_page()

    with tab4:
        render_monitoring_page()

    # Footer
    st.markdown("---")
    st.markdown(
        f"""
        <div class="footer">
            <p><strong>StockAI Trading System</strong> v1.0.0</p>
            <p>Advanced Multi-Agent AI Trading Platform</p>
            <p>Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p style="font-size: 0.8rem; color: #999;">
                ⚠️ For educational and research purposes only. Not financial advice.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Auto-refresh logic - reload state from state manager
    if st.session_state.settings.get("auto_refresh", False):
        import time

        time.sleep(st.session_state.settings.get("refresh_interval", 5))

        # Reload state from state manager
        if STATE_MANAGER is not None:
            try:
                current_state = STATE_MANAGER.load_state()
                st.session_state.trading_active = current_state.get(
                    "trading_active", False
                )
                st.session_state.cycle_count = current_state.get("cycle_count", 0)
                st.session_state.total_decisions = current_state.get(
                    "total_decisions", 0
                )
                st.session_state.total_trades = current_state.get("total_trades", 0)
                st.session_state.successful_trades = current_state.get(
                    "successful_trades", 0
                )
                st.session_state.portfolio = current_state.get("portfolio", {})
                st.session_state.system_health = current_state.get("system_health", {})
                st.session_state.recent_decisions = current_state.get(
                    "recent_decisions", []
                )
                st.session_state.analytics = current_state.get("analytics", {})
                st.session_state.last_update = datetime.now()
            except Exception as e:
                st.error(f"Error refreshing state: {e}")

        st.rerun()


if __name__ == "__main__":
    main()

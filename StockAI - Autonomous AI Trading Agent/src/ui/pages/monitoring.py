# System monitoring page component
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

def render_monitoring_page():
    """Render the system monitoring page."""
    st.subheader("📊 System Monitoring")
    
    # System health metrics
    render_system_health()
    
    # Performance metrics
    render_performance_metrics()
    
    # Logs viewer
    render_logs_viewer()
    
    # Model status
    render_model_status()

def render_system_health():
    """Render system health indicators."""
    st.subheader("🏥 System Health")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🟢 API Status", "Connected", delta="Stable")
    
    with col2:
        st.metric("🟢 Database", "Healthy", delta="99.9%")
    
    with col3:
        st.metric("🟢 Models", "Loaded", delta="5/5")
    
    with col4:
        st.metric("🟡 Memory", "78%", delta="+2%")
    
    # Detailed system metrics
    st.subheader("📊 System Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # CPU Usage
        render_cpu_usage()
    
    with col2:
        # Memory Usage
        render_memory_usage()

def render_cpu_usage():
    """Render CPU usage chart."""
    st.subheader("🖥️ CPU Usage")
    
    # Sample CPU data
    timestamps = pd.date_range(start=datetime.now() - timedelta(hours=1), end=datetime.now(), freq='1min')
    cpu_usage = [20 + (i % 30) for i in range(len(timestamps))]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=cpu_usage,
        mode='lines',
        name='CPU Usage',
        line=dict(color='blue', width=2)
    ))
    
    fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Warning (80%)")
    
    fig.update_layout(
        title="CPU Usage Over Time",
        xaxis_title="Time",
        yaxis_title="CPU Usage (%)",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_memory_usage():
    """Render memory usage chart."""
    st.subheader("💾 Memory Usage")
    
    # Sample memory data
    timestamps = pd.date_range(start=datetime.now() - timedelta(hours=1), end=datetime.now(), freq='1min')
    memory_usage = [60 + (i % 20) for i in range(len(timestamps))]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=memory_usage,
        mode='lines',
        name='Memory Usage',
        line=dict(color='green', width=2)
    ))
    
    fig.add_hline(y=90, line_dash="dash", line_color="red", annotation_text="Critical (90%)")
    
    fig.update_layout(
        title="Memory Usage Over Time",
        xaxis_title="Time",
        yaxis_title="Memory Usage (%)",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_performance_metrics():
    """Render performance metrics."""
    st.subheader("⚡ Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Response Time", "45ms", delta="-5ms")
    
    with col2:
        st.metric("Throughput", "1,234 req/s", delta="+50")
    
    with col3:
        st.metric("Error Rate", "0.1%", delta="-0.05%")
    
    with col4:
        st.metric("Uptime", "99.9%", delta="Stable")
    
    # Request latency chart
    st.subheader("📈 Request Latency")
    
    timestamps = pd.date_range(start=datetime.now() - timedelta(hours=1), end=datetime.now(), freq='1min')
    latency = [40 + (i % 20) for i in range(len(timestamps))]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=latency,
        mode='lines',
        name='Latency',
        line=dict(color='orange', width=2)
    ))
    
    fig.update_layout(
        title="Request Latency Over Time",
        xaxis_title="Time",
        yaxis_title="Latency (ms)",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_logs_viewer():
    """Render system logs viewer."""
    st.subheader("📝 System Logs")
    
    # Log level filter
    log_level = st.selectbox("Filter by Level", ["ALL", "INFO", "WARNING", "ERROR", "DEBUG"])
    
    # Sample logs data
    logs_data = {
        "Timestamp": [
            datetime.now() - timedelta(minutes=1),
            datetime.now() - timedelta(minutes=2),
            datetime.now() - timedelta(minutes=3),
            datetime.now() - timedelta(minutes=4),
            datetime.now() - timedelta(minutes=5),
            datetime.now() - timedelta(minutes=6),
            datetime.now() - timedelta(minutes=7),
            datetime.now() - timedelta(minutes=8)
        ],
        "Level": ["INFO", "INFO", "WARNING", "INFO", "ERROR", "INFO", "DEBUG", "INFO"],
        "Module": ["DecisionEngine", "DataFetcher", "RiskManager", "ExecutionAgent", "API", "PortfolioManager", "Models", "DataFetcher"],
        "Message": [
            "Trade executed: BUY 50 AAPL",
            "Analysis completed for TSLA",
            "Low confidence signal for GOOGL",
            "Portfolio updated successfully",
            "API connection timeout",
            "Risk assessment completed",
            "Model prediction: BUY",
            "Data fetched for MSFT"
        ]
    }
    
    df = pd.DataFrame(logs_data)
    
    # Filter by log level
    if log_level != "ALL":
        df = df[df["Level"] == log_level]
    
    # Color code log levels
    def color_log_level(val):
        if val == "ERROR":
            return "background-color: #f8d7da; color: #721c24"
        elif val == "WARNING":
            return "background-color: #fff3cd; color: #856404"
        elif val == "INFO":
            return "background-color: #d1ecf1; color: #0c5460"
        elif val == "DEBUG":
            return "background-color: #d4edda; color: #155724"
        else:
            return ""
    
    styled_df = df.style.applymap(color_log_level, subset=['Level'])
    st.dataframe(styled_df, use_container_width=True)
    
    # Auto-refresh option
    if st.checkbox("🔄 Auto-refresh logs"):
        time.sleep(5)
        st.rerun()

def render_model_status():
    """Render ML model status."""
    st.subheader("🤖 Model Status")
    
    # Model status table
    model_data = {
        "Model": ["SAC", "PPO", "A2C", "DQN", "TD3"],
        "Status": ["✅ Loaded", "✅ Loaded", "✅ Loaded", "✅ Loaded", "✅ Loaded"],
        "Last Updated": [
            datetime.now() - timedelta(hours=2),
            datetime.now() - timedelta(hours=1),
            datetime.now() - timedelta(hours=3),
            datetime.now() - timedelta(hours=1),
            datetime.now() - timedelta(hours=2)
        ],
        "Accuracy": ["78.5%", "82.1%", "75.3%", "79.8%", "81.2%"],
        "Predictions": [156, 142, 138, 145, 151]
    }
    
    df = pd.DataFrame(model_data)
    st.dataframe(df, use_container_width=True)
    
    # Model performance chart
    st.subheader("📊 Model Performance")
    
    fig = go.Figure(data=[
        go.Bar(
            x=model_data["Model"],
            y=[float(acc.replace('%', '')) for acc in model_data["Accuracy"]],
            marker_color='lightblue'
        )
    ])
    
    fig.update_layout(
        title="Model Accuracy Comparison",
        xaxis_title="Model",
        yaxis_title="Accuracy (%)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

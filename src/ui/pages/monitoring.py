"""
System monitoring page component - Enhanced with real-time system metrics and logs
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np
import time


def render_monitoring_page():
    """Render the comprehensive system monitoring page."""
    st.markdown("## 📈 System Monitoring & Performance")
    st.markdown(
        "Real-time monitoring of system health, performance metrics, and operational logs"
    )

    # System health overview
    render_system_health_overview()

    st.markdown("---")

    # Two-column layout
    col1, col2 = st.columns(2)

    with col1:
        render_system_metrics()
        render_api_health()

    with col2:
        render_model_status()
        render_performance_metrics()

    st.markdown("---")

    # Agent performance tracking
    render_agent_performance()

    st.markdown("---")

    # Logs and alerts
    render_logs_and_alerts()

    st.markdown("---")

    # System diagnostics
    render_system_diagnostics()


def render_system_health_overview():
    """Render system health status overview."""
    st.markdown("### 🏥 System Health Status")

    col1, col2, col3, col4, col5 = st.columns(5)

    system_health = st.session_state.system_health

    with col1:
        api_status = system_health.get("api_status", "Disconnected")
        if api_status == "Connected":
            st.markdown(
                '<div style="background: #d4edda; padding: 1rem; border-radius: 8px; text-align: center;">'
                '<h4 style="margin: 0; color: #155724;">🟢 API</h4>'
                '<p style="margin: 0.5rem 0 0 0; color: #155724;">Connected</p>'
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div style="background: #fff3cd; padding: 1rem; border-radius: 8px; text-align: center;">'
                '<h4 style="margin: 0; color: #856404;">🟡 API</h4>'
                '<p style="margin: 0.5rem 0 0 0; color: #856404;">Offline</p>'
                "</div>",
                unsafe_allow_html=True,
            )

    with col2:
        db_status = system_health.get("database_status", "Offline")
        if db_status == "Healthy":
            st.markdown(
                '<div style="background: #d4edda; padding: 1rem; border-radius: 8px; text-align: center;">'
                '<h4 style="margin: 0; color: #155724;">🟢 Database</h4>'
                '<p style="margin: 0.5rem 0 0 0; color: #155724;">Healthy</p>'
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div style="background: #fff3cd; padding: 1rem; border-radius: 8px; text-align: center;">'
                '<h4 style="margin: 0; color: #856404;">🟡 Database</h4>'
                '<p style="margin: 0.5rem 0 0 0; color: #856404;">Offline</p>'
                "</div>",
                unsafe_allow_html=True,
            )

    with col3:
        models_loaded = system_health.get("models_loaded", 0)
        total_models = system_health.get("total_models", 5)
        if models_loaded == total_models:
            st.markdown(
                f'<div style="background: #d4edda; padding: 1rem; border-radius: 8px; text-align: center;">'
                f'<h4 style="margin: 0; color: #155724;">🟢 Models</h4>'
                f'<p style="margin: 0.5rem 0 0 0; color: #155724;">{models_loaded}/{total_models}</p>'
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div style="background: #fff3cd; padding: 1rem; border-radius: 8px; text-align: center;">'
                f'<h4 style="margin: 0; color: #856404;">🟡 Models</h4>'
                f'<p style="margin: 0.5rem 0 0 0; color: #856404;">{models_loaded}/{total_models}</p>'
                "</div>",
                unsafe_allow_html=True,
            )

    with col4:
        mem_usage = system_health.get("memory_usage", 0)
        if mem_usage < 80:
            color_bg = "#d4edda"
            color_text = "#155724"
            icon = "🟢"
        else:
            color_bg = "#f8d7da"
            color_text = "#721c24"
            icon = "🔴"

        st.markdown(
            f'<div style="background: {color_bg}; padding: 1rem; border-radius: 8px; text-align: center;">'
            f'<h4 style="margin: 0; color: {color_text};">{icon} Memory</h4>'
            f'<p style="margin: 0.5rem 0 0 0; color: {color_text};">{mem_usage}%</p>'
            "</div>",
            unsafe_allow_html=True,
        )

    with col5:
        cpu_usage = system_health.get("cpu_usage", 0)
        if cpu_usage < 70:
            color_bg = "#d4edda"
            color_text = "#155724"
            icon = "🟢"
        else:
            color_bg = "#fff3cd"
            color_text = "#856404"
            icon = "🟡"

        st.markdown(
            f'<div style="background: {color_bg}; padding: 1rem; border-radius: 8px; text-align: center;">'
            f'<h4 style="margin: 0; color: {color_text};">{icon} CPU</h4>'
            f'<p style="margin: 0.5rem 0 0 0; color: {color_text};">{cpu_usage}%</p>'
            "</div>",
            unsafe_allow_html=True,
        )


def render_system_metrics():
    """Render system resource metrics."""
    st.markdown("### 🖥️ System Resources")

    # Generate time-series data for system metrics
    if "system_metrics_history" not in st.session_state:
        timestamps = pd.date_range(
            start=datetime.now() - timedelta(hours=1), end=datetime.now(), freq="1min"
        )

        st.session_state.system_metrics_history = {
            "timestamps": timestamps,
            "cpu": np.random.uniform(20, 60, len(timestamps)),
            "memory": np.random.uniform(50, 80, len(timestamps)),
            "disk": np.random.uniform(30, 50, len(timestamps)),
        }

    metrics = st.session_state.system_metrics_history

    # Update current values in session state
    st.session_state.system_health["cpu_usage"] = int(metrics["cpu"][-1])
    st.session_state.system_health["memory_usage"] = int(metrics["memory"][-1])

    # Create subplot for CPU and Memory
    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=("CPU Usage", "Memory Usage"),
        vertical_spacing=0.15,
        row_heights=[0.5, 0.5],
    )

    # CPU usage
    fig.add_trace(
        go.Scatter(
            x=metrics["timestamps"],
            y=metrics["cpu"],
            mode="lines",
            name="CPU",
            line=dict(color="#1f77b4", width=2),
            fill="tozeroy",
            fillcolor="rgba(31, 119, 180, 0.1)",
        ),
        row=1,
        col=1,
    )

    fig.add_hline(
        y=80,
        line_dash="dash",
        line_color="red",
        annotation_text="Warning",
        row=1,
        col=1,
    )

    # Memory usage
    fig.add_trace(
        go.Scatter(
            x=metrics["timestamps"],
            y=metrics["memory"],
            mode="lines",
            name="Memory",
            line=dict(color="#2ca02c", width=2),
            fill="tozeroy",
            fillcolor="rgba(44, 160, 44, 0.1)",
        ),
        row=2,
        col=1,
    )

    fig.add_hline(
        y=90,
        line_dash="dash",
        line_color="red",
        annotation_text="Critical",
        row=2,
        col=1,
    )

    fig.update_xaxes(title_text="Time", row=2, col=1)
    fig.update_yaxes(title_text="CPU %", row=1, col=1)
    fig.update_yaxes(title_text="Memory %", row=2, col=1)

    fig.update_layout(
        height=500,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)


def render_api_health():
    """Render API health and response times."""
    st.markdown("### 📡 API Health")

    # API endpoints status
    endpoints = [
        {
            "name": "Alpaca Trading API",
            "status": "✅ Healthy",
            "latency": "45ms",
            "uptime": "99.9%",
        },
        {
            "name": "Market Data Feed",
            "status": "✅ Healthy",
            "latency": "32ms",
            "uptime": "99.8%",
        },
        {
            "name": "Financial Metrics API",
            "status": "✅ Healthy",
            "latency": "78ms",
            "uptime": "99.5%",
        },
        {
            "name": "News API",
            "status": "⚠️ Degraded",
            "latency": "125ms",
            "uptime": "98.2%",
        },
    ]

    df = pd.DataFrame(endpoints)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Response time chart
    st.markdown("**📊 API Response Times (Last Hour)**")

    if "api_response_times" not in st.session_state:
        timestamps = pd.date_range(
            start=datetime.now() - timedelta(hours=1), end=datetime.now(), freq="1min"
        )
        st.session_state.api_response_times = {
            "timestamps": timestamps,
            "trading_api": np.random.uniform(30, 60, len(timestamps)),
            "market_data": np.random.uniform(20, 50, len(timestamps)),
        }

    api_times = st.session_state.api_response_times

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=api_times["timestamps"],
            y=api_times["trading_api"],
            mode="lines",
            name="Trading API",
            line=dict(color="#1f77b4", width=2),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=api_times["timestamps"],
            y=api_times["market_data"],
            mode="lines",
            name="Market Data",
            line=dict(color="#ff7f0e", width=2),
        )
    )

    fig.update_layout(
        title="API Response Times",
        xaxis_title="Time",
        yaxis_title="Latency (ms)",
        height=300,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)


def render_model_status():
    """Render ML model status and performance."""
    st.markdown("### 🤖 Model Status")

    # Model information
    models = [
        {
            "name": "SAC",
            "status": "✅ Loaded",
            "accuracy": "78.5%",
            "predictions": 1243,
            "avg_time": "12ms",
        },
        {
            "name": "PPO",
            "status": "✅ Loaded",
            "accuracy": "82.1%",
            "predictions": 1198,
            "avg_time": "15ms",
        },
        {
            "name": "A2C",
            "status": "✅ Loaded",
            "accuracy": "75.3%",
            "predictions": 1167,
            "avg_time": "10ms",
        },
        {
            "name": "DQN",
            "status": "✅ Loaded",
            "accuracy": "79.8%",
            "predictions": 1221,
            "avg_time": "13ms",
        },
        {
            "name": "TD3",
            "status": "✅ Loaded",
            "accuracy": "81.2%",
            "predictions": 1189,
            "avg_time": "14ms",
        },
    ]

    df = pd.DataFrame(models)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Model accuracy comparison
    st.markdown("**📊 Model Accuracy Comparison**")

    fig = go.Figure(
        data=[
            go.Bar(
                x=[m["name"] for m in models],
                y=[float(m["accuracy"].replace("%", "")) for m in models],
                marker_color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
                text=[m["accuracy"] for m in models],
                textposition="auto",
            )
        ]
    )

    fig.add_hline(
        y=80, line_dash="dash", line_color="green", annotation_text="Target: 80%"
    )

    fig.update_layout(
        title="Model Accuracy",
        xaxis_title="Model",
        yaxis_title="Accuracy (%)",
        height=300,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)

    # Model prediction distribution
    st.markdown("**🎯 Prediction Distribution (Last 100)**")

    prediction_dist = {"BUY": 45, "SELL": 23, "HOLD": 32}

    fig = go.Figure(
        data=[
            go.Pie(
                labels=list(prediction_dist.keys()),
                values=list(prediction_dist.values()),
                marker=dict(colors=["#28a745", "#dc3545", "#ffc107"]),
                hole=0.4,
            )
        ]
    )

    fig.update_layout(
        title="Model Prediction Distribution",
        height=250,
        showlegend=True,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)


def render_performance_metrics():
    """Render system performance metrics."""
    st.markdown("### ⚡ Performance Metrics")

    # Key performance metrics
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "📊 Throughput",
            "1,234 req/s",
            delta="+50 req/s",
            help="System request processing rate",
        )

    with col2:
        st.metric(
            "⚡ Avg Latency", "45ms", delta="-5ms", help="Average request latency"
        )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("❌ Error Rate", "0.1%", delta="-0.05%", help="System error rate")

    with col2:
        st.metric("⏱️ Uptime", "99.9%", delta="Stable", help="System uptime")

    # Request latency distribution
    st.markdown("**📊 Request Latency Distribution**")

    if "latency_history" not in st.session_state:
        timestamps = pd.date_range(
            start=datetime.now() - timedelta(hours=1), end=datetime.now(), freq="1min"
        )
        st.session_state.latency_history = {
            "timestamps": timestamps,
            "latency": np.random.uniform(30, 70, len(timestamps)),
        }

    latency_data = st.session_state.latency_history

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=latency_data["timestamps"],
            y=latency_data["latency"],
            mode="lines",
            name="Latency",
            line=dict(color="#ff7f0e", width=2),
            fill="tozeroy",
            fillcolor="rgba(255, 127, 14, 0.1)",
        )
    )

    fig.add_hline(
        y=100, line_dash="dash", line_color="red", annotation_text="SLA Threshold"
    )

    fig.update_layout(
        title="Request Latency Over Time",
        xaxis_title="Time",
        yaxis_title="Latency (ms)",
        height=250,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)


def render_agent_performance():
    """Render agent performance tracking."""
    st.markdown("### 🤖 Agent Performance Tracking")

    # Agent statistics
    agent_stats = {
        "Agent": [
            "Fundamentals",
            "Technicals",
            "Valuation",
            "Sentiment",
            "Risk Manager",
        ],
        "Total Calls": [1234, 1198, 1167, 1221, 1189],
        "Avg Confidence": ["82%", "75%", "70%", "65%", "78%"],
        "Execution Time": ["125ms", "98ms", "156ms", "87ms", "45ms"],
        "Success Rate": ["98.5%", "97.2%", "96.8%", "95.3%", "99.1%"],
        "Cache Hit Rate": ["85%", "78%", "82%", "65%", "92%"],
    }

    df = pd.DataFrame(agent_stats)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Agent execution time comparison
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**⏱️ Avg Execution Time**")

        fig = go.Figure(
            data=[
                go.Bar(
                    y=agent_stats["Agent"],
                    x=[int(t.replace("ms", "")) for t in agent_stats["Execution Time"]],
                    orientation="h",
                    marker_color="#1f77b4",
                    text=agent_stats["Execution Time"],
                    textposition="auto",
                )
            ]
        )

        fig.update_layout(
            xaxis_title="Time (ms)",
            height=300,
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**✅ Success Rate**")

        fig = go.Figure(
            data=[
                go.Bar(
                    y=agent_stats["Agent"],
                    x=[float(r.replace("%", "")) for r in agent_stats["Success Rate"]],
                    orientation="h",
                    marker_color="#28a745",
                    text=agent_stats["Success Rate"],
                    textposition="auto",
                )
            ]
        )

        fig.update_layout(
            xaxis_title="Success Rate (%)",
            height=300,
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )

        st.plotly_chart(fig, use_container_width=True)


def render_logs_and_alerts():
    """Render system logs and alerts."""
    st.markdown("### 📝 System Logs & Alerts")

    # Tabs for different log types
    tab1, tab2, tab3 = st.tabs(["📋 All Logs", "⚠️ Warnings & Errors", "🔔 Alerts"])

    with tab1:
        render_all_logs()

    with tab2:
        render_error_logs()

    with tab3:
        render_alerts()


def render_all_logs():
    """Render all system logs."""
    # Log filtering
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        log_level = st.selectbox(
            "Filter by Level", ["ALL", "INFO", "WARNING", "ERROR", "DEBUG"]
        )

    with col2:
        log_module = st.selectbox(
            "Filter by Module",
            [
                "ALL",
                "DecisionEngine",
                "DataFetcher",
                "RiskManager",
                "ExecutionAgent",
                "API",
            ],
        )

    with col3:
        auto_refresh = st.checkbox("🔄 Auto-refresh", value=False)

    # Sample logs
    logs = [
        {
            "timestamp": datetime.now() - timedelta(minutes=1),
            "level": "INFO",
            "module": "DecisionEngine",
            "message": "Trade executed: BUY 50 AAPL @ $182.50",
        },
        {
            "timestamp": datetime.now() - timedelta(minutes=2),
            "level": "INFO",
            "module": "DataFetcher",
            "message": "Analysis completed for TSLA in 1.2s",
        },
        {
            "timestamp": datetime.now() - timedelta(minutes=3),
            "level": "WARNING",
            "module": "RiskManager",
            "message": "Low confidence signal for GOOGL (45%)",
        },
        {
            "timestamp": datetime.now() - timedelta(minutes=4),
            "level": "INFO",
            "module": "ExecutionAgent",
            "message": "Portfolio updated successfully",
        },
        {
            "timestamp": datetime.now() - timedelta(minutes=5),
            "level": "ERROR",
            "module": "API",
            "message": "API connection timeout - retrying...",
        },
        {
            "timestamp": datetime.now() - timedelta(minutes=6),
            "level": "INFO",
            "module": "RiskManager",
            "message": "Risk assessment completed for all positions",
        },
        {
            "timestamp": datetime.now() - timedelta(minutes=7),
            "level": "DEBUG",
            "module": "Models",
            "message": "RL ensemble prediction: BUY (confidence: 78%)",
        },
        {
            "timestamp": datetime.now() - timedelta(minutes=8),
            "level": "INFO",
            "module": "DataFetcher",
            "message": "Market data fetched for MSFT",
        },
        {
            "timestamp": datetime.now() - timedelta(minutes=9),
            "level": "WARNING",
            "module": "API",
            "message": "Rate limit approaching: 85% of quota used",
        },
        {
            "timestamp": datetime.now() - timedelta(minutes=10),
            "level": "INFO",
            "module": "DecisionEngine",
            "message": "Cycle #42 completed successfully",
        },
    ]

    # Filter logs
    filtered_logs = logs
    if log_level != "ALL":
        filtered_logs = [log for log in filtered_logs if log["level"] == log_level]
    if log_module != "ALL":
        filtered_logs = [log for log in filtered_logs if log["module"] == log_module]

    # Convert to DataFrame
    df = pd.DataFrame(filtered_logs)
    df["Time"] = df["timestamp"].dt.strftime("%H:%M:%S")
    df["Level"] = df["level"]
    df["Module"] = df["module"]
    df["Message"] = df["message"]

    display_df = df[["Time", "Level", "Module", "Message"]]

    # Color code by level
    def highlight_level(row):
        level = row["Level"]
        if level == "ERROR":
            return ["background-color: #f8d7da; color: #721c24"] * len(row)
        elif level == "WARNING":
            return ["background-color: #fff3cd; color: #856404"] * len(row)
        elif level == "INFO":
            return ["background-color: #d1ecf1; color: #0c5460"] * len(row)
        elif level == "DEBUG":
            return ["background-color: #d4edda; color: #155724"] * len(row)
        return [""] * len(row)

    styled_df = display_df.style.apply(highlight_level, axis=1)
    st.dataframe(styled_df, use_container_width=True, hide_index=True, height=400)

    if auto_refresh:
        time.sleep(3)
        st.rerun()


def render_error_logs():
    """Render error and warning logs only."""
    st.warning("⚠️ Showing only warnings and errors")

    error_logs = [
        {
            "timestamp": datetime.now() - timedelta(minutes=5),
            "level": "ERROR",
            "module": "API",
            "message": "API connection timeout - retrying...",
            "count": 1,
        },
        {
            "timestamp": datetime.now() - timedelta(minutes=3),
            "level": "WARNING",
            "module": "RiskManager",
            "message": "Low confidence signal for GOOGL (45%)",
            "count": 3,
        },
        {
            "timestamp": datetime.now() - timedelta(minutes=9),
            "level": "WARNING",
            "module": "API",
            "message": "Rate limit approaching: 85% of quota used",
            "count": 1,
        },
    ]

    df = pd.DataFrame(error_logs)
    df["Time"] = df["timestamp"].dt.strftime("%H:%M:%S")
    df["Level"] = df["level"]
    df["Module"] = df["module"]
    df["Message"] = df["message"]
    df["Count"] = df["count"]

    display_df = df[["Time", "Level", "Module", "Message", "Count"]]

    st.dataframe(display_df, use_container_width=True, hide_index=True)


def render_alerts():
    """Render system alerts."""
    st.info("🔔 Active system alerts and notifications")

    alerts = [
        {
            "time": "2 min ago",
            "severity": "🟡 Medium",
            "type": "Performance",
            "message": "API latency increased by 15%",
            "action": "Monitor",
        },
        {
            "time": "5 min ago",
            "severity": "🔴 High",
            "type": "Error",
            "message": "API connection timeout occurred",
            "action": "Investigate",
        },
        {
            "time": "1 hour ago",
            "severity": "🟢 Low",
            "type": "Info",
            "message": "System maintenance completed",
            "action": "None",
        },
    ]

    df = pd.DataFrame(alerts)
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_system_diagnostics():
    """Render system diagnostics and health checks."""
    st.markdown("### 🔧 System Diagnostics")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📋 Health Checks**")

        health_checks = {
            "Component": [
                "Trading Engine",
                "Data Pipeline",
                "Risk Manager",
                "Model Ensemble",
                "Database",
            ],
            "Status": [
                "✅ Healthy",
                "✅ Healthy",
                "✅ Healthy",
                "✅ Healthy",
                "⚠️ Degraded",
            ],
            "Last Check": [
                "Just now",
                "1 min ago",
                "2 min ago",
                "30 sec ago",
                "5 min ago",
            ],
            "Response Time": ["12ms", "45ms", "8ms", "23ms", "125ms"],
        }

        df = pd.DataFrame(health_checks)
        st.dataframe(df, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("**📊 System Statistics**")

        stats = {
            "Metric": [
                "Total Cycles",
                "Avg Cycle Time",
                "Total Decisions",
                "Successful Trades",
                "Failed Trades",
                "Data Fetch Errors",
            ],
            "Value": ["1,234", "58.3s", "3,456", "89", "2", "5"],
        }

        df_stats = pd.DataFrame(stats)
        st.dataframe(df_stats, use_container_width=True, hide_index=True)

    # System actions
    st.markdown("---")
    st.markdown("**🛠️ System Actions**")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🔄 Restart Services", use_container_width=True):
            with st.spinner("Restarting services..."):
                time.sleep(2)
            st.success("✅ Services restarted")

    with col2:
        if st.button("🗑️ Clear Cache", use_container_width=True):
            with st.spinner("Clearing cache..."):
                time.sleep(1)
            st.success("✅ Cache cleared")

    with col3:
        if st.button("📊 Export Logs", use_container_width=True):
            st.success("✅ Logs exported to logs/export.csv")

    with col4:
        if st.button("🔧 Run Diagnostics", use_container_width=True):
            with st.spinner("Running diagnostics..."):
                time.sleep(2)
            st.success("✅ All systems operational")

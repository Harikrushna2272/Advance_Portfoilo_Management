# StockAI - Sophisticated Streamlit UI

## 🚀 Overview

This is a professional-grade Streamlit UI for the StockAI Advanced Multi-Agent Trading System. The UI provides real-time monitoring, comprehensive analysis, portfolio management, and system health tracking.

## ✨ Features

### 📊 Dashboard
- Real-time KPI metrics (Total Decisions, Trades, Win Rate, P&L)
- Portfolio value chart with 30-day performance
- Portfolio composition (donut chart)
- Signal distribution analysis
- Daily P&L tracking
- Recent trading decisions table
- Agent status monitoring

### 🔍 Analysis
- Deep dive into stock analysis with all 5 agents
- Individual agent analysis with detailed reasoning:
  - Fundamentals Agent (ROE, margins, growth metrics)
  - Technicals Agent (5 strategy breakdown)
  - Valuation Agent (DCF, Owner Earnings)
  - Sentiment Agent (insider trading)
  - Risk Manager (position limits)
- RL Ensemble predictions with model voting
- Portfolio Manager final decision
- Comprehensive technical charts:
  - Candlestick chart with moving averages
  - Bollinger Bands
  - Volume analysis
  - MACD indicator
  - RSI indicator
- Strategy breakdown visualization

### 💼 Portfolio
- Portfolio summary metrics
- Detailed positions table with P&L
- Trade history with status
- Portfolio allocation charts
- Sector allocation
- Risk metrics panel
- Risk analysis:
  - Position-level risk scores
  - Correlation matrix
  - Stress test scenarios
- Manual trade execution interface

### 📈 Monitoring
- System health status (API, Database, Models, CPU, Memory)
- Real-time system resource charts
- API health and response times
- ML model status and performance
- Performance metrics (throughput, latency, error rate)
- Agent performance tracking
- System logs with filtering
- Alerts and notifications
- System diagnostics and actions

## 📦 Installation

### 1. Install Required Dependencies

```bash
# Navigate to project directory
cd /Users/apple/Documents/B.Tech/reading_projects/Advance_Portfoilo_Management

# Install Streamlit and Plotly (if not already installed)
pip install streamlit plotly pandas numpy

# Or using uv
uv pip install streamlit plotly pandas numpy
```

### 2. Verify Installation

```bash
streamlit --version
```

## 🎯 Running the UI

### Option 1: Run from the UI directory

```bash
cd src/ui
streamlit run app.py
```

### Option 2: Run from project root

```bash
streamlit run src/ui/app.py
```

### Option 3: Run with custom port

```bash
streamlit run src/ui/app.py --server.port 8080
```

### Option 4: Run with auto-reload disabled

```bash
streamlit run src/ui/app.py --server.runOnSave false
```

## 🎨 UI Structure

```
src/ui/
├── app.py                 # Main application with navigation
├── pages/
│   ├── dashboard.py       # Dashboard with real-time metrics
│   ├── analysis.py        # Deep analysis with agents & RL
│   ├── portfolio.py       # Portfolio management & risk
│   └── monitoring.py      # System monitoring & logs
```

## 🔧 Configuration

The UI reads configuration from session state and integrates with:
- `src/config/settings.py` - Application settings
- `src/agents/decision_engine.py` - Trading decisions
- `src/agents/execution_agent.py` - Trade execution
- `src/models/rl_ensemble.py` - ML model predictions

## 🎮 How to Use

### 1. Start the System
1. Launch the Streamlit app
2. Click **"▶️ Start"** in the sidebar to activate the trading system
3. The system will show as "ACTIVE" with green indicators

### 2. Configure Settings
- **Trading Universe**: Select stocks to monitor
- **Confidence Threshold**: Set minimum confidence for trades (default: 60%)
- **Quantity Settings**: Configure base and max quantities
- **Cycle Interval**: Set time between trading cycles

### 3. Monitor Dashboard
- View real-time portfolio performance
- Track trading decisions and executions
- Monitor agent status and model predictions

### 4. Run Analysis
1. Go to **🔍 Analysis** tab
2. Select a stock from the dropdown
3. Click **"🔍 Run Analysis"**
4. Review agent signals, RL predictions, and portfolio manager decision
5. Execute trades directly from the analysis page

### 5. Manage Portfolio
- View current positions and P&L
- Check allocation and risk metrics
- Review trade history
- Execute manual trades if needed
- Analyze risk with correlation matrix and stress tests

### 6. Monitor System
- Check system health (API, database, models)
- View resource usage (CPU, memory)
- Monitor API response times
- Track model performance
- Review system logs and alerts

## 🎯 Key Features

### Real-Time Updates
- Auto-refresh option in sidebar
- Configurable refresh interval (1-60 seconds)
- Live data streaming (when integrated with backend)

### Interactive Charts
- Hover over charts for detailed information
- Zoom and pan on time-series data
- Click on data points for more details

### Professional Design
- Modern gradient colors
- Responsive layout
- Custom CSS styling
- Smooth animations
- Color-coded signals (Green=BUY, Red=SELL, Yellow=HOLD)

### Risk Management
- 20% position limit enforcement
- Portfolio concentration tracking
- Stress test scenarios
- Correlation analysis
- Real-time risk scoring

## 📱 Browser Support

The UI works best on:
- Chrome (recommended)
- Firefox
- Safari
- Edge

## 🔍 Demo Mode

The UI currently runs in **demo mode** with simulated data. To connect to the actual trading system:

1. Ensure all backend services are running
2. The UI will automatically detect and connect to:
   - Decision Engine
   - Execution Agent
   - RL Ensemble
   - Market Data APIs

## 🎨 Customization

### Change Theme Colors

Edit the CSS in `app.py`:

```python
# Find the <style> section and modify colors
--primary-color: #1f77b4;  # Change to your color
--success-color: #28a745;
--warning-color: #ffc107;
--danger-color: #dc3545;
```

### Modify Refresh Rate

In the sidebar:
1. Enable "🔄 Auto-refresh"
2. Adjust "Refresh interval" slider (1-60 seconds)

### Add New Metrics

Edit the respective page file in `src/ui/pages/` and add your custom metrics using Streamlit components.

## 🐛 Troubleshooting

### Port Already in Use
```bash
streamlit run app.py --server.port 8501  # Try different port
```

### Import Errors
```bash
# Ensure you're in the correct directory
cd /Users/apple/Documents/B.Tech/reading_projects/Advance_Portfoilo_Management
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Slow Performance
- Disable auto-refresh
- Reduce chart data points
- Clear browser cache

## 📊 Data Flow

```
User Interaction
    ↓
Streamlit UI (app.py)
    ↓
Session State Management
    ↓
Page Components (dashboard, analysis, portfolio, monitoring)
    ↓
Backend Integration (decision_engine, execution_agent, rl_ensemble)
    ↓
Real Trading System
```

## 🚀 Production Deployment

For production deployment:

1. **Use Streamlit Cloud**:
   ```bash
   # Push to GitHub
   # Connect Streamlit Cloud to your repo
   # Deploy automatically
   ```

2. **Use Docker**:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY . .
   RUN pip install streamlit plotly pandas numpy
   EXPOSE 8501
   CMD ["streamlit", "run", "src/ui/app.py"]
   ```

3. **Use PM2**:
   ```bash
   pm2 start "streamlit run src/ui/app.py" --name stockai-ui
   ```

## 📝 Notes

- The UI is designed to work in both **demo mode** and **production mode**
- Demo mode uses simulated data for testing
- Production mode integrates with actual trading system
- All charts and visualizations are interactive
- Data is stored in session state for persistence during the session

## 🎉 Enjoy!

You now have a sophisticated, production-ready UI for your StockAI trading system!

For questions or issues, please refer to the main project documentation.

---

**Version**: 1.0.0  
**Last Updated**: 2025-11-09  
**Author**: StockAI Team

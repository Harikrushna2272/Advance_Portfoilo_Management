# 📊 StockAI Streamlit UI Documentation

## 🎯 Overview

The StockAI Streamlit UI provides a comprehensive web interface for monitoring and controlling your AI trading system. It offers real-time dashboards, portfolio management, market analysis, and system monitoring capabilities.

## 🚀 Features

### **📊 Dashboard**
- **Real-time metrics**: Total decisions, trades executed, success rate, P&L
- **Portfolio composition**: Visual pie chart of asset allocation
- **Performance tracking**: 30-day portfolio performance chart
- **Recent decisions**: Live table of trading decisions with color-coded signals

### **🔍 Market Analysis**
- **Stock selection**: Choose from available stocks for analysis
- **Agent analysis**: Results from all 5 analytical agents
- **RL ensemble**: Individual model predictions and final decision
- **Technical indicators**: Interactive price charts with moving averages and RSI

### **💼 Portfolio Management**
- **Portfolio overview**: Total value, returns, and Sharpe ratio
- **Positions table**: Current holdings with P&L tracking
- **Trade execution**: Manual trade execution interface
- **Allocation charts**: Sector allocation and performance visualization

### **📊 System Monitoring**
- **System health**: API status, database health, model status
- **Performance metrics**: CPU, memory, response time monitoring
- **Logs viewer**: Real-time system logs with filtering
- **Model status**: ML model performance and accuracy tracking

## 🛠️ Installation & Setup

### **Option 1: Docker (Recommended)**

1. **Start the system:**
   ```bash
   make run
   ```

2. **Access the UI:**
   - Open your browser to: http://localhost:8501

### **Option 2: Local Development**

1. **Install dependencies:**
   ```bash
   make install
   ```

2. **Start the UI:**
   ```bash
   make ui
   ```

3. **Access the UI:**
   - Open your browser to: http://localhost:8501

## 🎛️ User Interface Guide

### **Sidebar Controls**

#### **Trading Controls**
- **🚀 Start Trading**: Activates the trading system
- **⏹️ Stop Trading**: Deactivates the trading system

#### **Configuration**
- **📊 Select Stocks**: Choose which stocks to monitor
- **🎯 Confidence Threshold**: Set minimum confidence for trades (50-95%)
- **📦 Base Quantity**: Set default trade quantity (1-1000 shares)

#### **System Status**
- **💰 Portfolio Value**: Current total portfolio value
- **💵 Available Cash**: Available cash for trading
- **📈 Active Positions**: Number of current positions

### **Main Tabs**

#### **📊 Dashboard Tab**
- **Key Metrics**: Overview of trading performance
- **Portfolio Chart**: Visual representation of asset allocation
- **Performance Chart**: Historical portfolio performance
- **Recent Decisions**: Live feed of trading decisions

#### **🔍 Analysis Tab**
- **Stock Selection**: Choose stock for detailed analysis
- **Agent Results**: Individual agent analysis results
- **RL Ensemble**: Machine learning model predictions
- **Technical Charts**: Price charts with indicators

#### **💼 Portfolio Tab**
- **Portfolio Overview**: Key portfolio metrics
- **Positions Table**: Current holdings and P&L
- **Trade Execution**: Manual trade interface
- **Allocation Charts**: Sector allocation visualization

#### **📊 Monitoring Tab**
- **System Health**: Service status indicators
- **Performance Metrics**: System resource usage
- **Logs Viewer**: Real-time system logs
- **Model Status**: ML model performance tracking

## 🎨 UI Components

### **Charts & Visualizations**
- **Plotly Integration**: Interactive charts with zoom, pan, and hover
- **Real-time Updates**: Live data updates every 60 seconds
- **Color Coding**: Green (bullish/BUY), Red (bearish/SELL), Yellow (neutral/HOLD)

### **Data Tables**
- **Styled Tables**: Color-coded signals and P&L
- **Sortable Columns**: Click headers to sort data
- **Responsive Design**: Tables adapt to screen size

### **Metrics Cards**
- **Key Performance Indicators**: Highlighted metrics with deltas
- **Status Indicators**: Visual health status with colors
- **Real-time Values**: Live updating numbers

## 🔧 Configuration

### **Environment Variables**
```bash
# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_THEME_BASE=light

# Trading Configuration
STOCK_LIST=AAPL,TSLA,GOOGL
CONFIDENCE_THRESHOLD=60.0
BASE_QUANTITY=100
```

### **Customization**
- **Themes**: Light/dark theme support
- **Colors**: Customizable color schemes
- **Layout**: Responsive design for different screen sizes
- **Charts**: Configurable chart types and styles

## 📱 Responsive Design

### **Desktop (1200px+)**
- **Full Layout**: All components visible
- **Side-by-side Charts**: Multiple charts in columns
- **Detailed Tables**: Full table data displayed

### **Tablet (768px - 1199px)**
- **Stacked Layout**: Components stack vertically
- **Simplified Tables**: Essential columns only
- **Touch-friendly**: Larger buttons and touch targets

### **Mobile (320px - 767px)**
- **Single Column**: All content in one column
- **Collapsible Sidebar**: Hidden by default
- **Simplified Charts**: Essential data only

## 🔒 Security Features

### **Input Validation**
- **Stock Symbol Validation**: Ensures valid ticker symbols
- **Quantity Limits**: Prevents invalid trade quantities
- **Confidence Bounds**: Validates confidence thresholds

### **Error Handling**
- **Graceful Degradation**: UI continues working with partial data
- **Error Messages**: Clear error notifications
- **Retry Mechanisms**: Automatic retry for failed operations

## 🚀 Performance Optimization

### **Caching**
- **Data Caching**: Reduces API calls and improves response time
- **Chart Caching**: Cached chart data for faster rendering
- **Session State**: Maintains state across page refreshes

### **Real-time Updates**
- **Auto-refresh**: Configurable refresh intervals
- **WebSocket Support**: Real-time data streaming (future)
- **Efficient Rendering**: Only updates changed components

## 🧪 Testing

### **UI Testing**
```bash
# Run UI tests
pytest tests/ui/ -v

# Run specific test
pytest tests/ui/test_dashboard.py -v
```

### **Manual Testing**
- **Cross-browser Testing**: Chrome, Firefox, Safari, Edge
- **Responsive Testing**: Different screen sizes
- **Performance Testing**: Load testing with multiple users

## 🐛 Troubleshooting

### **Common Issues**

#### **UI Not Loading**
```bash
# Check if Streamlit is running
curl http://localhost:8501

# Restart the service
make stop
make run
```

#### **Charts Not Displaying**
- **Check JavaScript**: Ensure JavaScript is enabled
- **Clear Cache**: Clear browser cache and cookies
- **Update Browser**: Use latest browser version

#### **Data Not Updating**
- **Check Backend**: Ensure trading system is running
- **Check Logs**: Review system logs for errors
- **Restart Services**: Restart all services

### **Debug Mode**
```bash
# Run with debug logging
STREAMLIT_LOGGER_LEVEL=debug make ui
```

## 📈 Future Enhancements

### **Planned Features**
- **Real-time WebSocket**: Live data streaming
- **Mobile App**: Native mobile application
- **Advanced Charts**: More technical indicators
- **Alerts System**: Push notifications for trades
- **Backtesting**: Historical strategy testing
- **Social Features**: Share strategies and results

### **API Integration**
- **REST API**: Full API for external integrations
- **Webhook Support**: Real-time event notifications
- **Third-party Integrations**: Broker APIs, news feeds

## 📚 Resources

### **Documentation**
- **Streamlit Docs**: https://docs.streamlit.io/
- **Plotly Docs**: https://plotly.com/python/
- **StockAI Docs**: See README.md and other documentation files

### **Support**
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Community support and discussions
- **Documentation**: Comprehensive guides and tutorials

---

**StockAI Streamlit UI** - Your gateway to intelligent trading! 🚀📈

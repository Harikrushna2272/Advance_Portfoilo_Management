# 🚀 StockAI Streamlit UI - Quick Start Guide

## ⚡ Get Started in 5 Minutes

### **Step 1: Setup**
```bash
# Clone and setup
git clone <your-repo>
cd "StockAI - Autonomous AI Trading Agent"
make setup
```

### **Step 2: Configure**
```bash
# Edit environment file
cp env.example .env
# Add your Alpaca API keys to .env
```

### **Step 3: Start the UI**
```bash
# Option 1: Docker (Recommended)
make run

# Option 2: Local
make install
make ui
```

### **Step 4: Access**
- Open browser to: **http://localhost:8501**
- You'll see the StockAI dashboard!

## 🎛️ Quick Tour

### **Sidebar Controls**
- **🚀 Start Trading**: Activate the trading system
- **📊 Select Stocks**: Choose stocks to monitor
- **🎯 Confidence Threshold**: Set minimum confidence (60% recommended)
- **📦 Base Quantity**: Set default trade size (100 shares recommended)

### **Main Tabs**

#### **📊 Dashboard**
- View real-time trading metrics
- See portfolio performance charts
- Monitor recent trading decisions

#### **🔍 Analysis**
- Select a stock for detailed analysis
- View results from all 5 agents
- See RL ensemble predictions
- Analyze technical indicators

#### **💼 Portfolio**
- Track current positions
- Execute manual trades
- View portfolio allocation
- Monitor P&L

#### **📊 Monitoring**
- Check system health
- View system logs
- Monitor model performance
- Track resource usage

## 🎯 Key Features

### **Real-time Updates**
- Dashboard refreshes every 60 seconds
- Live portfolio tracking
- Real-time decision logging

### **Interactive Charts**
- Click and drag to zoom
- Hover for detailed information
- Multiple chart types (candlestick, line, pie)

### **Color-coded Signals**
- 🟢 **Green**: BUY signals
- 🔴 **Red**: SELL signals  
- 🟡 **Yellow**: HOLD signals

### **Responsive Design**
- Works on desktop, tablet, and mobile
- Adaptive layout for different screen sizes
- Touch-friendly interface

## 🔧 Configuration Tips

### **Recommended Settings**
```bash
# In .env file
STOCK_LIST=AAPL,TSLA,GOOGL,MSFT,AMZN
CONFIDENCE_THRESHOLD=60.0
BASE_QUANTITY=100
CYCLE_INTERVAL=60
```

### **Trading Parameters**
- **Confidence Threshold**: 60-70% for conservative, 50-60% for aggressive
- **Base Quantity**: Start with 100 shares, adjust based on portfolio size
- **Stock Selection**: Choose 3-5 stocks for optimal performance

## 🚨 Important Notes

### **Paper Trading First**
- Always start with paper trading
- Use Alpaca paper trading API
- Test thoroughly before live trading

### **Risk Management**
- Never risk more than you can afford to lose
- Set appropriate position sizes
- Monitor system health regularly

### **API Keys**
- Keep your API keys secure
- Use environment variables
- Never commit keys to version control

## 🆘 Troubleshooting

### **UI Not Loading**
```bash
# Check if port 8501 is available
lsof -i :8501

# Restart the service
make stop
make run
```

### **Charts Not Displaying**
- Enable JavaScript in your browser
- Clear browser cache
- Try a different browser

### **Data Not Updating**
- Check if trading system is running
- Verify API connections
- Check system logs

## 📞 Support

- **Documentation**: See STREAMLIT_UI.md for detailed docs
- **Issues**: Report bugs on GitHub
- **Community**: Join discussions for help

---

**Happy Trading! 🚀📈**

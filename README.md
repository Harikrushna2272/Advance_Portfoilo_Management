# StockAI: Advanced Multi-Agent Trading System

**StockAI** is a sophisticate   │   ├── utils/                      # Utilities
│   │   ├── __init__.py
│   │   ├── logger.py               # Logging utilities
│   │   ├── validators.py           # Input validation
│   │   └── knowledge_graph.py      # Knowledge graph utilities-driven trading system that combines 4 analytical agents with a 5-model ensemble reinforcement learning approach for intelligent trade decision-making. The system processes real-time market data, performs comprehensive analysis, and executes quantity-based trades using the Alpaca API.

## 🎯 System Architecture

The system follows a **4 Agents → 5 RL Models → Portfolio Manager** workflow:

1. **4 Analytical Agents** (no weights) provide market insights
2. **5 RL Models** generate machine learning predictions  
3. **Portfolio Manager** combines all signals and determines final quantity

## ✨ Key Features

### **Real-Time Data Processing**
- **WebSocket Streaming:** Live market data from Alpaca Markets
- **Financial API Integration:** Historical data and fundamentals
- **Data Preprocessing:** 14 technical indicators for RL models

### **Multi-Agent Analysis System**
- **Fundamentals Agent:** Company financial health analysis
- **Technicals Agent:** Price action and pattern recognition
- **Valuation Agent:** Intrinsic value and DCF analysis
- **Sentiment Agent:** Advanced sentiment analysis with knowledge graphs
  - Company relationships and network effects
  - News sentiment analysis using NLP
  - Insider trading patterns
  - Weighted multi-factor sentiment scoring
- **Risk Manager:** Portfolio risk assessment

### **Knowledge Graph Integration**
- **Company Relationships:** Maps connections between companies
- **News Impact Analysis:** NLP-based sentiment extraction
- **Network Effect Modeling:** Relationship strength calculation
- **Multi-Source Sentiment:** Combines news, relationships, and insider data
- **Weighted Decision Making:** 60% knowledge graph, 40% insider trading

### **5-Model RL Ensemble**
- **SAC (Soft Actor-Critic):** Continuous action space optimization
- **PPO (Proximal Policy Optimization):** Stable policy updates
- **A2C (Advantage Actor-Critic):** Fast real-time learning
- **DQN (Deep Q-Network):** Discrete action space decisions
- **TD3 (Twin Delayed Deep Deterministic):** Robust continuous control

### **Intelligent Portfolio Management**
- **Quantity-Based Trading:** Specific share quantities for each trade
- **Risk-Adjusted Position Sizing:** Dynamic quantity calculation
- **Confidence-Based Execution:** Only trades with >60% confidence
- **Real-Time Portfolio Tracking:** Continuous position monitoring

## 📁 Project Structure

```
StockAI - Autonomous AI Trading Agent/
├── src/                            # Source code (modular structure)
│   ├── __init__.py                 # Package initialization
│   ├── main.py                     # Main application entry point
│   ├── core/                       # Core business logic
│   │   ├── __init__.py
│   │   ├── decision_engine.py      # Decision making engine
│   │   └── portfolio_manager.py    # Portfolio management
│   ├── agents/                     # Analytical agents
│   │   ├── __init__.py
│   │   ├── data_fetcher.py         # Real-time data acquisition
│   │   ├── execution_agent.py      # Trade execution
│   │   ├── fundamentals_agent.py   # Financial analysis
│   │   ├── technicals_agent.py     # Technical analysis
│   │   ├── valuation_agent.py      # Valuation analysis
│   │   ├── sentiment_agent.py      # Sentiment analysis
│   │   └── risk_manager.py         # Risk assessment
│   ├── models/                     # Machine learning models
│   │   ├── __init__.py
│   │   ├── ensemble_model.py       # 5-model RL ensemble
│   │   └── training_modedl.py      # Model training
│   ├── data/                       # Data processing
│   │   ├── __init__.py
│   │   └── preprocessor.py         # Feature engineering
│   ├── utils/                      # Utilities
│   │   ├── __init__.py
│   │   ├── logger.py               # Logging utilities
│   │   └── validators.py           # Input validation
│   ├── config/                     # Configuration
│   │   ├── __init__.py
│   │   └── settings.py             # Application settings
│   └── ui/                         # Streamlit Web UI
│       ├── __init__.py
│       ├── app.py                  # Main UI application
│       ├── streamlit_app.py        # Simplified Streamlit app
│       ├── pages/                  # UI page components
│       │   ├── dashboard.py        # Dashboard page
│       │   ├── analysis.py         # Analysis page
│       │   ├── portfolio.py        # Portfolio page
│       │   └── monitoring.py       # Monitoring page
│       ├── components/             # Reusable UI components
│       └── utils/                  # UI utilities
├── tests/                          # Test suite
│   ├── unit/                       # Unit tests
│   └── integration/                # Integration tests
├── docker/                         # Docker configuration
│   ├── init.sql                    # Database initialization
│   ├── prometheus.yml              # Monitoring config
│   └── grafana/                    # Grafana dashboards
├── logs/                           # Application logs
├── models/                         # Trained model files
├── data/                           # Data storage
├── Dockerfile                      # Container definition
├── docker-compose.yml              # Multi-container setup
├── Makefile                        # Development commands
├── requirements.txt                # Python dependencies
├── env.example                     # Environment template
└── README.md                       # This file
```

## 🚀 Installation

### **Option 1: Docker (Recommended)**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your_username/StockAI.git
   cd StockAI
   ```

2. **Setup Environment:**
   ```bash
   make setup
   # Edit .env file with your API keys
   ```

3. **Run with Docker:**
   ```bash
   make run
   ```

### **Option 2: Local Development**

1. **Clone and Setup:**
   ```bash
   git clone https://github.com/your_username/StockAI.git
   cd StockAI
   make setup
   ```

2. **Install Dependencies:**
   ```bash
   make install
   ```
   
   **Note:** Make sure to install TA-Lib and other dependencies separately if you encounter issues:
   ```bash
   # On macOS
   brew install ta-lib
   pip install TA-Lib
   
   # On Ubuntu/Debian
   sudo apt-get install libta-lib-dev
   pip install TA-Lib
   
   # Install spaCy language model (required for sentiment analysis)
   python -m spacy download en_core_web_sm
   ```

3. **Configure Environment:**
   Copy and edit the environment file:
   ```bash
   cp env.example .env
   # Edit .env with your API keys and configuration
   ```

4. **Train RL Models:**
   ```bash
   python src/models/training_modedl.py
   ```

## 🔄 Workflow Overview

### **Step 1: Data Acquisition**
- Real-time WebSocket data streaming
- Historical data from financial APIs
- 14 technical indicators preprocessing

### **Step 2: Multi-Agent Analysis**
- **Fundamentals:** ROE, margins, growth metrics
- **Technicals:** Trend, momentum, volatility analysis
- **Valuation:** DCF, owner earnings, market comparison
- **Sentiment:** 
  - Knowledge graph-based relationship analysis
  - News sentiment using NLP
  - Insider trading patterns
  - Network effect calculations
  - Weighted sentiment scoring (60% KG, 40% insider)
- **Risk:** Position limits and portfolio assessment

### **Step 3: RL Ensemble Prediction**
- 5 RL models process preprocessed features
- Equal 20% weight for each model
- Majority voting for ensemble decision

### **Step 4: Portfolio Manager Decision**
- Combines agent consensus with RL prediction
- Calculates optimal quantity based on confidence
- Applies risk adjustments for position sizing

### **Step 5: Trade Execution**
- Executes trades with specific quantities
- Only trades with >60% confidence
- Real-time portfolio tracking

## 🎯 Usage

### **Docker Commands:**
```bash
# Start the system
make run

# View logs
make logs

# Stop the system
make stop

# Clean up
make clean
```

### **Development Commands:**
```bash
# Run locally
make dev

# Start Streamlit UI
make ui

# Run tests
make test

# Format code
make format

# Run linting
make lint
```

### **Monitoring:**
```bash
# View monitoring dashboards
make monitor
# Streamlit UI: http://localhost:8501
# Grafana: http://localhost:3000 (admin/admin)
# Prometheus: http://localhost:9090
```

### **Database Operations:**
```bash
# Reset database
make db-reset

# Create backup
make backup

# Restore backup
make restore
```

## 🖥️ Streamlit Web UI

StockAI includes a comprehensive web interface built with Streamlit:

### **Features:**
- **📊 Real-time Dashboard**: Live trading metrics and portfolio performance
- **🔍 Market Analysis**: Interactive stock analysis with technical indicators
- **💼 Portfolio Management**: Position tracking and manual trade execution
- **📊 System Monitoring**: Health status, logs, and model performance

### **Quick Start:**
```bash
# Start the UI
make ui

# Access at: http://localhost:8501
```

### **UI Components:**
- **Dashboard**: Portfolio overview, performance charts, recent decisions
- **Analysis**: Stock selection, agent results, RL ensemble predictions
- **Portfolio**: Position management, trade execution, allocation charts
- **Monitoring**: System health, performance metrics, logs viewer

For detailed UI documentation, see [STREAMLIT_UI.md](STREAMLIT_UI.md)

## 📊 Example Output

```
🚀 Starting StockAI - Advanced Multi-Agent Trading System...
📊 Portfolio initialized with $100,000
🎯 Monitoring 3 stocks: AAPL, TSLA, GOOGL

🔄 === CYCLE #1 - 2024-01-15 10:30:00 ===

📈 Analyzing AAPL...
📊 Fundamentals: bullish (80%)
📊 Technicals: neutral (65%)
📊 Valuation: bullish (75%)
📊 Sentiment: bearish (60%)
📊 Risk: neutral (70%)

🤖 Getting 5 RL Models ensemble decision...
🎯 SAC: BUY (prediction: 1)
🎯 PPO: BUY (prediction: 1)
🎯 A2C: HOLD (prediction: 0)
🎯 DQN: BUY (prediction: 1)
🎯 TD3: SELL (prediction: -1)
🎯 RL Ensemble: BUY (confidence: 40%, score: 0.400)

🎯 Portfolio Manager making final decision...
🎯 Final Decision: BUY
📊 Confidence: 44.0%
📦 Quantity: 30 shares
📈 Agent Consensus: neutral ({'bullish': 2, 'bearish': 1, 'neutral': 2})
🤖 RL Decision: BUY (40%)

💼 Executing BUY order for AAPL: 30 shares
✅ Trade execution completed for AAPL: BUY 30 shares
```

## ⚙️ Configuration

### **Stock List**
Update `utils/config.py` to monitor different stocks:
```python
STOCK_LIST = ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN"]
```

### **RL Model Paths**
Configure your trained model paths:
```python
ENSEMBLE_MODEL_PATHS = [
    "models/trained_rl_model_sac.pkl",
    "models/trained_rl_model_ppo.pkl",
    "models/trained_rl_model_a2c.pkl",
    "models/trained_rl_model_dqn.pkl",
    "models/trained_rl_model_td3.pkl"
]
```

### **Trading Parameters**
- **Confidence Threshold:** 60% minimum for trade execution
- **Base Quantity:** 100 shares (adjustable)
- **Risk Multipliers:** 0.5x (high risk) to 1.2x (low risk)
- **Cycle Interval:** 60 seconds

## 🛡️ Risk Management

- **Position Limits:** Maximum 20% of portfolio per stock
- **Cash Management:** Maintains minimum cash reserves
- **Confidence Filtering:** Only executes high-confidence trades
- **Error Handling:** Graceful degradation on failures
- **Paper Trading:** Test with Alpaca paper trading first

## 📈 Performance Features

- **Real-Time Monitoring:** 60-second analysis cycles
- **Decision History:** Tracks all trading decisions
- **Performance Metrics:** Accuracy and signal distribution
- **Error Logging:** Comprehensive error tracking
- **Portfolio Tracking:** Real-time position monitoring

## 🔧 Dependencies

- **pandas:** Data manipulation and analysis
- **numpy:** Numerical computations
- **joblib:** Model serialization
- **stable_baselines3:** Reinforcement learning models
- **talib:** Technical analysis indicators
- **alpaca-trade-api:** Trade execution
- **websocket-client:** Real-time data streaming
- **requests:** API communications

## 📚 Documentation

- **NEW_WORKFLOW.md:** Detailed workflow explanation
- **Code Comments:** Comprehensive inline documentation
- **Example Outputs:** Sample decision processes
- **Configuration Guide:** Setup and customization

## ⚠️ Disclaimer

This system is for educational and research purposes. Always test with paper trading before using real money. Past performance does not guarantee future results. Trading involves risk of loss.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Reference : 

- **reference**: [GitHub Discussions](https://github.com/virattt/ai-hedge-fund)


## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**StockAI** - Advanced Multi-Agent Trading System with Ensemble Reinforcement Learning 🚀

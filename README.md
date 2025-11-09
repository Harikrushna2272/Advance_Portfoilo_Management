# StockAI: Advanced Multi-Agent Portfolio Management System

**StockAI** is a production-ready, AI-powered algorithmic trading system that combines **4 specialized AI agents** with a **5-model ensemble reinforcement learning** approach for intelligent, data-driven trading decisions. The system processes real-time market data, performs comprehensive multi-factor analysis, and executes quantity-based trades using the Alpaca API.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🎯 System Architecture

The system follows a **Data Collection → Multi-Agent Analysis → RL Ensemble → Decision → Execution** workflow:

```
┌─────────────────────────────────────────────────────────────┐
│                    TRADING WORKFLOW                         │
│                 (Orchestrates Everything)                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌─────────────┐ ┌────────────────┐
│ DATA LAYER   │ │ ANALYSIS    │ │ EXECUTION      │
├──────────────┤ ├─────────────┤ ├────────────────┤
│• API Tools   │ │• 4 AI Agents│ │• Portfolio Exec│
│• Caching     │ │• 5 RL Models│ │• Alpaca Trader │
│• Validation  │ │• Decision   │ │• Risk Controls │
│• Preprocess  │ │  Engine     │ │• Order Mgmt    │
└──────────────┘ └─────────────┘ └────────────────┘
```

### Core Components

1. **Data Collection Layer** - Real-time and historical market data
2. **4 Analytical Agents** - Multi-perspective market analysis
3. **5-Model RL Ensemble** - Machine learning predictions
4. **Decision Engine** - Consensus-based decision making
5. **Portfolio Executor** - Risk-managed trade execution
6. **Alpaca Integration** - Live trading and paper trading

## ✨ Key Features

### **Real-Time Data Processing**
- **Financial APIs Integration:** Historical prices, fundamentals, insider trading
- **Smart Caching:** In-memory caching to reduce API costs
- **Data Validation:** Automatic quality checks and preprocessing
- **14 Technical Indicators:** MACD, RSI, Bollinger Bands, SMAs, and more

### **Multi-Agent Analysis System**
- **🏢 Fundamentals Agent:** 
  - Financial health analysis (ROE, margins, growth)
  - Profitability and efficiency metrics
  - Returns: signal (bullish/bearish/neutral) + confidence score

- **📈 Technicals Agent:** 
  - Price action and pattern recognition
  - MACD, RSI, moving average analysis
  - Trend and momentum indicators

- **💰 Valuation Agent:** 
  - Intrinsic value calculation using DCF
  - Owner earnings analysis
  - P/E ratio and market comparison

- **🧠 Sentiment Agent:** 
  - Insider trading pattern analysis
  - Buying vs. selling behavior tracking
  - Weighted sentiment scoring

- **🛡️ Risk Manager:** 
  - Portfolio risk assessment
  - Position limit validation (max 20% per stock)
  - Risk scoring and multipliers

### **5-Model RL Ensemble**
Trained models for robust predictions:
- **SAC (Soft Actor-Critic):** Continuous action optimization
- **PPO (Proximal Policy Optimization):** Stable policy updates
- **A2C (Advantage Actor-Critic):** Fast real-time learning
- **TD3 (Twin Delayed DDPG):** Robust continuous control
- **DDPG (Deep Deterministic Policy Gradient):** Deterministic actions

**Ensemble Strategy:**
- Equal 20% weight per model
- Majority voting mechanism
- Confidence scoring from agreement level
- Graceful handling of individual model failures

### **Intelligent Decision Engine**
- **Consensus Building:** Combines 4 agent signals democratically (no hardcoded weights)
- **RL Integration:** Incorporates 5-model ensemble predictions
- **Confidence Scoring:** Weighted confidence calculation
- **Quantity Determination:** Dynamic position sizing based on:
  - Overall confidence level
  - Risk assessment scores
  - Portfolio constraints
  - Available buying power

### **Risk-Managed Execution**
- **Position Limits:** Maximum 20% portfolio allocation per stock
- **Confidence Threshold:** Only trades with ≥60% confidence
- **Buying Power Checks:** Validates cash availability
- **Order Tracking:** Real-time order status monitoring
- **Paper Trading:** Safe testing environment before live trading

### **Professional Web UI (Streamlit)**
- **📊 Real-time Dashboard:** Portfolio metrics, performance charts
- **🔍 Stock Analysis:** Interactive analysis with agent results
- **💼 Portfolio Management:** Position tracking, manual execution
- **📈 System Monitoring:** Health status, logs, performance metrics
- **⚙️ Configuration Panel:** Dynamic settings management

## 📁 Project Structure

```
Advance_Portfoilo_Management/
├── src/                            # Main source code
│   ├── main.py                     # Modern async entry point
│   ├── config/
│   │   └── settings.py             # Pydantic-based configuration
│   ├── agents/                     # AI Agents (9 files)
│   │   ├── fundamentals_agent.py   # Financial health analysis
│   │   ├── technicals_agent.py     # Technical analysis
│   │   ├── valuation_agent.py      # Intrinsic value calculation
│   │   ├── sentiment_agent.py      # Sentiment analysis
│   │   ├── risk_manager.py         # Risk assessment
│   │   ├── portfolio_manager.py    # Portfolio decisions
│   │   ├── decision_engine.py      # Master orchestrator
│   │   ├── execution_agent.py      # Trade execution interface
│   │   └── data_fetcher.py         # Data acquisition
│   ├── models/                     # Machine Learning (3 files)
│   │   ├── rl_ensemble.py          # 5-model ensemble (KEY)
│   │   ├── ensemble_model.py       # Legacy wrapper
│   │   └── training_modedl.py      # Model training pipeline
│   ├── trading/                    # Trading System (3 files)
│   │   ├── alpaca_trader.py        # Alpaca API integration (KEY)
│   │   ├── portfolio_executor.py   # Execution engine
│   │   └── trading_workflow.py     # Complete workflow (KEY)
│   ├── data/                       # Data Management (4 files)
│   │   ├── models.py               # Pydantic data models
│   │   ├── cache.py                # API response caching
│   │   └── preprocessor.py         # Data preprocessing
│   ├── tools/
│   │   └── api.py                  # Financial data APIs (KEY)
│   ├── utils/                      # Utilities
│   │   ├── logger.py               # Logging system
│   │   ├── validators.py           # Input validation
│   │   ├── knowledge_graph.py      # Knowledge graph
│   │   └── data_preprocessor.py    # RL preprocessing (KEY)
│   └── ui/                         # Streamlit Web UI (5 files)
│       ├── app.py                  # Main UI application (KEY)
│       └── pages/                  # UI page components
│           ├── dashboard.py        # Dashboard page
│           ├── analysis.py         # Analysis page
│           ├── portfolio.py        # Portfolio page
│           └── monitoring.py       # Monitoring page
├── models/                         # Trained RL model files
│   ├── agent_sac.zip              # SAC model
│   ├── agent_ppo.zip              # PPO model
│   ├── agent_a2c.zip              # A2C model
│   ├── agent_td3.zip              # TD3 model
│   └── agent_ddpg.zip             # DDPG model
├── tests/                          # Test suite
│   ├── unit/                       # Unit tests
│   └── integration/                # Integration tests
├── docker/                         # Docker configuration
├── logs/                           # Application logs
├── data/                           # Data storage
├── Dockerfile                      # Container definition
├── docker-compose.yml              # Multi-container setup
├── Makefile                        # Development commands
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables
├── env.example                    # Environment template
├── main.py                        # Legacy entry point
├── test_system.py                 # System tests
└── README.md                      # This file
```

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8 or higher
- pip package manager
- API keys (Alpaca, Financial Datasets, optional OpenAI)

### **Option 1: Docker (Recommended)**

1. **Clone and Setup:**
   ```bash
   git clone <repository-url>
   cd Advance_Portfoilo_Management
   cp env.example .env
   # Edit .env with your API keys
   ```

2. **Run with Docker:**
   ```bash
   docker-compose up -d
   ```

3. **Access Services:**
   - Streamlit UI: http://localhost:8501
   - Grafana: http://localhost:3000 (admin/admin)
   - Prometheus: http://localhost:9090

### **Option 2: Local Development**

1. **Clone Repository:**
   ```bash
   git clone <repository-url>
   cd Advance_Portfoilo_Management
   ```

2. **Setup Environment:**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   **Optional but Recommended (for advanced technical analysis):**
   ```bash
   # On macOS
   brew install ta-lib
   pip install TA-Lib
   
   # On Ubuntu/Debian
   sudo apt-get install libta-lib-dev
   pip install TA-Lib
   ```

4. **Run the System:**
   
   **Option A: Complete Trading Workflow (Recommended)**
   ```bash
   python src/trading/trading_workflow.py
   ```

   **Option B: Modern Async Entry Point**
   ```bash
   python src/main.py
   ```

   **Option C: Streamlit Web UI**
   ```bash
   streamlit run src/ui/app.py
   ```

   **Option D: Legacy Entry Point**
   ```bash
   python main.py
   ```

## ⚙️ Configuration

### **Required Environment Variables**

Create a `.env` file in the project root:

```env
# === API Keys ===
# Alpaca Trading (Required) - Get at: https://alpaca.markets
ALPACA_API_KEY=your_alpaca_api_key
ALPACA_API_SECRET=your_alpaca_api_secret
ALPACA_BASE_URL=https://paper-api.alpaca.markets  # Paper trading

# Financial Data API (Required) - Get at: https://financialdatasets.ai
FINANCIAL_DATASETS_API_KEY=your_financial_datasets_key

# OpenAI (Optional but recommended for advanced reasoning)
OPENAI_API_KEY=your_openai_api_key

# === Trading Settings ===
STOCK_LIST=AAPL,MSFT,GOOGL,TSLA,AMZN
CONFIDENCE_THRESHOLD=60.0
MAX_POSITION_PCT=0.20
BASE_QUANTITY=100
INITIAL_CASH=100000.0

# === System Settings ===
DEBUG=false
LOG_LEVEL=INFO
CHECK_INTERVAL=60  # seconds
```

### **Trading Parameters**

Edit `src/config/settings.py` or use environment variables:

- **`STOCK_LIST`**: Comma-separated ticker symbols to monitor
- **`CONFIDENCE_THRESHOLD`**: Minimum confidence for trade execution (default: 60%)
- **`MAX_POSITION_PCT`**: Maximum portfolio allocation per stock (default: 20%)
- **`BASE_QUANTITY`**: Base share quantity for trades (default: 100)
- **`CHECK_INTERVAL`**: Seconds between trading cycles (default: 60)

### **Model Paths**

Pre-trained models are located in `models/`:
- `agent_sac.zip` - Soft Actor-Critic
- `agent_ppo.zip` - Proximal Policy Optimization
- `agent_a2c.zip` - Advantage Actor-Critic
- `agent_td3.zip` - Twin Delayed DDPG
- `agent_ddpg.zip` - Deep Deterministic Policy Gradient

## 🔄 Complete Trading Workflow

### **Step-by-Step Execution**

#### **1. Initialize System** (Once)
- Load configuration from `.env`
- Initialize Alpaca connection (paper or live trading)
- Load 5 RL models from `models/` directory
- Create decision engine with all 4 agents
- Setup portfolio tracking and logging

#### **2. Check Market Status** (Each Cycle)
- Query Alpaca API for market hours
- Skip cycle if market is closed
- Log next market open time if closed

#### **3. Fetch Account Data**
- Get current cash balance
- Get buying power
- Get all current positions
- Calculate total portfolio value

#### **4. For Each Stock in Watchlist:**

**a) Data Collection** (`src/tools/api.py`)
```
→ Fetch 30 days historical prices
→ Get financial metrics (P/E, ROE, margins, growth)
→ Get insider trading data
→ Cache all responses (in-memory TTL cache)
```

**b) Agent Analysis** (Parallel Execution)
```
Fundamentals Agent → Analyzes 4 aspects:
  • Profitability (ROE, ROA, margins)
  • Growth (revenue, earnings growth)
  • Financial Health (debt ratios, liquidity)
  • Efficiency (asset turnover, ratios)
  → Returns: {signal: "bullish/bearish/neutral", confidence: 0-100, reasoning: "..."}

Technicals Agent → Calculates indicators:
  • MACD (trend following)
  • RSI (momentum oscillator)
  • Moving averages (SMA crossovers)
  → Returns: {signal, confidence, reasoning}

Valuation Agent → Computes:
  • DCF (Discounted Cash Flow)
  • Owner earnings
  • P/E ratio comparison
  → Returns: {signal, confidence, reasoning}

Sentiment Agent → Analyzes:
  • Insider buying vs. selling
  • Transaction patterns
  • Weighted sentiment scoring
  → Returns: {signal, confidence, reasoning}
```

**c) RL Data Preprocessing** (`src/utils/data_preprocessor.py`)
```
Calculate 14 technical features:
  1. Open price (normalized)
  2. High price
  3. Low price
  4. Close price
  5. Volume
  6. Day of week (0-4)
  7. MACD
  8. Bollinger Band Upper
  9. Bollinger Band Lower
  10. RSI_30
  11. CCI_30 (Commodity Channel Index)
  12. DX_30 (Directional Index)
  13. SMA_30 (30-day moving average)
  14. SMA_60 (60-day moving average)

→ Handle missing values (forward fill)
→ Normalize features
→ Create observation array (14 floats)
```

**d) RL Ensemble Prediction** (`src/models/rl_ensemble.py`)
```
Pass observation to 5 models:
  SAC → predicts action (BUY=1, HOLD=0, SELL=-1)
  PPO → predicts action
  A2C → predicts action
  TD3 → predicts action
  DDPG → predicts action

Voting mechanism:
  • Count votes for BUY/HOLD/SELL
  • Majority wins
  • Calculate confidence from agreement:
    - 5/5 agreement = 100% confidence
    - 4/5 agreement = 80% confidence
    - 3/5 agreement = 60% confidence

→ Returns: {action: "BUY/HOLD/SELL", confidence: 0-100}
```

**e) Decision Engine** (`src/agents/decision_engine.py`)
```
Combine signals:
  1. Count agent consensus (4 agents vote)
     • bullish_count, bearish_count, neutral_count
  
  2. Get RL ensemble decision
     • action + confidence
  
  3. Calculate weighted confidence:
     • agent_weight = average of 4 agent confidences
     • rl_weight = ensemble confidence
     • final_confidence = 0.5 * agent_weight + 0.5 * rl_weight
  
  4. Determine final signal:
     • If majority bullish + RL=BUY → BUY
     • If majority bearish + RL=SELL → SELL
     • Otherwise → HOLD
  
  5. Calculate quantity:
     • base_quantity = 100 shares
     • confidence_multiplier = final_confidence / 100
     • risk_multiplier = from risk_manager (0.5x to 1.2x)
     • quantity = base_quantity * confidence_multiplier * risk_multiplier

→ Returns: {signal, confidence, quantity, reasoning}
```

**f) Risk Validation** (`src/agents/risk_manager.py`)
```
Check constraints:
  ✓ Position limit: new_position ≤ 20% of portfolio value
  ✓ Confidence threshold: confidence ≥ 60%
  ✓ Buying power: cost ≤ available cash
  ✓ Minimum quantity: quantity > 0

If any check fails → reject trade
→ Returns: {valid: true/false, reason: "..."}
```

**g) Trade Execution** (`src/trading/alpaca_trader.py`)
```
If signal = BUY and valid:
  → Submit market buy order to Alpaca
  → Track order ID
  → Wait for fill confirmation
  → Update positions

If signal = SELL and valid:
  → Submit market sell order
  → Track order ID
  → Wait for fill confirmation
  → Update positions

If signal = HOLD or invalid:
  → Skip trade
  → Log reason
```

**h) Update Portfolio**
```
→ Refresh current positions from Alpaca
→ Update cost basis
→ Calculate unrealized P/L
→ Update portfolio value
```

#### **5. Cycle Summary**
```
→ Log all decisions made
→ Show signal distribution (BUY/SELL/HOLD counts)
→ Report trades executed
→ Log any errors encountered
```

#### **6. Performance Tracking** (Every 10 cycles)
```
→ Calculate average confidence
→ Show signal distribution
→ Display win rate (if tracking)
→ Log system statistics
```

#### **7. Wait for Next Cycle**
```
→ Sleep for CHECK_INTERVAL seconds (default: 60)
→ Repeat from Step 2
```

### **Data Flow Diagram**

```
┌─────────────────────────────────────────────────┐
│         Financial Data APIs                     │
│  (Financial Datasets, Alpaca Market Data)       │
└────────────┬────────────────────────────────────┘
             │
             ├─→ Price Data (OHLCV, 30 days)
             ├─→ Financial Metrics (P/E, ROE, margins)
             ├─→ Insider Trades (buying/selling patterns)
             └─→ Market Cap, Line Items
                        │
                        ▼
             ┌─────────────────────┐
             │   Cache Layer       │
             │  (In-Memory, TTL)   │
             └─────────────────────┘
                        │
          ┌─────────────┴─────────────┐
          │                           │
          ▼                           ▼
┌───────────────────┐      ┌──────────────────────┐
│  4 AI Agents      │      │  Data Preprocessor   │
│  (Parallel)       │      │  (14 Features)       │
├───────────────────┤      ├──────────────────────┤
│• Fundamentals     │      │• MACD, RSI, BBands   │
│• Technicals       │      │• SMAs, CCI, DX       │
│• Valuation        │      │• Normalization       │
│• Sentiment        │      │• Validation          │
└─────────┬─────────┘      └──────────┬───────────┘
          │                           │
          │                           ▼
          │                ┌─────────────────────┐
          │                │  5 RL Models        │
          │                │  (Ensemble)         │
          │                ├─────────────────────┤
          │                │• SAC (20% weight)   │
          │                │• PPO (20% weight)   │
          │                │• A2C (20% weight)   │
          │                │• TD3 (20% weight)   │
          │                │• DDPG (20% weight)  │
          │                │  ↓                  │
          │                │  Majority Voting    │
          │                └──────────┬──────────┘
          │                           │
          └───────────┬───────────────┘
                      ▼
          ┌─────────────────────────┐
          │   Decision Engine       │
          │  (Master Orchestrator)  │
          ├─────────────────────────┤
          │• Combine agent consensus│
          │• Integrate RL prediction│
          │• Calculate confidence   │
          │• Determine quantity     │
          └───────────┬─────────────┘
                      │
                      ▼
          ┌─────────────────────────┐
          │   Risk Manager          │
          │  (Validation)           │
          ├─────────────────────────┤
          │• Position limits (20%)  │
          │• Confidence threshold   │
          │• Buying power check     │
          └───────────┬─────────────┘
                      │
                      ▼
          ┌─────────────────────────┐
          │   Alpaca Trader         │
          │  (Execution)            │
          ├─────────────────────────┤
          │• Submit orders          │
          │• Track fills            │
          │• Update positions       │
          └─────────────────────────┘
```

## 📊 Example Output

```bash
🚀 Starting StockAI Trading System...
📊 Initializing portfolio with $100,000.00
🔧 Loading 5 RL models...
  ✓ SAC model loaded
  ✓ PPO model loaded
  ✓ A2C model loaded
  ✓ TD3 model loaded
  ✓ DDPG model loaded
🎯 Monitoring stocks: AAPL, MSFT, GOOGL

🔄 === TRADING CYCLE #1 === [2024-01-15 10:30:15]

📈 Analyzing AAPL...
  💰 Current price: $185.43
  📊 Market cap: $2.89T
  
  🤖 Agent Analysis:
    • Fundamentals: BULLISH (confidence: 82%)
      ↳ Strong ROE (28.5%), high margins (25.3%), steady growth
    • Technicals: NEUTRAL (confidence: 68%)
      ↳ MACD positive, RSI at 58 (neutral zone)
    • Valuation: BULLISH (confidence: 75%)
      ↳ DCF value $195, current price undervalued
    • Sentiment: BEARISH (confidence: 60%)
      ↳ Recent insider selling detected
  
  📊 Agent Consensus: BULLISH (3/4 agents)
  
  🧠 RL Ensemble Prediction:
    • SAC: BUY
    • PPO: BUY
    • A2C: HOLD
    • TD3: BUY
    • DDPG: BUY
    ↳ Ensemble Decision: BUY (confidence: 80%, 4/5 agreement)
  
  🎯 Final Decision:
    Signal: BUY
    Confidence: 76.25% (agent: 71.25%, RL: 80%)
    Quantity: 76 shares
    Total Cost: $14,092.68
  
  ✅ Risk Validation: PASSED
    • Position size: $14,092 (14.1% of portfolio) ✓
    • Confidence: 76.25% ≥ 60% ✓
    • Buying power: $100,000 available ✓
  
  💼 Executing BUY order: 76 shares @ market
  ✓ Order submitted: order_id=abc123...
  ✓ Order filled: 76 shares @ $185.42 avg
  ✓ Total cost: $14,091.92

📈 Analyzing MSFT...
  💰 Current price: $420.15
  
  🤖 Agent Analysis:
    • Fundamentals: NEUTRAL (confidence: 65%)
    • Technicals: BEARISH (confidence: 70%)
    • Valuation: NEUTRAL (confidence: 62%)
    • Sentiment: NEUTRAL (confidence: 58%)
  
  📊 Agent Consensus: NEUTRAL (3/4 agents)
  
  🧠 RL Ensemble: HOLD (confidence: 60%, 3/5 agreement)
  
  🎯 Final Decision: HOLD
    Confidence: 62.5% (below action threshold)
    ↳ Skipping trade for MSFT

📈 Analyzing GOOGL...
  💰 Current price: $142.88
  
  🤖 Agent Analysis:
    • Fundamentals: BULLISH (confidence: 78%)
    • Technicals: BULLISH (confidence: 72%)
    • Valuation: NEUTRAL (confidence: 68%)
    • Sentiment: BULLISH (confidence: 74%)
  
  📊 Agent Consensus: BULLISH (3/4 agents)
  
  🧠 RL Ensemble: BUY (confidence: 80%, 4/5 agreement)
  
  🎯 Final Decision: BUY
    Confidence: 76.0%
    Quantity: 60 shares
  
  💼 Executing BUY order: 60 shares @ market
  ✓ Order filled: 60 shares @ $142.87 avg
  ✓ Total cost: $8,572.20

📊 Cycle Summary:
  • Decisions: 3 total (2 BUY, 0 SELL, 1 HOLD)
  • Trades Executed: 2
  • Total Deployed: $22,664.12
  • Cash Remaining: $77,335.88
  • Portfolio Value: $100,000.00 (unrealized P/L: $0.00)

⏳ Waiting 60 seconds until next cycle...
```

## 🖥️ Streamlit Web UI

### **Launching the UI**
```bash
streamlit run src/ui/app.py
# Access at: http://localhost:8501
```

### **UI Features**

#### **📊 Dashboard Tab**
- **Portfolio Overview:**
  - Total value, cash balance, invested amount
  - Daily P/L and total return percentage
- **Performance Charts:**
  - Portfolio value over time
  - Allocation pie chart
  - Recent performance trends
- **Recent Decisions:**
  - Latest trading signals
  - Confidence scores
  - Execution status

#### **🔍 Analysis Tab**
- **Stock Selection:** Choose any ticker to analyze
- **Real-time Analysis:**
  - All 4 agent results with confidence scores
  - RL ensemble prediction breakdown
  - Final decision with reasoning
- **Technical Indicators:** Interactive charts
- **Historical Performance:** Past decisions and outcomes

#### **💼 Portfolio Tab**
- **Current Positions:**
  - Holdings with quantities
  - Cost basis and current value
  - Unrealized P/L per position
- **Allocation Charts:**
  - Position size distribution
  - Sector allocation (if available)
- **Manual Trade Execution:**
  - Override system and place manual orders
  - Set custom quantities and order types

#### **📈 Monitoring Tab**
- **System Health:**
  - Trading status (running/stopped)
  - Market hours status
  - Last update timestamp
- **Performance Metrics:**
  - Win rate statistics
  - Average confidence scores
  - Signal distribution
- **Logs Viewer:**
  - Real-time log streaming
  - Error tracking
  - Decision history

#### **⚙️ Settings Panel** (Sidebar)
- **Trading Configuration:**
  - Stock list management
  - Confidence threshold adjustment
  - Position size limits
  - Trading interval
- **System Controls:**
  - Start/stop trading
  - Force single cycle
  - Emergency stop all
- **API Status:**
  - Connection health
  - API rate limits
  - Cache statistics

### **UI Screenshots**
For detailed UI documentation, see [UI_README.md](UI_README.md)

## 🛡️ Risk Management

### **Position Limits**
- Maximum 20% of portfolio per stock
- Prevents over-concentration in single positions
- Dynamically calculated based on current portfolio value

### **Confidence Filtering**
- Minimum 60% confidence required for execution
- Filters out low-conviction signals
- Reduces false positives and overtrading

### **Cash Management**
- Maintains minimum cash reserves
- Validates buying power before each trade
- Prevents over-leveraging

### **Order Validation**
- Pre-execution checks for all orders
- Validates quantities and prices
- Confirms account status before submission

### **Error Handling**
- Graceful degradation on API failures
- Automatic retry logic with exponential backoff
- Comprehensive error logging

### **Paper Trading Mode**
- Default to Alpaca paper trading environment
- Test strategies with zero risk
- Full feature parity with live trading

## 📈 Performance Tracking

### **Decision History**
- All trading decisions logged with timestamps
- Includes: ticker, signal, confidence, quantity, reasoning
- Stored in structured format for analysis

### **Performance Metrics**
- **Win Rate:** Percentage of profitable trades
- **Signal Distribution:** BUY/SELL/HOLD breakdown
- **Average Confidence:** Mean confidence across all decisions
- **Execution Success Rate:** Orders filled vs. submitted

### **Real-Time Monitoring**
- 60-second analysis cycles (configurable)
- Continuous portfolio value tracking
- Unrealized P/L calculation
- Market hours awareness

### **Logging System**
- Multi-level logging (DEBUG, INFO, WARNING, ERROR)
- Separate log files for different components
- Console output with colored formatting
- Log rotation and archival

## 🧪 Testing

### **Run System Tests**
```bash
python test_system.py
```

### **Test Individual Components**

**Test RL Ensemble:**
```bash
python src/models/rl_ensemble.py
```

**Test Data Preprocessing:**
```bash
python src/utils/data_preprocessor.py
```

**Test Alpaca Connection:**
```bash
python src/trading/alpaca_trader.py
```

**Test Decision Engine:**
```bash
python src/agents/decision_engine.py
```

### **Unit Tests**
```bash
pytest tests/unit/
```

### **Integration Tests**
```bash
pytest tests/integration/
```

## 🔧 Dependencies

### **Core Dependencies**

**AI & Machine Learning:**
- `langchain` (0.3.0) - AI agent framework
- `langchain-openai` (0.3.0) - OpenAI integration
- `langgraph` (0.2.56) - Multi-agent workflows
- `stable-baselines3` (≥2.0.0) - RL models (SAC, PPO, A2C, TD3, DDPG)
- `gymnasium` (≥0.29.0) - RL environments

**Data Processing:**
- `pandas` (≥1.5.0) - Data manipulation
- `numpy` (≥1.26.0) - Numerical computing
- `scikit-learn` (≥1.1.0) - ML utilities

**Trading & APIs:**
- `alpaca-trade-api` (≥3.0.0) - Trading execution
- `requests` (≥2.28.0) - HTTP requests

**Configuration:**
- `pydantic` (≥2.0.0) - Settings validation
- `python-dotenv` (≥1.0.0) - Environment variables

**Utilities:**
- `colorama` (≥0.4.6) - Colored output
- `rich` (≥13.9.4) - Rich formatting
- `joblib` (≥1.2.0) - Model serialization

**Optional:**
- `streamlit` - Web UI
- `plotly` - Interactive charts
- `TA-Lib` - Advanced technical indicators

### **Installing All Dependencies**
```bash
pip install -r requirements.txt
```

## 📚 Documentation

- **[COMPLETE_SYSTEM_GUIDE.md](COMPLETE_SYSTEM_GUIDE.md)** - Comprehensive system overview
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - AI agent integration details
- **[ALPACA_TRADING_GUIDE.md](ALPACA_TRADING_GUIDE.md)** - Trading execution guide
- **[RL_ENSEMBLE_GUIDE.md](RL_ENSEMBLE_GUIDE.md)** - RL model ensemble documentation
- **[UI_README.md](UI_README.md)** - Streamlit UI documentation
- **[SETUP_AND_TESTING.md](SETUP_AND_TESTING.md)** - Setup and testing guide
- **[TEST_RESULTS.md](TEST_RESULTS.md)** - System test results
- **[ERRORS_FIXED.md](ERRORS_FIXED.md)** - Fixed issues log
- **[FIXES_APPLIED.md](FIXES_APPLIED.md)** - Applied fixes documentation

## 🎓 Key Design Decisions

### **1. No Hardcoded Agent Weights**
- All 4 agents contribute equally to consensus
- Democratic decision-making process
- Prevents bias toward single analysis method

### **2. Equal-Weight RL Ensemble**
- Each of 5 models gets 20% voting weight
- Majority voting determines ensemble action
- Robust to individual model failures

### **3. Quantity-Based Trading**
- Calculates specific share quantities (not just BUY/SELL signals)
- Position sizing based on confidence and risk
- Dynamic allocation based on portfolio constraints

### **4. Confidence Threshold Filtering**
- Only executes trades with ≥60% confidence
- Reduces overtrading and false signals
- Improves risk-adjusted returns

### **5. Multi-Layer Caching**
- In-memory TTL-based API response caching
- Reduces API costs and latency
- Faster decision cycles

### **6. Graceful Degradation**
- Fallback calculations if TA-Lib unavailable
- Manual indicator computation as backup
- System functional even with missing dependencies

### **7. Paper Trading Default**
- Safe testing environment out-of-the-box
- Easy switch to live trading via config
- Full feature parity between paper and live

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Run code formatting: `black src/`
6. Commit changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### **Development Setup**
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run code formatting
black src/

# Run linting
flake8 src/

# Run type checking
mypy src/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**IMPORTANT:** This system is for **educational and research purposes only**. 

- Always test with **paper trading** before using real money
- Past performance does **not** guarantee future results
- Trading involves **risk of loss** - never invest more than you can afford to lose
- The authors are **not** responsible for any financial losses
- Consult a licensed financial advisor before making investment decisions
- Use at your own risk

## 🙏 Acknowledgments

- **Reference Project:** [AI Hedge Fund by virattt](https://github.com/virattt/ai-hedge-fund)
- **Alpaca Markets:** For providing paper trading API
- **Stable-Baselines3:** For RL model implementations
- **LangChain:** For AI agent framework
- **Streamlit:** For web UI framework

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/your_username/StockAI/issues)
- **Discussions:** [GitHub Discussions](https://github.com/your_username/StockAI/discussions)
- **Documentation:** See `docs/` directory for detailed guides

---

**StockAI** - Advanced Multi-Agent Portfolio Management with Ensemble Reinforcement Learning 🚀

*Built with Python, LangChain, Stable-Baselines3, and Alpaca API*

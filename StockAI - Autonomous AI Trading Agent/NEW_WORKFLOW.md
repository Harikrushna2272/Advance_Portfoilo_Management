# 🎯 New Workflow: 4 Agents + 5 RL Models + Portfolio Manager

## 📊 Updated Advance Portfolio System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    NEW STOCKAI DECISION WORKFLOW                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │   Market    │───▶│   Data       │───▶│ 4-Analysis  │───▶│ 5-Model     │ │
│  │   Data      │    │ Preprocessor │    │   Agents    │    │ Ensemble RL │ │
│  └─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘ │
│         │                   │                   │                   │       │
│         ▼                   ▼                   ▼                   ▼       │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │ WebSocket   │    │ 14 Technical │    │ Fundamentals│    │ SAC Model   │ │
│  │ Stream      │    │ Indicators   │    │ Technicals  │    │ PPO Model   │ │
│  │ Financial   │    │ (MACD, RSI,  │    │ Valuation   │    │ A2C Model   │ │
│  │ API         │    │ Bollinger,   │    │ Sentiment   │    │ DQN Model   │ │
│  │             │    │ SMA, etc.)   │    │ Risk        │    │ TD3 Model   │ │
│  └─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │   PORTFOLIO MANAGER     │
                    │                         │
                    │ • Agent Consensus       │
                    │ • RL Ensemble Decision  │
                    │ • Quantity Calculation  │
                    │ • Final BUY/SELL/HOLD   │
                    └─────────────────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │   TRADE EXECUTION       │
                    │                         │
                    │ • Alpaca API            │
                    │ • Quantity-based Orders │
                    │ • Portfolio Updates     │
                    │ • Performance Tracking  │
                    └─────────────────────────┘
```

---

## 🔄 New Decision Flow

### **Phase 1: 4 Agent Analysis (No Weights)**

```python
# Step 1: Run 4 core agents without weights
core_agents = ["fundamentals", "technicals", "valuation", "sentiment", "risk"]

agent_signals = {}
agent_confidences = {}

for agent_name in core_agents:
    result = analysis_results["agents"][agent_name]
    agent_signals[agent_name] = result["signal"]
    agent_confidences[agent_name] = result["confidence"]
```

**Agent Outputs:**
```python
# Example results:
agent_signals = {
    "fundamentals": "bullish",    # Company financial health
    "technicals": "neutral",      # Price action & patterns  
    "valuation": "bullish",       # Intrinsic value analysis
    "sentiment": "bearish",       # Market sentiment
    "risk": "neutral"            # Risk assessment
}

agent_confidences = {
    "fundamentals": 80,
    "technicals": 65,
    "valuation": 75,
    "sentiment": 60,
    "risk": 70
}
```

---

### **Phase 2: 5 RL Models Ensemble (20% Each)**

```python
# Step 2: 5 RL Models with equal 20% weight each
rl_weights = {"SAC": 0.2, "PPO": 0.2, "A2C": 0.2, "DQN": 0.2, "TD3": 0.2}

# Individual model votes
model_votes = {
    "SAC": 1,   # BUY
    "PPO": 1,   # BUY
    "A2C": 0,   # HOLD
    "DQN": 1,   # BUY
    "TD3": -1   # SELL
}

# Calculate weighted score
weighted_score = 0
for model, vote in model_votes.items():
    weighted_score += vote * rl_weights[model]

# weighted_score = 1*0.2 + 1*0.2 + 0*0.2 + 1*0.2 + (-1)*0.2 = 0.4
```

**RL Ensemble Decision:**
```python
if weighted_score > 0.1:
    rl_signal = "BUY"
    rl_confidence = min(95, abs(weighted_score) * 100)
elif weighted_score < -0.1:
    rl_signal = "SELL"
    rl_confidence = min(95, abs(weighted_score) * 100)
else:
    rl_signal = "HOLD"
    rl_confidence = 50

# Result: rl_signal = "BUY", rl_confidence = 40%
```

---

### **Phase 3: Portfolio Manager Decision**

```python
# Step 3: Portfolio Manager combines 4 Agents + 5 RL Models

# Count agent signals
signal_counts = {"bullish": 0, "bearish": 0, "neutral": 0}
for agent, signal in agent_signals.items():
    if signal in ["bullish", "BUY", "buy"]:
        signal_counts["bullish"] += 1
    elif signal in ["bearish", "SELL", "sell"]:
        signal_counts["bearish"] += 1
    else:
        signal_counts["neutral"] += 1

# signal_counts = {"bullish": 2, "bearish": 1, "neutral": 2}

# Determine agent consensus
if signal_counts["bullish"] > signal_counts["bearish"] and signal_counts["bullish"] > signal_counts["neutral"]:
    agent_consensus = "bullish"
elif signal_counts["bearish"] > signal_counts["bullish"] and signal_counts["bearish"] > signal_counts["neutral"]:
    agent_consensus = "bearish"
else:
    agent_consensus = "neutral"

# agent_consensus = "neutral" (no clear majority)
```

**Final Decision Logic:**
```python
# Combine agent consensus with RL decision
if agent_consensus == "bullish" and rl_signal == "BUY":
    final_signal = "BUY"
    final_confidence = min(95, (avg_agent_confidence + rl_confidence) / 2)
    quantity_multiplier = 1.0
elif agent_consensus == "bearish" and rl_signal == "SELL":
    final_signal = "SELL"
    final_confidence = min(95, (avg_agent_confidence + rl_confidence) / 2)
    quantity_multiplier = 1.0
elif agent_consensus == "bullish" or rl_signal == "BUY":
    final_signal = "BUY"
    final_confidence = min(90, (avg_agent_confidence + rl_confidence) / 2 * 0.8)
    quantity_multiplier = 0.7
elif agent_consensus == "bearish" or rl_signal == "SELL":
    final_signal = "SELL"
    final_confidence = min(90, (avg_agent_confidence + rl_confidence) / 2 * 0.8)
    quantity_multiplier = 0.7
else:
    final_signal = "HOLD"
    final_confidence = 50
    quantity_multiplier = 0
```

**Quantity Calculation:**
```python
# Calculate quantity based on confidence and risk
base_quantity = 100  # Base quantity
quantity = int(base_quantity * (final_confidence / 100) * quantity_multiplier)

# Risk adjustment
risk_signal = agent_signals.get("risk", "neutral")
if risk_signal == "bearish":
    quantity = int(quantity * 0.5)  # Reduce quantity for high risk
elif risk_signal == "bullish":
    quantity = int(quantity * 1.2)  # Increase quantity for low risk

# Cap quantity
quantity = max(0, min(quantity, 500))  # Cap between 0 and 500
```

---

## 📊 Example Decision Process

### **Input Data:**
```python
# Stock: AAPL
# Agent Results:
agent_signals = {
    "fundamentals": "bullish",    # 80% confidence
    "technicals": "neutral",      # 65% confidence
    "valuation": "bullish",       # 75% confidence
    "sentiment": "bearish",       # 60% confidence
    "risk": "neutral"            # 70% confidence
}

# RL Model Votes:
model_votes = {
    "SAC": 1,   # BUY
    "PPO": 1,   # BUY
    "A2C": 0,   # HOLD
    "DQN": 1,   # BUY
    "TD3": -1   # SELL
}
```

### **Step-by-Step Calculation:**

#### **1. Agent Consensus:**
```python
signal_counts = {"bullish": 2, "bearish": 1, "neutral": 2}
agent_consensus = "neutral"  # No clear majority
avg_agent_confidence = (80 + 65 + 75 + 60 + 70) / 5 = 70%
```

#### **2. RL Ensemble Decision:**
```python
weighted_score = 1*0.2 + 1*0.2 + 0*0.2 + 1*0.2 + (-1)*0.2 = 0.4
rl_signal = "BUY"  # weighted_score > 0.1
rl_confidence = min(95, 0.4 * 100) = 40%
```

#### **3. Portfolio Manager Decision:**
```python
# agent_consensus = "neutral", rl_signal = "BUY"
# Since rl_signal == "BUY", we go with BUY
final_signal = "BUY"
final_confidence = min(90, (70 + 40) / 2 * 0.8) = 44%
quantity_multiplier = 0.7

# Quantity calculation
base_quantity = 100
quantity = int(100 * (44 / 100) * 0.7) = 30

# Risk adjustment (risk = "neutral")
quantity = int(30 * 1.0) = 30

# Final quantity
quantity = max(0, min(30, 500)) = 30
```

### **Final Decision:**
```python
final_decision = {
    "signal": "BUY",
    "confidence": 44.0,
    "quantity": 30,
    "agent_consensus": "neutral",
    "agent_signal_counts": {"bullish": 2, "bearish": 1, "neutral": 2},
    "rl_decision": {
        "signal": "BUY",
        "confidence": 40,
        "model_votes": {"SAC": 1, "PPO": 1, "A2C": 0, "DQN": 1, "TD3": -1}
    },
    "reasoning": "Mixed signals from agents (bullish: 2, bearish: 1, neutral: 2) | RL ensemble suggests BUY | Partial alignment - moderate confidence trade"
}
```

---

## 🎯 Key Features of New Flow

### **1. Simplified Agent Weights**
- **4 Core Agents** provide signals without weights
- **Agent Consensus** determined by majority vote
- **No complex weighting** for individual agents

### **2. Equal RL Model Weights**
- **5 RL Models** each get exactly 20% weight
- **Majority Voting** among RL models
- **Transparent Decision** process

### **3. Portfolio Manager Integration**
- **Combines** agent consensus with RL decision
- **Calculates** optimal quantity based on confidence
- **Risk Adjustment** based on risk manager signal

### **4. Quantity-Based Execution**
- **Specific Quantity** for each trade
- **Risk-Adjusted** position sizing
- **Confidence-Based** quantity scaling

---

## 🔄 Complete New Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    NEW DECISION WORKFLOW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 🚀 System Startup                                          │
│     ├── Initialize Decision Engine (loads 5 RL models)         │
│     ├── Initialize Execution Agent (Alpaca API)                │
│     └── Initialize Portfolio ($100k starting capital)          │
│                                                                 │
│  2. 📊 Data Acquisition                                        │
│     ├── WebSocket Stream (real-time prices)                    │
│     ├── Financial API (historical data)                        │
│     └── Market Data (OHLCV)                                    │
│                                                                 │
│  3. Data Preprocessing                                      │
│     ├── Calculate 14 Technical Indicators                      │
│     ├── Handle NaN values                                      │
│     └── Return RL-ready features                               │
│                                                                 │
│  4. 🧠 4-Agent Analysis (No Weights)                         │
│     ├── Fundamentals Agent → Signal + Confidence               │
│     ├── Technicals Agent → Signal + Confidence                 │
│     ├── Valuation Agent → Signal + Confidence                  │
│     ├── Sentiment Agent → Signal + Confidence                  │
│     └── Risk Manager → Signal + Confidence                     │
│                                                                 │
│  5. 🤖 5-Model RL Ensemble (20% Each)                         │
│     ├── SAC Model: BUY/SELL/HOLD                               │
│     ├── PPO Model: BUY/SELL/HOLD                               │
│     ├── A2C Model: BUY/SELL/HOLD                               │
│     ├── DQN Model: BUY/SELL/HOLD                               │
│     ├── TD3 Model: BUY/SELL/HOLD                               │
│     └── Weighted Score (20% each) → RL Decision                │
│                                                                 │
│  6. 🎯 Portfolio Manager Decision                              │
│     ├── Agent Consensus (majority vote)                        │
│     ├── RL Ensemble Decision                                   │
│     ├── Combine Signals → Final Signal                         │
│     ├── Calculate Quantity (confidence-based)                  │
│     └── Risk Adjustment                                        │
│                                                                 │
│  7. 💼 Trade Execution                                         │
│     ├── High Confidence Check (>60%)                           │
│     ├── Quantity Validation (>0)                               │
│     ├── Alpaca API Call (with quantity)                        │
│     └── Portfolio Update                                       │
│                                                                 │
│  8. 📈 Performance Monitoring                                  │
│     ├── Cycle Summary                                          │
│     ├── Signal Distribution                                    │
│     ├── Decision History                                       │
│     └── Error Logging                                          │
│                                                                 │
│  ⏰ Wait 60 seconds → Repeat                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Decision Logic Summary

### **Agent Consensus Rules:**
- **Bullish Majority**: More bullish than bearish/neutral
- **Bearish Majority**: More bearish than bullish/neutral  
- **Neutral**: No clear majority

### **RL Ensemble Rules:**
- **Weighted Score > 0.1**: BUY
- **Weighted Score < -0.1**: SELL
- **-0.1 ≤ Score ≤ 0.1**: HOLD

### **Portfolio Manager Rules:**
- **Strong Alignment**: Agent consensus + RL decision match → High confidence
- **Partial Alignment**: Either agents or RL suggest direction → Moderate confidence
- **No Alignment**: Both neutral → HOLD

### **Quantity Rules:**
- **Base Quantity**: 100 shares
- **Confidence Multiplier**: 0-100% based on final confidence
- **Risk Multiplier**: 0.5x (high risk) to 1.2x (low risk)
- **Final Cap**: 0-500 shares

This new workflow provides a cleaner, more transparent decision-making process with equal emphasis on all components! 🚀

# RL Ensemble Integration Guide

## Overview

The **Advance_Portfolio_Management** system now includes a fully integrated **5-Model RL Ensemble** for advanced trading decisions. This ensemble combines multiple Reinforcement Learning algorithms to provide robust, data-driven predictions.

---

## Table of Contents

1. [What is RL Ensemble?](#what-is-rl-ensemble)
2. [Model Architecture](#model-architecture)
3. [How It Works](#how-it-works)
4. [Integration Architecture](#integration-architecture)
5. [Quick Start](#quick-start)
6. [API Reference](#api-reference)
7. [Training Your Own Models](#training-your-own-models)
8. [Troubleshooting](#troubleshooting)

---

## What is RL Ensemble?

### The 5 RL Models

Our ensemble combines 5 state-of-the-art Reinforcement Learning algorithms:

| Model | Full Name | Best For | Characteristics |
|-------|-----------|----------|-----------------|
| **SAC** | Soft Actor-Critic | Continuous control | Entropy-based exploration, stable |
| **PPO** | Proximal Policy Optimization | Stable learning | Clipped surrogate objective, robust |
| **A2C** | Advantage Actor-Critic | Fast decisions | Synchronous updates, efficient |
| **TD3** | Twin Delayed DDPG | Robust control | Twin Q-networks, reduced overestimation |
| **DDPG** | Deep Deterministic Policy Gradient | Continuous actions | Deterministic policy, off-policy |

### Why Ensemble?

✅ **Robustness**: Multiple models reduce individual model bias  
✅ **Consensus**: Majority voting leads to more reliable decisions  
✅ **Diversity**: Different algorithms capture different market patterns  
✅ **Confidence**: Agreement level indicates decision confidence  

---

## Model Architecture

### Input Features (14 total)

The RL models take 14 features as input:

**Price Features:**
- `close`: Closing price
- `high`: Highest price
- `low`: Lowest price
- `open`: Opening price
- `volume`: Trading volume

**Time Feature:**
- `day`: Day of week (0=Monday, 6=Sunday)

**Technical Indicators:**
- `macd`: MACD indicator
- `boll_ub`: Bollinger Bands upper bound
- `boll_lb`: Bollinger Bands lower bound
- `rsi_30`: 30-period Relative Strength Index
- `cci_30`: 30-period Commodity Channel Index
- `dx_30`: 30-period Directional Movement Index
- `close_30_sma`: 30-day Simple Moving Average
- `close_60_sma`: 60-day Simple Moving Average

### Output Actions

Each model outputs a continuous action value, which is then mapped to discrete trading signals:

- **Action > 0.5** → **BUY** signal
- **Action < -0.5** → **SELL** signal
- **-0.5 ≤ Action ≤ 0.5** → **HOLD** signal

### Ensemble Decision

The final decision uses **majority voting**:
```
If most models say BUY → Ensemble says BUY
If most models say SELL → Ensemble says SELL
Otherwise → HOLD
```

---

## How It Works

### Complete Pipeline

```
Stock Data (OHLCV)
        ↓
Data Preprocessing
  - Calculate indicators
  - Normalize features
  - Extract latest observation
        ↓
RLEnsemble
  - SAC prediction
  - PPO prediction
  - A2C prediction
  - TD3 prediction
  - DDPG prediction
        ↓
Majority Voting
        ↓
Final Signal (BUY/SELL/HOLD)
  + Confidence Score
        ↓
Decision Engine
  (combines with AI agents)
        ↓
Trading Execution
```

### Decision Flow Example

```python
# Stock data comes in
AAPL: close=150.00, high=152.00, low=148.00, ...

# Preprocessing extracts features
features = [150.00, 152.00, 148.00, ..., 12.5, 145.0, 148.5]  # 14 features

# Each model makes prediction
SAC:  0.8  → BUY
PPO:  0.6  → BUY
A2C:  0.4  → HOLD
TD3:  0.9  → BUY
DDPG: 0.7  → BUY

# Ensemble decision
Votes: BUY=4, HOLD=1, SELL=0
Result: BUY with 80% confidence (4/5 models agree)
```

---

## Integration Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│              Trading Workflow                           │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ AI Agents    │ │ RL Ensemble  │ │ Risk Manager │
│ (4 agents)   │ │ (5 models)   │ │              │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │ Decision Engine  │
              │ (Final signal)   │
              └─────────┬────────┘
                        │
                        ▼
              ┌──────────────────┐
              │ Alpaca Trader    │
              └──────────────────┘
```

### File Structure

```
Advance_Portfoilo_Management/
├── models/                          # Trained RL models
│   ├── agent_sac.zip
│   ├── agent_ppo.zip
│   ├── agent_a2c.zip
│   ├── agent_td3.zip
│   └── agent_ddpg.zip
├── src/
│   ├── models/
│   │   ├── rl_ensemble.py          # RL ensemble implementation
│   │   └── ensemble_model.py       # Legacy wrapper
│   ├── utils/
│   │   └── data_preprocessor.py    # Feature extraction
│   └── agents/
│       └── decision_engine.py      # Integration point
```

---

## Quick Start

### 1. Verify Models Are Present

```bash
ls -lh models/
# Should see:
# agent_sac.zip
# agent_ppo.zip
# agent_a2c.zip
# agent_td3.zip
# agent_ddpg.zip
```

### 2. Test RL Ensemble

```python
from models.rl_ensemble import RLEnsemble
import numpy as np

# Create ensemble
ensemble = RLEnsemble()

# Check status
print(f"Loaded models: {ensemble.get_loaded_models()}")
print(f"Ensemble ready: {ensemble.is_ready()}")

# Create sample observation (14 features)
sample_obs = np.array([
    150.0,  # close
    152.0,  # high
    148.0,  # low
    149.0,  # open
    1000000,  # volume
    2,  # day (Tuesday)
    0.5,  # macd
    155.0,  # boll_ub
    145.0,  # boll_lb
    55.0,  # rsi_30
    10.0,  # cci_30
    25.0,  # dx_30
    148.5,  # close_30_sma
    147.0,  # close_60_sma
], dtype=np.float32)

# Get prediction
action, details = ensemble.predict(sample_obs)
print(f"Action: {details['signal']}")
print(f"Confidence: {details['confidence']:.1f}%")
```

### 3. Test with Real Data

```python
from models.rl_ensemble import RLEnsemble
from utils.data_preprocessor import preprocess_for_rl
from tools.api import get_price_data

# Get stock data
stock_data = get_price_data("AAPL", "2024-01-01", "2024-11-01")

# Preprocess for RL
observation = preprocess_for_rl(stock_data)

if observation is not None:
    # Create ensemble
    ensemble = RLEnsemble()
    
    # Get prediction
    action, details = ensemble.predict(observation)
    
    print(f"RL Ensemble Decision for AAPL:")
    print(f"  Signal: {details['signal']}")
    print(f"  Confidence: {details['confidence']:.1f}%")
    print(f"  Model Predictions: {details['model_predictions']}")
else:
    print("Failed to preprocess data")
```

### 4. Full Pipeline Test

```python
from trading.trading_workflow import create_workflow

# Create workflow (includes RL ensemble)
workflow = create_workflow(
    tickers=["AAPL"],
    dry_run=True,
    min_confidence=60.0
)

# Run one cycle
result = workflow.run_single_cycle()
print(f"Cycle result: {result}")
```

---

## API Reference

### RLEnsemble Class

```python
from models.rl_ensemble import RLEnsemble

ensemble = RLEnsemble(models_dir=None)
```

#### Methods

##### `predict(observation, deterministic=True)`

Make prediction using ensemble.

**Args:**
- `observation` (np.ndarray): Feature array of shape (14,)
- `deterministic` (bool): Use deterministic actions (default: True)

**Returns:**
- `action` (int): Discrete action (0=HOLD, 1=BUY, 2=SELL)
- `details` (dict): Detailed prediction information

**Example:**
```python
action, details = ensemble.predict(obs)
print(f"Action: {details['signal']}")
print(f"Confidence: {details['confidence']:.1f}%")
```

##### `predict_with_details(observation)`

Get detailed prediction breakdown.

**Returns:**
Dictionary with:
- `action_code`: Discrete action code
- `action_name`: Human-readable action
- `signal`: Trading signal (BUY/SELL/HOLD)
- `confidence`: Confidence score (0-100)
- `model_predictions`: Individual model predictions
- `num_models`: Number of models used
- `prediction_std`: Standard deviation of predictions

**Example:**
```python
details = ensemble.predict_with_details(obs)
print(f"Signal: {details['signal']}")
print(f"Individual predictions: {details['model_predictions']}")
```

##### `get_loaded_models()`

Get list of successfully loaded models.

**Returns:**
List of model names (e.g., ['SAC', 'PPO', 'A2C', 'TD3', 'DDPG'])

##### `is_ready()`

Check if ensemble is ready for predictions.

**Returns:**
Boolean indicating if at least one model is loaded

### StockDataPreprocessor Class

```python
from utils.data_preprocessor import StockDataPreprocessor

preprocessor = StockDataPreprocessor()
```

#### Methods

##### `preprocess(stock_data)`

Preprocess stock data to create all required features.

**Args:**
- `stock_data` (pd.DataFrame): DataFrame with OHLCV data

**Returns:**
DataFrame with 14 required features

##### `get_latest_observation(df)`

Extract latest observation for RL prediction.

**Args:**
- `df` (pd.DataFrame): Preprocessed DataFrame

**Returns:**
Numpy array of shape (14,) with latest features

### Convenience Functions

##### `preprocess_for_rl(stock_data)`

One-step preprocessing and feature extraction.

**Args:**
- `stock_data` (pd.DataFrame): Raw stock data

**Returns:**
Numpy array ready for RL model, or None if failed

**Example:**
```python
from utils.data_preprocessor import preprocess_for_rl

observation = preprocess_for_rl(stock_data)
if observation is not None:
    action, details = ensemble.predict(observation)
```

---

## Training Your Own Models

### Requirements

```bash
pip install stable-baselines3 gym
```

### Training Script Example

```python
import gym
import numpy as np
from stable_baselines3 import SAC, PPO, A2C, TD3, DDPG
from stable_baselines3.common.vec_env import DummyVecEnv

# Create your trading environment
# (You need to implement a gym.Env for stock trading)
env = DummyVecEnv([lambda: YourTradingEnv()])

# Train SAC
model = SAC("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100000)
model.save("models/agent_sac")

# Train PPO
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100000)
model.save("models/agent_ppo")

# Repeat for A2C, TD3, DDPG...
```

### Model Format

Models should be saved as `.zip` files using Stable-Baselines3's save method. Place them in the `models/` directory with these exact names:
- `agent_sac.zip`
- `agent_ppo.zip`
- `agent_a2c.zip`
- `agent_td3.zip`
- `agent_ddpg.zip`

---

## Troubleshooting

### Issue 1: "Stable-Baselines3 not installed"

**Solution:**
```bash
pip install stable-baselines3
```

### Issue 2: "No RL models loaded"

**Cause:** Model files not found in `models/` directory

**Solution:**
```bash
# Check if models exist
ls -lh models/

# If missing, copy from Training_RL_Agents
cp /path/to/Training_RL_Agents/agent_*.zip models/
```

### Issue 3: "TA-Lib not available"

**Cause:** TA-Lib C library not installed

**Solution:**
```bash
# Option 1: Install TA-Lib (recommended)
# macOS:
brew install ta-lib
pip install TA-Lib

# Linux:
sudo apt-get install ta-lib
pip install TA-Lib

# Option 2: Use pandas_ta (automatic fallback)
pip install pandas-ta
```

### Issue 4: "Invalid observation shape"

**Cause:** Wrong number of features

**Solution:**
Ensure your stock data has all OHLCV columns and enough historical data (60+ days) for technical indicators.

```python
# Check data shape
print(f"Stock data shape: {stock_data.shape}")
print(f"Columns: {stock_data.columns.tolist()}")

# Verify preprocessing
from utils.data_preprocessor import StockDataPreprocessor

preprocessor = StockDataPreprocessor()
processed = preprocessor.preprocess(stock_data)
print(f"Processed shape: {processed.shape}")  # Should be (n_rows, 14)
```

### Issue 5: "All model predictions failed"

**Cause:** Models incompatible with observation format

**Check:**
1. Observation is numpy array of shape (14,)
2. Observation is float32 dtype
3. No NaN or inf values in observation

**Solution:**
```python
import numpy as np

# Check observation
print(f"Observation shape: {observation.shape}")  # Should be (14,)
print(f"Observation dtype: {observation.dtype}")  # Should be float32
print(f"Has NaN: {np.any(np.isnan(observation))}")  # Should be False
print(f"Has inf: {np.any(np.isinf(observation))}")  # Should be False

# Convert if needed
observation = np.array(observation, dtype=np.float32)
observation = np.nan_to_num(observation, nan=0.0, posinf=0.0, neginf=0.0)
```

---

## Best Practices

### 1. Data Quality

✅ **Do:** Use at least 60 days of historical data  
✅ **Do:** Verify data has no missing values  
✅ **Do:** Check for outliers and anomalies  
❌ **Don't:** Use data with gaps or missing OHLCV  

### 2. Model Usage

✅ **Do:** Check if ensemble is ready before predicting  
✅ **Do:** Use deterministic=True for inference  
✅ **Do:** Monitor individual model predictions  
❌ **Don't:** Ignore confidence scores  
❌ **Don't:** Trade with <60% confidence  

### 3. Integration

✅ **Do:** Combine RL with AI agent signals  
✅ **Do:** Use RL as one input, not sole decision maker  
✅ **Do:** Apply risk controls  
❌ **Don't:** Override risk limits based on RL alone  

### 4. Performance

✅ **Do:** Monitor ensemble agreement levels  
✅ **Do:** Log individual model predictions  
✅ **Do:** Track prediction accuracy over time  
❌ **Don't:** Ignore consistent model disagreements  

---

## Performance Metrics

### Tracking RL Ensemble Performance

```python
# In your decision engine or workflow
rl_stats = {
    "predictions": [],
    "confidences": [],
    "agreements": []
}

# After each prediction
details = ensemble.predict_with_details(observation)
rl_stats["predictions"].append(details["signal"])
rl_stats["confidences"].append(details["confidence"])

# Calculate agreement rate
std = details["prediction_std"]
agreement = 100 * (1 - std) if std < 1 else 0
rl_stats["agreements"].append(agreement)

# Analyze
print(f"Average Confidence: {np.mean(rl_stats['confidences']):.1f}%")
print(f"Average Agreement: {np.mean(rl_stats['agreements']):.1f}%")
print(f"Signal Distribution: {Counter(rl_stats['predictions'])}")
```

---

## Summary

### What You Have Now

✅ **5 Trained RL Models** - Ready to use  
✅ **Automatic Preprocessing** - Handles feature extraction  
✅ **Ensemble Voting** - Robust decision making  
✅ **Full Integration** - Works with AI agents and Alpaca  
✅ **Confidence Scores** - Know when to trust predictions  

### Quick Reference

```python
# Complete workflow
from models.rl_ensemble import RLEnsemble
from utils.data_preprocessor import preprocess_for_rl
from tools.api import get_price_data

# 1. Get data
data = get_price_data("AAPL", "2024-01-01", "2024-11-01")

# 2. Preprocess
observation = preprocess_for_rl(data)

# 3. Predict
ensemble = RLEnsemble()
action, details = ensemble.predict(observation)

# 4. Use result
print(f"RL says: {details['signal']} (confidence: {details['confidence']:.1f}%)")
```

**For questions or issues, check the troubleshooting section or review the code comments in `src/models/rl_ensemble.py`.**

---

**Happy Trading with RL! 🤖📈**

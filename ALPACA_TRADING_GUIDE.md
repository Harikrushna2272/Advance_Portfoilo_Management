# Alpaca Trading Integration Guide

## Overview

The Advance_Portfolio_Management system now includes comprehensive **Alpaca API integration** for live and paper trading. This guide covers everything you need to know to trade stocks using the Alpaca platform.

---

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Setup & Configuration](#setup--configuration)
4. [Quick Start](#quick-start)
5. [API Reference](#api-reference)
6. [Trading Workflow](#trading-workflow)
7. [Risk Management](#risk-management)
8. [Examples](#examples)
9. [Troubleshooting](#troubleshooting)

---

## Features

### ✅ **AlpacaTrader** (`src/trading/alpaca_trader.py`)

Comprehensive trading interface:
- **Account Management** - Get account info, buying power, portfolio value
- **Position Management** - Track positions, quantities, P/L
- **Market Data** - Latest prices, quotes, historical bars
- **Order Execution** - Market, limit, stop-loss orders
- **Order Management** - Track, cancel, and monitor orders
- **Risk Controls** - Position limits, buying power checks
- **Intelligent Caching** - Reduces API calls, improves performance

### ✅ **PortfolioExecutor** (`src/trading/portfolio_executor.py`)

Executes trading decisions:
- **Decision Execution** - Convert AI/RL decisions into trades
- **Risk Validation** - Check position limits before trading
- **Dry Run Mode** - Test strategies without real money
- **Execution Tracking** - Monitor all trades and results
- **Analytics** - Success rates, trade statistics

### ✅ **TradingWorkflow** (`src/trading/trading_workflow.py`)

Complete automated trading pipeline:
- **Data Collection** - Fetch market data
- **Multi-Agent Analysis** - Run all AI agents
- **RL Predictions** - 5-model ensemble predictions
- **Order Execution** - Execute trades via Alpaca
- **Continuous Trading** - Automated trading cycles
- **Performance Monitoring** - Track portfolio performance

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Trading Workflow                       │
│  (Orchestrates entire trading pipeline)                 │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Decision   │ │  Portfolio   │ │    Alpaca    │
│    Engine    │ │  Executor    │ │    Trader    │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       │ AI Signals     │ Execution      │ API Calls
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
                ┌───────────────┐
                │ Alpaca Market │
                └───────────────┘
```

### Component Relationships

1. **AlpacaTrader** - Low-level API wrapper
   - Communicates directly with Alpaca API
   - Handles authentication, orders, positions
   - Provides caching and error handling

2. **PortfolioExecutor** - Decision execution layer
   - Uses AlpacaTrader for order submission
   - Applies risk controls and validation
   - Tracks execution results

3. **TradingWorkflow** - High-level orchestrator
   - Coordinates data collection
   - Runs decision engine
   - Uses PortfolioExecutor for trades
   - Manages trading cycles

---

## Setup & Configuration

### 1. Install Dependencies

```bash
pip install alpaca-trade-api python-dotenv
```

### 2. Get Alpaca API Keys

1. Sign up at [Alpaca Markets](https://alpaca.markets/)
2. Navigate to **Paper Trading** dashboard
3. Generate API keys (Key ID and Secret Key)

### 3. Configure Environment

Edit your `.env` file:

```env
# Alpaca API Configuration
ALPACA_API_KEY=your_alpaca_api_key_here
ALPACA_API_SECRET=your_alpaca_secret_key_here

# Paper trading (recommended for testing)
ALPACA_BASE_URL=https://paper-api.alpaca.markets

# Live trading (use with caution!)
# ALPACA_BASE_URL=https://api.alpaca.markets
```

### 4. Verify Connection

```python
from trading.alpaca_trader import AlpacaTrader

# Test connection
trader = AlpacaTrader(paper_trading=True)
account = trader.get_account()
print(f"Account Balance: ${account['cash']:.2f}")
print(f"Portfolio Value: ${account['portfolio_value']:.2f}")
```

---

## Quick Start

### Example 1: Simple Buy/Sell

```python
from trading.alpaca_trader import AlpacaTrader

# Initialize trader
trader = AlpacaTrader(paper_trading=True)

# Buy 10 shares of AAPL
order = trader.buy("AAPL", 10)
print(f"Buy order submitted: {order['id']}")

# Sell 5 shares of AAPL
order = trader.sell("AAPL", 5)
print(f"Sell order submitted: {order['id']}")
```

### Example 2: Execute Trading Decisions

```python
from trading.portfolio_executor import PortfolioExecutor, TradingDecision

# Create executor in dry-run mode (safe!)
executor = PortfolioExecutor(dry_run=True, min_confidence=60.0)

# Create trading decision
decision = TradingDecision(
    symbol="AAPL",
    signal="BUY",
    confidence=75.0,
    quantity=10,
    reasoning="Strong fundamentals and momentum"
)

# Execute decision
result = executor.execute_decision(decision)
print(f"Execution result: {result.success}")
```

### Example 3: Run Full Trading Workflow

```python
from trading.trading_workflow import create_workflow

# Create workflow for multiple tickers
workflow = create_workflow(
    tickers=["AAPL", "MSFT", "GOOGL"],
    dry_run=True,  # Safe mode
    min_confidence=60.0,
    max_position_pct=0.20,
    check_interval=300  # 5 minutes
)

# Run for 3 cycles
workflow.run_continuous(max_cycles=3)
```

---

## API Reference

### AlpacaTrader

#### Account Management

```python
# Get account information
account = trader.get_account()
# Returns: {"cash": float, "portfolio_value": float, "buying_power": float, ...}

# Get buying power
buying_power = trader.get_buying_power()

# Get cash balance
cash = trader.get_cash_balance()

# Get portfolio value
value = trader.get_portfolio_value()
```

#### Position Management

```python
# Get position for a symbol
position = trader.get_position("AAPL")
# Returns: PortfolioPosition object or None

# Get all positions
positions = trader.get_all_positions()

# Get quantity of shares owned
qty = trader.get_position_quantity("AAPL")
```

#### Market Data

```python
# Get latest price
price = trader.get_latest_price("AAPL")

# Get latest quote (bid/ask)
quote = trader.get_latest_quote("AAPL")

# Get historical bars
bars = trader.get_bars("AAPL", timeframe="1Day", limit=100)
```

#### Order Execution

```python
# Buy shares (market order)
order = trader.buy("AAPL", qty=10)

# Sell shares (market order)
order = trader.sell("AAPL", qty=10)

# Submit custom order
order = trader.submit_order(
    symbol="AAPL",
    qty=10,
    side="buy",
    order_type="limit",
    limit_price=150.00,
    time_in_force="gtc"
)
```

#### Order Management

```python
# Get order by ID
order = trader.get_order(order_id)

# Get all orders
orders = trader.get_all_orders(status="open")

# Cancel order
trader.cancel_order(order_id)

# Cancel all orders
trader.cancel_all_orders()
```

#### Position Closing

```python
# Close entire position
trader.close_position("AAPL")

# Close partial position
trader.close_position("AAPL", qty=5)

# Close all positions
trader.close_all_positions()
```

#### Risk Controls

```python
# Check if trade can be executed
can_trade, reason = trader.can_trade("AAPL", qty=10, side="buy")

# Get maximum quantity within position limits
max_qty = trader.get_max_quantity("AAPL", max_position_value_pct=0.20)
```

#### Utility Methods

```python
# Check if market is open
is_open = trader.is_market_open()

# Get market hours
hours = trader.get_market_hours()

# Get portfolio summary
summary = trader.get_portfolio_summary()
```

### PortfolioExecutor

```python
from trading.portfolio_executor import PortfolioExecutor, TradingDecision

# Initialize executor
executor = PortfolioExecutor(
    dry_run=True,
    max_position_pct=0.20,
    min_confidence=60.0
)

# Execute single decision
result = executor.execute_decision(decision)

# Execute multiple decisions
results = executor.execute_decisions(decisions_dict)

# Get execution statistics
stats = executor.get_execution_stats()

# Print execution summary
executor.print_execution_summary()
```

### TradingWorkflow

```python
from trading.trading_workflow import create_workflow

# Create workflow
workflow = create_workflow(
    tickers=["AAPL", "MSFT"],
    dry_run=True,
    min_confidence=60.0,
    max_position_pct=0.20,
    check_interval=60
)

# Run single cycle
result = workflow.run_single_cycle()

# Run continuous (with max cycles)
workflow.run_continuous(max_cycles=10)

# Run continuous (infinite)
workflow.run_continuous()
```

---

## Trading Workflow

### Complete Trading Pipeline

```python
from trading.trading_workflow import TradingWorkflow

# 1. Initialize workflow
workflow = TradingWorkflow(
    tickers=["AAPL", "MSFT", "GOOGL", "TSLA"],
    dry_run=True,  # Start with paper trading
    min_confidence=70.0,  # Only trade high-confidence signals
    max_position_pct=0.15,  # Max 15% per position
    check_interval=300  # Check every 5 minutes
)

# 2. Run automated trading
workflow.run_continuous()
```

### What Happens in Each Cycle:

1. **Market Check** - Verify market is open
2. **Account Status** - Get current cash, positions, buying power
3. **Risk Validation** - Check portfolio risk levels
4. **Data Collection** - Fetch market data for all tickers
5. **Agent Analysis** - Run fundamentals, technicals, sentiment, valuation agents
6. **RL Predictions** - 5-model ensemble predictions
7. **Decision Making** - Combine all signals into final decisions
8. **Risk Controls** - Apply position limits and buying power checks
9. **Order Execution** - Submit orders to Alpaca
10. **Tracking** - Record results and update statistics

---

## Risk Management

### Built-in Risk Controls

#### 1. Position Size Limits

```python
# Maximum 20% of portfolio per position
executor = PortfolioExecutor(max_position_pct=0.20)

# Automatically enforced on all trades
```

#### 2. Confidence Threshold

```python
# Only trade signals with >60% confidence
executor = PortfolioExecutor(min_confidence=60.0)

# Low confidence signals are skipped
```

#### 3. Buying Power Checks

```python
# Automatically validates buying power before trades
can_trade, reason = trader.can_trade("AAPL", qty=100, side="buy")

if not can_trade:
    print(f"Trade rejected: {reason}")
```

#### 4. Position Validation

```python
# Can't sell more than you own
position_qty = trader.get_position_quantity("AAPL")
if qty > position_qty:
    # Trade rejected
```

#### 5. Account Status Checks

```python
# Trading blocked if account has issues
account = trader.get_account()

if account["trading_blocked"]:
    # Stop trading

if account["account_blocked"]:
    # Stop trading
```

### Manual Risk Controls

```python
# Set stop-loss orders
trader.submit_order(
    symbol="AAPL",
    qty=10,
    side="sell",
    order_type="stop",
    stop_price=140.00  # Sell if price drops to $140
)

# Set limit orders (don't buy above certain price)
trader.buy(
    symbol="AAPL",
    qty=10,
    order_type="limit",
    limit_price=150.00  # Only buy if price is $150 or less
)

# Close all positions in emergency
trader.close_all_positions()

# Cancel all pending orders
trader.cancel_all_orders()
```

---

## Examples

### Example 1: Check Account & Positions

```python
from trading.alpaca_trader import AlpacaTrader

trader = AlpacaTrader(paper_trading=True)

# Get account info
account = trader.get_account()
print(f"Cash: ${account['cash']:,.2f}")
print(f"Portfolio Value: ${account['portfolio_value']:,.2f}")
print(f"Buying Power: ${account['buying_power']:,.2f}")

# Get all positions
positions = trader.get_all_positions()
for pos in positions:
    print(f"{pos.symbol}: {pos.quantity} shares @ ${pos.current_price:.2f}")
    print(f"  P/L: ${pos.unrealized_pl:.2f} ({pos.unrealized_plpc:.2f}%)")
```

### Example 2: Execute Strategy Decision

```python
from trading.portfolio_executor import create_executor, TradingDecision

# Create executor
executor = create_executor(dry_run=True, min_confidence=65.0)

# Decision from your strategy
decision = TradingDecision(
    symbol="TSLA",
    signal="BUY",
    confidence=78.5,
    quantity=15,
    reasoning="Strong momentum + positive fundamentals"
)

# Execute
result = executor.execute_decision(decision)

if result.success:
    print(f"✅ Trade executed: {result.action} {result.executed_quantity} shares")
else:
    print(f"❌ Trade failed: {result.error_message}")
```

### Example 3: Batch Trading

```python
from trading.portfolio_executor import create_executor, TradingDecision

executor = create_executor(dry_run=True)

# Multiple decisions
decisions = {
    "AAPL": TradingDecision("AAPL", "BUY", 75.0, 10, "Strong buy signal"),
    "MSFT": TradingDecision("MSFT", "HOLD", 55.0, 0, "Mixed signals"),
    "GOOGL": TradingDecision("GOOGL", "SELL", 80.0, 5, "Overbought")
}

# Execute all at once
results = executor.execute_decisions(decisions)

# Print summary
executor.print_execution_summary()
```

### Example 4: Automated Trading Bot

```python
from trading.trading_workflow import create_workflow

# Create bot
bot = create_workflow(
    tickers=["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"],
    dry_run=True,
    min_confidence=70.0,
    max_position_pct=0.15,
    check_interval=300  # 5 minutes
)

# Run continuously
try:
    bot.run_continuous()
except KeyboardInterrupt:
    print("Bot stopped by user")
```

### Example 5: Portfolio Rebalancing

```python
from trading.alpaca_trader import AlpacaTrader

trader = AlpacaTrader(paper_trading=True)

# Get current positions
positions = trader.get_all_positions()
account = trader.get_account()
total_value = account["portfolio_value"]

# Rebalance to 10% each
target_pct = 0.10

for pos in positions:
    current_value = pos.market_value
    current_pct = current_value / total_value
    
    if current_pct > target_pct * 1.1:  # More than 10% over target
        # Sell excess
        excess_value = current_value - (total_value * target_pct)
        shares_to_sell = int(excess_value / pos.current_price)
        trader.sell(pos.symbol, shares_to_sell)
        print(f"Rebalancing {pos.symbol}: selling {shares_to_sell} shares")
```

---

## Troubleshooting

### Common Issues

#### Issue 1: "Alpaca API credentials not found"

**Solution:**
```bash
# Make sure .env file exists and has keys
cp env.example .env
nano .env

# Add your keys:
ALPACA_API_KEY=your_key_here
ALPACA_API_SECRET=your_secret_here
```

#### Issue 2: "Trading is blocked on this account"

**Solution:**
- Check your Alpaca account status
- Verify account is approved and funded
- Check for pattern day trader restrictions

#### Issue 3: "Insufficient buying power"

**Solution:**
```python
# Check buying power before trading
buying_power = trader.get_buying_power()
price = trader.get_latest_price("AAPL")
max_qty = int(buying_power / price)

print(f"Can afford {max_qty} shares")
```

#### Issue 4: "Market is closed"

**Solution:**
```python
# Check market hours
if not trader.is_market_open():
    hours = trader.get_market_hours()
    print(f"Market closed. Opens at: {hours['next_open']}")
```

#### Issue 5: Orders not filling

**Possible causes:**
- Using limit orders with price too far from market
- Low liquidity stocks
- After-hours trading

**Solution:**
```python
# Use market orders for immediate execution
trader.buy("AAPL", 10)  # Default is market order

# Or use realistic limit prices
current_price = trader.get_latest_price("AAPL")
trader.buy("AAPL", 10, order_type="limit", limit_price=current_price * 1.01)
```

---

## Best Practices

### 1. Always Start with Paper Trading

```python
# ✅ Good: Test with paper trading first
trader = AlpacaTrader(paper_trading=True)

# ❌ Bad: Jump straight to live trading
# trader = AlpacaTrader(paper_trading=False)
```

### 2. Use Dry Run Mode

```python
# ✅ Good: Test strategies in dry-run mode
executor = PortfolioExecutor(dry_run=True)

# Once confident, switch to live
# executor = PortfolioExecutor(dry_run=False)
```

### 3. Set Conservative Limits

```python
# ✅ Good: Conservative position sizing
executor = PortfolioExecutor(
    max_position_pct=0.10,  # 10% max per position
    min_confidence=70.0      # High confidence threshold
)
```

### 4. Monitor Execution

```python
# ✅ Good: Track and review execution
results = executor.execute_decisions(decisions)
executor.print_execution_summary()

# Check for failures
for symbol, result in results.items():
    if not result.success:
        print(f"Failed: {symbol} - {result.error_message}")
```

### 5. Handle Errors Gracefully

```python
# ✅ Good: Proper error handling
try:
    order = trader.buy("AAPL", 10)
    if order:
        print(f"Order placed: {order['id']}")
    else:
        print("Order failed")
except Exception as e:
    print(f"Error: {e}")
    # Don't crash, continue trading other symbols
```

---

## Advanced Features

### Custom Order Types

```python
# Stop-loss order
trader.submit_order(
    symbol="AAPL",
    qty=10,
    side="sell",
    order_type="stop",
    stop_price=145.00
)

# Limit order
trader.submit_order(
    symbol="AAPL",
    qty=10,
    side="buy",
    order_type="limit",
    limit_price=150.00
)

# Stop-limit order
trader.submit_order(
    symbol="AAPL",
    qty=10,
    side="sell",
    order_type="stop_limit",
    stop_price=145.00,
    limit_price=144.00
)
```

### Order Time-in-Force

```python
# Good-till-canceled (default)
trader.buy("AAPL", 10, time_in_force="gtc")

# Day order (expires at market close)
trader.buy("AAPL", 10, time_in_force="day")

# Immediate-or-cancel
trader.buy("AAPL", 10, time_in_force="ioc")

# Fill-or-kill
trader.buy("AAPL", 10, time_in_force="fok")
```

---

## Conclusion

The Alpaca integration provides a complete, production-ready trading system with:

- ✅ Comprehensive API coverage
- ✅ Built-in risk management
- ✅ Dry-run and paper trading support
- ✅ Execution tracking and analytics
- ✅ Full automation capabilities

**Start with paper trading, test thoroughly, and only go live when confident!**

For more information:
- [Alpaca Documentation](https://alpaca.markets/docs/)
- [Alpaca Python SDK](https://github.com/alpacahq/alpaca-trade-api-python)
- Project INTEGRATION_GUIDE.md

**Happy Trading! 📈💰**

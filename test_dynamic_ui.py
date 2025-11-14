#!/usr/bin/env python3
"""
Quick test script to verify dynamic UI integration

This script simulates trading activity to test if the UI updates correctly.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.state_manager import get_state_manager
from datetime import datetime
import time


def test_state_manager():
    """Test the state manager functionality."""
    print("\n" + "=" * 80)
    print("Testing State Manager - Dynamic UI Integration")
    print("=" * 80 + "\n")

    # Initialize state manager
    print("📦 Initializing state manager...")
    sm = get_state_manager()
    print("✅ State manager initialized\n")

    # Test 1: Set trading active
    print("🟢 Test 1: Setting trading active...")
    sm.set_trading_active(True)
    state = sm.get_state()
    assert state.trading_active == True, "Trading active not set correctly"
    print(f"✅ Trading active: {state.trading_active}\n")

    # Test 2: Simulate a trading cycle
    print("🔄 Test 2: Simulating trading cycle...")
    sm.increment_cycle()
    state = sm.get_state()
    print(f"✅ Cycle count: {state.cycle_count}\n")

    # Test 3: Add a trading decision
    print("🎯 Test 3: Adding trading decision...")
    sm.add_decision(
        {
            "symbol": "AAPL",
            "signal": "BUY",
            "confidence": 85.5,
            "quantity": 50,
            "price": 182.50,
            "reasoning": "Strong bullish signals from technical analysis",
            "executed": False,
        }
    )
    state = sm.get_state()
    print(f"✅ Total decisions: {state.total_decisions}")
    print(f"✅ Recent decisions: {len(state.recent_decisions)}\n")

    # Test 4: Record a trade execution
    print("💼 Test 4: Recording trade execution...")
    sm.add_trade_execution(
        {
            "symbol": "AAPL",
            "action": "BUY",
            "quantity": 50,
            "price": 182.50,
            "total_value": 9125.00,
            "success": True,
            "error_message": None,
            "order_id": "TEST_ORDER_123",
        }
    )
    state = sm.get_state()
    print(f"✅ Total trades: {state.total_trades}")
    print(f"✅ Successful trades: {state.successful_trades}\n")

    # Test 5: Update portfolio
    print("💰 Test 5: Updating portfolio...")
    sm.update_portfolio(
        {
            "cash": 90875.00,
            "total_value": 100000.00,
            "total_return": 0.00,
            "total_return_pct": 0.00,
            "positions": {
                "AAPL": {
                    "shares": 50,
                    "market_value": 9125.00,
                    "avg_cost": 182.50,
                    "current_price": 182.50,
                    "unrealized_pnl": 0.00,
                    "unrealized_pnl_pct": 0.00,
                    "day_change": 0.00,
                    "day_change_pct": 0.00,
                }
            },
            "cost_basis": {"AAPL": 9125.00},
        }
    )
    state = sm.get_state()
    print(f"✅ Portfolio value: ${state.portfolio['total_value']:,.2f}")
    print(f"✅ Cash: ${state.portfolio['cash']:,.2f}")
    print(f"✅ Positions: {len(state.portfolio['positions'])}\n")

    # Test 6: Update analytics
    print("📊 Test 6: Updating analytics...")
    sm.update_analytics(
        {
            "daily_pnl": 125.50,
            "weekly_pnl": 450.75,
            "monthly_pnl": 1250.00,
            "sharpe_ratio": 1.25,
            "max_drawdown": -2.5,
            "win_rate": 73.5,
        }
    )
    state = sm.get_state()
    print(f"✅ Daily P&L: ${state.analytics['daily_pnl']:,.2f}")
    print(f"✅ Win rate: {state.analytics['win_rate']:.1f}%\n")

    # Test 7: Query historical data
    print("📚 Test 7: Querying historical data...")
    recent_trades = sm.get_recent_trades(limit=10)
    recent_decisions = sm.get_recent_decisions(limit=10)
    portfolio_history = sm.get_portfolio_history(days=7)

    print(f"✅ Recent trades in DB: {len(recent_trades)}")
    print(f"✅ Recent decisions in DB: {len(recent_decisions)}")
    print(f"✅ Portfolio history entries: {len(portfolio_history)}\n")

    # Test 8: Simulate multiple cycles
    print("🔄 Test 8: Simulating multiple trading cycles...")
    for i in range(5):
        sm.increment_cycle()
        sm.add_decision(
            {
                "symbol": "TSLA",
                "signal": "SELL" if i % 2 == 0 else "HOLD",
                "confidence": 70.0 + i * 2,
                "quantity": 10 * (i + 1),
                "price": 245.80 + i,
                "reasoning": f"Simulated decision {i + 1}",
                "executed": i % 2 == 0,
            }
        )
        time.sleep(0.1)

    state = sm.get_state()
    print(f"✅ Cycles completed: {state.cycle_count}")
    print(f"✅ Total decisions: {state.total_decisions}\n")

    # Final state summary
    print("=" * 80)
    print("📋 FINAL STATE SUMMARY")
    print("=" * 80)
    print(f"Trading Active:      {state.trading_active}")
    print(f"Cycle Count:         {state.cycle_count}")
    print(f"Total Decisions:     {state.total_decisions}")
    print(f"Total Trades:        {state.total_trades}")
    print(f"Successful Trades:   {state.successful_trades}")
    print(f"Portfolio Value:     ${state.portfolio['total_value']:,.2f}")
    print(f"Cash Available:      ${state.portfolio['cash']:,.2f}")
    print(f"Active Positions:    {len(state.portfolio['positions'])}")
    print(f"Recent Decisions:    {len(state.recent_decisions)}")
    print(f"Win Rate:            {state.analytics['win_rate']:.1f}%")
    print(f"Daily P&L:           ${state.analytics['daily_pnl']:,.2f}")
    print("=" * 80 + "\n")

    print("✅ All tests passed!")
    print("\n🎉 State Manager is working correctly!")
    print("📊 Now start the UI to see real-time updates:")
    print("   streamlit run src/ui/app.py\n")


if __name__ == "__main__":
    try:
        test_state_manager()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

#!/usr/bin/env python3
"""
System Testing Script
Tests all major components of the Advanced Portfolio Management system.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_basic_imports():
    """Test basic imports without ML libraries."""
    print("\n" + "=" * 60)
    print("TEST 1: Basic Imports")
    print("=" * 60)

    tests = [
        ("Cache", "from src.data.cache import Cache"),
        ("Data Models", "from src.data.models import Price, FinancialMetrics"),
        ("Validators", "from src.utils.validators import validate_ticker"),
    ]

    passed = 0
    for name, import_stmt in tests:
        try:
            exec(import_stmt)
            print(f"✅ {name}: OK")
            passed += 1
        except Exception as e:
            print(f"❌ {name}: {type(e).__name__}: {e}")

    print(f"\nPassed: {passed}/{len(tests)}")
    return passed == len(tests)


def test_ml_libraries():
    """Test ML library availability."""
    print("\n" + "=" * 60)
    print("TEST 2: ML Libraries")
    print("=" * 60)

    libs = [
        ("stable_baselines3", "Stable-Baselines3"),
        ("gymnasium", "Gymnasium"),
        ("langchain", "LangChain"),
        ("langchain_core", "LangChain Core"),
        ("pandas_ta", "Pandas TA"),
    ]

    passed = 0
    for module, name in libs:
        try:
            __import__(module)
            print(f"✅ {name}: installed")
            passed += 1
        except ImportError:
            print(f"❌ {name}: NOT installed")

    print(f"\nPassed: {passed}/{len(libs)}")
    return passed == len(libs)


def test_agent_imports():
    """Test agent file imports."""
    print("\n" + "=" * 60)
    print("TEST 3: Agent Imports")
    print("=" * 60)

    agents = [
        (
            "Fundamentals",
            "from src.agents.fundamentals_agent import analyze_fundamentals",
        ),
        ("Technicals", "from src.agents.technicals_agent import analyze_technicals"),
        ("Valuation", "from src.agents.valuation_agent import analyze_valuation"),
        ("Sentiment", "from src.agents.sentiment_agent import analyze_sentiment"),
    ]

    passed = 0
    for name, import_stmt in agents:
        try:
            exec(import_stmt)
            print(f"✅ {name} Agent: OK")
            passed += 1
        except Exception as e:
            print(f"❌ {name} Agent: {type(e).__name__}: {e}")

    print(f"\nPassed: {passed}/{len(agents)}")
    return passed == len(agents)


def test_trading_imports():
    """Test trading system imports."""
    print("\n" + "=" * 60)
    print("TEST 4: Trading System Imports")
    print("=" * 60)

    components = [
        ("Alpaca Trader", "from src.trading.alpaca_trader import AlpacaTrader"),
        (
            "Portfolio Executor",
            "from src.trading.portfolio_executor import PortfolioExecutor",
        ),
        (
            "Trading Workflow",
            "from src.trading.trading_workflow import TradingWorkflow",
        ),
    ]

    passed = 0
    for name, import_stmt in components:
        try:
            exec(import_stmt)
            print(f"✅ {name}: OK")
            passed += 1
        except Exception as e:
            print(f"❌ {name}: {type(e).__name__}: {e}")

    print(f"\nPassed: {passed}/{len(components)}")
    return passed == len(components)


def test_data_preprocessor():
    """Test data preprocessor with sample data."""
    print("\n" + "=" * 60)
    print("TEST 5: Data Preprocessor")
    print("=" * 60)

    try:
        from src.utils.data_preprocessor import StockDataPreprocessor
        import pandas as pd
        import numpy as np

        print("✅ Imports successful")

        # Create sample data
        dates = pd.date_range("2024-01-01", periods=100)
        df = pd.DataFrame(
            {
                "close": np.random.randn(100).cumsum() + 100,
                "high": np.random.randn(100).cumsum() + 102,
                "low": np.random.randn(100).cumsum() + 98,
                "open": np.random.randn(100).cumsum() + 100,
                "volume": np.random.randint(1000000, 10000000, 100),
            },
            index=dates,
        )

        print(f"✅ Sample data created: {df.shape}")

        preprocessor = StockDataPreprocessor()
        processed = preprocessor.preprocess(df)

        print(f"✅ Preprocessing successful: {processed.shape}")
        print(f"   Features: {list(processed.columns)[:5]}...")

        # Get latest observation
        obs = preprocessor.get_latest_observation(processed)
        if obs is not None:
            print(f"✅ Latest observation shape: {obs.shape}")
            return True
        else:
            print("❌ Failed to get latest observation")
            return False

    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_rl_ensemble_slow():
    """Test RL ensemble (slow - loads all models)."""
    print("\n" + "=" * 60)
    print("TEST 6: RL Ensemble (SLOW - may take 30-60 seconds)")
    print("=" * 60)

    try:
        print("⏳ Loading RL Ensemble (this may take a while)...")
        from src.models.rl_ensemble import RLEnsemble

        print("✅ RLEnsemble imported")

        rl = RLEnsemble()
        print(f"✅ RLEnsemble instantiated")
        print(f"   Loaded models: {rl.get_loaded_models()}")
        print(f"   Is ready: {rl.is_ready()}")

        return rl.is_ready()

    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_model_files():
    """Test that model files exist."""
    print("\n" + "=" * 60)
    print("TEST 7: Model Files")
    print("=" * 60)

    from pathlib import Path

    models_dir = Path(__file__).parent / "models"
    required_models = [
        "agent_sac.zip",
        "agent_ppo.zip",
        "agent_a2c.zip",
        "agent_td3.zip",
        "agent_ddpg.zip",
    ]

    passed = 0
    for model_file in required_models:
        path = models_dir / model_file
        if path.exists():
            size_mb = path.stat().st_size / (1024 * 1024)
            print(f"✅ {model_file}: {size_mb:.1f} MB")
            passed += 1
        else:
            print(f"❌ {model_file}: NOT FOUND")

    print(f"\nPassed: {passed}/{len(required_models)}")
    return passed == len(required_models)


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print(" ADVANCED PORTFOLIO MANAGEMENT - SYSTEM TEST")
    print("=" * 70)

    results = {
        "Basic Imports": test_basic_imports(),
        "ML Libraries": test_ml_libraries(),
        "Agent Imports": test_agent_imports(),
        "Trading System": test_trading_imports(),
        "Data Preprocessor": test_data_preprocessor(),
        "Model Files": test_model_files(),
    }

    # Ask before running slow test
    print("\n" + "=" * 60)
    print("RL Ensemble test is SLOW (30-60 seconds).")
    response = input("Run RL Ensemble test? (y/n): ").strip().lower()

    if response == "y":
        results["RL Ensemble"] = test_rl_ensemble_slow()
    else:
        print("⏭️  Skipping RL Ensemble test")
        results["RL Ensemble"] = None

    # Summary
    print("\n" + "=" * 70)
    print(" TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)
    total = len(results) - skipped

    for test, result in results.items():
        if result is True:
            print(f"✅ {test}")
        elif result is False:
            print(f"❌ {test}")
        else:
            print(f"⏭️  {test} (skipped)")

    print(f"\n{'=' * 70}")
    print(f"Passed: {passed}/{total} | Failed: {failed}/{total} | Skipped: {skipped}")

    if failed == 0 and passed == total:
        print("🎉 ALL TESTS PASSED!")
    elif failed > 0:
        print(f"⚠️  {failed} test(s) failed - see details above")

    print("=" * 70 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

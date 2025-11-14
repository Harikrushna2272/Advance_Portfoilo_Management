"""
Trading Workflow Orchestrator

Integrates the entire trading pipeline:
1. Data Collection
2. Agent Analysis
3. Decision Engine
4. Order Execution
5. Portfolio Monitoring
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import time

from src.trading.alpaca_trader import AlpacaTrader
from src.trading.portfolio_executor import PortfolioExecutor, TradingDecision
from src.agents.decision_engine import create_decision_engine
from src.agents.data_fetcher import get_stock_data
from src.core.state_manager import get_state_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TradingWorkflow:
    """
    Complete trading workflow orchestrator.

    Coordinates:
    - Market data collection
    - Multi-agent analysis
    - RL ensemble predictions
    - Risk management
    - Order execution
    - Performance tracking
    """

    def __init__(
        self,
        tickers: List[str],
        dry_run: bool = True,
        min_confidence: float = 60.0,
        max_position_pct: float = 0.20,
        check_interval: int = 60,
    ):
        """
        Initialize Trading Workflow.

        Args:
            tickers: List of stock tickers to trade
            dry_run: Simulate trades without executing (default: True)
            min_confidence: Minimum confidence to execute trade (default: 60%)
            max_position_pct: Max position size as % of portfolio (default: 20%)
            check_interval: Seconds between trading cycles (default: 60)
        """
        self.tickers = tickers
        self.dry_run = dry_run
        self.min_confidence = min_confidence
        self.max_position_pct = max_position_pct
        self.check_interval = check_interval

        # Initialize components
        logger.info("Initializing Trading Workflow components...")

        # Alpaca trader
        self.trader = AlpacaTrader(paper_trading=True)
        logger.info("✅ Alpaca Trader initialized")

        # Portfolio executor
        self.executor = PortfolioExecutor(
            trader=self.trader,
            dry_run=dry_run,
            min_confidence=min_confidence,
            max_position_pct=max_position_pct,
        )
        logger.info("✅ Portfolio Executor initialized")

        # Decision engine
        self.decision_engine = create_decision_engine()
        logger.info("✅ Decision Engine initialized")

        # Trading stats
        self.cycle_count = 0
        self.total_trades = 0
        self.successful_trades = 0

        # Initialize state manager for real-time UI sync
        self.state_manager = get_state_manager()
        logger.info("✅ State Manager initialized")

        # Update initial settings in state
        self.state_manager.update_state(
            settings={
                "stock_list": tickers,
                "confidence_threshold": int(min_confidence),
                "max_position_pct": max_position_pct * 100,
                "cycle_interval": check_interval,
                "auto_refresh": True,
                "refresh_interval": 5,
            }
        )

        logger.info(f"🚀 Trading Workflow ready for {len(tickers)} tickers")
        logger.info(f"Mode: {'DRY RUN' if dry_run else 'LIVE TRADING'}")

    def run_single_cycle(self) -> Dict:
        """
        Run a single trading cycle.

        Returns:
            Dictionary with cycle results
        """
        self.cycle_count += 1
        cycle_start = datetime.now()

        # Update cycle count in state
        self.state_manager.increment_cycle()

        logger.info(f"\n{'=' * 80}")
        logger.info(
            f"CYCLE #{self.cycle_count} - {cycle_start.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        logger.info(f"{'=' * 80}\n")

        # Check if market is open
        if not self.trader.is_market_open():
            logger.warning("⏸️  Market is closed. Skipping cycle.")
            market_hours = self.trader.get_market_hours()
            if market_hours:
                logger.info(f"Next market open: {market_hours['next_open']}")
            return {"status": "market_closed", "cycle": self.cycle_count}

        # Get account info
        try:
            account = self.trader.get_account(force_refresh=True)
            logger.info(f"💰 Account Status:")
            logger.info(f"   Cash: ${account['cash']:,.2f}")
            logger.info(f"   Portfolio Value: ${account['portfolio_value']:,.2f}")
            logger.info(f"   Buying Power: ${account['buying_power']:,.2f}")

            # Update system health in state
            system_health = {
                "api_status": "Connected",
                "database_status": "Online",
                "models_loaded": 5,
                "total_models": 5,
                "memory_usage": 45,  # Can be replaced with actual psutil data
                "cpu_usage": 30,
            }
            self.state_manager.update_state(system_health=system_health)

        except Exception as e:
            logger.error(f"❌ Failed to get account info: {e}")
            # Update error status
            system_health = self.state_manager.get_state().system_health
            system_health["api_status"] = "Error"
            self.state_manager.update_state(system_health=system_health)
            return {"status": "error", "error": str(e)}

        # Validate portfolio risk
        is_valid, warnings = self.executor.validate_portfolio_risk()
        if warnings:
            for warning in warnings:
                logger.warning(warning)

        # Set date range for analysis
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        # Portfolio snapshot for decision engine
        positions = self.trader.get_all_positions(force_refresh=True)
        portfolio = {
            "cash": account["cash"],
            "positions": {
                pos.symbol: {"shares": pos.quantity, "value": pos.market_value}
                for pos in positions
            },
            "cost_basis": {pos.symbol: pos.cost_basis for pos in positions},
        }

        # Update portfolio in state with detailed position info
        portfolio_state = {
            "cash": account["cash"],
            "total_value": account["portfolio_value"],
            "total_return": account["portfolio_value"]
            - 100000.0,  # Assuming 100k initial
            "total_return_pct": ((account["portfolio_value"] - 100000.0) / 100000.0)
            * 100,
            "positions": {},
            "cost_basis": {},
        }

        for pos in positions:
            portfolio_state["positions"][pos.symbol] = {
                "shares": pos.quantity,
                "market_value": pos.market_value,
                "avg_cost": pos.avg_entry_price,
                "current_price": pos.current_price,
                "unrealized_pnl": pos.unrealized_pl,
                "unrealized_pnl_pct": pos.unrealized_plpc * 100,
                "day_change": pos.change_today,
                "day_change_pct": pos.unrealized_intraday_plpc * 100,
            }
            portfolio_state["cost_basis"][pos.symbol] = pos.cost_basis

        self.state_manager.update_portfolio(portfolio_state)

        # Analyze each ticker
        decisions = {}
        cycle_results = {
            "cycle": self.cycle_count,
            "timestamp": cycle_start.isoformat(),
            "tickers_analyzed": [],
            "decisions": {},
            "executions": {},
            "errors": [],
        }

        for ticker in self.tickers:
            logger.info(f"\n📊 Analyzing {ticker}...")

            try:
                # Get stock data
                stock_data = get_stock_data(ticker)
                if stock_data is None or stock_data.empty:
                    logger.warning(f"❌ No data available for {ticker}")
                    cycle_results["errors"].append(f"No data for {ticker}")
                    continue

                # Run comprehensive analysis
                analysis = self.decision_engine.run_comprehensive_analysis(
                    stock=ticker,
                    stock_data=stock_data,
                    start_date=start_date,
                    end_date=end_date,
                    portfolio=portfolio,
                )

                if "error" in analysis:
                    logger.error(
                        f"❌ Analysis failed for {ticker}: {analysis['error']}"
                    )
                    cycle_results["errors"].append(f"Analysis failed for {ticker}")
                    continue

                # Extract decision
                final_decision = analysis["final_decision"]

                # Create trading decision
                trading_decision = TradingDecision(
                    symbol=ticker,
                    signal=final_decision["signal"],
                    confidence=final_decision["confidence"],
                    quantity=final_decision["quantity"],
                    reasoning=final_decision.get("reasoning", "No reasoning provided"),
                )

                decisions[ticker] = trading_decision
                cycle_results["tickers_analyzed"].append(ticker)
                cycle_results["decisions"][ticker] = {
                    "signal": final_decision["signal"],
                    "confidence": final_decision["confidence"],
                    "quantity": final_decision["quantity"],
                }

                # Log decision
                logger.info(f"🎯 Decision for {ticker}:")
                logger.info(f"   Signal: {final_decision['signal']}")
                logger.info(f"   Confidence: {final_decision['confidence']:.1f}%")
                logger.info(f"   Quantity: {final_decision['quantity']}")
                logger.info(f"   Reasoning: {final_decision.get('reasoning', 'N/A')}")

                # Add decision to state
                current_price = (
                    stock_data["Close"].iloc[-1] if not stock_data.empty else 0
                )
                self.state_manager.add_decision(
                    {
                        "symbol": ticker,
                        "signal": final_decision["signal"],
                        "confidence": final_decision["confidence"],
                        "quantity": final_decision["quantity"],
                        "price": current_price,
                        "reasoning": final_decision.get("reasoning", "N/A"),
                        "executed": False,  # Will be updated after execution
                    }
                )

            except Exception as e:
                logger.error(f"❌ Error analyzing {ticker}: {e}")
                cycle_results["errors"].append(f"Error analyzing {ticker}: {str(e)}")

        # Execute decisions
        if decisions:
            logger.info(f"\n💼 Executing {len(decisions)} trading decisions...")
            execution_results = self.executor.execute_decisions(decisions)

            # Track results
            for ticker, result in execution_results.items():
                cycle_results["executions"][ticker] = {
                    "action": result.action,
                    "success": result.success,
                    "quantity": result.executed_quantity,
                    "order_id": result.order_id,
                    "error": result.error_message,
                }

                if result.success and result.action in ["BUY", "SELL"]:
                    self.successful_trades += 1
                self.total_trades += 1

                # Record trade execution in state
                self.state_manager.add_trade_execution(
                    {
                        "symbol": ticker,
                        "action": result.action,
                        "quantity": result.executed_quantity,
                        "price": result.executed_price
                        if hasattr(result, "executed_price")
                        else 0,
                        "total_value": result.executed_quantity * result.executed_price
                        if hasattr(result, "executed_price")
                        else 0,
                        "success": result.success,
                        "error_message": result.error_message,
                        "order_id": result.order_id,
                    }
                )

        # Print cycle summary
        logger.info(f"\n{'=' * 80}")
        logger.info(f"CYCLE #{self.cycle_count} SUMMARY")
        logger.info(f"{'=' * 80}")
        logger.info(f"Tickers Analyzed: {len(cycle_results['tickers_analyzed'])}")
        logger.info(f"Decisions Made: {len(cycle_results['decisions'])}")
        logger.info(
            f"Trades Executed: {len([r for r in cycle_results['executions'].values() if r['success']])}"
        )
        logger.info(f"Errors: {len(cycle_results['errors'])}")

        if cycle_results["errors"]:
            logger.info(f"\nErrors:")
            for error in cycle_results["errors"]:
                logger.error(f"  - {error}")

        # Signal distribution
        signals = [d["signal"] for d in cycle_results["decisions"].values()]
        if signals:
            buy_count = signals.count("BUY")
            sell_count = signals.count("SELL")
            hold_count = signals.count("HOLD")
            logger.info(
                f"\nSignal Distribution: BUY({buy_count}) | SELL({sell_count}) | HOLD({hold_count})"
            )

        logger.info(f"{'=' * 80}\n")

        return cycle_results

    def run_continuous(self, max_cycles: Optional[int] = None):
        """
        Run trading workflow continuously.

        Args:
            max_cycles: Maximum number of cycles (None = infinite)
        """
        logger.info(f"\n🚀 Starting Continuous Trading Workflow")
        logger.info(f"Tickers: {', '.join(self.tickers)}")
        logger.info(f"Check Interval: {self.check_interval} seconds")
        logger.info(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE TRADING'}")
        logger.info(f"Min Confidence: {self.min_confidence}%")
        logger.info(f"Max Position: {self.max_position_pct * 100}%")

        if max_cycles:
            logger.info(f"Max Cycles: {max_cycles}")

        logger.info(f"\n{'=' * 80}\n")

        try:
            while True:
                # Run cycle
                result = self.run_single_cycle()

                # Check if we've reached max cycles
                if max_cycles and self.cycle_count >= max_cycles:
                    logger.info(f"✅ Reached maximum cycles ({max_cycles})")
                    break

                # Print overall stats every 10 cycles
                if self.cycle_count % 10 == 0:
                    self.print_overall_stats()

                # Wait for next cycle
                logger.info(
                    f"⏰ Waiting {self.check_interval} seconds for next cycle..."
                )
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            logger.info(f"\n⚠️  Trading workflow interrupted by user")
        except Exception as e:
            logger.error(f"❌ Fatal error in trading workflow: {e}")
            raise
        finally:
            self.shutdown()

    def print_overall_stats(self):
        """Print overall trading statistics."""
        logger.info(f"\n{'=' * 80}")
        logger.info(f"OVERALL TRADING STATISTICS")
        logger.info(f"{'=' * 80}")
        logger.info(f"Total Cycles: {self.cycle_count}")
        logger.info(f"Total Trades: {self.total_trades}")
        logger.info(f"Successful Trades: {self.successful_trades}")

        if self.total_trades > 0:
            success_rate = (self.successful_trades / self.total_trades) * 100
            logger.info(f"Success Rate: {success_rate:.1f}%")

        # Portfolio summary
        try:
            summary = self.trader.get_portfolio_summary()
            logger.info(f"\nPortfolio Summary:")
            logger.info(f"  Cash: ${summary['account']['cash']:,.2f}")
            logger.info(
                f"  Portfolio Value: ${summary['account']['portfolio_value']:,.2f}"
            )
            logger.info(f"  Total Positions: {summary['total_positions']}")
            logger.info(
                f"  Unrealized P/L: ${summary['total_unrealized_pl']:,.2f} ({summary['total_unrealized_pl_pct']:.2f}%)"
            )
        except Exception as e:
            logger.error(f"Failed to get portfolio summary: {e}")

        # Execution stats
        exec_stats = self.executor.get_execution_stats()
        logger.info(f"\nExecution Statistics:")
        logger.info(f"  Total Executions: {exec_stats['total_executions']}")
        logger.info(f"  Buys: {exec_stats.get('buys', 0)}")
        logger.info(f"  Sells: {exec_stats.get('sells', 0)}")
        logger.info(f"  Holds: {exec_stats.get('holds', 0)}")

        logger.info(f"{'=' * 80}\n")

    def shutdown(self):
        """Shutdown workflow and cleanup."""
        logger.info(f"\n{'=' * 80}")
        logger.info("SHUTTING DOWN TRADING WORKFLOW")
        logger.info(f"{'=' * 80}")

        # Print final stats
        self.print_overall_stats()

        # Cancel any pending orders
        if not self.dry_run:
            logger.info("Canceling all pending orders...")
            self.trader.cancel_all_orders()

        logger.info("✅ Trading workflow shutdown complete")


def create_workflow(
    tickers: List[str],
    dry_run: bool = True,
    min_confidence: float = 60.0,
    max_position_pct: float = 0.20,
    check_interval: int = 60,
) -> TradingWorkflow:
    """Create a TradingWorkflow instance."""
    return TradingWorkflow(
        tickers=tickers,
        dry_run=dry_run,
        min_confidence=min_confidence,
        max_position_pct=max_position_pct,
        check_interval=check_interval,
    )


if __name__ == "__main__":
    # Example: Run trading workflow for AAPL, MSFT, GOOGL
    tickers = ["AAPL", "MSFT", "GOOGL"]

    workflow = create_workflow(
        tickers=tickers,
        dry_run=True,  # Safe mode - no real trades
        min_confidence=60.0,
        max_position_pct=0.20,
        check_interval=300,  # 5 minutes
    )

    # Run for 3 cycles as a test
    workflow.run_continuous(max_cycles=3)

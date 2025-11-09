"""
Portfolio Executor

Integrates decision engine with Alpaca trading to execute portfolio decisions.
Handles order execution, position management, and risk controls.
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
import pandas as pd

from src.trading.alpaca_trader import AlpacaTrader, TradeOrder

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class TradingDecision:
    """Represents a trading decision from the decision engine."""

    symbol: str
    signal: str  # BUY, SELL, HOLD
    confidence: float
    quantity: int
    reasoning: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class ExecutionResult:
    """Result of trade execution."""

    symbol: str
    action: str
    intended_quantity: int
    executed_quantity: int
    success: bool
    order_id: Optional[str] = None
    error_message: Optional[str] = None
    execution_price: Optional[float] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class PortfolioExecutor:
    """
    Executes portfolio decisions using Alpaca API.

    Features:
    - Execute buy/sell decisions from decision engine
    - Risk management and position sizing
    - Order tracking and execution monitoring
    - Portfolio rebalancing
    - Execution analytics
    """

    def __init__(
        self,
        trader: Optional[AlpacaTrader] = None,
        max_position_pct: float = 0.20,
        min_confidence: float = 60.0,
        enable_risk_controls: bool = True,
        dry_run: bool = False,
    ):
        """
        Initialize Portfolio Executor.

        Args:
            trader: AlpacaTrader instance (creates new if None)
            max_position_pct: Max position size as % of portfolio (default: 20%)
            min_confidence: Minimum confidence to execute trade (default: 60%)
            enable_risk_controls: Enable risk control checks (default: True)
            dry_run: Simulate trades without executing (default: False)
        """
        self.trader = trader or AlpacaTrader(paper_trading=True)
        self.max_position_pct = max_position_pct
        self.min_confidence = min_confidence
        self.enable_risk_controls = enable_risk_controls
        self.dry_run = dry_run

        # Execution history
        self.execution_history: List[ExecutionResult] = []

        logger.info(f"Portfolio Executor initialized (dry_run={dry_run})")

    # ============================================
    # Decision Execution
    # ============================================

    def execute_decision(
        self, decision: TradingDecision, force: bool = False
    ) -> ExecutionResult:
        """
        Execute a single trading decision.

        Args:
            decision: TradingDecision object
            force: Force execution even if confidence is low

        Returns:
            ExecutionResult with execution details
        """
        logger.info(f"\n{'=' * 60}")
        logger.info(f"Processing decision for {decision.symbol}")
        logger.info(
            f"Signal: {decision.signal}, Confidence: {decision.confidence}%, Quantity: {decision.quantity}"
        )
        logger.info(f"Reasoning: {decision.reasoning}")
        logger.info(f"{'=' * 60}")

        # Validate decision
        if not force and decision.confidence < self.min_confidence:
            logger.warning(
                f"⚠️  Confidence {decision.confidence}% below minimum {self.min_confidence}%"
            )
            result = ExecutionResult(
                symbol=decision.symbol,
                action="SKIP",
                intended_quantity=decision.quantity,
                executed_quantity=0,
                success=False,
                error_message=f"Confidence {decision.confidence}% below threshold {self.min_confidence}%",
            )
            self.execution_history.append(result)
            return result

        # Handle HOLD signal
        if decision.signal.upper() == "HOLD":
            logger.info(f"⏸️  HOLD signal for {decision.symbol} - No action taken")
            result = ExecutionResult(
                symbol=decision.symbol,
                action="HOLD",
                intended_quantity=0,
                executed_quantity=0,
                success=True,
            )
            self.execution_history.append(result)
            return result

        # Execute BUY or SELL
        if decision.signal.upper() == "BUY":
            result = self._execute_buy(decision)
        elif decision.signal.upper() == "SELL":
            result = self._execute_sell(decision)
        else:
            logger.error(f"❌ Invalid signal: {decision.signal}")
            result = ExecutionResult(
                symbol=decision.symbol,
                action="ERROR",
                intended_quantity=decision.quantity,
                executed_quantity=0,
                success=False,
                error_message=f"Invalid signal: {decision.signal}",
            )

        self.execution_history.append(result)
        return result

    def _execute_buy(self, decision: TradingDecision) -> ExecutionResult:
        """Execute buy order."""
        symbol = decision.symbol
        quantity = decision.quantity

        # Validate quantity
        if quantity <= 0:
            logger.warning(f"⚠️  Invalid quantity {quantity} for BUY order")
            return ExecutionResult(
                symbol=symbol,
                action="BUY",
                intended_quantity=quantity,
                executed_quantity=0,
                success=False,
                error_message="Invalid quantity",
            )

        # Apply risk controls
        if self.enable_risk_controls:
            adjusted_qty, reason = self._apply_risk_controls(symbol, quantity, "buy")
            if adjusted_qty != quantity:
                logger.info(
                    f"📊 Quantity adjusted by risk controls: {quantity} → {adjusted_qty} ({reason})"
                )
                quantity = adjusted_qty

            if quantity == 0:
                logger.warning(f"⚠️  Risk controls rejected BUY order: {reason}")
                return ExecutionResult(
                    symbol=symbol,
                    action="BUY",
                    intended_quantity=decision.quantity,
                    executed_quantity=0,
                    success=False,
                    error_message=f"Risk control: {reason}",
                )

        # Check if trade can be executed
        can_trade, trade_reason = self.trader.can_trade(symbol, quantity, "buy")
        if not can_trade:
            logger.error(f"❌ Cannot execute BUY: {trade_reason}")
            return ExecutionResult(
                symbol=symbol,
                action="BUY",
                intended_quantity=decision.quantity,
                executed_quantity=0,
                success=False,
                error_message=trade_reason,
            )

        # Execute order
        if self.dry_run:
            logger.info(f"🔍 [DRY RUN] Would BUY {quantity} shares of {symbol}")
            return ExecutionResult(
                symbol=symbol,
                action="BUY",
                intended_quantity=decision.quantity,
                executed_quantity=quantity,
                success=True,
                order_id="DRY_RUN",
                execution_price=self.trader.get_latest_price(symbol),
            )

        # Submit order to Alpaca
        logger.info(f"💰 Executing BUY order: {symbol} x {quantity}")
        order = self.trader.buy(symbol, quantity)

        if order:
            logger.info(
                f"✅ BUY order executed: {symbol} x {quantity} (Order ID: {order['id']})"
            )
            return ExecutionResult(
                symbol=symbol,
                action="BUY",
                intended_quantity=decision.quantity,
                executed_quantity=quantity,
                success=True,
                order_id=order["id"],
                execution_price=order.get("filled_avg_price"),
            )
        else:
            logger.error(f"❌ BUY order failed for {symbol}")
            return ExecutionResult(
                symbol=symbol,
                action="BUY",
                intended_quantity=decision.quantity,
                executed_quantity=0,
                success=False,
                error_message="Order submission failed",
            )

    def _execute_sell(self, decision: TradingDecision) -> ExecutionResult:
        """Execute sell order."""
        symbol = decision.symbol
        quantity = decision.quantity

        # Get current position
        current_position = self.trader.get_position_quantity(symbol, force_refresh=True)

        if current_position <= 0:
            logger.warning(f"⚠️  No position to sell for {symbol}")
            return ExecutionResult(
                symbol=symbol,
                action="SELL",
                intended_quantity=quantity,
                executed_quantity=0,
                success=False,
                error_message="No position to sell",
            )

        # Adjust quantity if trying to sell more than owned
        actual_quantity = min(quantity, current_position)
        if actual_quantity != quantity:
            logger.info(
                f"📊 Sell quantity adjusted: {quantity} → {actual_quantity} (max available)"
            )
            quantity = actual_quantity

        # Check if trade can be executed
        can_trade, trade_reason = self.trader.can_trade(symbol, quantity, "sell")
        if not can_trade:
            logger.error(f"❌ Cannot execute SELL: {trade_reason}")
            return ExecutionResult(
                symbol=symbol,
                action="SELL",
                intended_quantity=decision.quantity,
                executed_quantity=0,
                success=False,
                error_message=trade_reason,
            )

        # Execute order
        if self.dry_run:
            logger.info(f"🔍 [DRY RUN] Would SELL {quantity} shares of {symbol}")
            return ExecutionResult(
                symbol=symbol,
                action="SELL",
                intended_quantity=decision.quantity,
                executed_quantity=quantity,
                success=True,
                order_id="DRY_RUN",
                execution_price=self.trader.get_latest_price(symbol),
            )

        # Submit order to Alpaca
        logger.info(f"💸 Executing SELL order: {symbol} x {quantity}")
        order = self.trader.sell(symbol, quantity)

        if order:
            logger.info(
                f"✅ SELL order executed: {symbol} x {quantity} (Order ID: {order['id']})"
            )
            return ExecutionResult(
                symbol=symbol,
                action="SELL",
                intended_quantity=decision.quantity,
                executed_quantity=quantity,
                success=True,
                order_id=order["id"],
                execution_price=order.get("filled_avg_price"),
            )
        else:
            logger.error(f"❌ SELL order failed for {symbol}")
            return ExecutionResult(
                symbol=symbol,
                action="SELL",
                intended_quantity=decision.quantity,
                executed_quantity=0,
                success=False,
                error_message="Order submission failed",
            )

    # ============================================
    # Batch Execution
    # ============================================

    def execute_decisions(
        self, decisions: Dict[str, TradingDecision], parallel: bool = False
    ) -> Dict[str, ExecutionResult]:
        """
        Execute multiple trading decisions.

        Args:
            decisions: Dictionary of symbol -> TradingDecision
            parallel: Execute in parallel (not implemented yet)

        Returns:
            Dictionary of symbol -> ExecutionResult
        """
        logger.info(f"\n{'=' * 60}")
        logger.info(f"Executing {len(decisions)} trading decisions")
        logger.info(f"{'=' * 60}\n")

        results = {}
        for symbol, decision in decisions.items():
            result = self.execute_decision(decision)
            results[symbol] = result

        # Print summary
        successful = sum(1 for r in results.values() if r.success)
        logger.info(f"\n{'=' * 60}")
        logger.info(f"Execution Summary: {successful}/{len(decisions)} successful")
        logger.info(f"{'=' * 60}\n")

        return results

    # ============================================
    # Risk Controls
    # ============================================

    def _apply_risk_controls(
        self, symbol: str, quantity: int, side: str
    ) -> Tuple[int, str]:
        """
        Apply risk controls to adjust order quantity.

        Returns:
            (adjusted_quantity, reason) tuple
        """
        # Get maximum allowed quantity
        max_qty = self.trader.get_max_quantity(symbol, self.max_position_pct)

        if side == "buy":
            # Check against max position size
            current_position = self.trader.get_position_quantity(symbol)
            max_additional = max_qty - current_position

            if max_additional <= 0:
                return (
                    0,
                    f"Position limit reached (max {max_qty}, current {current_position})",
                )

            if quantity > max_additional:
                return (
                    max_additional,
                    f"Position limit (max {max_qty}, current {current_position})",
                )

        return quantity, "OK"

    def validate_portfolio_risk(self) -> Tuple[bool, List[str]]:
        """
        Validate overall portfolio risk.

        Returns:
            (is_valid, warnings) tuple
        """
        warnings = []

        try:
            account = self.trader.get_account()
            positions = self.trader.get_all_positions()

            # Check for pattern day trader status
            if account.get("pattern_day_trader"):
                warnings.append("⚠️  Account flagged as Pattern Day Trader")

            # Check day trade count
            daytrade_count = account.get("daytrade_count", 0)
            if daytrade_count >= 3:
                warnings.append(f"⚠️  Day trade count: {daytrade_count}/3")

            # Check portfolio concentration
            total_value = account["portfolio_value"]
            for pos in positions:
                position_pct = (pos.market_value / total_value) * 100
                if position_pct > (self.max_position_pct * 100):
                    warnings.append(
                        f"⚠️  {pos.symbol} position ({position_pct:.1f}%) exceeds limit ({self.max_position_pct * 100}%)"
                    )

            # Check buying power
            if account["buying_power"] < account["cash"] * 0.1:
                warnings.append("⚠️  Low buying power")

            return len(warnings) == 0, warnings

        except Exception as e:
            return False, [f"❌ Error validating portfolio risk: {e}"]

    # ============================================
    # Analytics
    # ============================================

    def get_execution_stats(self) -> Dict:
        """Get execution statistics."""
        if not self.execution_history:
            return {"total_executions": 0}

        total = len(self.execution_history)
        successful = sum(1 for r in self.execution_history if r.success)
        buys = sum(1 for r in self.execution_history if r.action == "BUY" and r.success)
        sells = sum(
            1 for r in self.execution_history if r.action == "SELL" and r.success
        )
        holds = sum(1 for r in self.execution_history if r.action == "HOLD")

        return {
            "total_executions": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": (successful / total * 100) if total > 0 else 0,
            "buys": buys,
            "sells": sells,
            "holds": holds,
        }

    def print_execution_summary(self):
        """Print execution summary."""
        stats = self.get_execution_stats()

        print(f"\n{'=' * 60}")
        print("EXECUTION SUMMARY")
        print(f"{'=' * 60}")
        print(f"Total Executions: {stats['total_executions']}")
        print(f"Successful: {stats['successful']}")
        print(f"Failed: {stats['failed']}")
        print(f"Success Rate: {stats.get('success_rate', 0):.1f}%")
        print(f"\nActions:")
        print(f"  Buys: {stats.get('buys', 0)}")
        print(f"  Sells: {stats.get('sells', 0)}")
        print(f"  Holds: {stats.get('holds', 0)}")
        print(f"{'=' * 60}\n")

    def get_recent_executions(self, limit: int = 10) -> List[ExecutionResult]:
        """Get recent executions."""
        return self.execution_history[-limit:]


# Convenience functions
def create_executor(
    dry_run: bool = False, max_position_pct: float = 0.20, min_confidence: float = 60.0
) -> PortfolioExecutor:
    """Create a PortfolioExecutor instance."""
    return PortfolioExecutor(
        dry_run=dry_run,
        max_position_pct=max_position_pct,
        min_confidence=min_confidence,
    )


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)

    # Create executor in dry-run mode
    executor = create_executor(dry_run=True, min_confidence=50.0)

    # Create sample decisions
    decisions = {
        "AAPL": TradingDecision(
            symbol="AAPL",
            signal="BUY",
            confidence=75.0,
            quantity=10,
            reasoning="Strong fundamentals and technical momentum",
        ),
        "MSFT": TradingDecision(
            symbol="MSFT",
            signal="HOLD",
            confidence=55.0,
            quantity=0,
            reasoning="Mixed signals",
        ),
    }

    # Execute decisions
    results = executor.execute_decisions(decisions)

    # Print summary
    executor.print_execution_summary()

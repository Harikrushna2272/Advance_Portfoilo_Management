"""
Enhanced Alpaca Trading Module

This module provides a comprehensive interface for trading stocks using the Alpaca API.
It includes order management, portfolio tracking, risk controls, and error handling.
"""

import os
import logging
from typing import Dict, List, Optional, Union, Literal
from datetime import datetime, timedelta
from dataclasses import dataclass
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import APIError, TimeFrame
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class TradeOrder:
    """Represents a trade order with all necessary information."""

    symbol: str
    action: Literal["buy", "sell", "hold"]
    quantity: int
    confidence: float
    order_type: str = "market"
    time_in_force: str = "gtc"
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None

    def __post_init__(self):
        """Validate order parameters."""
        if self.action not in ["buy", "sell", "hold"]:
            raise ValueError(f"Invalid action: {self.action}")
        if self.quantity < 0:
            raise ValueError(f"Quantity must be positive: {self.quantity}")
        if self.confidence < 0 or self.confidence > 100:
            raise ValueError(f"Confidence must be between 0 and 100: {self.confidence}")


@dataclass
class PortfolioPosition:
    """Represents a portfolio position."""

    symbol: str
    quantity: int
    avg_entry_price: float
    current_price: float
    market_value: float
    unrealized_pl: float
    unrealized_plpc: float
    cost_basis: float

    @property
    def is_long(self) -> bool:
        return self.quantity > 0

    @property
    def is_short(self) -> bool:
        return self.quantity < 0


class AlpacaTrader:
    """
    Enhanced Alpaca trading interface with comprehensive features.

    Features:
    - Order execution (market, limit, stop-loss)
    - Portfolio management and tracking
    - Position sizing and risk controls
    - Order history and analytics
    - Real-time account data
    - Paper trading support
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        base_url: Optional[str] = None,
        paper_trading: bool = True,
    ):
        """
        Initialize Alpaca trader.

        Args:
            api_key: Alpaca API key (defaults to ALPACA_API_KEY env var)
            api_secret: Alpaca API secret (defaults to ALPACA_API_SECRET env var)
            base_url: Alpaca base URL (defaults to ALPACA_BASE_URL env var)
            paper_trading: Use paper trading account (default: True)
        """
        self.api_key = api_key or os.getenv("ALPACA_API_KEY")
        self.api_secret = api_secret or os.getenv("ALPACA_API_SECRET")

        # Determine base URL
        if base_url:
            self.base_url = base_url
        elif paper_trading:
            self.base_url = "https://paper-api.alpaca.markets"
        else:
            self.base_url = os.getenv("ALPACA_BASE_URL", "https://api.alpaca.markets")

        # Validate credentials
        if not self.api_key or not self.api_secret:
            raise ValueError(
                "Alpaca API credentials not found. Set ALPACA_API_KEY and ALPACA_API_SECRET environment variables."
            )

        # Initialize API client
        try:
            self.api = tradeapi.REST(
                self.api_key, self.api_secret, self.base_url, api_version="v2"
            )
            logger.info(f"Alpaca API initialized: {self.base_url}")
        except Exception as e:
            logger.error(f"Failed to initialize Alpaca API: {e}")
            raise

        # Cache for account and position data
        self._account_cache = None
        self._positions_cache = {}
        self._cache_timestamp = None
        self._cache_ttl = 60  # Cache TTL in seconds

    def _is_cache_valid(self) -> bool:
        """Check if cache is still valid."""
        if self._cache_timestamp is None:
            return False
        return (
            datetime.now() - self._cache_timestamp
        ).total_seconds() < self._cache_ttl

    def _refresh_cache(self):
        """Refresh account and position cache."""
        try:
            self._account_cache = self.api.get_account()
            positions = self.api.list_positions()
            self._positions_cache = {pos.symbol: pos for pos in positions}
            self._cache_timestamp = datetime.now()
            logger.debug("Cache refreshed successfully")
        except Exception as e:
            logger.error(f"Failed to refresh cache: {e}")

    # ============================================
    # Account Management
    # ============================================

    def get_account(self, force_refresh: bool = False) -> dict:
        """
        Get account information.

        Args:
            force_refresh: Force cache refresh

        Returns:
            Dictionary with account information
        """
        if force_refresh or not self._is_cache_valid():
            self._refresh_cache()

        if self._account_cache is None:
            raise Exception("Failed to retrieve account information")

        account = self._account_cache
        return {
            "cash": float(account.cash),
            "portfolio_value": float(account.portfolio_value),
            "buying_power": float(account.buying_power),
            "equity": float(account.equity),
            "last_equity": float(account.last_equity),
            "multiplier": int(account.multiplier),
            "long_market_value": float(account.long_market_value),
            "short_market_value": float(account.short_market_value),
            "initial_margin": float(account.initial_margin),
            "maintenance_margin": float(account.maintenance_margin),
            "daytrade_count": int(account.daytrade_count),
            "pattern_day_trader": account.pattern_day_trader,
            "trading_blocked": account.trading_blocked,
            "transfers_blocked": account.transfers_blocked,
            "account_blocked": account.account_blocked,
        }

    def get_buying_power(self, force_refresh: bool = False) -> float:
        """Get available buying power."""
        account = self.get_account(force_refresh)
        return account["buying_power"]

    def get_cash_balance(self, force_refresh: bool = False) -> float:
        """Get cash balance."""
        account = self.get_account(force_refresh)
        return account["cash"]

    def get_portfolio_value(self, force_refresh: bool = False) -> float:
        """Get total portfolio value."""
        account = self.get_account(force_refresh)
        return account["portfolio_value"]

    # ============================================
    # Position Management
    # ============================================

    def get_position(
        self, symbol: str, force_refresh: bool = False
    ) -> Optional[PortfolioPosition]:
        """
        Get position for a specific symbol.

        Args:
            symbol: Stock symbol
            force_refresh: Force cache refresh

        Returns:
            PortfolioPosition object or None if no position
        """
        if force_refresh or not self._is_cache_valid():
            self._refresh_cache()

        pos = self._positions_cache.get(symbol)
        if pos is None:
            return None

        return PortfolioPosition(
            symbol=pos.symbol,
            quantity=int(pos.qty),
            avg_entry_price=float(pos.avg_entry_price),
            current_price=float(pos.current_price),
            market_value=float(pos.market_value),
            unrealized_pl=float(pos.unrealized_pl),
            unrealized_plpc=float(pos.unrealized_plpc),
            cost_basis=float(pos.cost_basis),
        )

    def get_all_positions(self, force_refresh: bool = False) -> List[PortfolioPosition]:
        """Get all open positions."""
        if force_refresh or not self._is_cache_valid():
            self._refresh_cache()

        return [
            PortfolioPosition(
                symbol=pos.symbol,
                quantity=int(pos.qty),
                avg_entry_price=float(pos.avg_entry_price),
                current_price=float(pos.current_price),
                market_value=float(pos.market_value),
                unrealized_pl=float(pos.unrealized_pl),
                unrealized_plpc=float(pos.unrealized_plpc),
                cost_basis=float(pos.cost_basis),
            )
            for pos in self._positions_cache.values()
        ]

    def get_position_quantity(self, symbol: str, force_refresh: bool = False) -> int:
        """Get quantity of shares held for a symbol."""
        position = self.get_position(symbol, force_refresh)
        return position.quantity if position else 0

    # ============================================
    # Market Data
    # ============================================

    def get_latest_price(self, symbol: str) -> Optional[float]:
        """
        Get latest price for a symbol.

        Args:
            symbol: Stock symbol

        Returns:
            Latest price or None if not available
        """
        try:
            quote = self.api.get_latest_trade(symbol)
            return float(quote.price)
        except Exception as e:
            logger.error(f"Failed to get latest price for {symbol}: {e}")
            return None

    def get_latest_quote(self, symbol: str) -> Optional[Dict]:
        """Get latest quote (bid/ask) for a symbol."""
        try:
            quote = self.api.get_latest_quote(symbol)
            return {
                "symbol": symbol,
                "bid_price": float(quote.bid_price),
                "ask_price": float(quote.ask_price),
                "bid_size": int(quote.bid_size),
                "ask_size": int(quote.ask_size),
                "timestamp": quote.timestamp,
            }
        except Exception as e:
            logger.error(f"Failed to get latest quote for {symbol}: {e}")
            return None

    def get_bars(
        self,
        symbol: str,
        timeframe: str = "1Day",
        start: Optional[str] = None,
        end: Optional[str] = None,
        limit: int = 100,
    ) -> pd.DataFrame:
        """
        Get historical bar data.

        Args:
            symbol: Stock symbol
            timeframe: Bar timeframe (1Min, 5Min, 15Min, 1Hour, 1Day)
            start: Start date (YYYY-MM-DD)
            end: End date (YYYY-MM-DD)
            limit: Number of bars to fetch

        Returns:
            DataFrame with OHLCV data
        """
        try:
            # Map timeframe string to TimeFrame enum
            timeframe_map = {
                "1Min": TimeFrame.Minute,
                "5Min": TimeFrame(5, TimeFrame.Minute),
                "15Min": TimeFrame(15, TimeFrame.Minute),
                "1Hour": TimeFrame.Hour,
                "1Day": TimeFrame.Day,
            }

            tf = timeframe_map.get(timeframe, TimeFrame.Day)

            bars = self.api.get_bars(symbol, tf, start=start, end=end, limit=limit).df

            return bars
        except Exception as e:
            logger.error(f"Failed to get bars for {symbol}: {e}")
            return pd.DataFrame()

    # ============================================
    # Order Execution
    # ============================================

    def submit_order(
        self,
        symbol: str,
        qty: int,
        side: Literal["buy", "sell"],
        order_type: str = "market",
        time_in_force: str = "gtc",
        limit_price: Optional[float] = None,
        stop_price: Optional[float] = None,
        client_order_id: Optional[str] = None,
    ) -> Optional[dict]:
        """
        Submit an order to Alpaca.

        Args:
            symbol: Stock symbol
            qty: Quantity of shares
            side: "buy" or "sell"
            order_type: Order type (market, limit, stop, stop_limit)
            time_in_force: Time in force (day, gtc, ioc, fok)
            limit_price: Limit price for limit orders
            stop_price: Stop price for stop orders
            client_order_id: Custom order ID

        Returns:
            Order object or None if failed
        """
        try:
            logger.info(
                f"Submitting {side.upper()} order: {symbol} x {qty} @ {order_type}"
            )

            order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type=order_type,
                time_in_force=time_in_force,
                limit_price=limit_price,
                stop_price=stop_price,
                client_order_id=client_order_id,
            )

            logger.info(f"✅ Order submitted successfully: {order.id}")

            return {
                "id": order.id,
                "client_order_id": order.client_order_id,
                "symbol": order.symbol,
                "qty": int(order.qty),
                "side": order.side,
                "type": order.type,
                "time_in_force": order.time_in_force,
                "limit_price": float(order.limit_price) if order.limit_price else None,
                "stop_price": float(order.stop_price) if order.stop_price else None,
                "status": order.status,
                "created_at": order.created_at,
                "filled_avg_price": float(order.filled_avg_price)
                if order.filled_avg_price
                else None,
            }
        except APIError as e:
            logger.error(f"❌ Alpaca API error: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Order submission failed: {e}")
            return None

    def buy(
        self,
        symbol: str,
        qty: int,
        order_type: str = "market",
        limit_price: Optional[float] = None,
        stop_price: Optional[float] = None,
    ) -> Optional[dict]:
        """Submit a buy order."""
        return self.submit_order(
            symbol=symbol,
            qty=qty,
            side="buy",
            order_type=order_type,
            limit_price=limit_price,
            stop_price=stop_price,
        )

    def sell(
        self,
        symbol: str,
        qty: int,
        order_type: str = "market",
        limit_price: Optional[float] = None,
        stop_price: Optional[float] = None,
    ) -> Optional[dict]:
        """Submit a sell order."""
        return self.submit_order(
            symbol=symbol,
            qty=qty,
            side="sell",
            order_type=order_type,
            limit_price=limit_price,
            stop_price=stop_price,
        )

    def execute_trade_order(self, trade_order: TradeOrder) -> Optional[dict]:
        """
        Execute a TradeOrder object.

        Args:
            trade_order: TradeOrder object with trade details

        Returns:
            Order result or None
        """
        if trade_order.action == "hold":
            logger.info(f"⏸️  HOLD signal for {trade_order.symbol} - No action taken")
            return None

        if trade_order.quantity <= 0:
            logger.warning(
                f"❌ Invalid quantity {trade_order.quantity} for {trade_order.symbol}"
            )
            return None

        return self.submit_order(
            symbol=trade_order.symbol,
            qty=trade_order.quantity,
            side=trade_order.action,
            order_type=trade_order.order_type,
            time_in_force=trade_order.time_in_force,
            limit_price=trade_order.limit_price,
            stop_price=trade_order.stop_price,
        )

    # ============================================
    # Order Management
    # ============================================

    def get_order(self, order_id: str) -> Optional[dict]:
        """Get order by ID."""
        try:
            order = self.api.get_order(order_id)
            return {
                "id": order.id,
                "symbol": order.symbol,
                "qty": int(order.qty),
                "side": order.side,
                "type": order.type,
                "status": order.status,
                "filled_qty": int(order.filled_qty),
                "filled_avg_price": float(order.filled_avg_price)
                if order.filled_avg_price
                else None,
                "created_at": order.created_at,
                "updated_at": order.updated_at,
            }
        except Exception as e:
            logger.error(f"Failed to get order {order_id}: {e}")
            return None

    def get_all_orders(self, status: str = "open", limit: int = 100) -> List[dict]:
        """
        Get all orders with optional status filter.

        Args:
            status: Order status (open, closed, all)
            limit: Maximum number of orders to return

        Returns:
            List of order dictionaries
        """
        try:
            orders = self.api.list_orders(status=status, limit=limit)
            return [
                {
                    "id": order.id,
                    "symbol": order.symbol,
                    "qty": int(order.qty),
                    "side": order.side,
                    "type": order.type,
                    "status": order.status,
                    "filled_qty": int(order.filled_qty),
                    "filled_avg_price": float(order.filled_avg_price)
                    if order.filled_avg_price
                    else None,
                    "created_at": order.created_at,
                }
                for order in orders
            ]
        except Exception as e:
            logger.error(f"Failed to get orders: {e}")
            return []

    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order by ID."""
        try:
            self.api.cancel_order(order_id)
            logger.info(f"✅ Order {order_id} canceled successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to cancel order {order_id}: {e}")
            return False

    def cancel_all_orders(self) -> bool:
        """Cancel all open orders."""
        try:
            self.api.cancel_all_orders()
            logger.info("✅ All orders canceled successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to cancel all orders: {e}")
            return False

    # ============================================
    # Position Closing
    # ============================================

    def close_position(self, symbol: str, qty: Optional[int] = None) -> Optional[dict]:
        """
        Close a position (or partial position).

        Args:
            symbol: Stock symbol
            qty: Quantity to close (None = close all)

        Returns:
            Order result or None
        """
        try:
            position = self.get_position(symbol, force_refresh=True)
            if position is None:
                logger.warning(f"No position found for {symbol}")
                return None

            qty_to_close = qty if qty is not None else abs(position.quantity)

            if position.quantity > 0:
                # Long position - sell to close
                return self.sell(symbol, qty_to_close)
            elif position.quantity < 0:
                # Short position - buy to close
                return self.buy(symbol, qty_to_close)
            else:
                logger.info(f"No position to close for {symbol}")
                return None

        except Exception as e:
            logger.error(f"Failed to close position for {symbol}: {e}")
            return None

    def close_all_positions(self) -> bool:
        """Close all open positions."""
        try:
            self.api.close_all_positions()
            logger.info("✅ All positions closed successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to close all positions: {e}")
            return False

    # ============================================
    # Risk Controls
    # ============================================

    def can_trade(
        self, symbol: str, qty: int, side: Literal["buy", "sell"]
    ) -> tuple[bool, str]:
        """
        Check if a trade can be executed based on account status and risk controls.

        Returns:
            (can_trade, reason) tuple
        """
        try:
            account = self.get_account(force_refresh=True)

            # Check if account is blocked
            if account["trading_blocked"]:
                return False, "Trading is blocked on this account"

            if account["account_blocked"]:
                return False, "Account is blocked"

            # Check buying power for buy orders
            if side == "buy":
                current_price = self.get_latest_price(symbol)
                if current_price is None:
                    return False, f"Could not get price for {symbol}"

                required_buying_power = current_price * qty
                available_buying_power = account["buying_power"]

                if required_buying_power > available_buying_power:
                    return (
                        False,
                        f"Insufficient buying power: need ${required_buying_power:.2f}, have ${available_buying_power:.2f}",
                    )

            # Check if selling more than owned
            if side == "sell":
                position_qty = self.get_position_quantity(symbol, force_refresh=True)
                if qty > position_qty:
                    return False, f"Cannot sell {qty} shares, only own {position_qty}"

            return True, "OK"

        except Exception as e:
            return False, f"Error checking trade validity: {e}"

    def get_max_quantity(self, symbol: str, max_position_value_pct: float = 0.2) -> int:
        """
        Calculate maximum quantity that can be purchased based on buying power and position limit.

        Args:
            symbol: Stock symbol
            max_position_value_pct: Maximum position value as % of portfolio (default: 20%)

        Returns:
            Maximum quantity that can be purchased
        """
        try:
            current_price = self.get_latest_price(symbol)
            if current_price is None or current_price <= 0:
                return 0

            account = self.get_account(force_refresh=True)
            portfolio_value = account["portfolio_value"]
            buying_power = account["buying_power"]

            # Calculate max based on position limit
            max_position_value = portfolio_value * max_position_value_pct
            max_qty_by_position = int(max_position_value / current_price)

            # Calculate max based on buying power
            max_qty_by_bp = int(buying_power / current_price)

            # Return the minimum of the two
            return min(max_qty_by_position, max_qty_by_bp)

        except Exception as e:
            logger.error(f"Error calculating max quantity for {symbol}: {e}")
            return 0

    # ============================================
    # Utility Methods
    # ============================================

    def is_market_open(self) -> bool:
        """Check if market is currently open."""
        try:
            clock = self.api.get_clock()
            return clock.is_open
        except Exception as e:
            logger.error(f"Failed to check market status: {e}")
            return False

    def get_market_hours(self) -> Optional[dict]:
        """Get next market open/close times."""
        try:
            clock = self.api.get_clock()
            return {
                "is_open": clock.is_open,
                "next_open": clock.next_open,
                "next_close": clock.next_close,
                "timestamp": clock.timestamp,
            }
        except Exception as e:
            logger.error(f"Failed to get market hours: {e}")
            return None

    def get_portfolio_summary(self) -> dict:
        """Get comprehensive portfolio summary."""
        try:
            account = self.get_account(force_refresh=True)
            positions = self.get_all_positions(force_refresh=True)

            total_pl = sum(pos.unrealized_pl for pos in positions)
            total_pl_pct = (
                (total_pl / account["equity"]) * 100 if account["equity"] > 0 else 0
            )

            return {
                "account": account,
                "positions": [
                    {
                        "symbol": pos.symbol,
                        "quantity": pos.quantity,
                        "avg_entry_price": pos.avg_entry_price,
                        "current_price": pos.current_price,
                        "market_value": pos.market_value,
                        "unrealized_pl": pos.unrealized_pl,
                        "unrealized_plpc": pos.unrealized_plpc,
                    }
                    for pos in positions
                ],
                "total_positions": len(positions),
                "total_unrealized_pl": total_pl,
                "total_unrealized_pl_pct": total_pl_pct,
            }
        except Exception as e:
            logger.error(f"Failed to get portfolio summary: {e}")
            return {}


# Convenience function to create trader instance
def create_trader(paper_trading: bool = True) -> AlpacaTrader:
    """Create and return an AlpacaTrader instance."""
    return AlpacaTrader(paper_trading=paper_trading)


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)

    # Create trader
    trader = create_trader(paper_trading=True)

    # Get account info
    account = trader.get_account()
    print(f"Account Balance: ${account['cash']:.2f}")
    print(f"Portfolio Value: ${account['portfolio_value']:.2f}")

    # Check market status
    print(f"Market Open: {trader.is_market_open()}")

    # Get portfolio summary
    summary = trader.get_portfolio_summary()
    print(f"Total Positions: {summary['total_positions']}")

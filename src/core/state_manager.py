"""
Real-time State Manager
Synchronizes trading system state with UI through persistent storage
"""

import json
import sqlite3
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class TradingState:
    """Complete trading system state snapshot."""

    timestamp: str
    trading_active: bool
    cycle_count: int
    total_decisions: int
    total_trades: int
    successful_trades: int

    # Portfolio state
    portfolio: Dict[str, Any]

    # System health
    system_health: Dict[str, Any]

    # Recent decisions (last 50)
    recent_decisions: List[Dict[str, Any]]

    # Analytics
    analytics: Dict[str, Any]

    # Settings
    settings: Dict[str, Any]

    # Portfolio history
    portfolio_history: List[Dict[str, Any]]

    # Daily P&L history
    daily_pnl_history: List[Dict[str, Any]]


class StateManager:
    """
    Manages real-time state synchronization between trading system and UI.

    Uses both JSON files for quick access and SQLite for historical data.
    Thread-safe with locking mechanism.
    """

    def __init__(self, data_dir: str = "data/state"):
        """Initialize state manager."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.state_file = self.data_dir / "current_state.json"
        self.db_file = self.data_dir / "trading_history.db"

        self._lock = threading.Lock()

        # Initialize database
        self._init_database()

        # Initialize state if not exists
        if not self.state_file.exists():
            self._initialize_state()

        logger.info(f"StateManager initialized with data_dir: {self.data_dir}")

    def _init_database(self):
        """Initialize SQLite database for historical data."""
        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()

        # Trading decisions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trading_decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                symbol TEXT NOT NULL,
                signal TEXT NOT NULL,
                confidence REAL NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL,
                reasoning TEXT,
                executed BOOLEAN NOT NULL,
                order_id TEXT,
                cycle_count INTEGER
            )
        """)

        # Trade executions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trade_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                symbol TEXT NOT NULL,
                action TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL,
                total_value REAL,
                success BOOLEAN NOT NULL,
                error_message TEXT,
                order_id TEXT
            )
        """)

        # Portfolio snapshots table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS portfolio_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                total_value REAL NOT NULL,
                cash REAL NOT NULL,
                invested REAL NOT NULL,
                total_return REAL NOT NULL,
                total_return_pct REAL NOT NULL,
                positions_json TEXT NOT NULL
            )
        """)

        # Performance metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                daily_pnl REAL,
                weekly_pnl REAL,
                monthly_pnl REAL,
                sharpe_ratio REAL,
                max_drawdown REAL,
                win_rate REAL
            )
        """)

        conn.commit()
        conn.close()

        logger.info("Database initialized successfully")

    def _initialize_state(self):
        """Initialize default state."""
        initial_state = TradingState(
            timestamp=datetime.now().isoformat(),
            trading_active=False,
            cycle_count=0,
            total_decisions=0,
            total_trades=0,
            successful_trades=0,
            portfolio={
                "cash": 100000.0,
                "positions": {},
                "cost_basis": {},
                "total_value": 100000.0,
                "total_return": 0.0,
                "total_return_pct": 0.0,
            },
            system_health={
                "api_status": "Disconnected",
                "database_status": "Online",
                "models_loaded": 0,
                "total_models": 5,
                "memory_usage": 0,
                "cpu_usage": 0,
            },
            recent_decisions=[],
            analytics={
                "daily_pnl": 0.0,
                "weekly_pnl": 0.0,
                "monthly_pnl": 0.0,
                "sharpe_ratio": 0.0,
                "max_drawdown": 0.0,
                "win_rate": 0.0,
            },
            settings={
                "stock_list": ["AAPL", "TSLA", "GOOGL"],
                "confidence_threshold": 60,
                "base_quantity": 100,
                "max_quantity": 500,
                "cycle_interval": 60,
                "auto_refresh": True,
                "refresh_interval": 5,
            },
            portfolio_history=[],
            daily_pnl_history=[],
        )

        self._save_state(initial_state)
        logger.info("Initial state created")

    def _save_state(self, state: TradingState):
        """Save state to JSON file."""
        with self._lock:
            with open(self.state_file, "w") as f:
                json.dump(asdict(state), f, indent=2)

    def get_state(self) -> TradingState:
        """Get current state."""
        with self._lock:
            with open(self.state_file, "r") as f:
                data = json.load(f)
                return TradingState(**data)

    def update_state(self, **kwargs):
        """Update specific state fields."""
        state = self.get_state()

        for key, value in kwargs.items():
            if hasattr(state, key):
                setattr(state, key, value)

        state.timestamp = datetime.now().isoformat()
        self._save_state(state)

        logger.debug(f"State updated: {list(kwargs.keys())}")

    def update_portfolio(self, portfolio: Dict[str, Any]):
        """Update portfolio state and save snapshot."""
        self.update_state(portfolio=portfolio)

        # Save snapshot to database
        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO portfolio_snapshots
            (timestamp, total_value, cash, invested, total_return, total_return_pct, positions_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                datetime.now().isoformat(),
                portfolio.get("total_value", 0),
                portfolio.get("cash", 0),
                portfolio.get("total_value", 0) - portfolio.get("cash", 0),
                portfolio.get("total_return", 0),
                portfolio.get("total_return_pct", 0),
                json.dumps(portfolio.get("positions", {})),
            ),
        )

        conn.commit()
        conn.close()

        logger.info(f"Portfolio updated: ${portfolio.get('total_value', 0):,.2f}")

    def add_decision(self, decision: Dict[str, Any]):
        """Add a trading decision."""
        state = self.get_state()

        # Add to recent decisions (keep last 50)
        decision["timestamp"] = datetime.now().isoformat()
        state.recent_decisions.insert(0, decision)
        state.recent_decisions = state.recent_decisions[:50]

        state.total_decisions += 1

        self._save_state(state)

        # Save to database
        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO trading_decisions
            (timestamp, symbol, signal, confidence, quantity, price, reasoning, executed, order_id, cycle_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                decision["timestamp"],
                decision.get("symbol", ""),
                decision.get("signal", ""),
                decision.get("confidence", 0),
                decision.get("quantity", 0),
                decision.get("price", 0),
                decision.get("reasoning", ""),
                decision.get("executed", False),
                decision.get("order_id", ""),
                state.cycle_count,
            ),
        )

        conn.commit()
        conn.close()

        logger.info(
            f"Decision added: {decision.get('symbol')} - {decision.get('signal')}"
        )

    def add_trade_execution(self, execution: Dict[str, Any]):
        """Record a trade execution."""
        state = self.get_state()
        state.total_trades += 1

        if execution.get("success", False):
            state.successful_trades += 1

        self._save_state(state)

        # Save to database
        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO trade_executions
            (timestamp, symbol, action, quantity, price, total_value, success, error_message, order_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                datetime.now().isoformat(),
                execution.get("symbol", ""),
                execution.get("action", ""),
                execution.get("quantity", 0),
                execution.get("price", 0),
                execution.get("total_value", 0),
                execution.get("success", False),
                execution.get("error_message", ""),
                execution.get("order_id", ""),
            ),
        )

        conn.commit()
        conn.close()

        logger.info(
            f"Trade execution recorded: {execution.get('symbol')} - {execution.get('action')}"
        )

    def update_analytics(self, analytics: Dict[str, Any]):
        """Update performance analytics."""
        self.update_state(analytics=analytics)

        # Save to database
        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO performance_metrics
            (timestamp, daily_pnl, weekly_pnl, monthly_pnl, sharpe_ratio, max_drawdown, win_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                datetime.now().isoformat(),
                analytics.get("daily_pnl", 0),
                analytics.get("weekly_pnl", 0),
                analytics.get("monthly_pnl", 0),
                analytics.get("sharpe_ratio", 0),
                analytics.get("max_drawdown", 0),
                analytics.get("win_rate", 0),
            ),
        )

        conn.commit()
        conn.close()

        logger.info("Analytics updated")

    def increment_cycle(self):
        """Increment cycle counter."""
        state = self.get_state()
        state.cycle_count += 1
        self._save_state(state)

        logger.info(f"Cycle incremented to {state.cycle_count}")

    def set_trading_active(self, active: bool):
        """Set trading system active status."""
        self.update_state(trading_active=active)

        # Update system health
        state = self.get_state()
        system_health = state.system_health
        system_health["api_status"] = "Connected" if active else "Disconnected"
        self.update_state(system_health=system_health)

        logger.info(f"Trading active: {active}")

    def get_portfolio_history(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get portfolio value history."""
        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT timestamp, total_value, cash, invested, total_return, total_return_pct
            FROM portfolio_snapshots
            ORDER BY timestamp DESC
            LIMIT ?
        """,
            (days * 24,),
        )  # Assuming hourly snapshots

        rows = cursor.fetchall()
        conn.close()

        history = []
        for row in rows:
            history.append(
                {
                    "timestamp": row[0],
                    "total_value": row[1],
                    "cash": row[2],
                    "invested": row[3],
                    "total_return": row[4],
                    "total_return_pct": row[5],
                }
            )

        return list(reversed(history))

    def get_recent_trades(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent trade executions."""
        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT timestamp, symbol, action, quantity, price, total_value, success, error_message
            FROM trade_executions
            ORDER BY timestamp DESC
            LIMIT ?
        """,
            (limit,),
        )

        rows = cursor.fetchall()
        conn.close()

        trades = []
        for row in rows:
            trades.append(
                {
                    "timestamp": row[0],
                    "symbol": row[1],
                    "action": row[2],
                    "quantity": row[3],
                    "price": row[4],
                    "total_value": row[5],
                    "success": bool(row[6]),
                    "error_message": row[7],
                }
            )

        return trades

    def get_recent_decisions(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent trading decisions."""
        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT timestamp, symbol, signal, confidence, quantity, price, reasoning, executed
            FROM trading_decisions
            ORDER BY timestamp DESC
            LIMIT ?
        """,
            (limit,),
        )

        rows = cursor.fetchall()
        conn.close()

        decisions = []
        for row in rows:
            decisions.append(
                {
                    "timestamp": row[0],
                    "symbol": row[1],
                    "signal": row[2],
                    "confidence": row[3],
                    "quantity": row[4],
                    "price": row[5],
                    "reasoning": row[6],
                    "executed": bool(row[7]),
                }
            )

        return decisions

    def clear_old_data(self, days: int = 90):
        """Clear data older than specified days."""
        cutoff = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff.isoformat()

        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM trading_decisions WHERE timestamp < ?", (cutoff_str,)
        )
        cursor.execute(
            "DELETE FROM trade_executions WHERE timestamp < ?", (cutoff_str,)
        )
        cursor.execute(
            "DELETE FROM portfolio_snapshots WHERE timestamp < ?", (cutoff_str,)
        )
        cursor.execute(
            "DELETE FROM performance_metrics WHERE timestamp < ?", (cutoff_str,)
        )

        conn.commit()
        conn.close()

        logger.info(f"Cleared data older than {days} days")


# Global state manager instance
_state_manager: Optional[StateManager] = None


def get_state_manager() -> StateManager:
    """Get or create global state manager instance."""
    global _state_manager
    if _state_manager is None:
        _state_manager = StateManager()
    return _state_manager


if __name__ == "__main__":
    # Test the state manager
    logging.basicConfig(level=logging.INFO)

    sm = get_state_manager()

    # Test updates
    sm.set_trading_active(True)
    sm.increment_cycle()

    sm.add_decision(
        {
            "symbol": "AAPL",
            "signal": "BUY",
            "confidence": 85.5,
            "quantity": 50,
            "price": 182.50,
            "reasoning": "Strong technical signals",
            "executed": True,
        }
    )

    sm.add_trade_execution(
        {
            "symbol": "AAPL",
            "action": "BUY",
            "quantity": 50,
            "price": 182.50,
            "total_value": 9125.00,
            "success": True,
        }
    )

    sm.update_portfolio(
        {
            "cash": 90875.00,
            "total_value": 100000.00,
            "positions": {
                "AAPL": {"shares": 50, "market_value": 9125.00, "avg_cost": 182.50}
            },
        }
    )

    # Get state
    state = sm.get_state()
    print(f"\nCurrent State:")
    print(f"  Cycle: {state.cycle_count}")
    print(f"  Total Decisions: {state.total_decisions}")
    print(f"  Total Trades: {state.total_trades}")
    print(f"  Portfolio Value: ${state.portfolio['total_value']:,.2f}")
    print(f"  Recent Decisions: {len(state.recent_decisions)}")

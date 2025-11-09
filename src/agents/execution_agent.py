# execution_agent.py
import alpaca_trade_api as tradeapi
from src.config.settings import get_settings

# Get API credentials from settings
_settings = get_settings()
API_KEY = _settings.api_key
API_SECRET = _settings.api_secret
BASE_URL = _settings.base_url


class ExecutionAgent:
    def __init__(self):
        self.api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version="v2")

    def execute_trade(self, symbol, trade_signal, quantity=100):
        """
        Execute trade with specified quantity.

        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            trade_signal: Trade signal ('BUY', 'SELL', 'HOLD')
            quantity: Number of shares to trade
        """
        if trade_signal not in ["BUY", "SELL"]:
            print(f"⏸️  No valid trade signal for {symbol}. Holding position.")
            return

        if quantity <= 0:
            print(f"❌ Invalid quantity {quantity} for {symbol}. No trade executed.")
            return

        side = "buy" if trade_signal == "BUY" else "sell"
        try:
            print(f"💼 Executing {trade_signal} order for {symbol}: {quantity} shares")

            order = self.api.submit_order(
                symbol=symbol,
                qty=quantity,
                side=side,
                type="market",
                time_in_force="gtc",
            )
            print(f"✅ Executed {trade_signal} order for {symbol}: {quantity} shares")
            return order
        except Exception as e:
            print(f"❌ Trade execution failed for {symbol}: {e}")
            raise

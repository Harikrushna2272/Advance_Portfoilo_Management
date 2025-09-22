import json
import time
import threading
import pandas as pd
import websocket
from config import API_KEY, API_SECRET

class DataFetcher:
    def __init__(self, symbol):
        self.symbol = symbol
        self.ws_url = "wss://stream.data.alpaca.markets/v2/iex"
        self.latest_data = None
        self.socket = None
        self.connected = False
        self.lock = threading.Lock()

    def on_message(self, ws, message):
        data = json.loads(message)
        for item in data:
            if item.get("T") == "t":  # Trade update
                # Update the latest data with this trade update
                with self.lock:
                    self.latest_data = {
                        "Close": item.get("p"),
                        "Volume": item.get("s")
                    }
                # You can optionally print or process this update further
                # print(f"Updated data for {self.symbol}: {self.latest_data}")

    def on_open(self, ws):
        self.connected = True
        print("WebSocket connected, subscribing to live data...")
        auth_data = {
            "action": "auth",
            "key": API_KEY,
            "secret": API_SECRET
        }
        ws.send(json.dumps(auth_data))
        subscribe_message = {
            "action": "subscribe",
            "trades": [self.symbol]
        }
        ws.send(json.dumps(subscribe_message))

    def on_error(self, ws, error):
        print("WebSocket error:", error)

    def on_close(self, ws, close_status_code, close_msg):
        self.connected = False
        print("WebSocket closed.")

    def start_stream(self):
        self.socket = websocket.WebSocketApp(
            self.ws_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        # Run the WebSocket in a separate daemon thread
        thread = threading.Thread(target=self.socket.run_forever)
        thread.daemon = True
        thread.start()

    def get_latest_data(self):
        with self.lock:
            if self.latest_data is not None:
                # Create a DataFrame with aggregated values (High/Low set as Close since only one value is available)
                df = pd.DataFrame([{
                    "Close": self.latest_data["Close"],
                    "Volume": self.latest_data["Volume"],
                    "High": self.latest_data["Close"],
                    "Low": self.latest_data["Close"]
                }])
                return df
            else:
                return None

def get_stock_data(symbol):
    # Instantiate and start the continuous data fetcher
    fetcher = DataFetcher(symbol)
    fetcher.start_stream()

    # Wait until the WebSocket is connected
    timeout = 10
    start_time = time.time()
    while not fetcher.connected and time.time() - start_time < timeout:
        time.sleep(0.1)

    # Return the most recent data immediately (or None if not available yet)
    return fetcher.get_latest_data()

if __name__ == "__main__":
    import pprint
    data = get_stock_data("AAPL")
    pprint.pprint(data)

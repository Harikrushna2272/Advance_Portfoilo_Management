"""
Data Preprocessing for RL Ensemble Models

Prepares stock market data for RL model inference by:
1. Calculating technical indicators
2. Normalizing features
3. Handling missing values
4. Extracting the latest observation for prediction
"""

import pandas as pd
import numpy as np
import logging
from typing import Optional, Dict, List

# Try to import TA-Lib, fall back to pandas_ta if not available
try:
    import talib

    TALIB_AVAILABLE = True
except ImportError:
    TALIB_AVAILABLE = False
    try:
        import pandas_ta as ta

        PANDAS_TA_AVAILABLE = True
    except ImportError:
        PANDAS_TA_AVAILABLE = False
        logging.warning(
            "Neither TA-Lib nor pandas_ta available. Technical indicators will be limited."
        )

logger = logging.getLogger(__name__)


class StockDataPreprocessor:
    """
    Preprocesses stock data for RL model inference.

    Required features (14 total):
    - close, high, low, open, volume
    - day (day of week)
    - macd
    - boll_ub, boll_lb (Bollinger Bands)
    - rsi_30
    - cci_30
    - dx_30
    - close_30_sma, close_60_sma
    """

    REQUIRED_COLUMNS = [
        "close",
        "high",
        "low",
        "open",
        "volume",
        "day",
        "macd",
        "boll_ub",
        "boll_lb",
        "rsi_30",
        "cci_30",
        "dx_30",
        "close_30_sma",
        "close_60_sma",
    ]

    def __init__(self):
        """Initialize preprocessor."""
        self.feature_stats = {}  # For normalization if needed

    def preprocess(self, stock_data: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess stock data to create required features.

        Args:
            stock_data: DataFrame with OHLCV data

        Returns:
            DataFrame with all required features
        """
        try:
            # Validate input
            if not isinstance(stock_data, pd.DataFrame):
                raise ValueError("Input must be a pandas DataFrame")

            # Create a copy
            df = stock_data.copy()

            # Standardize column names
            df = self._standardize_columns(df)

            # Add day of week
            df = self._add_day_of_week(df)

            # Calculate technical indicators
            df = self._calculate_indicators(df)

            # Handle missing values
            df = self._handle_missing_values(df)

            # Validate output
            df = self._validate_features(df)

            logger.info(
                f"✅ Preprocessing complete: {len(df)} rows, {len(df.columns)} features"
            )

            return df

        except Exception as e:
            logger.error(f"❌ Preprocessing failed: {e}")
            raise

    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names to lowercase."""
        # Map common column name variations
        column_map = {
            "Close": "close",
            "High": "high",
            "Low": "low",
            "Open": "open",
            "Volume": "volume",
            "Date": "date",
            "Datetime": "date",
        }

        # Rename columns
        df = df.rename(columns=column_map)

        # Verify required OHLCV columns exist
        required_ohlcv = ["close", "high", "low", "open", "volume"]
        missing = [col for col in required_ohlcv if col not in df.columns]

        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        return df

    def _add_day_of_week(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add day of week feature."""
        if "date" in df.columns:
            df["day"] = pd.to_datetime(df["date"]).dt.dayofweek
        elif df.index.name == "Date" or isinstance(df.index, pd.DatetimeIndex):
            df["day"] = df.index.dayofweek
        else:
            # Default to 0 (Monday) if no date information
            df["day"] = 0
            logger.warning("No date column found, using default day=0")

        return df

    def _calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate all technical indicators."""
        if TALIB_AVAILABLE:
            df = self._calculate_indicators_talib(df)
        elif PANDAS_TA_AVAILABLE:
            df = self._calculate_indicators_pandas_ta(df)
        else:
            df = self._calculate_indicators_manual(df)

        return df

    def _calculate_indicators_talib(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate indicators using TA-Lib."""
        logger.info("Using TA-Lib for technical indicators")

        close = df["close"].values
        high = df["high"].values
        low = df["low"].values

        # MACD
        macd, macd_signal, macd_hist = talib.MACD(
            close, fastperiod=12, slowperiod=26, signalperiod=9
        )
        df["macd"] = macd

        # Bollinger Bands
        upper, middle, lower = talib.BBANDS(
            close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )
        df["boll_ub"] = upper
        df["boll_lb"] = lower

        # RSI
        df["rsi_30"] = talib.RSI(close, timeperiod=30)

        # CCI
        df["cci_30"] = talib.CCI(high, low, close, timeperiod=30)

        # DX
        df["dx_30"] = talib.DX(high, low, close, timeperiod=30)

        # Simple Moving Averages
        df["close_30_sma"] = talib.SMA(close, timeperiod=30)
        df["close_60_sma"] = talib.SMA(close, timeperiod=60)

        return df

    def _calculate_indicators_pandas_ta(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate indicators using pandas_ta."""
        logger.info("Using pandas_ta for technical indicators")

        # MACD
        macd = ta.macd(df["close"], fast=12, slow=26, signal=9)
        df["macd"] = macd["MACD_12_26_9"]

        # Bollinger Bands
        bbands = ta.bbands(df["close"], length=20, std=2)
        df["boll_ub"] = bbands["BBU_20_2.0"]
        df["boll_lb"] = bbands["BBL_20_2.0"]

        # RSI
        df["rsi_30"] = ta.rsi(df["close"], length=30)

        # CCI
        df["cci_30"] = ta.cci(df["high"], df["low"], df["close"], length=30)

        # DX
        adx = ta.adx(df["high"], df["low"], df["close"], length=30)
        df["dx_30"] = adx["DX_30"]

        # Simple Moving Averages
        df["close_30_sma"] = ta.sma(df["close"], length=30)
        df["close_60_sma"] = ta.sma(df["close"], length=60)

        return df

    def _calculate_indicators_manual(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate indicators manually (fallback)."""
        logger.warning(
            "Using manual calculation for technical indicators (limited accuracy)"
        )

        # Simple Moving Averages
        df["close_30_sma"] = df["close"].rolling(window=30).mean()
        df["close_60_sma"] = df["close"].rolling(window=60).mean()

        # Simple MACD approximation
        ema_12 = df["close"].ewm(span=12, adjust=False).mean()
        ema_26 = df["close"].ewm(span=26, adjust=False).mean()
        df["macd"] = ema_12 - ema_26

        # Bollinger Bands
        bb_middle = df["close"].rolling(window=20).mean()
        bb_std = df["close"].rolling(window=20).std()
        df["boll_ub"] = bb_middle + (bb_std * 2)
        df["boll_lb"] = bb_middle - (bb_std * 2)

        # RSI
        df["rsi_30"] = self._calculate_rsi(df["close"], period=30)

        # CCI (approximation)
        typical_price = (df["high"] + df["low"] + df["close"]) / 3
        sma_tp = typical_price.rolling(window=30).mean()
        mean_dev = typical_price.rolling(window=30).apply(
            lambda x: np.abs(x - x.mean()).mean()
        )
        df["cci_30"] = (typical_price - sma_tp) / (0.015 * mean_dev)

        # DX (simple approximation using price momentum)
        df["dx_30"] = df["close"].pct_change(30).abs() * 100

        return df

    @staticmethod
    def _calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI manually."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle NaN values in the data."""
        # Forward fill then backward fill
        df = df.fillna(method="ffill").fillna(method="bfill")

        # If still have NaN, fill with 0
        df = df.fillna(0)

        return df

    def _validate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ensure all required features exist."""
        # Add any missing required columns with zeros
        for col in self.REQUIRED_COLUMNS:
            if col not in df.columns:
                logger.warning(f"Missing feature '{col}', filling with zeros")
                df[col] = 0

        # Return only required columns in correct order
        return df[self.REQUIRED_COLUMNS]

    def get_latest_observation(self, df: pd.DataFrame) -> Optional[np.ndarray]:
        """
        Extract latest observation for RL model prediction.

        Args:
            df: Preprocessed DataFrame

        Returns:
            Numpy array of shape (14,) with latest features
        """
        try:
            if df.empty:
                logger.warning("Empty dataframe, cannot extract observation")
                return None

            # Get last row
            latest = df.iloc[-1][self.REQUIRED_COLUMNS].values

            # Ensure correct shape and type
            observation = np.array(latest, dtype=np.float32)

            if observation.shape[0] != 14:
                logger.error(
                    f"Invalid observation shape: {observation.shape}, expected (14,)"
                )
                return None

            # Check for any remaining NaN or inf
            if np.any(np.isnan(observation)) or np.any(np.isinf(observation)):
                logger.warning(
                    "Observation contains NaN or inf values, replacing with 0"
                )
                observation = np.nan_to_num(
                    observation, nan=0.0, posinf=0.0, neginf=0.0
                )

            return observation

        except Exception as e:
            logger.error(f"Failed to extract observation: {e}")
            return None


def preprocess_for_rl(stock_data: pd.DataFrame) -> Optional[np.ndarray]:
    """
    Convenience function to preprocess data and get latest observation.

    Args:
        stock_data: Raw stock data DataFrame

    Returns:
        Numpy array ready for RL model prediction, or None if failed
    """
    try:
        preprocessor = StockDataPreprocessor()
        processed_df = preprocessor.preprocess(stock_data)
        observation = preprocessor.get_latest_observation(processed_df)
        return observation
    except Exception as e:
        logger.error(f"Preprocessing failed: {e}")
        return None


# Legacy function names for backwards compatibility
def get_processed_features_for_rl(stock_data: pd.DataFrame) -> Optional[np.ndarray]:
    """Legacy function name - use preprocess_for_rl instead."""
    return preprocess_for_rl(stock_data)


def preprocess_data_for_ensemble_rl(
    stock_data: pd.DataFrame, start_date=None, end_date=None
) -> pd.DataFrame:
    """Legacy function - returns full preprocessed DataFrame."""
    preprocessor = StockDataPreprocessor()
    return preprocessor.preprocess(stock_data)


if __name__ == "__main__":
    # Test preprocessing
    logging.basicConfig(level=logging.INFO)

    # Create sample data
    dates = pd.date_range("2023-01-01", periods=100, freq="D")
    sample_data = pd.DataFrame(
        {
            "Date": dates,
            "Open": np.random.randn(100).cumsum() + 100,
            "High": np.random.randn(100).cumsum() + 102,
            "Low": np.random.randn(100).cumsum() + 98,
            "Close": np.random.randn(100).cumsum() + 100,
            "Volume": np.random.randint(1000000, 10000000, 100),
        }
    )

    print("Testing StockDataPreprocessor...")
    print(f"Input shape: {sample_data.shape}")

    # Test preprocessing
    observation = preprocess_for_rl(sample_data)

    if observation is not None:
        print(f"\n✅ Success!")
        print(f"Observation shape: {observation.shape}")
        print(f"Observation values: {observation}")
    else:
        print("\n❌ Preprocessing failed")

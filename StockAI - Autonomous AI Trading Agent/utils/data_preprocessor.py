import pandas as pd
import numpy as np
import talib
from datetime import datetime, timedelta

def preprocess_data_for_ensemble_rl(stock_data, start_date=None, end_date=None):
    """
    Preprocess stock data to create the required columns for ensemble RL models:
    close, high, low, open, volume, day, macd, boll_ub, boll_lb, rsi_30, cci_30, dx_30, close_30_sma, close_60_s
    """
    try:
        # Ensure we have a DataFrame
        if not isinstance(stock_data, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")
        
        # Create a copy to avoid modifying original data
        df = stock_data.copy()
        
        # Ensure required columns exist
        required_columns = ['Close', 'High', 'Low', 'Open', 'Volume']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Required column '{col}' not found in data")
        
        # Rename columns to lowercase for consistency
        df = df.rename(columns={
            'Close': 'close',
            'High': 'high', 
            'Low': 'low',
            'Open': 'open',
            'Volume': 'volume'
        })
        
        # Add day column (day of week)
        if 'Date' in df.columns:
            df['day'] = pd.to_datetime(df['Date']).dt.dayofweek
        else:
            df['day'] = 0  # Default to Monday if no date column
        
        # Calculate MACD
        df['macd'], df['macd_signal'], df['macd_hist'] = talib.MACD(
            df['close'], fastperiod=12, slowperiod=26, signalperiod=9
        )
        
        # Calculate Bollinger Bands
        df['boll_ub'], df['boll_mid'], df['boll_lb'] = talib.BBANDS(
            df['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )
        
        # Calculate RSI (30 period)
        df['rsi_30'] = talib.RSI(df['close'], timeperiod=30)
        
        # Calculate CCI (30 period)
        df['cci_30'] = talib.CCI(df['high'], df['low'], df['close'], timeperiod=30)
        
        # Calculate DX (30 period) - Directional Movement Index
        df['dx_30'] = talib.DX(df['high'], df['low'], df['close'], timeperiod=30)
        
        # Calculate Simple Moving Averages
        df['close_30_sma'] = talib.SMA(df['close'], timeperiod=30)
        df['close_60_sma'] = talib.SMA(df['close'], timeperiod=60)
        
        # Handle NaN values by forward filling
        df = df.fillna(method='ffill').fillna(method='bfill')
        
        # Select only the required columns for ensemble RL
        required_columns_rl = [
            'close', 'high', 'low', 'open', 'volume', 'day', 
            'macd', 'boll_ub', 'boll_lb', 'rsi_30', 'cci_30', 
            'dx_30', 'close_30_sma', 'close_60_sma'
        ]
        
        # Ensure all required columns exist
        for col in required_columns_rl:
            if col not in df.columns:
                print(f"Warning: Column '{col}' not found, filling with zeros")
                df[col] = 0
        
        # Return only the required columns
        processed_df = df[required_columns_rl].copy()
        
        # Remove any remaining NaN values
        processed_df = processed_df.dropna()
        
        return processed_df
    
    except Exception as e:
        print(f"Error in data preprocessing: {e}")
        # Return a minimal DataFrame with required columns
        return pd.DataFrame(columns=[
            'close', 'high', 'low', 'open', 'volume', 'day', 
            'macd', 'boll_ub', 'boll_lb', 'rsi_30', 'cci_30', 
            'dx_30', 'close_30_sma', 'close_60_sma'
        ])


def get_processed_features_for_rl(stock_data, lookback_period=30):
    """
    Extract features for RL ensemble models from preprocessed data.
    Returns the latest row of features for prediction.
    """
    try:
        # Preprocess the data
        processed_df = preprocess_data_for_ensemble_rl(stock_data)
        
        if processed_df.empty:
            print("Warning: No processed data available")
            return None
        
        # Get the latest row of features
        latest_features = processed_df.iloc[-1].values
        
        # Ensure we have the right number of features
        expected_features = 14  # Number of required columns
        if len(latest_features) != expected_features:
            print(f"Warning: Expected {expected_features} features, got {len(latest_features)}")
            # Pad with zeros if needed
            if len(latest_features) < expected_features:
                latest_features = np.pad(latest_features, (0, expected_features - len(latest_features)), 'constant')
            # Truncate if too many
            else:
                latest_features = latest_features[:expected_features]
        
        return latest_features
    
    except Exception as e:
        print(f"Error extracting features for RL: {e}")
        return None


def validate_processed_data(processed_df):
    """
    Validate that the processed data has all required columns and no NaN values.
    """
    required_columns = [
        'close', 'high', 'low', 'open', 'volume', 'day', 
        'macd', 'boll_ub', 'boll_lb', 'rsi_30', 'cci_30', 
        'dx_30', 'close_30_sma', 'close_60_sma'
    ]
    
    # Check if all required columns exist
    missing_columns = [col for col in required_columns if col not in processed_df.columns]
    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        return False
    
    # Check for NaN values
    nan_count = processed_df.isnull().sum().sum()
    if nan_count > 0:
        print(f"Found {nan_count} NaN values in processed data")
        return False
    
    # Check data types
    numeric_columns = [col for col in required_columns if col != 'day']
    for col in numeric_columns:
        if not pd.api.types.is_numeric_dtype(processed_df[col]):
            print(f"Column '{col}' is not numeric")
            return False
    
    print("Data validation passed")
    return True

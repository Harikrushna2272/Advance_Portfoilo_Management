import pandas as pd
from rl_training import train_rl_agent

# Load market data (Ensure you have at least 200 days of data for MA200)
market_data = pd.read_csv("Your_dataset_to_be_train")  # Replace with live data fetching method

train_rl_agent(market_data)

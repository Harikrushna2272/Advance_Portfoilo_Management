# config.py
API_KEY = "your_alpaca_api_key"
API_SECRET = "your_alpaca_secret"
BASE_URL = "https://paper-api.alpaca.markets"

NEWS_API_KEY = "your_news_api_key"
RL_MODEL_PATH = "models/trained_rl_model.pkl"

# List of stocks to monitor
STOCK_LIST = ["AAPL", "TSLA", "GOOGL"]

# List of paths to ensemble models (update with your actual model file paths)
ENSEMBLE_MODEL_PATHS = [
    "models/trained_rl_model_sac.pkl",    # Soft Actor-Critic
    "models/trained_rl_model_ppo.pkl",    # Proximal Policy Optimization
    "models/trained_rl_model_a2c.pkl",    # Advantage Actor-Critic
    "models/trained_rl_model_dqn.pkl",    # Deep Q-Network
    "models/trained_rl_model_td3.pkl"     # Twin Delayed Deep Deterministic
]

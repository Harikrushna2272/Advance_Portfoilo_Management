-- Database initialization script for StockAI
-- This script creates the necessary tables for the trading system

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS stockai;

-- Use the database
\c stockai;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create portfolios table
CREATE TABLE IF NOT EXISTS portfolios (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    initial_cash DECIMAL(15,2) NOT NULL,
    current_cash DECIMAL(15,2) NOT NULL,
    total_value DECIMAL(15,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create positions table
CREATE TABLE IF NOT EXISTS positions (
    id SERIAL PRIMARY KEY,
    portfolio_id INTEGER REFERENCES portfolios(id),
    symbol VARCHAR(10) NOT NULL,
    quantity INTEGER NOT NULL,
    cost_basis DECIMAL(10,2) NOT NULL,
    current_price DECIMAL(10,2),
    market_value DECIMAL(15,2),
    unrealized_pnl DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(portfolio_id, symbol)
);

-- Create trades table
CREATE TABLE IF NOT EXISTS trades (
    id SERIAL PRIMARY KEY,
    portfolio_id INTEGER REFERENCES portfolios(id),
    symbol VARCHAR(10) NOT NULL,
    action VARCHAR(10) NOT NULL, -- BUY, SELL
    quantity INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(15,2) NOT NULL,
    commission DECIMAL(10,2) DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create analysis_results table
CREATE TABLE IF NOT EXISTS analysis_results (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    analysis_type VARCHAR(50) NOT NULL, -- fundamentals, technicals, valuation, sentiment, risk
    signal VARCHAR(20) NOT NULL, -- bullish, bearish, neutral
    confidence DECIMAL(5,2) NOT NULL,
    details JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create rl_predictions table
CREATE TABLE IF NOT EXISTS rl_predictions (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    model_name VARCHAR(50) NOT NULL,
    prediction INTEGER NOT NULL, -- 1=BUY, -1=SELL, 0=HOLD
    confidence DECIMAL(5,2),
    features JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create final_decisions table
CREATE TABLE IF NOT EXISTS final_decisions (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    signal VARCHAR(20) NOT NULL, -- BUY, SELL, HOLD
    confidence DECIMAL(5,2) NOT NULL,
    quantity INTEGER NOT NULL,
    agent_consensus VARCHAR(20),
    rl_decision VARCHAR(20),
    reasoning TEXT,
    executed BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create system_logs table
CREATE TABLE IF NOT EXISTS system_logs (
    id SERIAL PRIMARY KEY,
    level VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    module VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_positions_portfolio_symbol ON positions(portfolio_id, symbol);
CREATE INDEX IF NOT EXISTS idx_trades_portfolio_timestamp ON trades(portfolio_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_analysis_results_symbol_timestamp ON analysis_results(symbol, timestamp);
CREATE INDEX IF NOT EXISTS idx_rl_predictions_symbol_timestamp ON rl_predictions(symbol, timestamp);
CREATE INDEX IF NOT EXISTS idx_final_decisions_symbol_timestamp ON final_decisions(symbol, timestamp);
CREATE INDEX IF NOT EXISTS idx_system_logs_timestamp ON system_logs(timestamp);

-- Insert default user (for testing)
INSERT INTO users (username, email, password_hash) 
VALUES ('admin', 'admin@stockai.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Q8Q8Q8')
ON CONFLICT (username) DO NOTHING;

-- Insert default portfolio
INSERT INTO portfolios (user_id, name, initial_cash, current_cash, total_value)
SELECT 1, 'Default Portfolio', 100000.00, 100000.00, 100000.00
WHERE NOT EXISTS (SELECT 1 FROM portfolios WHERE name = 'Default Portfolio');

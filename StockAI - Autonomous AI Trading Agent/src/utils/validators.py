# Validation utilities for StockAI
import re
from typing import List, Optional
from src.utils.logger import get_logger

logger = get_logger(__name__)


def validate_stock_symbol(symbol: str) -> bool:
    """
    Validate stock symbol format.
    
    Args:
        symbol: Stock symbol to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not symbol or not isinstance(symbol, str):
        logger.warning(f"Invalid symbol type: {type(symbol)}")
        return False
    
    # Basic validation: 1-5 uppercase letters
    pattern = r'^[A-Z]{1,5}$'
    if not re.match(pattern, symbol.upper()):
        logger.warning(f"Invalid symbol format: {symbol}")
        return False
    
    return True


def validate_trade_signal(signal: str) -> bool:
    """
    Validate trade signal.
    
    Args:
        signal: Trade signal to validate
        
    Returns:
        True if valid, False otherwise
    """
    valid_signals = ["BUY", "SELL", "HOLD", "buy", "sell", "hold"]
    
    if signal not in valid_signals:
        logger.warning(f"Invalid trade signal: {signal}")
        return False
    
    return True


def validate_quantity(quantity: int) -> bool:
    """
    Validate trade quantity.
    
    Args:
        quantity: Quantity to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(quantity, int) or quantity <= 0:
        logger.warning(f"Invalid quantity: {quantity}")
        return False
    
    return True


def validate_confidence(confidence: float) -> bool:
    """
    Validate confidence score.
    
    Args:
        confidence: Confidence score to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(confidence, (int, float)) or not (0 <= confidence <= 100):
        logger.warning(f"Invalid confidence: {confidence}")
        return False
    
    return True


def validate_stock_list(stock_list: List[str]) -> bool:
    """
    Validate list of stock symbols.
    
    Args:
        stock_list: List of stock symbols
        
    Returns:
        True if all valid, False otherwise
    """
    if not isinstance(stock_list, list) or not stock_list:
        logger.warning("Invalid stock list: empty or not a list")
        return False
    
    for symbol in stock_list:
        if not validate_stock_symbol(symbol):
            return False
    
    return True


def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input.
    
    Args:
        input_str: Input string to sanitize
        
    Returns:
        Sanitized string
    """
    if not isinstance(input_str, str):
        return str(input_str)
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', input_str)
    return sanitized.strip()

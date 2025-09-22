# Unit tests for validators
import pytest
from src.utils.validators import (
    validate_stock_symbol,
    validate_trade_signal,
    validate_quantity,
    validate_confidence,
    validate_stock_list,
    sanitize_input
)


class TestValidators:
    """Test cases for validation utilities."""
    
    def test_validate_stock_symbol_valid(self):
        """Test valid stock symbols."""
        assert validate_stock_symbol("AAPL") == True
        assert validate_stock_symbol("TSLA") == True
        assert validate_stock_symbol("GOOGL") == True
        assert validate_stock_symbol("MSFT") == True
    
    def test_validate_stock_symbol_invalid(self):
        """Test invalid stock symbols."""
        assert validate_stock_symbol("") == False
        assert validate_stock_symbol("123") == False
        assert validate_stock_symbol("aapl") == False  # lowercase
        assert validate_stock_symbol("AAPL123") == False  # numbers
        assert validate_stock_symbol("A") == True  # single letter is valid
        assert validate_stock_symbol("ABCDEF") == False  # too long
    
    def test_validate_trade_signal_valid(self):
        """Test valid trade signals."""
        assert validate_trade_signal("BUY") == True
        assert validate_trade_signal("SELL") == True
        assert validate_trade_signal("HOLD") == True
        assert validate_trade_signal("buy") == True
        assert validate_trade_signal("sell") == True
        assert validate_trade_signal("hold") == True
    
    def test_validate_trade_signal_invalid(self):
        """Test invalid trade signals."""
        assert validate_trade_signal("INVALID") == False
        assert validate_trade_signal("") == False
        assert validate_trade_signal("Buy") == False  # mixed case
    
    def test_validate_quantity_valid(self):
        """Test valid quantities."""
        assert validate_quantity(1) == True
        assert validate_quantity(100) == True
        assert validate_quantity(1000) == True
    
    def test_validate_quantity_invalid(self):
        """Test invalid quantities."""
        assert validate_quantity(0) == False
        assert validate_quantity(-1) == False
        assert validate_quantity("100") == False  # string
        assert validate_quantity(1.5) == False  # float
    
    def test_validate_confidence_valid(self):
        """Test valid confidence scores."""
        assert validate_confidence(0) == True
        assert validate_confidence(50) == True
        assert validate_confidence(100) == True
        assert validate_confidence(75.5) == True
    
    def test_validate_confidence_invalid(self):
        """Test invalid confidence scores."""
        assert validate_confidence(-1) == False
        assert validate_confidence(101) == False
        assert validate_confidence("50") == False  # string
        assert validate_confidence(None) == False
    
    def test_validate_stock_list_valid(self):
        """Test valid stock lists."""
        assert validate_stock_list(["AAPL", "TSLA"]) == True
        assert validate_stock_list(["GOOGL"]) == True
        assert validate_stock_list(["AAPL", "TSLA", "GOOGL", "MSFT"]) == True
    
    def test_validate_stock_list_invalid(self):
        """Test invalid stock lists."""
        assert validate_stock_list([]) == False
        assert validate_stock_list(["INVALID"]) == False
        assert validate_stock_list(["AAPL", "INVALID"]) == False
        assert validate_stock_list("AAPL") == False  # not a list
    
    def test_sanitize_input(self):
        """Test input sanitization."""
        assert sanitize_input("normal text") == "normal text"
        assert sanitize_input("text with <script>") == "text with script"
        assert sanitize_input("text with 'quotes'") == "text with quotes"
        assert sanitize_input("  spaced text  ") == "spaced text"
        assert sanitize_input(123) == "123"  # convert to string

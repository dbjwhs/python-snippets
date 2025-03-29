# MIT License
# Copyright (c) 2025 dbjwhs

"""Unit tests for the negative space module.

Tests the SafeString class functionality.
"""

import pytest

from negative_space.negative_space import SafeString


class TestSafeString:
    """Test suite for the SafeString class."""
    
    def test_valid_string(self) -> None:
        """Test that a valid string is accepted."""
        ss = SafeString()
        ss.set_value("Hello, World!")
        assert ss.get_value() == "Hello, World!"
    
    def test_empty_string(self) -> None:
        """Test that an empty string is rejected."""
        ss = SafeString()
        with pytest.raises(ValueError, match="Empty string not allowed"):
            ss.set_value("")
    
    def test_control_character(self) -> None:
        """Test that a string with a control character is rejected."""
        ss = SafeString()
        with pytest.raises(ValueError, match="String contains forbidden character"):
            ss.set_value("Hello\nWorld")
    
    def test_max_length(self) -> None:
        """Test that a string exceeding the maximum length is rejected."""
        ss = SafeString(5)
        with pytest.raises(ValueError, match="String length exceeds maximum"):
            ss.set_value("Too long string")
    
    def test_add_forbidden_char(self) -> None:
        """Test adding a new forbidden character."""
        ss = SafeString()
        ss.set_value("Test!")
        ss.add_forbidden_char("!")
        # Value should be cleared because it contained the newly forbidden character
        assert ss.get_value() == ""
        
        # Try setting a string with the newly forbidden character
        with pytest.raises(ValueError, match="String contains forbidden character"):
            ss.set_value("Hello!")
    
    def test_add_already_forbidden_char(self) -> None:
        """Test adding a character that is already forbidden."""
        ss = SafeString()
        # Control characters are already forbidden
        ss.add_forbidden_char("\n")
        # Should not throw any exceptions, just do nothing
        
    def test_multiple_validations(self) -> None:
        """Test multiple validations on the same SafeString instance."""
        ss = SafeString(10)
        
        # Valid string
        ss.set_value("Valid")
        assert ss.get_value() == "Valid"
        
        # Invalid string (too long)
        with pytest.raises(ValueError):
            ss.set_value("This is too long")
        
        # Value should remain unchanged
        assert ss.get_value() == "Valid"
        
        # Add a forbidden character
        ss.add_forbidden_char("V")
        
        # Value should be cleared because it contained the newly forbidden character
        assert ss.get_value() == ""
        
        # Try setting a new valid string
        ss.set_value("Hello")
        assert ss.get_value() == "Hello"
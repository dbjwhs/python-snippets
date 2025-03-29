# MIT License
# Copyright (c) 2025 dbjwhs

"""Negative space programming implementation.

Implements the negative space programming paradigm which focuses on
defining what should not happen rather than what should happen.
"""

from icecream import ic

"""
Negative space programming is a coding philosophy that emerged from multiple disciplines:
- visual arts (negative space concept, early 1900s)
- defensive programming (1970s)
- design by contract (bertrand meyer, 1986)

key principles:
1. define behavior by restrictions rather than permissions
2. explicitly handle edge cases and failures
3. focus on what cannot happen rather than what can
4. establish clear boundaries through constraints
"""


class SafeString:
    """SafeString class demonstrates negative space programming principles.
    
    Implements negative space principles by explicitly defining what cannot
    happen rather than what can.
    """

    def __init__(self, max_length: int = 100) -> None:
        """Initialize with constraints on what's not allowed.
        
        Args:
            max_length: The maximum allowed length for the string value

        """
        self._value: str = ""
        self._max_length: int = max_length
        self._forbidden_chars: set[int] = set()
        
        # Explicitly forbid control characters
        for bad_char in range(32):
            self._forbidden_chars.add(bad_char)
        
        # DEL character
        self._forbidden_chars.add(127)
    
    def set_value(self, value: str) -> None:
        """Set string value with negative space validation.
        
        Args:
            value: The string value to set
            
        Raises:
            ValueError: If the string violates any constraints

        """
        # Check what's not allowed first
        if not value:
            # make this info since we have negative tests, but should be error/critical
            ic("Empty string not allowed")
            raise ValueError("Empty string not allowed")
        
        if len(value) > self._max_length:
            # make this info since we have negative tests, but should be error/critical
            ic(f"String exceeds maximum length of {self._max_length}")
            raise ValueError("String length exceeds maximum")
        
        # Check for forbidden characters
        for c in value:
            if ord(c) in self._forbidden_chars:
                # make this info since we have negative tests, but should be error/critical
                ic(f"String contains forbidden character: {ord(c)}")
                raise ValueError("String contains forbidden character")
        
        # If we haven't thrown by now, the string is valid
        self._value = value
        ic(f"Successfully set string value: {self._value}")
    
    def add_forbidden_char(self, bad_char: str) -> None:
        """Add a new forbidden character.
        
        Args:
            bad_char: The character to forbid

        """
        char_code = ord(bad_char)
        
        # Check if character is already forbidden
        if char_code in self._forbidden_chars:
            ic(f"Character {char_code} is already forbidden")
            return
        
        self._forbidden_chars.add(char_code)
        ic(f"Added forbidden character: {char_code}")
        
        # If the current value contains the newly forbidden character, clear it
        if bad_char in self._value:
            self._value = ""
            ic("Cleared current value due to new forbidden character")
    
    def get_value(self) -> str:
        """Getter for the string value.
        
        Returns:
            The current string value

        """
        return self._value


def main() -> None:
    """Demonstrate SafeString functionality with examples."""
    ic("Starting SafeString demonstration")
    
    # Create a SafeString with default max length
    safe_string = SafeString()
    
    # Set a valid value
    safe_string.set_value("Hello, World!")
    assert safe_string.get_value() == "Hello, World!"
    
    # Try setting an empty string (should raise ValueError)
    try:
        safe_string.set_value("")
    except ValueError as e:
        ic(f"Error caught (expected): {e}")
    
    # Try setting a string with control character (should raise ValueError)
    try:
        safe_string.set_value("Hello\nWorld")
    except ValueError as e:
        ic(f"Error caught (expected): {e}")
    
    # Try setting a string exceeding maximum length
    try:
        short_safe_string = SafeString(5)
        short_safe_string.set_value("Too long string")
    except ValueError as e:
        ic(f"Error caught (expected): {e}")
    
    # Test adding a new forbidden character
    test_string = SafeString()
    test_string.set_value("Test!")
    test_string.add_forbidden_char("!")
    assert test_string.get_value() == ""
    
    ic("All tests completed successfully")


if __name__ == "__main__":
    main()
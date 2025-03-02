# MIT License
# Copyright (c) 2025 dbjwhs

"""Context module for the Interpreter pattern implementation."""

from interpreter_pattern.logger import Logger
from interpreter_pattern.logger import LogLevel


class Context:
    """
    Enhanced context class for the Interpreter pattern with operation tracking.
    
    The Context class provides a storage mechanism for variables and keeps track
    of operation counts during expression interpretation.
    """
    
    def __init__(self) -> None:
        """Initialize a new Context instance."""
        self._variables: dict[str, int] = {}
        self._operation_count: int = 0
    
    def reset_operation_count(self) -> None:
        """Reset the operation counter to zero."""
        self._operation_count = 0
        Logger.get_instance().log(LogLevel.DEBUG, "Context: Reset operation count")
    
    def set_variable(self, name: str, value: int) -> None:
        """Set a variable value in the context.
        
        Args:
            name: The variable name.
            value: The variable value.
        """
        self._variables[name] = value
        Logger.get_instance().log(
            LogLevel.DEBUG, 
            "Context: Setting variable '{}' to {}", 
            name, 
            value
        )
    
    def get_variable(self, name: str) -> int:
        """Get a variable value from the context.
        
        Args:
            name: The variable name.
            
        Returns:
            The variable value.
            
        Raises:
            ValueError: If the variable does not exist.
        """
        if name not in self._variables:
            Logger.get_instance().log(
                LogLevel.ERROR, 
                "Context: Variable not found: {}", 
                name
            )
            raise ValueError(f"Variable not found: {name}")
        
        value = self._variables[name]
        Logger.get_instance().log(
            LogLevel.DEBUG, 
            "Context: Retrieved variable '{}' = {}", 
            name, 
            value
        )
        return value
    
    def increment_operations(self) -> None:
        """Increment the operation counter."""
        self._operation_count += 1
        Logger.get_instance().log(
            LogLevel.DEBUG, 
            "Context: Operation count: {}", 
            self._operation_count
        )
    
    def get_operation_count(self) -> int:
        """Get the current operation count.
        
        Returns:
            The operation count.
        """
        return self._operation_count
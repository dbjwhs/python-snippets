# MIT License
# Copyright (c) 2025 dbjwhs

"""Expressions module for the Interpreter pattern implementation."""

from abc import ABC
from abc import abstractmethod

from interpreter_pattern.context import Context
from interpreter_pattern.logger import Logger
from interpreter_pattern.logger import LogLevel


class Expression(ABC):
    """
    Abstract Expression interface with debug capabilities.
    
    This is the base class for all expression types in the interpreter pattern.
    """
    
    @abstractmethod
    def interpret(self, context: Context) -> int:
        """
        Interpret the expression within the given context.
        
        Args:
            context: The context for interpretation.
            
        Returns:
            The result of interpreting the expression.
        """
        pass
    
    @abstractmethod
    def to_string(self) -> str:
        """
        Convert the expression to a string representation.
        
        Returns:
            The string representation of the expression.
        """
        pass
    
    def debug_print(self, depth: int = 0) -> None:
        """
        Print debug information about the expression.
        
        Args:
            depth: The indentation depth.
        """
        Logger.get_instance().log_with_depth(
            LogLevel.DEBUG, 
            depth, 
            f"Expression: {self.to_string()}"
        )


class NumberExpression(Expression):
    """
    Terminal expression for number literals.
    
    This class represents a constant integer value in the expression tree.
    """
    
    def __init__(self, number: int) -> None:
        """
        Initialize a new NumberExpression with a value.
        
        Args:
            number: The numerical value.
        """
        self._number: int = number
        Logger.get_instance().log(
            LogLevel.DEBUG, 
            "Creating NumberExpression with value {}", 
            self._number
        )
    
    def interpret(self, context: Context) -> int:
        """
        Interpret the number expression.
        
        Args:
            context: The context for interpretation.
            
        Returns:
            The numerical value.
        """
        context.increment_operations()
        Logger.get_instance().log(
            LogLevel.DEBUG, 
            "NumberExpression: Interpreting constant {}", 
            self._number
        )
        return self._number
    
    def to_string(self) -> str:
        """
        Convert the number expression to a string.
        
        Returns:
            The string representation of the number.
        """
        return str(self._number)


class VariableExpression(Expression):
    """
    Terminal expression for variables.
    
    This class represents a variable reference in the expression tree.
    """
    
    def __init__(self, name: str) -> None:
        """
        Initialize a new VariableExpression with a name.
        
        Args:
            name: The variable name.
        """
        self._name: str = name
        Logger.get_instance().log(
            LogLevel.DEBUG, 
            "Creating VariableExpression for '{}'", 
            self._name
        )
    
    def interpret(self, context: Context) -> int:
        """
        Interpret the variable expression by looking up its value.
        
        Args:
            context: The context containing variable values.
            
        Returns:
            The variable value.
            
        Raises:
            ValueError: If the variable is not defined in the context.
        """
        context.increment_operations()
        value = context.get_variable(self._name)
        Logger.get_instance().log(
            LogLevel.DEBUG, 
            "VariableExpression: Retrieved '{}' = {}", 
            self._name, 
            value
        )
        return value
    
    def to_string(self) -> str:
        """
        Convert the variable expression to a string.
        
        Returns:
            The variable name.
        """
        return self._name


class BinaryExpression(Expression, ABC):
    """
    Base class for binary operations.
    
    This abstract class represents operations that have a left and right operand.
    """
    
    def __init__(self, left: Expression, right: Expression, operator_symbol: str) -> None:
        """
        Initialize a new BinaryExpression.
        
        Args:
            left: The left operand expression.
            right: The right operand expression.
            operator_symbol: The symbol representing the operation.
        """
        self._left: Expression = left
        self._right: Expression = right
        self._operator_symbol: str = operator_symbol
        Logger.get_instance().log(
            LogLevel.DEBUG, 
            "Creating BinaryExpression with operator '{}'", 
            self._operator_symbol
        )
    
    def debug_print(self, depth: int = 0) -> None:
        """
        Print debug information about the binary expression and its operands.
        
        Args:
            depth: The indentation depth.
        """
        super().debug_print(depth)
        self._left.debug_print(depth + 1)
        self._right.debug_print(depth + 1)
    
    def to_string(self) -> str:
        """
        Convert the binary expression to a string.
        
        Returns:
            The string representation of the binary expression.
        """
        return f"({self._left.to_string()} {self._operator_symbol} {self._right.to_string()})"


class AddExpression(BinaryExpression):
    """
    Non-terminal expression for addition.
    
    This class represents the addition operation in the expression tree.
    """
    
    def __init__(self, left: Expression, right: Expression) -> None:
        """
        Initialize a new AddExpression.
        
        Args:
            left: The left operand expression.
            right: The right operand expression.
        """
        super().__init__(left, right, "+")
    
    def interpret(self, context: Context) -> int:
        """
        Interpret the addition expression.
        
        Args:
            context: The context for interpretation.
            
        Returns:
            The result of adding the left and right operands.
        """
        context.increment_operations()
        result = self._left.interpret(context) + self._right.interpret(context)
        Logger.get_instance().log(
            LogLevel.DEBUG, 
            "AddExpression: {} = {}", 
            self.to_string(), 
            result
        )
        return result


class SubtractExpression(BinaryExpression):
    """
    Non-terminal expression for subtraction.
    
    This class represents the subtraction operation in the expression tree.
    """
    
    def __init__(self, left: Expression, right: Expression) -> None:
        """
        Initialize a new SubtractExpression.
        
        Args:
            left: The left operand expression.
            right: The right operand expression.
        """
        super().__init__(left, right, "-")
    
    def interpret(self, context: Context) -> int:
        """
        Interpret the subtraction expression.
        
        Args:
            context: The context for interpretation.
            
        Returns:
            The result of subtracting the right operand from the left operand.
        """
        context.increment_operations()
        result = self._left.interpret(context) - self._right.interpret(context)
        Logger.get_instance().log(
            LogLevel.DEBUG, 
            "SubtractExpression: {} = {}", 
            self.to_string(), 
            result
        )
        return result


class MultiplyExpression(BinaryExpression):
    """
    Non-terminal expression for multiplication.
    
    This class represents the multiplication operation in the expression tree.
    """
    
    def __init__(self, left: Expression, right: Expression) -> None:
        """
        Initialize a new MultiplyExpression.
        
        Args:
            left: The left operand expression.
            right: The right operand expression.
        """
        super().__init__(left, right, "*")
    
    def interpret(self, context: Context) -> int:
        """
        Interpret the multiplication expression.
        
        Args:
            context: The context for interpretation.
            
        Returns:
            The result of multiplying the left and right operands.
        """
        context.increment_operations()
        result = self._left.interpret(context) * self._right.interpret(context)
        Logger.get_instance().log(
            LogLevel.DEBUG, 
            "MultiplyExpression: {} = {}", 
            self.to_string(), 
            result
        )
        return result


class DivideExpression(BinaryExpression):
    """
    Non-terminal expression for division.
    
    This class represents the division operation in the expression tree.
    """
    
    def __init__(self, left: Expression, right: Expression) -> None:
        """
        Initialize a new DivideExpression.
        
        Args:
            left: The left operand expression.
            right: The right operand expression.
        """
        super().__init__(left, right, "/")
    
    def interpret(self, context: Context) -> int:
        """
        Interpret the division expression.
        
        Args:
            context: The context for interpretation.
            
        Returns:
            The result of dividing the left operand by the right operand.
            
        Raises:
            ZeroDivisionError: If the right operand evaluates to zero.
        """
        context.increment_operations()
        right_value = self._right.interpret(context)
        if right_value == 0:
            Logger.get_instance().log(LogLevel.INFO, "DivideExpression: Division by zero")
            raise ZeroDivisionError("Division by zero")
        
        result = self._left.interpret(context) // right_value  # Using integer division
        Logger.get_instance().log(
            LogLevel.DEBUG, 
            "DivideExpression: {} = {}", 
            self.to_string(), 
            result
        )
        return result


class ModuloExpression(BinaryExpression):
    """
    Non-terminal expression for modulo.
    
    This class represents the modulo operation in the expression tree.
    """
    
    def __init__(self, left: Expression, right: Expression) -> None:
        """
        Initialize a new ModuloExpression.
        
        Args:
            left: The left operand expression.
            right: The right operand expression.
        """
        super().__init__(left, right, "%")
    
    def interpret(self, context: Context) -> int:
        """
        Interpret the modulo expression.
        
        Args:
            context: The context for interpretation.
            
        Returns:
            The remainder of dividing the left operand by the right operand.
            
        Raises:
            ZeroDivisionError: If the right operand evaluates to zero.
        """
        context.increment_operations()
        right_value = self._right.interpret(context)
        if right_value == 0:
            Logger.get_instance().log(LogLevel.ERROR, "ModuloExpression: Modulo by zero")
            raise ZeroDivisionError("Modulo by zero")
        
        result = self._left.interpret(context) % right_value
        Logger.get_instance().log(
            LogLevel.DEBUG, 
            "ModuloExpression: {} = {}", 
            self.to_string(), 
            result
        )
        return result


class PowerExpression(BinaryExpression):
    """
    Non-terminal expression for power operation.
    
    This class represents the exponentiation operation in the expression tree.
    """
    
    def __init__(self, left: Expression, right: Expression) -> None:
        """
        Initialize a new PowerExpression.
        
        Args:
            left: The left operand expression (base).
            right: The right operand expression (exponent).
        """
        super().__init__(left, right, "^")
    
    def interpret(self, context: Context) -> int:
        """
        Interpret the power expression.
        
        Args:
            context: The context for interpretation.
            
        Returns:
            The result of raising the left operand to the power of the right operand.
            
        Raises:
            ValueError: If the exponent is negative.
        """
        context.increment_operations()
        base = self._left.interpret(context)
        exponent = self._right.interpret(context)
        
        if exponent < 0:
            Logger.get_instance().log(LogLevel.ERROR, "PowerExpression: Negative exponent")
            raise ValueError("Negative exponent not supported")
        
        result = 1
        for _ in range(exponent):
            result *= base
        
        Logger.get_instance().log(
            LogLevel.DEBUG, 
            "PowerExpression: {} = {}", 
            self.to_string(), 
            result
        )
        return result
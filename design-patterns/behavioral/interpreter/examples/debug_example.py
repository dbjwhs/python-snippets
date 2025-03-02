# MIT License
# Copyright (c) 2025 dbjwhs

"""
Debugging example demonstrating the Interpreter pattern with icecream.

This example shows how to use the icecream package for enhanced debugging
with the Interpreter pattern implementation.
"""

from icecream import ic

from interpreter_pattern.context import Context
from interpreter_pattern.expressions import AddExpression
from interpreter_pattern.expressions import Expression
from interpreter_pattern.expressions import MultiplyExpression
from interpreter_pattern.expressions import NumberExpression
from interpreter_pattern.expressions import VariableExpression
from interpreter_pattern.logger import Logger
from interpreter_pattern.logger import LogLevel


def create_test_expression() -> Expression:
    """Create a test expression for demonstration purposes.
    
    Creates the expression: (x + 5) * (y + 2)
    
    Returns:
        The constructed expression tree.
    """
    # Show the expression creation with icecream
    left = AddExpression(
        VariableExpression("x"),
        NumberExpression(5)
    )
    ic(left.to_string())
    
    right = AddExpression(
        VariableExpression("y"),
        NumberExpression(2)
    )
    ic(right.to_string())
    
    expr = MultiplyExpression(left, right)
    ic(expr.to_string())
    
    return expr


def main() -> None:
    """Main function to demonstrate debugging with icecream."""
    # Configure icecream for the whole module
    ic.configureOutput(prefix="DEBUG: ", includeContext=True)
    
    # Create a context with variables
    context = Context()
    context.set_variable("x", 10)
    context.set_variable("y", 7)
    
    # Use icecream to inspect variable values
    ic(context._variables)
    
    # Create and evaluate an expression
    expr = create_test_expression()
    
    # Set logger level to debug to see detailed logs
    logger = Logger.get_instance()
    logger.set_level(LogLevel.DEBUG)
    
    # Show the full expression
    ic("About to evaluate:", expr.to_string())
    
    # Evaluate the expression and show the result
    result = expr.interpret(context)
    ic("Evaluation result:", result)
    
    # Show operation count
    ic("Total operations:", context.get_operation_count())
    
    # Calculation breakdown using icecream
    x_value = context._variables["x"]
    y_value = context._variables["y"]
    left_result = x_value + 5
    right_result = y_value + 2
    expected_result = left_result * right_result
    
    ic(x_value, y_value, left_result, right_result, expected_result)
    
    # Verify result
    assert result == expected_result
    print("Calculation verified successfully!")


if __name__ == "__main__":
    main()
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Calculator example demonstrating the Interpreter pattern.

This example shows how to use the Interpreter pattern to build
and evaluate mathematical expressions with variables.
"""

from interpreter_pattern.context import Context
from interpreter_pattern.expressions import AddExpression
from interpreter_pattern.expressions import DivideExpression
from interpreter_pattern.expressions import Expression
from interpreter_pattern.expressions import ModuloExpression
from interpreter_pattern.expressions import MultiplyExpression
from interpreter_pattern.expressions import NumberExpression
from interpreter_pattern.expressions import PowerExpression
from interpreter_pattern.expressions import SubtractExpression
from interpreter_pattern.expressions import VariableExpression
from interpreter_pattern.logger import Logger
from interpreter_pattern.logger import LogLevel


def create_addition(left: Expression, right: Expression) -> Expression:
    """Create an addition expression."""
    return AddExpression(left, right)


def create_subtraction(left: Expression, right: Expression) -> Expression:
    """Create a subtraction expression."""
    return SubtractExpression(left, right)


def create_multiplication(left: Expression, right: Expression) -> Expression:
    """Create a multiplication expression."""
    return MultiplyExpression(left, right)


def create_division(left: Expression, right: Expression) -> Expression:
    """Create a division expression."""
    return DivideExpression(left, right)


def create_modulo(left: Expression, right: Expression) -> Expression:
    """Create a modulo expression."""
    return ModuloExpression(left, right)


def create_power(left: Expression, right: Expression) -> Expression:
    """Create a power expression."""
    return PowerExpression(left, right)


def create_binary_expression(
    left: Expression, operator: str, right: Expression
) -> Expression | None:
    """
    Create a binary expression based on the operator.
    
    Args:
        left: The left operand expression.
        operator: The operator symbol.
        right: The right operand expression.
        
    Returns:
        The binary expression or None if the operator is invalid.
    """
    # Map operators to their corresponding expression creation functions
    operator_map = {
        "+": create_addition,
        "-": create_subtraction,
        "*": create_multiplication,
        "/": create_division,
        "%": create_modulo,
        "^": create_power,
    }
    
    # Look up and call the appropriate function if the operator is supported
    if operator in operator_map:
        return operator_map[operator](left, right)
    
    return None


def parse_token(token: str, context: Context) -> Expression:
    """
    Parse a single token into an expression.
    
    Args:
        token: The token to parse.
        context: The context containing variable values.
        
    Returns:
        The parsed expression.
    """
    if token.isdigit() or (token[0] == "-" and token[1:].isdigit()):
        return NumberExpression(int(token))
    else:
        return VariableExpression(token)


def create_expression(expression_str: str, context: Context) -> Expression | None:
    """
    Simple parser to create an expression tree from a string.
    
    This is a very basic parser that only handles a subset of expressions.
    In a real-world scenario, you would use a proper parser generator.
    
    Args:
        expression_str: The expression string to parse.
        context: The context containing variable values.
        
    Returns:
        The parsed expression tree.
    
    Note:
        This is a simplified parser for demonstration purposes.
        It only handles basic expressions like "a + b * c".
        It does not handle parentheses or operator precedence properly.
    """
    # This is a highly simplified parser for demonstration
    # In a real implementation, you would use a proper parser generator
    tokens = expression_str.replace("(", " ( ").replace(")", " ) ").split()
    
    if len(tokens) == 1:
        # Single token, either a number or a variable
        return parse_token(tokens[0], context)
    
    # Very simple expression handling for demo purposes
    # Check for simple three-token expression (left op right)
    token_count = 3
    if len(tokens) == token_count:
        left = create_expression(tokens[0], context)
        operator = tokens[1]
        right = create_expression(tokens[2], context)
        
        if left is not None and right is not None:
            return create_binary_expression(left, operator, right)
    
    # Fallback for more complex expressions - not fully implemented
    # In a real implementation, you would handle operator precedence, parentheses, etc.
    Logger.get_instance().log(
        LogLevel.ERROR,
        "Cannot parse complex expression: {}",
        expression_str
    )
    return None


def main() -> None:
    """Main function to demonstrate the calculator example."""
    logger = Logger.get_instance()
    logger.log(LogLevel.INFO, "Starting Calculator Example")
    
    # Create context and set variables
    context = Context()
    context.set_variable("x", 10)
    context.set_variable("y", 5)
    context.set_variable("z", 2)
    
    # Simple expressions
    expressions = [
        "5 + 3",
        "x - y",
        "y * z",
        "x / y",
        "10 % 3",
        "2 ^ 3"
    ]
    
    for expr_str in expressions:
        logger.log(LogLevel.INFO, "Evaluating: {}", expr_str)
        expression = create_expression(expr_str, context)
        if expression:
            expression.debug_print()
            result = expression.interpret(context)
            logger.log(LogLevel.INFO, "Result: {} = {}", expr_str, result)
        else:
            logger.log(LogLevel.ERROR, "Failed to parse expression: {}", expr_str)
    
    logger.log(LogLevel.INFO, "Calculator Example completed")


if __name__ == "__main__":
    main()
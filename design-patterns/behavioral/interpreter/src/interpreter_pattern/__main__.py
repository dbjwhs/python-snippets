# MIT License
# Copyright (c) 2025 dbjwhs

"""Main module for the Interpreter pattern implementation."""

from interpreter_pattern.context import Context
from interpreter_pattern.expressions import AddExpression
from interpreter_pattern.expressions import DivideExpression
from interpreter_pattern.expressions import ModuloExpression
from interpreter_pattern.expressions import MultiplyExpression
from interpreter_pattern.expressions import NumberExpression
from interpreter_pattern.expressions import PowerExpression
from interpreter_pattern.expressions import SubtractExpression
from interpreter_pattern.expressions import VariableExpression
from interpreter_pattern.logger import Logger
from interpreter_pattern.logger import LogLevel


def test_basic_arithmetic(logger: Logger) -> None:
    """Test basic arithmetic operations.
    
    Args:
        logger: The logger instance.
    """
    logger.log(LogLevel.INFO, "Test 1: Basic arithmetic operations")
    
    # Test addition
    expr = AddExpression(
        NumberExpression(5),
        NumberExpression(3)
    )
    
    expr.debug_print()
    context = Context()
    result = expr.interpret(context)
    expected_sum = 8
    assert result == expected_sum
    logger.log(LogLevel.INFO, "Test 1a: Addition passed, result: {}", result)
    
    # Test multiplication
    expr2 = MultiplyExpression(
        NumberExpression(4),
        NumberExpression(6)
    )
    
    expr2.debug_print()
    result = expr2.interpret(context)
    expected_product = 24
    assert result == expected_product
    logger.log(LogLevel.INFO, "Test 1b: Multiplication passed, result: {}", result)


def test_variable_operations(logger: Logger) -> None:
    """Test operations with variables.
    
    Args:
        logger: The logger instance.
    """
    context = Context()
    context.set_variable("x", 10)
    context.set_variable("y", 5)
    logger.log(LogLevel.INFO, "Test 2: Variable operations")
    
    div_expr = DivideExpression(
        VariableExpression("x"),
        VariableExpression("y")
    )
    
    div_expr.debug_print()
    result = div_expr.interpret(context)
    expected_quotient = 2
    assert result == expected_quotient
    logger.log(LogLevel.INFO, "Test 2: Division with variables passed, result: {}", result)


def test_complex_expression(logger: Logger) -> None:
    """Test complex expression tree.
    
    Args:
        logger: The logger instance.
    """
    context = Context()
    context.set_variable("a", 15)
    context.set_variable("b", 3)
    logger.log(LogLevel.INFO, "Test 3: Complex expression tree")
    
    # Creates: ((a + 5) * (b - 1)) % 4
    complex_expr = ModuloExpression(
        MultiplyExpression(
            AddExpression(
                VariableExpression("a"),
                NumberExpression(5)
            ),
            SubtractExpression(
                VariableExpression("b"),
                NumberExpression(1)
            )
        ),
        NumberExpression(4)
    )
    
    complex_expr.debug_print()
    result = complex_expr.interpret(context)
    expected_remainder = 0
    assert result == expected_remainder
    logger.log(LogLevel.INFO, "Test 3: Complex expression evaluation passed, result: {}", result)


def test_power_operations(logger: Logger) -> None:
    """Test power operations.
    
    Args:
        logger: The logger instance.
    """
    context = Context()
    logger.log(LogLevel.INFO, "Test 4: Power operations")
    
    power_expr = PowerExpression(
        NumberExpression(2),
        NumberExpression(3)
    )
    
    power_expr.debug_print()
    result = power_expr.interpret(context)
    expected_power = 8
    assert result == expected_power
    logger.log(LogLevel.INFO, "Test 4: Power operation passed, result: {}", result)


def test_error_handling(logger: Logger) -> None:
    """Test error handling.
    
    Args:
        logger: The logger instance.
    """
    context = Context()
    logger.log(LogLevel.INFO, "Test 5: Error handling")
    
    # Test division by zero
    expr1 = DivideExpression(
        NumberExpression(10),
        NumberExpression(0)
    )
    
    try:
        expr1.debug_print()
        # Will raise ZeroDivisionError, store in a variable just for consistency
        _ = expr1.interpret(context)
        # Using raise instead of assert False
        raise AssertionError("Should have thrown division by zero exception")
    except ZeroDivisionError as e:
        logger.log(
            LogLevel.INFO,
            "Test 5a: Division by zero exception caught correctly, error: {}",
            str(e)
        )
    
    # Test undefined variable
    var_expr = VariableExpression("undefined")
    try:
        var_expr.debug_print()
        # Will raise ValueError, store in a variable just for consistency
        _ = var_expr.interpret(context)
        # Using raise instead of assert False
        raise AssertionError("Should have thrown undefined variable exception")
    except ValueError as e:
        logger.log(
            LogLevel.INFO,
            "Test 5b: Undefined variable exception caught correctly, error: {}",
            str(e)
        )


def test_operation_counting(logger: Logger) -> None:
    """Test operation counting.
    
    Args:
        logger: The logger instance.
    """
    context = Context()
    logger.log(LogLevel.INFO, "Test 6: Operation counting")
    
    # Reset operation count before this test
    context.reset_operation_count()
    
    # Create expression: (2 * 3) + 4
    expr = AddExpression(
        MultiplyExpression(
            NumberExpression(2),
            NumberExpression(3)
        ),
        NumberExpression(4)
    )
    
    expr.debug_print()
    result = expr.interpret(context)
    
    # Count should be:
    # 1 for multiply
    # 1 for add
    # 3 for number expressions (2, 3, and 4)
    # Total: 5 operations
    expected_operations = 5
    assert context.get_operation_count() == expected_operations
    logger.log(
        LogLevel.INFO,
        "Test 6: Operation counting passed. Total operations: {}, interpret result: {}",
        context.get_operation_count(),
        result
    )


def run_tests() -> None:
    """Run comprehensive tests for the Interpreter pattern implementation."""
    logger = Logger.get_instance()
    logger.log(LogLevel.INFO, "Starting comprehensive interpreter pattern tests")
    
    # Run all test cases
    test_basic_arithmetic(logger)
    test_variable_operations(logger)
    test_complex_expression(logger)
    test_power_operations(logger)
    test_error_handling(logger)
    test_operation_counting(logger)


def main() -> None:
    """Main function to demonstrate the Interpreter pattern."""
    try:
        logger = Logger.get_instance()
        logger.log(LogLevel.INFO, "Starting interpreter pattern demonstration")
        
        # Set log level based on your needs
        # logger.set_level(LogLevel.DEBUG)  # For detailed debug output
        
        run_tests()
        
        logger.log(LogLevel.INFO, "All tests passed successfully")
    except Exception as e:
        Logger.get_instance().log(
            LogLevel.ERROR,
            "Test failed with error: {}",
            str(e)
        )


if __name__ == "__main__":
    main()
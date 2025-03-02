# MIT License
# Copyright (c) 2025 dbjwhs

"""Test module for the Interpreter pattern implementation."""

import pytest

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


def test_number_expression(context: Context, setup_logger: Logger) -> None:
    """Test the number expression."""
    value = 5
    expr = NumberExpression(value)
    expr.debug_print()
    assert expr.interpret(context) == value
    assert expr.to_string() == "5"


def test_variable_expression(context: Context, setup_logger: Logger) -> None:
    """Test the variable expression."""
    var_name = "x"
    var_value = 10
    context.set_variable(var_name, var_value)
    expr = VariableExpression(var_name)
    expr.debug_print()
    assert expr.interpret(context) == var_value
    assert expr.to_string() == var_name


def test_add_expression(context: Context, setup_logger: Logger) -> None:
    """Test the add expression."""
    left_val = 5
    right_val = 3
    expected_sum = left_val + right_val
    expr = AddExpression(NumberExpression(left_val), NumberExpression(right_val))
    expr.debug_print()
    assert expr.interpret(context) == expected_sum
    assert expr.to_string() == f"({left_val} + {right_val})"


def test_subtract_expression(context: Context, setup_logger: Logger) -> None:
    """Test the subtract expression."""
    left_val = 8
    right_val = 3
    expected_diff = left_val - right_val
    expr = SubtractExpression(NumberExpression(left_val), NumberExpression(right_val))
    expr.debug_print()
    assert expr.interpret(context) == expected_diff
    assert expr.to_string() == f"({left_val} - {right_val})"


def test_multiply_expression(context: Context, setup_logger: Logger) -> None:
    """Test the multiply expression."""
    left_val = 4
    right_val = 6
    expected_product = left_val * right_val
    expr = MultiplyExpression(NumberExpression(left_val), NumberExpression(right_val))
    expr.debug_print()
    assert expr.interpret(context) == expected_product
    assert expr.to_string() == f"({left_val} * {right_val})"


def test_divide_expression(context: Context, setup_logger: Logger) -> None:
    """Test the divide expression."""
    left_val = 10
    right_val = 2
    expected_quotient = left_val // right_val  # Integer division
    expr = DivideExpression(NumberExpression(left_val), NumberExpression(right_val))
    expr.debug_print()
    assert expr.interpret(context) == expected_quotient
    assert expr.to_string() == f"({left_val} / {right_val})"


def test_modulo_expression(context: Context, setup_logger: Logger) -> None:
    """Test the modulo expression."""
    left_val = 10
    right_val = 3
    expected_remainder = left_val % right_val
    expr = ModuloExpression(NumberExpression(left_val), NumberExpression(right_val))
    expr.debug_print()
    assert expr.interpret(context) == expected_remainder
    assert expr.to_string() == f"({left_val} % {right_val})"


def test_power_expression(context: Context, setup_logger: Logger) -> None:
    """Test the power expression."""
    base = 2
    exponent = 3
    expected_power = base ** exponent
    expr = PowerExpression(NumberExpression(base), NumberExpression(exponent))
    expr.debug_print()
    assert expr.interpret(context) == expected_power
    assert expr.to_string() == f"({base} ^ {exponent})"


def test_variable_operations(context: Context, setup_logger: Logger) -> None:
    """Test operations with variables."""
    x_var = "x"
    x_val = 10
    y_var = "y"
    y_val = 5
    expected_result = x_val // y_val  # Integer division
    
    context.set_variable(x_var, x_val)
    context.set_variable(y_var, y_val)
    
    expr = DivideExpression(VariableExpression(x_var), VariableExpression(y_var))
    expr.debug_print()
    assert expr.interpret(context) == expected_result


def test_complex_expression(context: Context, setup_logger: Logger) -> None:
    """Test a complex expression tree."""
    context.set_variable("a", 15)
    context.set_variable("b", 3)
    
    # Creates: ((a + 5) * (b - 1)) % 4
    expr = ModuloExpression(
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
    
    expr.debug_print()
    assert expr.interpret(context) == 0


def test_operation_counting(context: Context, setup_logger: Logger) -> None:
    """Test operation counting."""
    context.reset_operation_count()
    
    # Create expression: (2 * 3) + 4
    left_factor1 = 2
    left_factor2 = 3
    right_addend = 4
    expected_operations = 5  # 1 multiply + 1 add + 3 numbers
    expected_result = (left_factor1 * left_factor2) + right_addend
    
    expr = AddExpression(
        MultiplyExpression(
            NumberExpression(left_factor1),
            NumberExpression(left_factor2)
        ),
        NumberExpression(right_addend)
    )
    
    expr.debug_print()
    result = expr.interpret(context)
    
    # Count should be:
    # 1 for multiply
    # 1 for add
    # 3 for number expressions (2, 3, and 4)
    # Total: 5 operations
    assert context.get_operation_count() == expected_operations
    assert result == expected_result


def test_division_by_zero(context: Context, setup_logger: Logger) -> None:
    """Test division by zero."""
    expr = DivideExpression(NumberExpression(10), NumberExpression(0))
    expr.debug_print()
    
    with pytest.raises(ZeroDivisionError, match="Division by zero"):
        expr.interpret(context)


def test_modulo_by_zero(context: Context, setup_logger: Logger) -> None:
    """Test modulo by zero."""
    expr = ModuloExpression(NumberExpression(10), NumberExpression(0))
    expr.debug_print()
    
    with pytest.raises(ZeroDivisionError, match="Modulo by zero"):
        expr.interpret(context)


def test_undefined_variable(context: Context, setup_logger: Logger) -> None:
    """Test undefined variable."""
    expr = VariableExpression("undefined")
    expr.debug_print()
    
    with pytest.raises(ValueError, match="Variable not found: undefined"):
        expr.interpret(context)


def test_negative_exponent(context: Context, setup_logger: Logger) -> None:
    """Test negative exponent."""
    expr = PowerExpression(NumberExpression(2), NumberExpression(-1))
    expr.debug_print()
    
    with pytest.raises(ValueError, match="Negative exponent not supported"):
        expr.interpret(context)
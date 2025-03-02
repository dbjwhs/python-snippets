# MIT License
# Copyright (c) 2025 dbjwhs

"""
Interpreter Pattern implementation in Python.

This package provides a complete implementation of the Interpreter design pattern,
allowing for the interpretation and evaluation of expressions in a custom language.
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


__all__ = [
    "AddExpression",
    "Context",
    "DivideExpression",
    "Expression",
    "ModuloExpression",
    "MultiplyExpression", 
    "NumberExpression",
    "PowerExpression",
    "SubtractExpression",
    "VariableExpression",
]
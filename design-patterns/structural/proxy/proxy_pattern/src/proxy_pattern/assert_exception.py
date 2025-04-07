# MIT License
# Copyright (c) 2025 dbjwhs

"""Assertion utilities for the Proxy pattern implementation."""

from collections.abc import Callable
from typing import Any, TypeVar, cast

T = TypeVar('T', bound=Exception)


def assert_exception(
    func: Callable[..., Any], exception_type: type[T], *args: Any, **kwargs: Any
) -> T:
    """Assert that the given function raises the specified exception and return it.
    
    Args:
        func: The function to call
        exception_type: The expected exception type
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        The exception that was raised
        
    Raises:
        AssertionError: If no exception was raised or if the raised exception 
            is not of the expected type
    """
    try:
        func(*args, **kwargs)
        func_name = getattr(func, "__name__", str(func))
        raise AssertionError(f"Function {func_name} did not raise {exception_type.__name__}")
    except Exception as e:
        if not isinstance(e, exception_type):
            func_name = getattr(func, "__name__", str(func))
            error_msg = (
                f"Function {func_name} raised {type(e).__name__} "
                f"instead of {exception_type.__name__}"
            )
            raise AssertionError(error_msg) from e
        return cast(T, e)
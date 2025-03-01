# MIT License
# Copyright (c) 2025 dbjwhs

"""Expense handler classes for the Chain of Responsibility pattern."""

from abc import ABC, abstractmethod

from .logger import Logger, LogLevel


class ExpenseHandler(ABC):
    """Base expense handler class.
    
    This is the abstract handler class in the Chain of Responsibility pattern.
    Each handler has a reference to the next handler in the chain.
    """

    def __init__(self, approval_limit: float, position_name: str) -> None:
        """Initialize a new ExpenseHandler.
        
        Args:
            approval_limit: The maximum amount this handler can approve
            position_name: The name of the position/role
        """
        self._logger: Logger = Logger.get_instance()
        self._next_handler: ExpenseHandler | None = None
        self._approval_limit: float = approval_limit
        self._position_name: str = position_name

    def set_next(self, next_handler: "ExpenseHandler") -> "ExpenseHandler":
        """Set the next handler in the chain.
        
        Args:
            next_handler: The next handler in the chain
            
        Returns:
            The next handler to allow for chaining.
        """
        self._next_handler = next_handler
        return next_handler

    @staticmethod
    def _format_usd(amount: float) -> str:
        """Format a float value as a USD string with 2 decimal places.
        
        Args:
            amount: The amount to format
            
        Returns:
            A string representation with 2 decimal places
        """
        return f"{amount:.2f}"

    def process_request(self, amount: float, purpose: str) -> bool:
        """Process an expense request.
        
        Args:
            amount: The amount of the expense
            purpose: The purpose of the expense
            
        Returns:
            True if the request is approved, False otherwise.
        """
        # Validate input
        if amount < 0:
            self._logger.log(
                LogLevel.INFO,
                f"Error: Invalid negative amount ${self._format_usd(amount)}"
            )
            return False

        if not purpose:
            self._logger.log(LogLevel.INFO, "Error: Purpose cannot be empty")
            return False

        if amount <= self._approval_limit:
            self._approve_expense(amount, purpose)
            return True
        elif self._next_handler:
            # Pass to next handler if amount exceeds current handler's limit
            self._logger.log(
                LogLevel.INFO,
                f"{self._position_name}: amount exceeds my approval limit. forwarding request..."
            )
            return self._next_handler.process_request(amount, purpose)
        else:
            # If no next handler and amount exceeds limit
            self._logger.log(
                LogLevel.INFO,
                f"Error: expense of ${self._format_usd(amount)} cannot be approved. "
                "No handler with sufficient authority in chain."
            )
            return False

    def _approve_expense(self, amount: float, purpose: str) -> None:
        """Approve an expense request.
        
        Args:
            amount: The amount of the expense
            purpose: The purpose of the expense
        """
        self._logger.log(
            LogLevel.INFO,
            f"{self._position_name} approved expense of ${self._format_usd(amount)} for {purpose}"
        )
        
        # Hook for additional approval actions
        self._post_approve_expense(purpose)

    @abstractmethod
    def _post_approve_expense(self, purpose: str) -> None:
        """Hook method for additional approval actions.
        
        Args:
            purpose: The purpose of the expense
        """
        pass


class TeamLeader(ExpenseHandler):
    """Team leader can approve small expenses."""
    
    def __init__(self) -> None:
        """Initialize a TeamLeader handler with a $1000 approval limit."""
        super().__init__(1000.0, "team leader")
        
    def _post_approve_expense(self, purpose: str) -> None:
        """Implement the abstract method for TeamLeader.
        
        Args:
            purpose: The purpose of the expense
        """
        pass


class DepartmentManager(ExpenseHandler):
    """Department manager can approve medium expenses."""
    
    def __init__(self) -> None:
        """Initialize a DepartmentManager handler with a $5000 approval limit."""
        super().__init__(5000.0, "department manager")
        
    def _post_approve_expense(self, purpose: str) -> None:
        """Implement the abstract method for DepartmentManager.
        
        Args:
            purpose: The purpose of the expense
        """
        pass


class Director(ExpenseHandler):
    """Director can approve large expenses."""
    
    def __init__(self) -> None:
        """Initialize a Director handler with a $20000 approval limit."""
        super().__init__(20000.0, "director")
        
    def _post_approve_expense(self, purpose: str) -> None:
        """Implement the abstract method for Director.
        
        Args:
            purpose: The purpose of the expense
        """
        pass


class CEO(ExpenseHandler):
    """CEO can approve very large expenses."""
    
    def __init__(self) -> None:
        """Initialize a CEO handler with a $100000 approval limit."""
        super().__init__(100000.0, "ceo")
    
    def _post_approve_expense(self, purpose: str) -> None:
        """Override the post-approval hook to add financial review note.
        
        Args:
            purpose: The purpose of the expense
        """
        self._logger.log(LogLevel.INFO, "expense will be reported in quarterly financial review")


class Crom(ExpenseHandler):
    """Crom is grim and rejects all requests."""
    
    def __init__(self) -> None:
        """Initialize a Crom handler with a $1 approval limit."""
        super().__init__(1.0, "CROM")
    
    def process_request(self, amount: float, purpose: str) -> bool:
        """Override to reject all requests.
        
        Args:
            amount: The amount of the expense
            purpose: The purpose of the expense
            
        Returns:
            Always False, as Crom rejects all requests.
        """
        self._logger.log(
            LogLevel.INFO,
            f"I am {self._position_name}! By the Gods! "
            f"I will not approve ${self._format_usd(amount)}"
        )
        return False
        
    def _post_approve_expense(self, purpose: str) -> None:
        """Implement the abstract method for Crom.
        
        Args:
            purpose: The purpose of the expense
        """
        pass
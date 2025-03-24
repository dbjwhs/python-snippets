# MIT License
# Copyright (c) 2025 dbjwhs

"""Strategy design pattern implementation."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

from icecream import ic


class Logger:
    """Simple logger using icecream for demonstration."""

    _instance: Optional["Logger"] = None

    def __new__(cls) -> "Logger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def log(message: str) -> None:
        """Log a message."""
        ic(message)


class PaymentStrategy(ABC):
    """Abstract strategy interface for payment methods."""

    def __init__(self) -> None:
        """Initialize payment strategy with logger."""
        self._logger = Logger()

    @abstractmethod
    def pay(self, amount: float) -> bool:
        """Process payment with the given amount.

        Args:
            amount: The amount to pay

        Returns:
            bool: Whether the payment was successful
        """
        pass

    @property
    @abstractmethod
    def payment_method(self) -> str:
        """Return the payment method name for testing.

        Returns:
            str: The name of the payment method
        """
        pass


@dataclass
class CreditCardStrategy(PaymentStrategy):
    """Concrete strategy for credit card payments."""

    name: str
    card_number: str
    cvv: str
    expiry_date: str
    
    def __post_init__(self) -> None:
        """Initialize parent class after dataclass initialization."""
        super().__init__()

    def pay(self, amount: float) -> bool:
        """Process payment with credit card.

        Args:
            amount: The amount to pay

        Returns:
            bool: Always returns True for this demo
        """
        self._logger.log(
            f"Paid {amount:.2f} using credit card ending with "
            f"{self.card_number[-4:]}"
        )
        return True

    @property
    def payment_method(self) -> str:
        """Return the payment method name.

        Returns:
            str: Name of the payment method
        """
        return "CreditCard"


@dataclass
class PayPalStrategy(PaymentStrategy):
    """Concrete strategy for PayPal payments."""

    email: str
    password: str
    
    def __post_init__(self) -> None:
        """Initialize parent class after dataclass initialization."""
        super().__init__()

    def pay(self, amount: float) -> bool:
        """Process payment with PayPal.

        Args:
            amount: The amount to pay

        Returns:
            bool: Always returns True for this demo
        """
        self._logger.log(f"Paid {amount:.2f} using PayPal account: {self.email}")
        return True

    @property
    def payment_method(self) -> str:
        """Return the payment method name.

        Returns:
            str: Name of the payment method
        """
        return "PayPal"


@dataclass
class CryptoStrategy(PaymentStrategy):
    """Concrete strategy for cryptocurrency payments."""

    wallet_id: str
    
    def __post_init__(self) -> None:
        """Initialize parent class after dataclass initialization."""
        super().__init__()

    def pay(self, amount: float) -> bool:
        """Process payment with cryptocurrency.

        Args:
            amount: The amount to pay

        Returns:
            bool: Always returns True for this demo
        """
        self._logger.log(f"Paid {amount:.2f} using crypto wallet: {self.wallet_id}")
        return True

    @property
    def payment_method(self) -> str:
        """Return the payment method name.

        Returns:
            str: Name of the payment method
        """
        return "Crypto"


@dataclass
class ShoppingCart:
    """Context class that uses different payment strategies."""

    _payment_strategy: PaymentStrategy | None = field(default=None)
    _total: float = field(default=0.0)
    _logger: Logger = field(default_factory=Logger)

    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        """Set the payment strategy at runtime.

        Args:
            strategy: The payment strategy to use
        """
        self._payment_strategy = strategy

    def add_to_total(self, amount: float) -> None:
        """Add amount to cart total.

        Args:
            amount: The amount to add to the total
        """
        self._total += amount

    def checkout(self, report_no_error: bool = False) -> bool:
        """Execute the payment using the selected strategy.

        Args:
            report_no_error: If True, suppress errors about missing strategy

        Returns:
            bool: Whether the checkout was successful
        """
        if not self._payment_strategy and not report_no_error:
            self._logger.log("No payment strategy selected!")
            return False
        return True if report_no_error else self._payment_strategy.pay(self._total)

    @property
    def total(self) -> float:
        """Get the current total.

        Returns:
            float: The current total amount
        """
        return self._total
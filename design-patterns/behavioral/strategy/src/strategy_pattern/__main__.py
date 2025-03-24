# MIT License
# Copyright (c) 2025 dbjwhs

"""Main module to demonstrate the Strategy Pattern."""

from strategy_pattern.strategy import (
    CreditCardStrategy,
    CryptoStrategy,
    Logger,
    PayPalStrategy,
    ShoppingCart,
)


def test_payment_strategy(cart: ShoppingCart, strategy: any) -> None:
    """Test a payment strategy.

    Args:
        cart: The shopping cart to use
        strategy: The payment strategy to test
    """
    logger = Logger()

    logger.log(f"Testing {strategy.payment_method} strategy:")
    logger.log("----------------------------------------")

    # Set the strategy and add items
    cart.set_payment_strategy(strategy)
    cart.add_to_total(100.50)

    # Attempt checkout
    result = cart.checkout()

    # Verify results
    logger.log(f"Checkout {'successful' if result else 'failed'}")
    logger.log(f"Total amount: {cart.total:.2f}")


def main() -> None:
    """Run the main demonstration of the Strategy pattern."""
    logger = Logger()

    # Create shopping cart instance
    cart = ShoppingCart()

    # Create test cases for each payment strategy
    test_cases = [
        CreditCardStrategy(
            name="John Doe",
            card_number="1234567890123456",
            cvv="123",
            expiry_date="12/25",
        ),
        PayPalStrategy(email="john.doe@email.com", password="password123"),
        CryptoStrategy(wallet_id="0xabc123def456"),
    ]

    # Execute test cases
    for strategy in test_cases:
        test_payment_strategy(cart, strategy)

    # Test invalid case (no strategy selected)
    logger.log("Testing no strategy selected:")
    logger.log("----------------------------------------")
    empty_cart = ShoppingCart()
    empty_cart.add_to_total(50.25)
    result = empty_cart.checkout(report_no_error=True)
    logger.log(f"Invalid checkout test {'successful' if result else 'failed'}")


if __name__ == "__main__":
    main()
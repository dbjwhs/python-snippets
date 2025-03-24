#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""Example usage of the Strategy pattern for payment processing."""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Import strategy components after modifying path
# fmt: off
from strategy_pattern.strategy import (  # noqa: E402
    CreditCardStrategy,
    CryptoStrategy,
    PayPalStrategy,
    ShoppingCart,
)

# fmt: on


def run_payment_example() -> None:
    """Run an example of using the Strategy pattern for payments."""
    # Create a shopping cart
    cart = ShoppingCart()
    
    # Add some items to the cart
    cart.add_to_total(50.0)  # First item
    cart.add_to_total(25.75)  # Second item
    print(f"Shopping cart total: ${cart.total:.2f}")
    
    # Initialize payment strategies
    credit_card = CreditCardStrategy(
        name="John Doe",
        card_number="4111111111111111",
        cvv="123",
        expiry_date="12/25"
    )
    
    paypal = PayPalStrategy(
        email="john.doe@example.com",
        password="securepassword"
    )
    
    crypto = CryptoStrategy(
        wallet_id="0x1a2b3c4d5e6f"
    )
    
    # Choose a strategy based on user preference (simulated here)
    payment_choice = input(
        "Choose payment method (1=Credit Card, 2=PayPal, 3=Cryptocurrency): "
    ).strip()
    
    # Set the appropriate strategy
    if payment_choice == "1":
        cart.set_payment_strategy(credit_card)
        print("Using credit card payment method")
    elif payment_choice == "2":
        cart.set_payment_strategy(paypal)
        print("Using PayPal payment method")
    elif payment_choice == "3":
        cart.set_payment_strategy(crypto)
        print("Using cryptocurrency payment method")
    else:
        print("Invalid choice! Defaulting to credit card.")
        cart.set_payment_strategy(credit_card)
    
    # Process payment
    if cart.checkout():
        print("Payment successful!")
    else:
        print("Payment failed!")


if __name__ == "__main__":
    run_payment_example()
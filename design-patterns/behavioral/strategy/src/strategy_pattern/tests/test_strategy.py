# MIT License
# Copyright (c) 2025 dbjwhs

"""Unit tests for the Strategy Pattern implementation."""


from strategy_pattern.strategy import (
    CreditCardStrategy,
    CryptoStrategy,
    PayPalStrategy,
    ShoppingCart,
)


class TestShoppingCart:
    """Test suite for the ShoppingCart class."""

    def test_shopping_cart_initialization(self) -> None:
        """Test shopping cart initialization."""
        cart = ShoppingCart()
        assert cart.total == 0.0
        assert cart._payment_strategy is None

    def test_add_to_total(self) -> None:
        """Test adding to cart total."""
        cart = ShoppingCart()
        first_amount = 10.5
        second_amount = 20.75
        expected_total = first_amount + second_amount
        
        cart.add_to_total(first_amount)
        assert cart.total == first_amount
        cart.add_to_total(second_amount)
        assert cart.total == expected_total

    def test_checkout_no_strategy(self) -> None:
        """Test checkout with no strategy set."""
        cart = ShoppingCart()
        cart.add_to_total(50.25)
        # Should fail without strategy
        assert not cart.checkout()
        # Should succeed with report_no_error=True
        assert cart.checkout(report_no_error=True)


class TestPaymentStrategies:
    """Test suite for the payment strategies."""

    def test_credit_card_strategy(self) -> None:
        """Test credit card payment strategy."""
        strategy = CreditCardStrategy(
            name="John Doe",
            card_number="1234567890123456",
            cvv="123",
            expiry_date="12/25",
        )
        assert strategy.payment_method == "CreditCard"
        
        # Test payment
        cart = ShoppingCart()
        cart.set_payment_strategy(strategy)
        cart.add_to_total(100.0)
        assert cart.checkout()

    def test_paypal_strategy(self) -> None:
        """Test PayPal payment strategy."""
        strategy = PayPalStrategy(
            email="john.doe@email.com",
            password="password123",
        )
        assert strategy.payment_method == "PayPal"
        
        # Test payment
        cart = ShoppingCart()
        cart.set_payment_strategy(strategy)
        cart.add_to_total(75.50)
        assert cart.checkout()

    def test_crypto_strategy(self) -> None:
        """Test cryptocurrency payment strategy."""
        strategy = CryptoStrategy(wallet_id="0xabc123def456")
        assert strategy.payment_method == "Crypto"
        
        # Test payment
        cart = ShoppingCart()
        cart.set_payment_strategy(strategy)
        cart.add_to_total(200.0)
        assert cart.checkout()

    def test_strategy_switching(self) -> None:
        """Test switching between different payment strategies."""
        cart = ShoppingCart()
        cart.add_to_total(150.0)
        
        # Start with credit card
        cc_strategy = CreditCardStrategy(
            name="John Doe",
            card_number="1234567890123456",
            cvv="123",
            expiry_date="12/25",
        )
        cart.set_payment_strategy(cc_strategy)
        assert cart.checkout()
        
        # Switch to PayPal
        pp_strategy = PayPalStrategy(
            email="john.doe@email.com",
            password="password123",
        )
        cart.set_payment_strategy(pp_strategy)
        assert cart.checkout()
        
        # Switch to crypto
        crypto_strategy = CryptoStrategy(wallet_id="0xabc123def456")
        cart.set_payment_strategy(crypto_strategy)
        assert cart.checkout()
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Rule Engine Example using the Interpreter Pattern.

This example demonstrates how to use the Interpreter pattern to build
a simple rule engine for evaluating business rules.
"""

from dataclasses import dataclass
from enum import Enum

from interpreter_pattern.context import Context
from interpreter_pattern.expressions import Expression
from interpreter_pattern.expressions import NumberExpression
from interpreter_pattern.expressions import SubtractExpression
from interpreter_pattern.expressions import VariableExpression
from interpreter_pattern.logger import Logger
from interpreter_pattern.logger import LogLevel


@dataclass
class Product:
    """Product class for the rule engine example."""
    
    id: str
    name: str
    price: float
    category: str
    in_stock: int
    min_age: int


@dataclass
class Customer:
    """Customer class for the rule engine example."""
    
    id: str
    name: str
    age: int
    loyalty_points: int
    is_premium: bool


class RuleAction(Enum):
    """Enum for rule actions."""
    
    APPLY_DISCOUNT = 0
    BLOCK_PURCHASE = 1
    FLAG_FOR_REVIEW = 2
    AWARD_BONUS_POINTS = 3


class Rule:
    """Rule class for the rule engine example."""
    
    def __init__(
        self, name: str, condition: Expression, action: RuleAction, action_value: int = 0
    ) -> None:
        """
        Initialize a new Rule.
        
        Args:
            name: The rule name.
            condition: The condition expression.
            action: The action to take if the condition is true.
            action_value: The value for the action (e.g., discount percentage).
        """
        self.name = name
        self.condition = condition
        self.action = action
        self.action_value = action_value
    
    def evaluate(self, context: Context) -> bool:
        """
        Evaluate the rule condition.
        
        Args:
            context: The context containing variables for evaluation.
            
        Returns:
            True if the condition is true, False otherwise.
        """
        Logger.get_instance().log(LogLevel.INFO, "Evaluating rule: {}", self.name)
        result = self.condition.interpret(context) != 0
        Logger.get_instance().log(
            LogLevel.INFO, 
            "Rule '{}' evaluated to: {}", 
            self.name, 
            result
        )
        return result


class RuleEngine:
    """Rule engine for evaluating business rules."""
    
    def __init__(self) -> None:
        """Initialize a new RuleEngine."""
        self.rules: list[Rule] = []
        self.context = Context()
    
    def add_rule(self, rule: Rule) -> None:
        """
        Add a rule to the rule engine.
        
        Args:
            rule: The rule to add.
        """
        self.rules.append(rule)
        Logger.get_instance().log(LogLevel.INFO, "Added rule: {}", rule.name)
    
    def prepare_context(self, product: Product, customer: Customer) -> None:
        """
        Prepare the context with product and customer data.
        
        Args:
            product: The product data.
            customer: The customer data.
        """
        # Product variables
        self.context.set_variable("prod_price", int(product.price))
        self.context.set_variable("prod_stock", product.in_stock)
        self.context.set_variable("prod_min_age", product.min_age)
        
        # Customer variables
        self.context.set_variable("cust_age", customer.age)
        self.context.set_variable("cust_loyalty", customer.loyalty_points)
        self.context.set_variable("cust_premium", 1 if customer.is_premium else 0)
    
    def evaluate_rules(self, product: Product, customer: Customer) -> dict[RuleAction, int]:
        """
        Evaluate all rules for a product and customer.
        
        Args:
            product: The product data.
            customer: The customer data.
            
        Returns:
            A dictionary of actions to take with their values.
        """
        self.prepare_context(product, customer)
        
        Logger.get_instance().log(
            LogLevel.INFO, 
            "Evaluating rules for product '{}' and customer '{}'",
            product.name,
            customer.name
        )
        
        actions: dict[RuleAction, int] = {}
        
        for rule in self.rules:
            if rule.evaluate(self.context):
                # If multiple rules trigger the same action, take the highest value
                if rule.action in actions:
                    actions[rule.action] = max(actions[rule.action], rule.action_value)
                else:
                    actions[rule.action] = rule.action_value
                
                Logger.get_instance().log(
                    LogLevel.INFO, 
                    "Rule '{}' triggered action: {} with value: {}", 
                    rule.name, 
                    rule.action.name, 
                    rule.action_value
                )
        
        return actions


def create_age_rule() -> Rule:
    """
    Create a rule for age verification.
    
    Returns:
        The age verification rule.
    """
    # Rule: Block purchase if customer age < product minimum age
    condition = SubtractExpression(
        VariableExpression("cust_age"),
        VariableExpression("prod_min_age")
    )
    
    # If condition <= 0, block purchase
    return Rule(
        "Age Verification",
        condition,
        RuleAction.BLOCK_PURCHASE
    )


def create_premium_discount_rule() -> Rule:
    """
    Create a rule for premium customer discount.
    
    Returns:
        The premium discount rule.
    """
    # Rule: Apply 10% discount if customer is premium
    condition = VariableExpression("cust_premium")
    
    return Rule(
        "Premium Discount",
        condition,
        RuleAction.APPLY_DISCOUNT,
        10  # 10% discount
    )


def create_loyalty_discount_rule() -> Rule:
    """
    Create a rule for loyalty points discount.
    
    Returns:
        The loyalty discount rule.
    """
    # Rule: Apply 5% discount if customer has 1000+ loyalty points
    # "loyalty_points >= 1000" as "loyalty_points - 1000 >= 0"
    condition = SubtractExpression(
        VariableExpression("cust_loyalty"),
        NumberExpression(1000)
    )
    
    return Rule(
        "Loyalty Discount",
        condition,
        RuleAction.APPLY_DISCOUNT,
        5  # 5% discount
    )


def create_stock_rule() -> Rule:
    """
    Create a rule for low stock flagging.
    
    Returns:
        The low stock rule.
    """
    # Rule: Flag for review if stock is less than 5
    # "stock < 5" as "5 - stock > 0"
    condition = SubtractExpression(
        NumberExpression(5),
        VariableExpression("prod_stock")
    )
    
    return Rule(
        "Low Stock Alert",
        condition,
        RuleAction.FLAG_FOR_REVIEW
    )


def create_bonus_points_rule() -> Rule:
    """
    Create a rule for awarding bonus points.
    
    Returns:
        The bonus points rule.
    """
    # Rule: Award 50 bonus points if purchase price > 100
    # "price > 100" as "price - 100 > 0"
    condition = SubtractExpression(
        VariableExpression("prod_price"),
        NumberExpression(100)
    )
    
    return Rule(
        "Bonus Points",
        condition,
        RuleAction.AWARD_BONUS_POINTS,
        50  # 50 bonus points
    )


def process_purchase(
    engine: RuleEngine, product: Product, customer: Customer
) -> dict[str, str]:
    """
    Process a purchase using the rule engine.
    
    Args:
        engine: The rule engine.
        product: The product being purchased.
        customer: The customer making the purchase.
        
    Returns:
        A dictionary with the purchase details and applied rules.
    """
    actions = engine.evaluate_rules(product, customer)
    
    # Initial result
    result = {
        "customer": customer.name,
        "product": product.name,
        "base_price": f"${product.price:.2f}",
        "status": "Approved"
    }
    
    # Apply actions
    if RuleAction.BLOCK_PURCHASE in actions:
        result["status"] = "Blocked"
        result["reason"] = "Age requirement not met"
        return result
    
    # Calculate final price
    final_price = product.price
    if RuleAction.APPLY_DISCOUNT in actions:
        discount_percent = actions[RuleAction.APPLY_DISCOUNT]
        discount_amount = product.price * (discount_percent / 100)
        final_price -= discount_amount
        result["discount"] = f"{discount_percent}% (${discount_amount:.2f})"
    
    result["final_price"] = f"${final_price:.2f}"
    
    if RuleAction.FLAG_FOR_REVIEW in actions:
        result["flagged"] = "Yes - Low stock"
    
    if RuleAction.AWARD_BONUS_POINTS in actions:
        result["bonus_points"] = str(actions[RuleAction.AWARD_BONUS_POINTS])
    
    return result


def main() -> None:
    """Main function to demonstrate the rule engine example."""
    logger = Logger.get_instance()
    logger.log(LogLevel.INFO, "Starting Rule Engine Example")
    
    # Create rule engine
    engine = RuleEngine()
    
    # Add rules
    engine.add_rule(create_age_rule())
    engine.add_rule(create_premium_discount_rule())
    engine.add_rule(create_loyalty_discount_rule())
    engine.add_rule(create_stock_rule())
    engine.add_rule(create_bonus_points_rule())
    
    # Create products
    products = [
        Product("P001", "Gaming Console", 299.99, "Electronics", 10, 16),
        Product("P002", "Adult Beverage", 24.99, "Beverages", 3, 21),
        Product("P003", "Basic Toy", 14.99, "Toys", 20, 3),
    ]
    
    # Create customers
    customers = [
        Customer("C001", "Jane Smith", 25, 1200, True),
        Customer("C002", "Bob Johnson", 17, 500, False),
        Customer("C003", "Alice Brown", 35, 2000, True),
    ]
    
    # Process some purchases
    for product in products:
        for customer in customers:
            logger.log(
                LogLevel.INFO, 
                "\n--- Processing purchase: {} buying {} ---", 
                customer.name, 
                product.name
            )
            
            result = process_purchase(engine, product, customer)
            
            # Print result
            logger.log(LogLevel.INFO, "Purchase details:")
            for key, value in result.items():
                logger.log(LogLevel.INFO, "  {}: {}", key, value)
            
            logger.log(LogLevel.INFO, "---\n")
    
    logger.log(LogLevel.INFO, "Rule Engine Example completed")


if __name__ == "__main__":
    main()
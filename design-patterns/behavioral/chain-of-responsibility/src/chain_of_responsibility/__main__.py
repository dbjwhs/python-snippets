# MIT License
# Copyright (c) 2025 dbjwhs

"""Main entry point for the Chain of Responsibility module.

This module contains the main function that demonstrates the Chain of Responsibility pattern
with the expense approval example.
"""

from typing import Final

from .expense_handler import (
    CEO,
    Crom,
    DepartmentManager,
    Director,
    ExpenseHandler,
    TeamLeader,
)
from .expense_request import ExpenseRequest
from .logger import LogLevel, Logger


def main() -> None:
    """Run the Chain of Responsibility demonstration."""
    logger: Final[Logger] = Logger.get_instance()

    # Test case 1: Create our hierarchy
    team_leader = TeamLeader()
    dept_manager = DepartmentManager()
    director = Director()
    ceo = CEO()
    crom = Crom()

    # Create our chain
    team_leader.set_next(dept_manager)
    dept_manager.set_next(director)
    director.set_next(ceo)
    ceo.set_next(crom)

    standard_requests: list[ExpenseRequest] = [
        ExpenseRequest(800.0, "office supplies"),
        ExpenseRequest(3000.0, "team building event"),
        ExpenseRequest(12000.0, "new software licenses"),
        ExpenseRequest(45000.0, "department renovation"),
        ExpenseRequest(200000.0, "new satellite office"),
    ]

    approved_str: Final[str] = "APPROVED"
    rejected_str: Final[str] = "REJECTED"

    logger.log(LogLevel.INFO, "expense approval chain of responsibility - test cases")
    logger.log(LogLevel.INFO, "-------------------")
    logger.log(LogLevel.INFO, "test case 1: standard approval chain")
    logger.log(LogLevel.INFO, "-------------------")

    for request in standard_requests:
        logger.log(
            LogLevel.INFO, 
            f"expense request: ${ExpenseHandler._format_usd(request.amount)} for {request.purpose}"
        )
        success = team_leader.process_request(request.amount, request.purpose)
        logger.log(LogLevel.INFO, f"Request status: {approved_str if success else rejected_str}")
        logger.log(LogLevel.INFO, "-------------------")

    # Test case 2: Broken chain (missing CEO)
    logger.log(LogLevel.INFO, "-------------------")
    logger.log(LogLevel.INFO, "test case 2: broken chain (missing ceo)")

    leader2 = TeamLeader()
    manager2 = DepartmentManager()
    director2 = Director()

    leader2.set_next(manager2)
    manager2.set_next(director2)

    logger.log(LogLevel.INFO, "testing high-value request with incomplete chain:")
    incomplete_chain_result = leader2.process_request(50000.0, "data center upgrade")
    logger.log(
        LogLevel.INFO, 
        f"Request status: {approved_str if incomplete_chain_result else rejected_str}"
    )

    # Test case 3: Direct access to middle of chain
    logger.log(LogLevel.INFO, "-------------------")
    logger.log(LogLevel.INFO, "test case 3: direct access to middle of chain")
    logger.log(LogLevel.INFO, "bypassing team leader, starting from department manager:")
    mid_chain_result = dept_manager.process_request(4000.0, "emergency repairs")
    logger.log(
        LogLevel.INFO, 
        f"Request status: {approved_str if mid_chain_result else rejected_str}"
    )

    # Test case 4: Edge cases
    logger.log(LogLevel.INFO, "-------------------")
    logger.log(LogLevel.INFO, "test case 4: edge cases")

    logger.log(LogLevel.INFO, "testing zero amount request:")
    zero_amount_result = team_leader.process_request(0.0, "subscription renewal")
    logger.log(
        LogLevel.INFO,
        f"Request status: {approved_str if zero_amount_result else rejected_str}"
    )

    logger.log(LogLevel.INFO, "testing amount at exact approval limit:")
    exact_limit_result1 = team_leader.process_request(1000.0, "exactly at team leader limit")
    logger.log(
        LogLevel.INFO,
        f"Team leader limit test status: {approved_str if exact_limit_result1 else rejected_str}"
    )

    exact_limit_result2 = dept_manager.process_request(
        5000.0, "exactly at department manager limit"
    )
    logger.log(
        LogLevel.INFO,
        f"Department manager limit test status: "
        f"{approved_str if exact_limit_result2 else rejected_str}"
    )

    logger.log(LogLevel.INFO, "testing negative amount (invalid input):")
    negative_amount_result = team_leader.process_request(-500.0, "invalid negative expense")
    logger.log(
        LogLevel.INFO,
        f"Request status: {approved_str if negative_amount_result else rejected_str}"
    )

    # Test case 5: Single handler chain
    logger.log(LogLevel.INFO, "-------------------")
    logger.log(LogLevel.INFO, "test case 5: single handler chain")
    solo_leader = TeamLeader()

    logger.log(LogLevel.INFO, "testing with single handler:")
    solo_within_limit = solo_leader.process_request(500.0, "within solo handler limit")
    logger.log(
        LogLevel.INFO,
        f"Within limit request status: {approved_str if solo_within_limit else rejected_str}"
    )

    solo_exceeds_limit = solo_leader.process_request(2000.0, "exceeds solo handler limit")
    logger.log(
        LogLevel.INFO,
        f"Exceeds limit request status: {approved_str if solo_exceeds_limit else rejected_str}"
    )


if __name__ == "__main__":
    main()
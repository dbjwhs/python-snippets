# MIT License
# Copyright (c) 2025 dbjwhs

"""Tests for the expense handler implementation."""

import pytest

from src.chain_of_responsibility.expense_handler import (
    CEO,
    Crom,
    DepartmentManager,
    Director,
    TeamLeader,
)


class TestExpenseHandler:
    """Unit tests for the ExpenseHandler classes."""

    def test_team_leader_approval(self):
        """Test that team leader approves expenses within limit."""
        team_leader = TeamLeader()
        
        # Within limit
        assert team_leader.process_request(800.0, "office supplies") is True
        
        # At limit
        assert team_leader.process_request(1000.0, "exactly at limit") is True
        
        # Above limit, no next handler
        assert team_leader.process_request(1200.0, "exceeds limit") is False

    def test_handler_chain(self):
        """Test that the handler chain works correctly."""
        team_leader = TeamLeader()
        dept_manager = DepartmentManager()
        director = Director()
        ceo = CEO()
        
        # Set up the chain
        team_leader.set_next(dept_manager)
        dept_manager.set_next(director)
        director.set_next(ceo)
        
        # Test different expense levels
        assert team_leader.process_request(500.0, "small expense") is True
        assert team_leader.process_request(3000.0, "medium expense") is True
        assert team_leader.process_request(10000.0, "large expense") is True
        assert team_leader.process_request(50000.0, "very large expense") is True
        assert team_leader.process_request(200000.0, "beyond all limits") is False

    def test_input_validation(self):
        """Test the input validation in the handler."""
        team_leader = TeamLeader()
        
        # Negative amount
        assert team_leader.process_request(-100.0, "negative amount") is False
        
        # Empty purpose
        assert team_leader.process_request(100.0, "") is False

    def test_crom_always_rejects(self):
        """Test that Crom always rejects requests."""
        crom = Crom()
        
        # Even very small amounts should be rejected
        assert crom.process_request(0.01, "tiny expense") is False
        
        # Zero amount should also be rejected
        assert crom.process_request(0.0, "zero expense") is False

    def test_direct_handler_access(self):
        """Test accessing handlers directly in the middle of a chain."""
        team_leader = TeamLeader()
        dept_manager = DepartmentManager()
        director = Director()
        
        # Set up the chain
        team_leader.set_next(dept_manager)
        dept_manager.set_next(director)
        
        # Access department manager directly
        assert dept_manager.process_request(4000.0, "direct access") is True
        
        # Access director directly
        assert director.process_request(15000.0, "direct access") is True
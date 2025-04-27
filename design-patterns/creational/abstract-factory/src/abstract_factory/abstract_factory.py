#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Abstract Factory Design Pattern Implementation.

This module demonstrates the Abstract Factory pattern which provides an interface
for creating families of related objects without specifying their concrete classes.

Key components:
1. Abstract Factory (UIFactory): Declares interface for creating abstract products
2. Concrete Factories: Implement operations to create concrete products
3. Abstract Products: Declare interfaces for product families
4. Concrete Products: Implement the product interfaces
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

from icecream import ic


@runtime_checkable
class Button(Protocol):
    """Abstract Product: Button interface."""

    text: str
    theme: str

    def render(self) -> None:
        """Render the button to the UI."""
        ...

    def get_theme(self) -> str:
        """Return the theme of this button."""
        ...


@runtime_checkable
class Checkbox(Protocol):
    """Abstract Product: Checkbox interface."""

    theme: str
    checked: bool

    def toggle(self) -> None:
        """Toggle the checkbox state."""
        ...

    def render(self) -> None:
        """Render the checkbox to the UI."""
        ...

    def get_theme(self) -> str:
        """Return the theme of this checkbox."""
        ...

    def is_checked(self) -> bool:
        """Return whether the checkbox is checked."""
        ...


@dataclass
class LightButton:
    """Concrete Product: Light theme button implementation."""

    text: str
    theme: str = field(default="light", init=False)

    def render(self) -> None:
        """Render the light-themed button."""
        ic(f"rendering light button with text: {self.text}")

    def get_theme(self) -> str:
        """Return the theme of this button."""
        return self.theme


@dataclass
class LightCheckbox:
    """Concrete Product: Light theme checkbox implementation."""

    theme: str = field(default="light", init=False)
    checked: bool = field(default=False)

    def toggle(self) -> None:
        """Toggle the checkbox state."""
        self.checked = not self.checked
        ic(f"light checkbox toggled to: {self.checked}")

    def render(self) -> None:
        """Render the light-themed checkbox."""
        ic(f"rendering light checkbox, checked: {self.checked}")

    def get_theme(self) -> str:
        """Return the theme of this checkbox."""
        return self.theme

    def is_checked(self) -> bool:
        """Return whether the checkbox is checked."""
        return self.checked


@dataclass
class DarkButton:
    """Concrete Product: Dark theme button implementation."""

    text: str
    theme: str = field(default="dark", init=False)

    def render(self) -> None:
        """Render the dark-themed button."""
        ic(f"rendering dark button with text: {self.text}")

    def get_theme(self) -> str:
        """Return the theme of this button."""
        return self.theme


@dataclass
class DarkCheckbox:
    """Concrete Product: Dark theme checkbox implementation."""

    theme: str = field(default="dark", init=False)
    checked: bool = field(default=False)

    def toggle(self) -> None:
        """Toggle the checkbox state."""
        self.checked = not self.checked
        ic(f"dark checkbox toggled to: {self.checked}")

    def render(self) -> None:
        """Render the dark-themed checkbox."""
        ic(f"rendering dark checkbox, checked: {self.checked}")

    def get_theme(self) -> str:
        """Return the theme of this checkbox."""
        return self.theme

    def is_checked(self) -> bool:
        """Return whether the checkbox is checked."""
        return self.checked


class UIFactory(ABC):
    """Abstract Factory: Declares interface for creating UI components."""

    @abstractmethod
    def create_button(self, text: str) -> Button:
        """Create a button component."""
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        """Create a checkbox component."""
        pass

    @abstractmethod
    def get_theme(self) -> str:
        """Return the theme of this factory."""
        pass


class LightThemeFactory(UIFactory):
    """Concrete Factory: Creates light theme components."""

    def create_button(self, text: str) -> Button:
        """Create a light theme button."""
        return LightButton(text)

    def create_checkbox(self) -> Checkbox:
        """Create a light theme checkbox."""
        return LightCheckbox()

    def get_theme(self) -> str:
        """Return the theme of this factory."""
        return "light"


class DarkThemeFactory(UIFactory):
    """Concrete Factory: Creates dark theme components."""

    def create_button(self, text: str) -> Button:
        """Create a dark theme button."""
        return DarkButton(text)

    def create_checkbox(self) -> Checkbox:
        """Create a dark theme checkbox."""
        return DarkCheckbox()

    def get_theme(self) -> str:
        """Return the theme of this factory."""
        return "dark"


def verify_theme_consistency(factory: UIFactory, button: Button, checkbox: Checkbox) -> None:
    """Helper function to verify theme consistency."""
    assert factory.get_theme() == button.get_theme(), "Button theme must match factory theme"
    assert factory.get_theme() == checkbox.get_theme(), "Checkbox theme must match factory theme"
    ic(f"Theme consistency verified for {factory.get_theme()} theme")


def main() -> None:
    """Run the demo application."""
    # Test light theme
    ic("Starting light theme tests")
    light_factory = LightThemeFactory()
    light_button = light_factory.create_button("OK")
    light_checkbox = light_factory.create_checkbox()

    # Verify light theme consistency
    verify_theme_consistency(light_factory, light_button, light_checkbox)

    # Test light theme components
    light_button.render()
    light_checkbox.render()
    assert not light_checkbox.is_checked(), "Checkbox should start unchecked"
    light_checkbox.toggle()
    assert light_checkbox.is_checked(), "Checkbox should be checked after toggle"

    # Test dark theme
    ic("Starting dark theme tests")
    dark_factory = DarkThemeFactory()
    dark_button = dark_factory.create_button("Cancel")
    dark_checkbox = dark_factory.create_checkbox()

    # Verify dark theme consistency
    verify_theme_consistency(dark_factory, dark_button, dark_checkbox)

    # Test dark theme components
    dark_button.render()
    dark_checkbox.render()
    assert not dark_checkbox.is_checked(), "Checkbox should start unchecked"
    dark_checkbox.toggle()
    assert dark_checkbox.is_checked(), "Checkbox should be checked after toggle"

    ic("All tests completed successfully")


if __name__ == "__main__":
    main()
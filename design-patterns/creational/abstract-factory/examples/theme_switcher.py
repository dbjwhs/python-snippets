#!/usr/bin/env python3
"""
Example application demonstrating the abstract factory pattern for theme switching.

This example creates a simple application that can switch between light and dark themes,
with all UI components automatically updating to match the selected theme.
"""

from icecream import ic

from abstract_factory.abstract_factory import (
    DarkThemeFactory,
    LightThemeFactory,
    UIFactory,
)


class Application:
    """Example application using the abstract factory pattern."""

    def __init__(self, factory: UIFactory) -> None:
        """Initialize the application with a UI factory."""
        self.factory = factory
        self.components = []
        self._create_ui()

    def _create_ui(self) -> None:
        """Create the UI components using the current factory."""
        self.components.clear()
        
        # Create buttons
        submit_btn = self.factory.create_button("Submit")
        cancel_btn = self.factory.create_button("Cancel")
        
        # Create checkboxes
        terms_cb = self.factory.create_checkbox()
        newsletter_cb = self.factory.create_checkbox()
        
        # Add all components to our list
        self.components.extend([submit_btn, cancel_btn, terms_cb, newsletter_cb])

    def change_theme(self, factory: UIFactory) -> None:
        """Change the application's theme by setting a new factory."""
        ic(f"Changing theme from {self.factory.get_theme()} to {factory.get_theme()}")
        self.factory = factory
        self._create_ui()

    def render(self) -> None:
        """Render all UI components."""
        ic(f"Rendering application with {self.factory.get_theme()} theme")
        for component in self.components:
            component.render()


def main() -> None:
    """Run the theme switcher example."""
    # Start with light theme
    light_factory = LightThemeFactory()
    app = Application(light_factory)
    
    # Render the application with light theme
    ic("Rendering with light theme:")
    app.render()
    
    # Switch to dark theme
    dark_factory = DarkThemeFactory()
    app.change_theme(dark_factory)
    
    # Render with dark theme
    ic("Rendering with dark theme:")
    app.render()


if __name__ == "__main__":
    main()
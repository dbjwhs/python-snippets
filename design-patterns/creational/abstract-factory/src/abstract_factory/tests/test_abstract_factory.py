"""Unit tests for the abstract_factory module."""


from abstract_factory.abstract_factory import (
    DarkThemeFactory,
    LightThemeFactory,
    verify_theme_consistency,
)


class TestLightThemeFactory:
    """Tests for the LightThemeFactory class."""

    def setup_method(self) -> None:
        """Set up the test fixture."""
        self.factory = LightThemeFactory()
        self.button = self.factory.create_button("OK")
        self.checkbox = self.factory.create_checkbox()

    def test_factory_theme(self) -> None:
        """Test that the factory returns the correct theme."""
        assert self.factory.get_theme() == "light"

    def test_button_creation(self) -> None:
        """Test button creation and properties."""
        assert self.button.get_theme() == "light"
        assert self.button.text == "OK"

    def test_checkbox_creation(self) -> None:
        """Test checkbox creation and properties."""
        assert self.checkbox.get_theme() == "light"
        assert not self.checkbox.is_checked()

    def test_checkbox_toggle(self) -> None:
        """Test checkbox toggle functionality."""
        assert not self.checkbox.is_checked()
        self.checkbox.toggle()
        assert self.checkbox.is_checked()
        self.checkbox.toggle()
        assert not self.checkbox.is_checked()

    def test_theme_consistency(self) -> None:
        """Test theme consistency between factory and products."""
        verify_theme_consistency(self.factory, self.button, self.checkbox)


class TestDarkThemeFactory:
    """Tests for the DarkThemeFactory class."""

    def setup_method(self) -> None:
        """Set up the test fixture."""
        self.factory = DarkThemeFactory()
        self.button = self.factory.create_button("Cancel")
        self.checkbox = self.factory.create_checkbox()

    def test_factory_theme(self) -> None:
        """Test that the factory returns the correct theme."""
        assert self.factory.get_theme() == "dark"

    def test_button_creation(self) -> None:
        """Test button creation and properties."""
        assert self.button.get_theme() == "dark"
        assert self.button.text == "Cancel"

    def test_checkbox_creation(self) -> None:
        """Test checkbox creation and properties."""
        assert self.checkbox.get_theme() == "dark"
        assert not self.checkbox.is_checked()

    def test_checkbox_toggle(self) -> None:
        """Test checkbox toggle functionality."""
        assert not self.checkbox.is_checked()
        self.checkbox.toggle()
        assert self.checkbox.is_checked()
        self.checkbox.toggle()
        assert not self.checkbox.is_checked()

    def test_theme_consistency(self) -> None:
        """Test theme consistency between factory and products."""
        verify_theme_consistency(self.factory, self.button, self.checkbox)
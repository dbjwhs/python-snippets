"""
Main entry point for the command pattern package.

This module runs the same tests as in the C++ example.
"""

from icecream import ic

from command_pattern.command import (
    Document,
    DocumentEditor,
    EraseCommand,
    HomeAutomationSystem,
    InsertCommand,
    PowerCommand,
    SceneCommand,
    SetTemperatureCommand,
    SmartDevice,
)


def run_document_tests() -> None:
    """Run tests for the document editing example."""
    doc = Document()
    editor = DocumentEditor(doc)

    ic("Testing basic insert command...")
    editor.execute_command(InsertCommand(doc, "Hello", 0))
    assert doc.content == "Hello"
    ic("Content after insert:", doc.content)

    ic("Testing basic erase command...")
    editor.execute_command(EraseCommand(doc, 0, 2))
    assert doc.content == "llo"
    ic("Content after erase:", doc.content)

    ic("Testing undo functionality...")
    editor.undo()  # undo erase
    assert doc.content == "Hello"
    ic("Content after undo:", doc.content)

    ic("Testing redo functionality...")
    editor.redo()  # redo erase
    assert doc.content == "llo"
    ic("Content after redo:", doc.content)

    ic("Testing multiple commands...")
    editor.execute_command(InsertCommand(doc, " World", 3))
    assert doc.content == "llo World"
    editor.execute_command(EraseCommand(doc, 3, 1))  # erase the space
    assert doc.content == "lloWorld"
    ic("Content after multiple commands:", doc.content)

    ic("Testing multiple undos...")
    editor.undo()  # undo last erase
    editor.undo()  # undo last insert
    editor.undo()  # undo first erase
    assert doc.content == "Hello"
    ic("Content after multiple undos:", doc.content)

    ic("All document tests passed!")


def run_smart_device_tests() -> None:
    """Run tests for the smart home automation example."""
    ic("Starting Smart Home Automation Tests...")

    living_room_light = SmartDevice("LR_LIGHT_1")
    bedroom_light = SmartDevice("BR_LIGHT_1")
    thermostat = SmartDevice("THERM_1")

    # Verify initial states
    ic("Verifying initial device states...")
    assert not living_room_light.is_on, "Light should be off initially"
    assert not bedroom_light.is_on, "Light should be off initially"
    assert thermostat.temperature == 20, "Thermostat should start at 20°C"
    ic("✓ All devices initialized correctly")

    home = HomeAutomationSystem()

    ic("Creating 'movie time' scene...")
    movie_scene = SceneCommand()
    movie_scene.add_command(PowerCommand(living_room_light, False))
    movie_scene.add_command(SetTemperatureCommand(thermostat, 22))

    home.create_scene("movie_time", movie_scene)
    ic("✓ Scene created successfully")

    ic("Activating 'movie time' scene...")
    home.activate_scene("movie_time")
    assert not living_room_light.is_on, "Living room light should be off"
    assert thermostat.temperature == 22, "Temperature should be 22°C"
    ic("✓ Scene activated: lights dimmed and temperature set to 22°C")

    ic("Adjusting temperature for cold person...")
    home.execute_command(SetTemperatureCommand(thermostat, 24))
    assert thermostat.temperature == 24, "Temperature should be 24°C"
    ic("✓ Temperature increased to 24°C")

    ic("Testing undo functionality for temperature change...")
    home.undo_last()
    assert thermostat.temperature == 22, "Temperature should be back to 22°C"
    ic("✓ Temperature successfully reverted to 22°C")

    # Test edge cases
    ic("Testing edge cases...")

    ic("Testing scene activation with non-existent scene...")
    home.activate_scene("non_existent_scene")
    assert not living_room_light.is_on, "Light state shouldn't change"
    assert thermostat.temperature == 22, "Temperature shouldn't change"
    ic("✓ Non-existent scene handled correctly")

    ic("Testing multiple undo operations...")
    home.undo_last()  # should undo the movie scene activation
    home.undo_last()  # should do nothing as stack is empty
    ic("✓ Multiple undos handled without errors")

    ic("All Smart Home Automation tests passed successfully!")


def main() -> None:
    """Main entry point for the package."""
    ic.configureOutput(prefix="[Command Pattern] ")
    
    ic("Command Pattern Examples")
    ic("======================")

    try:
        run_smart_device_tests()
        run_document_tests()
        ic("All tests completed successfully!")
    except Exception as e:
        ic("Error during testing:", str(e))
        raise


if __name__ == "__main__":
    main()
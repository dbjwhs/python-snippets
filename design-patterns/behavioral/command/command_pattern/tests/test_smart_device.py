"""
Tests for the smart device functionality of the Command pattern.
"""


from command_pattern.command import (
    HomeAutomationSystem,
    PowerCommand,
    SceneCommand,
    SetTemperatureCommand,
    SmartDevice,
)


def test_smart_device_initialization() -> None:
    """Test that a smart device is initialized with default values."""
    device = SmartDevice("test_device")
    assert device.id == "test_device"
    assert device.is_on is False
    assert device.brightness == 0
    assert device.temperature == 20


def test_smart_device_power() -> None:
    """Test the power operation on a smart device."""
    device = SmartDevice("test_device")
    assert not device.is_on

    device.power(True)
    assert device.is_on

    device.power(False)
    assert not device.is_on


def test_smart_device_temperature() -> None:
    """Test the temperature operation on a smart device."""
    device = SmartDevice("test_device")
    assert device.temperature == 20

    device.set_temperature(25)
    assert device.temperature == 25

    device.set_temperature(18)
    assert device.temperature == 18


def test_smart_device_brightness() -> None:
    """Test the brightness operation on a smart device."""
    device = SmartDevice("test_device")
    assert device.brightness == 0

    device.set_brightness(50)
    assert device.brightness == 50

    device.set_brightness(100)
    assert device.brightness == 100


def test_power_command() -> None:
    """Test the PowerCommand class."""
    device = SmartDevice("test_device")
    assert not device.is_on

    # Turn on
    cmd = PowerCommand(device, True)
    cmd.execute()
    assert device.is_on

    # Undo (turn off)
    cmd.undo()
    assert not device.is_on

    # Turn off when already off
    cmd = PowerCommand(device, False)
    cmd.execute()
    assert not device.is_on

    # Undo (should stay off since it was off before)
    cmd.undo()
    assert not device.is_on


def test_temperature_command() -> None:
    """Test the SetTemperatureCommand class."""
    device = SmartDevice("test_device")
    assert device.temperature == 20

    # Set temperature to 25
    cmd = SetTemperatureCommand(device, 25)
    cmd.execute()
    assert device.temperature == 25

    # Undo (back to 20)
    cmd.undo()
    assert device.temperature == 20

    # Change temperature multiple times
    cmd1 = SetTemperatureCommand(device, 22)
    cmd1.execute()
    assert device.temperature == 22

    cmd2 = SetTemperatureCommand(device, 18)
    cmd2.execute()
    assert device.temperature == 18

    # Undo in reverse order
    cmd2.undo()
    assert device.temperature == 22
    cmd1.undo()
    assert device.temperature == 20


def test_scene_command() -> None:
    """Test the SceneCommand class."""
    light = SmartDevice("light")
    thermostat = SmartDevice("thermostat")

    # Create a scene that turns on light and sets temperature
    scene = SceneCommand()
    scene.add_command(PowerCommand(light, True))
    scene.add_command(SetTemperatureCommand(thermostat, 23))

    # Execute scene
    scene.execute()
    assert light.is_on
    assert thermostat.temperature == 23

    # Undo scene (should undo in reverse order)
    scene.undo()
    assert light.is_on is False
    assert thermostat.temperature == 20

    # Test clone method
    scene_clone = scene.clone()
    scene_clone.execute()
    assert light.is_on
    assert thermostat.temperature == 23


def test_home_automation_system() -> None:
    """Test the HomeAutomationSystem class."""
    light = SmartDevice("light")
    thermostat = SmartDevice("thermostat")
    home = HomeAutomationSystem()

    # Test execute command
    home.execute_command(PowerCommand(light, True))
    assert light.is_on

    # Test undo
    home.undo_last()
    assert not light.is_on

    # Test scene creation and activation
    scene = SceneCommand()
    scene.add_command(PowerCommand(light, True))
    scene.add_command(SetTemperatureCommand(thermostat, 23))

    home.create_scene("evening", scene)
    home.activate_scene("evening")
    assert light.is_on
    assert thermostat.temperature == 23

    # Test non-existent scene
    original_temp = thermostat.temperature
    light.power(False)  # turn off light manually
    home.activate_scene("non_existent")
    assert not light.is_on  # should remain off
    assert thermostat.temperature == original_temp  # should remain unchanged

    # Test undoing scene activation
    home.undo_last()  # undo evening scene
    assert not light.is_on
    assert thermostat.temperature == 20

    # Test multiple undos when history is empty
    home.undo_last()  # should do nothing as history is empty
    home.undo_last()  # should do nothing as history is empty
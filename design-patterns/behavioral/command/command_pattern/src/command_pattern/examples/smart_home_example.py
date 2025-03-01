"""
Example usage of the command pattern for smart home automation.

This example demonstrates how to use the command pattern to implement
a smart home system with scenes and device control.
"""

from icecream import ic

from command_pattern.command import (
    HomeAutomationSystem,
    PowerCommand,
    SceneCommand,
    SetTemperatureCommand,
    SmartDevice,
)


def print_device_states(
    living_room_light: SmartDevice,
    kitchen_light: SmartDevice,
    bedroom_light: SmartDevice,
    thermostat: SmartDevice,
) -> None:
    """Print the current state of all devices."""
    ic(f"  {living_room_light.id}: {'ON' if living_room_light.is_on else 'OFF'}")
    ic(f"  {kitchen_light.id}: {'ON' if kitchen_light.is_on else 'OFF'}")
    ic(f"  {bedroom_light.id}: {'ON' if bedroom_light.is_on else 'OFF'}")
    ic(f"  {thermostat.id}: {thermostat.temperature}°C")


def create_scenes(
    home: HomeAutomationSystem,
    living_room_light: SmartDevice,
    kitchen_light: SmartDevice,
    bedroom_light: SmartDevice,
    thermostat: SmartDevice,
) -> None:
    """Create different scenes for the home automation system."""
    ic("Creating scenes:")
    
    # Create "Morning" scene
    morning_scene = SceneCommand()
    morning_scene.add_command(PowerCommand(living_room_light, True))
    morning_scene.add_command(PowerCommand(kitchen_light, True))
    morning_scene.add_command(PowerCommand(bedroom_light, False))
    morning_scene.add_command(SetTemperatureCommand(thermostat, 21))
    home.create_scene("Morning", morning_scene)
    ic("  'Morning' scene created")
    
    # Create "Evening" scene
    evening_scene = SceneCommand()
    evening_scene.add_command(PowerCommand(living_room_light, True))
    evening_scene.add_command(PowerCommand(kitchen_light, False))
    evening_scene.add_command(PowerCommand(bedroom_light, False))
    evening_scene.add_command(SetTemperatureCommand(thermostat, 20))
    home.create_scene("Evening", evening_scene)
    ic("  'Evening' scene created")
    
    # Create "Night" scene
    night_scene = SceneCommand()
    night_scene.add_command(PowerCommand(living_room_light, False))
    night_scene.add_command(PowerCommand(kitchen_light, False))
    night_scene.add_command(PowerCommand(bedroom_light, True))
    night_scene.add_command(SetTemperatureCommand(thermostat, 18))
    home.create_scene("Night", night_scene)
    ic("  'Night' scene created")


def main() -> None:
    """Run the smart home automation example."""
    # Configure icecream
    ic.configureOutput(prefix="[Smart Home] ")
    
    # Create smart devices
    living_room_light = SmartDevice("Living Room Light")
    kitchen_light = SmartDevice("Kitchen Light")
    bedroom_light = SmartDevice("Bedroom Light")
    thermostat = SmartDevice("Main Thermostat")
    
    # Create home automation system
    home = HomeAutomationSystem()
    
    ic("Command Pattern - Smart Home Automation Example")
    ic("----------------------------------------------")
    ic("Initial device states:")
    print_device_states(living_room_light, kitchen_light, bedroom_light, thermostat)
    
    # Example 1: Individual commands
    ic("Executing individual commands:")
    ic("  Turning on Living Room Light...")
    home.execute_command(PowerCommand(living_room_light, True))
    ic("  Setting thermostat to 22°C...")
    home.execute_command(SetTemperatureCommand(thermostat, 22))
    
    ic("Current device states:")
    print_device_states(living_room_light, kitchen_light, bedroom_light, thermostat)
    
    # Example 2: Creating and activating scenes
    create_scenes(home, living_room_light, kitchen_light, bedroom_light, thermostat)
    
    # Activate "Evening" scene
    ic("Activating 'Evening' scene...")
    home.activate_scene("Evening")
    
    ic("Current device states:")
    print_device_states(living_room_light, kitchen_light, bedroom_light, thermostat)
    
    # Adjust temperature manually
    ic("Adjusting temperature manually to 22°C...")
    home.execute_command(SetTemperatureCommand(thermostat, 22))
    ic(f"  {thermostat.id}: {thermostat.temperature}°C")
    
    # Demonstrate undo
    ic("Undo last operation (temperature adjustment)...")
    home.undo_last()
    ic(f"  {thermostat.id}: {thermostat.temperature}°C")
    
    # Activate "Night" scene
    ic("Activating 'Night' scene...")
    home.activate_scene("Night")
    
    ic("Final device states:")
    print_device_states(living_room_light, kitchen_light, bedroom_light, thermostat)
    
    ic("Smart home automation operations completed.")


if __name__ == "__main__":
    main()
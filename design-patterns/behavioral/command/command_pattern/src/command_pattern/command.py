"""
Command Pattern Implementation.

This module provides a comprehensive implementation of the Command design pattern
including document editing and smart home automation examples.
"""

import abc
from dataclasses import dataclass, field
from typing import Generic, TypeVar


class Command(abc.ABC):
    """
    Abstract base class defining the interface for all concrete commands.

    This is the key piece of the Command pattern, allowing us to treat
    all commands uniformly and store them for undo/redo operations.
    """

    @abc.abstractmethod
    def execute(self) -> None:
        """Performs the command."""
        pass

    @abc.abstractmethod
    def undo(self) -> None:
        """Reverses the effect of the command."""
        pass

    @abc.abstractmethod
    def clone(self) -> "Command":
        """Creates a deep copy of the command."""
        pass


@dataclass
class Document:
    """Document class that commands will modify."""

    content: str = ""

    def insert(self, text: str, position: int) -> None:
        """Insert text at the specified position."""
        self.content = self.content[:position] + text + self.content[position:]

    def erase(self, position: int, length: int) -> None:
        """Erase text starting at position with specified length."""
        self.content = self.content[:position] + self.content[position + length:]


@dataclass
class InsertCommand(Command):
    """Concrete command for inserting text."""

    document: Document
    text: str
    position: int

    def execute(self) -> None:
        """Execute the insert command."""
        self.document.insert(self.text, self.position)

    def undo(self) -> None:
        """Undo the insert command by erasing the inserted text."""
        self.document.erase(self.position, len(self.text))

    def clone(self) -> "InsertCommand":
        """Create a deep copy of this command."""
        return InsertCommand(
            document=self.document,
            text=self.text,
            position=self.position
        )


@dataclass
class EraseCommand(Command):
    """Concrete command for erasing text."""

    document: Document
    position: int
    length: int
    erased_text: str = field(init=False, default="")

    def __post_init__(self) -> None:
        """Initialize the erased_text field after creation."""
        self.erased_text = self.document.content[self.position:self.position + self.length]

    def execute(self) -> None:
        """Execute the erase command."""
        # Save text before erasing if we haven't already
        if not self.erased_text:
            self.erased_text = self.document.content[self.position:self.position + self.length]
        self.document.erase(self.position, self.length)

    def undo(self) -> None:
        """Undo the erase command by inserting the erased text."""
        self.document.insert(self.erased_text, self.position)

    def clone(self) -> "EraseCommand":
        """Create a deep copy of this command."""
        cmd = EraseCommand(
            document=self.document,
            position=self.position,
            length=self.length
        )
        cmd.erased_text = self.erased_text
        return cmd


T = TypeVar("T", bound=Command)


class CommandStack(Generic[T]):
    """Stack of commands for undo/redo operations."""

    def __init__(self) -> None:
        """Initialize an empty command stack."""
        self._stack: list[T] = []

    def push(self, command: T) -> None:
        """Push a command onto the stack."""
        self._stack.append(command)

    def pop(self) -> T | None:
        """Pop a command from the stack if not empty."""
        if not self.is_empty():
            return self._stack.pop()
        return None

    def peek(self) -> T | None:
        """Peek at the top command without popping it."""
        if not self.is_empty():
            return self._stack[-1]
        return None

    def is_empty(self) -> bool:
        """Check if the stack is empty."""
        return len(self._stack) == 0

    def clear(self) -> None:
        """Clear all commands from the stack."""
        self._stack.clear()


@dataclass
class DocumentEditor:
    """
    Command invoker class that maintains command history.

    This class demonstrates how commands can be treated as objects
    and provides undo/redo functionality.
    """

    document: Document
    undo_stack: CommandStack[Command] = field(default_factory=CommandStack)
    redo_stack: CommandStack[Command] = field(default_factory=CommandStack)

    def execute_command(self, command: Command) -> None:
        """Execute a command and add it to the undo stack."""
        command.execute()
        self.undo_stack.push(command)
        # Clear redo stack as a new command breaks the redo chain
        self.redo_stack.clear()

    def undo(self) -> None:
        """Undo the last command."""
        command = self.undo_stack.pop()
        if command:
            command.undo()
            self.redo_stack.push(command)

    def redo(self) -> None:
        """Redo the last undone command."""
        command = self.redo_stack.pop()
        if command:
            command.execute()
            self.undo_stack.push(command)


@dataclass
class SmartDevice:
    """Smart device class for home automation example."""

    id: str
    brightness: int = 0
    temperature: int = 20
    is_on: bool = False

    def power(self, state: bool) -> None:
        """Set the power state of the device."""
        self.is_on = state

    def set_brightness(self, level: int) -> None:
        """Set the brightness level of the device."""
        self.brightness = level

    def set_temperature(self, temp: int) -> None:
        """Set the temperature of the device."""
        self.temperature = temp


@dataclass
class PowerCommand(Command):
    """Concrete command for controlling device power."""

    device: SmartDevice
    new_state: bool
    previous_state: bool = field(init=False)

    def __post_init__(self) -> None:
        """Initialize previous_state after creation."""
        self.previous_state = self.device.is_on

    def execute(self) -> None:
        """Execute the power command."""
        self.device.power(self.new_state)

    def undo(self) -> None:
        """Undo the power command by restoring previous state."""
        self.device.power(self.previous_state)

    def clone(self) -> "PowerCommand":
        """Create a deep copy of this command."""
        cmd = PowerCommand(device=self.device, new_state=self.new_state)
        cmd.previous_state = self.previous_state
        return cmd


@dataclass
class SetTemperatureCommand(Command):
    """Concrete command for setting device temperature."""

    device: SmartDevice
    new_temp: int
    previous_temp: int = field(init=False)

    def __post_init__(self) -> None:
        """Initialize previous_temp after creation."""
        self.previous_temp = self.device.temperature

    def execute(self) -> None:
        """Execute the temperature command."""
        self.device.set_temperature(self.new_temp)

    def undo(self) -> None:
        """Undo the temperature command by restoring previous temperature."""
        self.device.set_temperature(self.previous_temp)

    def clone(self) -> "SetTemperatureCommand":
        """Create a deep copy of this command."""
        cmd = SetTemperatureCommand(device=self.device, new_temp=self.new_temp)
        cmd.previous_temp = self.previous_temp
        return cmd


class SceneCommand(Command):
    """Composite command for scene setting."""

    def __init__(self) -> None:
        """Initialize with an empty list of commands."""
        self.commands: list[Command] = []

    def add_command(self, command: Command) -> None:
        """Add a command to the scene."""
        self.commands.append(command)

    def execute(self) -> None:
        """Execute all commands in the scene."""
        for cmd in self.commands:
            cmd.execute()

    def undo(self) -> None:
        """Undo all commands in the scene in reverse order."""
        for cmd in reversed(self.commands):
            cmd.undo()

    def clone(self) -> "SceneCommand":
        """Create a deep copy of this command."""
        new_scene = SceneCommand()
        for cmd in self.commands:
            new_scene.add_command(cmd.clone())
        return new_scene


class HomeAutomationSystem:
    """Home automation system that uses commands to control devices."""

    def __init__(self) -> None:
        """Initialize with empty history and scenes dictionary."""
        self.history: CommandStack[Command] = CommandStack()
        self.scenes: dict[str, SceneCommand] = {}

    def execute_command(self, command: Command) -> None:
        """Execute a command and add it to history."""
        command.execute()
        self.history.push(command)

    def undo_last(self) -> None:
        """Undo the last command."""
        command = self.history.pop()
        if command:
            command.undo()

    def create_scene(self, name: str, scene: SceneCommand) -> None:
        """Create and store a named scene."""
        self.scenes[name] = scene

    def activate_scene(self, name: str) -> None:
        """Activate a named scene if it exists."""
        if name in self.scenes:
            # Clone the scene instead of using the original
            self.execute_command(self.scenes[name].clone())
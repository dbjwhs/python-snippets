"""
Basic example of the Adapter design pattern.

This example demonstrates a simple adapter pattern implementation
with a real-world analogy of power adapters.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto

from icecream import ic


class PowerType(Enum):
    """Types of power sources."""
    EUROPEAN_SOCKET = auto()
    US_SOCKET = auto()
    UK_SOCKET = auto()
    USB_C = auto()
    USB_A = auto()


class OutputVoltage(Enum):
    """Output voltage types."""
    V_5 = 5
    V_12 = 12
    V_110 = 110
    V_220 = 220


# Target interface
class DevicePowerSupply(ABC):
    """Abstract interface for device power supplies."""

    @abstractmethod
    def provide_power(self) -> bool:
        """Provide power to a device."""
        pass

    @abstractmethod
    def get_voltage(self) -> OutputVoltage:
        """Get the output voltage."""
        pass


# Concrete implementations representing different power sources
@dataclass
class EuropeanSocket:
    """European wall socket power source."""

    voltage: OutputVoltage = OutputVoltage.V_220

    def connect_european_plug(self) -> bool:
        """Connect using European plug."""
        ic("Connected to European socket (220V)")
        return True


@dataclass
class USSocket:
    """US wall socket power source."""

    voltage: OutputVoltage = OutputVoltage.V_110

    def connect_us_plug(self) -> bool:
        """Connect using US plug."""
        ic("Connected to US socket (110V)")
        return True


@dataclass
class UsbCPort:
    """USB-C port power source."""

    voltage: OutputVoltage = OutputVoltage.V_5
    supports_power_delivery: bool = True

    def connect_usb_c(self) -> bool:
        """Connect using USB-C."""
        ic(f"Connected to USB-C port (5V{', with Power Delivery' if self.supports_power_delivery else ''})")
        return True


# Adapters to standardize interface
class EuropeanSocketAdapter(DevicePowerSupply):
    """Adapter for European socket to standard power supply interface."""

    def __init__(self) -> None:
        """Initialize the adapter."""
        self._socket = EuropeanSocket()

    def provide_power(self) -> bool:
        """Provide power through the European socket."""
        return self._socket.connect_european_plug()

    def get_voltage(self) -> OutputVoltage:
        """Get the output voltage."""
        return self._socket.voltage


class USSocketAdapter(DevicePowerSupply):
    """Adapter for US socket to standard power supply interface."""

    def __init__(self) -> None:
        """Initialize the adapter."""
        self._socket = USSocket()

    def provide_power(self) -> bool:
        """Provide power through the US socket."""
        return self._socket.connect_us_plug()

    def get_voltage(self) -> OutputVoltage:
        """Get the output voltage."""
        return self._socket.voltage


class UsbCAdapter(DevicePowerSupply):
    """Adapter for USB-C port to standard power supply interface."""

    def __init__(self, supports_pd: bool = True) -> None:
        """Initialize the adapter with Power Delivery support option."""
        self._port = UsbCPort(supports_power_delivery=supports_pd)

    def provide_power(self) -> bool:
        """Provide power through the USB-C port."""
        return self._port.connect_usb_c()

    def get_voltage(self) -> OutputVoltage:
        """Get the output voltage."""
        return self._port.voltage


# Client code
@dataclass
class ElectronicDevice:
    """A generic electronic device that needs power."""

    name: str
    required_voltage: OutputVoltage

    def charge_with(self, power_supply: DevicePowerSupply) -> bool:
        """Charge the device using the provided power supply."""
        # Get power
        power_connected = power_supply.provide_power()
        if not power_connected:
            ic(f"Failed to connect {self.name} to power supply")
            return False

        # Check voltage compatibility
        supply_voltage = power_supply.get_voltage()
        if supply_voltage != self.required_voltage:
            ic(f"Warning: {self.name} requires {self.required_voltage.value}V "
               f"but power supply provides {supply_voltage.value}V")
            ic("Using voltage converter...")

        ic(f"Successfully charging {self.name}")
        return True


def demonstrate_power_adapters() -> None:
    """Demonstrate the use of power adapters."""
    ic("Power Adapter Pattern Demonstration")
    ic("-" * 40)

    # Create devices with different power requirements
    devices: list[ElectronicDevice] = [
        ElectronicDevice("Laptop", OutputVoltage.V_220),
        ElectronicDevice("Phone", OutputVoltage.V_5),
        ElectronicDevice("Hair Dryer", OutputVoltage.V_110)
    ]

    # Create different power supply adapters
    power_supplies: list[DevicePowerSupply] = [
        EuropeanSocketAdapter(),
        USSocketAdapter(),
        UsbCAdapter()
    ]

    # Test each device with each power supply
    for device in devices:
        ic(f"\nTesting {device.name} (requires {device.required_voltage.value}V):")
        for power_supply in power_supplies:
            device.charge_with(power_supply)

    ic("\nPower adapter demonstration completed")


if __name__ == "__main__":
    demonstrate_power_adapters()

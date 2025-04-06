"""
Tests for the Adapter pattern implementation.
"""

from adapter_pattern.adapter import APFSAdapter, FAT32Adapter, FileOperationsManager, IFileSystem


class TestFileSystemAdapters:
    """Test cases for file system adapters."""

    def test_apfs_adapter_creation(self) -> None:
        """Test that APFS adapter can be created."""
        adapter = APFSAdapter()
        assert isinstance(adapter, IFileSystem)
        assert adapter.supports_symlinks() is True
        assert adapter.supports_permissions() is True

    def test_fat32_adapter_creation(self) -> None:
        """Test that FAT32 adapter can be created."""
        adapter = FAT32Adapter()
        assert isinstance(adapter, IFileSystem)
        assert adapter.supports_symlinks() is False
        assert adapter.supports_permissions() is False

    def test_apfs_sanitizes_filenames(self) -> None:
        """Test that APFS adapter sanitizes filenames."""
        adapter = APFSAdapter()

        # Test handling hidden files (leading dots)
        result = adapter.create_directory(".hidden")
        assert result is True

        # Test handling special characters
        result = adapter.copy_file("file:with/special\0chars.txt", "destination.txt")
        assert result is True

    def test_fat32_sanitizes_filenames(self) -> None:
        """Test that FAT32 adapter sanitizes filenames."""
        adapter = FAT32Adapter()

        # Test handling invalid windows characters
        result = adapter.create_directory("test<file>name*.txt")
        assert result is True

        # Test handling spaces and special characters
        result = adapter.copy_file("my file name: special * chars?.txt", "dest.txt")
        assert result is True

    def test_empty_path_handling(self) -> None:
        """Test handling of empty paths."""
        apfs_adapter = APFSAdapter()
        fat32_adapter = FAT32Adapter()

        assert apfs_adapter.create_directory("") is False
        assert fat32_adapter.create_directory("") is False

    def test_file_operations_manager(self) -> None:
        """Test that file operations manager works with both adapters."""
        # Test with APFS adapter
        apfs_manager = FileOperationsManager(APFSAdapter())
        assert apfs_manager.file_system.supports_symlinks() is True

        # Test with FAT32 adapter
        fat32_manager = FileOperationsManager(FAT32Adapter())
        assert fat32_manager.file_system.supports_symlinks() is False


from adapter_pattern.examples.basic_adapter_example import (
    DevicePowerSupply,
    ElectronicDevice,
    EuropeanSocketAdapter,
    OutputVoltage,
    UsbCAdapter,
    USSocketAdapter,
)


class TestPowerAdapters:
    """Test cases for power adapters."""

    def test_power_adapters_creation(self) -> None:
        """Test that power adapters can be created."""
        european = EuropeanSocketAdapter()
        us = USSocketAdapter()
        usb_c = UsbCAdapter()

        assert isinstance(european, DevicePowerSupply)
        assert isinstance(us, DevicePowerSupply)
        assert isinstance(usb_c, DevicePowerSupply)

    def test_power_adapters_voltages(self) -> None:
        """Test that power adapters report correct voltages."""
        european = EuropeanSocketAdapter()
        us = USSocketAdapter()
        usb_c = UsbCAdapter()

        assert european.get_voltage() == OutputVoltage.V_220
        assert us.get_voltage() == OutputVoltage.V_110
        assert usb_c.get_voltage() == OutputVoltage.V_5

    def test_device_charging(self) -> None:
        """Test that devices can charge with adapters."""
        laptop = ElectronicDevice("Laptop", OutputVoltage.V_220)
        phone = ElectronicDevice("Phone", OutputVoltage.V_5)

        european = EuropeanSocketAdapter()
        usb_c = UsbCAdapter()

        # Matching voltage requirements
        assert laptop.charge_with(european) is True
        assert phone.charge_with(usb_c) is True

        # Mismatched voltage (still works but with warning)
        assert laptop.charge_with(usb_c) is True

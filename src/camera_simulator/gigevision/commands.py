from enum import Enum

from pydantic import BaseModel, computed_field

from src.camera_simulator.gigevision.camera_register import CameraRegister


class PackageType(bytes, Enum):
    ACK = b"\x00\x00"
    CMD = b"\x42"
    ERROR = b"\x80"
    UNKNOWN = b"\x8f"


class CommandType(bytes, Enum):
    DISCOVERY_CMD = b"\x00\x02"
    DISCOVERY_ACK = b"\x00\x03"
    FORCEIP_CMD = b"\x00\x04"
    FORCEIP_ACK = b"\x00\x05"
    PACKETRESEND_CMD = b"\x00\x40"
    READREG_CMD = b"\x00\x80"
    READREG_ACK = b"\x00\x81"
    WRITEREG_CMD = b"\x00\x82"
    WRITEREG_ACK = b"\x00\x83"
    READMEM_CMD = b"\x00\x84"
    READMEM_ACK = b"\x00\x85"
    WRITEMEM_CMD = b"\x00\x86"
    WRITEMEM_ACK = b"\x00\x87"
    PENDING_ACK = b"\x00\x89"


class DiscoveryAck(BaseModel):
    register: CameraRegister

    model_config = {"arbitrary_types_allowed": True}

    @computed_field  # type: ignore[prop-decorator]
    @property
    def payload(self) -> bytes:
        major_version = self.register.get("MajorVersion")
        minor_version = self.register.get("MinorVersion")
        device_mode = self.register.get("Device_Mode")
        mac_high = self.register.get("Device_MAC_address_High_Network_interface_0")
        mac_low = self.register.get("Device_MAC_address_Low_Network_interface_0")
        vendor_name = self.register.get("VendorName")
        model_name = self.register.get("ModelName")
        user_defined_name = self.register.get("UserDefinedName")
        serial_number = self.register.get("Serial_number")
        manufacturer_info = self.register.get("Manufacturer_specific_information")
        device_version = self.register.get("Device_version")
        current_ip = self.register.get("Current_IP_address_Network_interface_0")
        current_netmask = self.register.get("Current_subnet_mask_Network_interface_0")

        if not all(
            [
                major_version,
                minor_version,
                device_mode,
                mac_high,
                mac_low,
                vendor_name,
                model_name,
                user_defined_name,
                serial_number,
                manufacturer_info,
                device_version,
                current_ip,
                current_netmask,
            ]
        ):
            raise ValueError("One or more required registers are missing.")

        return (
            PackageType.ACK
            + CommandType.DISCOVERY_ACK
            + major_version.to_bytes()
            + minor_version.to_bytes()
            + device_mode.to_bytes()
            + mac_high.to_bytes()
            + mac_low.to_bytes()
            + current_ip.to_bytes()
            + current_netmask.to_bytes()
            + bytes(4)
            + bytes(4)
            + bytes(12)
            + current_ip.to_bytes()
            + bytes(12)
            + current_netmask.to_bytes()
            + bytes(12)
            + bytes(4)
            + vendor_name.to_bytes()
            + model_name.to_bytes()
            + device_version.to_bytes()
            + manufacturer_info.to_bytes()
            + serial_number.to_bytes()
            + user_defined_name.to_bytes()
        )


class ReadRegisterAck(BaseModel):
    register_address: int
    value: int

    def to_bytes(self) -> bytes:
        return (
            PackageType.ACK
            + CommandType.READREG_ACK
            + self.register_address.to_bytes(4, byteorder="big")
            + self.value.to_bytes(4, byteorder="big")
        )


class WriteRegisterAck(BaseModel):
    register_address: int

    def to_bytes(self) -> bytes:
        return (
            PackageType.ACK
            + CommandType.WRITEREG_ACK
            + self.register_address.to_bytes(4, byteorder="big")
        )


class ReadMemoryAck(BaseModel):
    address: int
    data: bytes

    model_config = {"arbitrary_types_allowed": True}

    def to_bytes(self) -> bytes:
        return (
            PackageType.ACK
            + CommandType.READMEM_ACK
            + self.address.to_bytes(4, byteorder="big")
            + len(self.data).to_bytes(4, byteorder="big")
            + self.data
        )


class WriteMemoryAck(BaseModel):
    address: int
    bytes_written: int

    def to_bytes(self) -> bytes:
        return (
            PackageType.ACK
            + CommandType.WRITEMEM_ACK
            + self.address.to_bytes(4, byteorder="big")
            + self.bytes_written.to_bytes(4, byteorder="big")
        )

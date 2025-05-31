from typing import Any, Literal

from pydantic import BaseModel

from src.camera_simulator.gigevision.config_parser import CameraConfig


class RegisterInfo(BaseModel):
    name: str
    address: int
    size: int
    description: str = ""
    value: int | bytes = 0

    model_config = {"arbitrary_types_allowed": True}

    def __str__(self) -> str:
        return f"{self.name} (0x{self.address:04x}): [{self.size} bytes]"

    def __repr__(self) -> str:
        return f"RegisterInfo(name={self.name}, address=0x{self.address:04x}, size={self.size}, value={self.value})"

    def to_bytes(self, byteorder: Literal["big", "little"] = "big") -> bytes:
        if isinstance(self.value, bytes):
            return self.value.ljust(self.size, b"\x00")[: self.size]
        return self.value.to_bytes(self.size, byteorder=byteorder)


class CameraRegister(BaseModel):
    camera_config: CameraConfig
    registers: list[RegisterInfo] = []

    model_config = {"arbitrary_types_allowed": True}

    def model_post_init(self, __context: Any) -> None:
        self.registers = [
            RegisterInfo(name="MajorVersion", address=0x0000, size=2),
            RegisterInfo(name="MinorVersion", address=0x0002, size=2),
            RegisterInfo(name="Device_Mode", address=0x0004, size=4),
            RegisterInfo(
                name="Device_MAC_address_High_Network_interface_0",
                address=0x0008,
                size=3,
            ),
            RegisterInfo(
                name="Device_MAC_address_Low_Network_interface_0",
                address=0x000C,
                size=3,
            ),
            RegisterInfo(
                name="Supported_IP_configuration_Network_interface_0",
                address=0x0010,
                size=4,
            ),
            RegisterInfo(
                name="Current_IP_configuration_procedure_Network_interface_0",
                address=0x0014,
                size=4,
            ),
            RegisterInfo(
                name="Current_IP_address_Network_interface_0", address=0x0024, size=4
            ),
            RegisterInfo(
                name="Current_subnet_mask_Network_interface_0", address=0x0034, size=4
            ),
            RegisterInfo(
                name="Current_default_Gateway_Network_interface_0",
                address=0x0044,
                size=4,
            ),
            RegisterInfo(name="VendorName", address=0x0048, size=32),
            RegisterInfo(name="ModelName", address=0x0068, size=32),
            RegisterInfo(name="Device_version", address=0x0088, size=32),
            RegisterInfo(
                name="Manufacturer_specific_information", address=0x00A8, size=48
            ),
            RegisterInfo(name="Serial_number", address=0x00D8, size=16),
            RegisterInfo(name="UserDefinedName", address=0x00E8, size=16),
            RegisterInfo(
                name="XML_Device_Description_File_First_URL", address=0x0200, size=512
            ),
            RegisterInfo(
                name="XML_Device_Description_File_Second_URL", address=0x0400, size=512
            ),
            RegisterInfo(name="Number_of_network_interfaces", address=0x0600, size=4),
            RegisterInfo(
                name="Persistent_IP_address_Network_interface_0", address=0x064C, size=4
            ),
            RegisterInfo(
                name="Persistent_subnet_mask_Network_interface_0",
                address=0x065C,
                size=4,
            ),
            RegisterInfo(
                name="Persistent_default_gateway_Network_interface_0",
                address=0x066C,
                size=4,
            ),
            RegisterInfo(name="Link_Speed_Network_interface_0", address=0x0670, size=4),
            RegisterInfo(
                name="MAC_address_High_Network_interface_1", address=0x0680, size=4
            ),
            RegisterInfo(
                name="MAC_address_Low_Network_interface_1", address=0x0684, size=4
            ),
            RegisterInfo(
                name="Supported_IP_configuration_Network_interface_1",
                address=0x0688,
                size=4,
            ),
            RegisterInfo(
                name="Current_IP_configuration_procedure_Network_interface_1",
                address=0x068C,
                size=4,
            ),
            RegisterInfo(
                name="Current_IP_address_Network_interface_1", address=0x069C, size=4
            ),
            RegisterInfo(
                name="Current_subnet_mask_Network_interface_1", address=0x06AC, size=4
            ),
            RegisterInfo(
                name="Current_default_gateway_Network_interface_1",
                address=0x06BC,
                size=4,
            ),
            RegisterInfo(
                name="Persistent_IP_address_Network_interface_1", address=0x06CC, size=4
            ),
            RegisterInfo(
                name="Persistent_subnet_mask_Network_interface_1",
                address=0x06DC,
                size=4,
            ),
            RegisterInfo(
                name="Persistent_default_gateway_Network_interface_1",
                address=0x06EC,
                size=4,
            ),
            RegisterInfo(name="Link_Speed_Network_interface_1", address=0x06F0, size=4),
            RegisterInfo(
                name="MAC_address_High_Network_interface_2", address=0x0700, size=4
            ),
            RegisterInfo(
                name="MAC_address_Low_Network_interface_2", address=0x0704, size=4
            ),
            RegisterInfo(
                name="Supported_IP_configuration_Network_interface_2",
                address=0x0708,
                size=4,
            ),
            RegisterInfo(
                name="Current_IP_configuration_procedure_Network_interface_2",
                address=0x070C,
                size=4,
            ),
            RegisterInfo(
                name="Current_IP_address_Network_interface_2", address=0x071C, size=4
            ),
            RegisterInfo(
                name="Current_subnet_mask_Network_interface_2", address=0x072C, size=4
            ),
            RegisterInfo(
                name="Current_default_gateway_Network_interface_2",
                address=0x073C,
                size=4,
            ),
            RegisterInfo(
                name="Persistent_IP_address_Network_interface_2", address=0x074C, size=4
            ),
            RegisterInfo(
                name="Persistent_subnet_mask_Network_interface_2",
                address=0x075C,
                size=4,
            ),
            RegisterInfo(
                name="Persistent_default_gateway_Network_interface_2",
                address=0x076C,
                size=4,
            ),
            RegisterInfo(name="Link_Speed_Network_interface_2", address=0x0770, size=4),
            RegisterInfo(
                name="MAC_address_High_Network_interface_3", address=0x0780, size=4
            ),
            RegisterInfo(
                name="MAC_address_Low_Network_interface_3", address=0x0784, size=4
            ),
            RegisterInfo(
                name="Supported_IP_configuration_Network_interface_3",
                address=0x0788,
                size=4,
            ),
            RegisterInfo(
                name="Current_IP_configuration_procedure_Network_interface_3",
                address=0x078C,
                size=4,
            ),
            RegisterInfo(
                name="Current_IP_address_Network_interface_3", address=0x079C, size=4
            ),
            RegisterInfo(
                name="Current_subnet_mask_Network_interface_3", address=0x07AC, size=4
            ),
            RegisterInfo(
                name="Current_default_gateway_Network_interface_3",
                address=0x07BC,
                size=4,
            ),
            RegisterInfo(
                name="Persistent_IP_address_Network_interface_3", address=0x07CC, size=4
            ),
            RegisterInfo(
                name="Persistent_subnet_mask_Network_interface_3",
                address=0x07DC,
                size=4,
            ),
            RegisterInfo(
                name="Persistent_default_gateway_Network_interface_3",
                address=0x07EC,
                size=4,
            ),
            RegisterInfo(name="Link_Speed_Network_interface_3", address=0x07F0, size=4),
            RegisterInfo(name="Number_of_Message_channels", address=0x0900, size=4),
            RegisterInfo(name="Number_of_Stream_channels", address=0x0904, size=4),
            RegisterInfo(name="Number_of_Action_Signals", address=0x0908, size=4),
            RegisterInfo(name="Action_Device_Key", address=0x090C, size=4),
            RegisterInfo(name="Stream_channels_Capability", address=0x092C, size=4),
            RegisterInfo(name="Message_channel_Capability", address=0x0930, size=4),
            RegisterInfo(name="GVCP_Capability", address=0x0934, size=4),
            RegisterInfo(name="Heartbeat_timeout", address=0x0938, size=4),
            RegisterInfo(name="Timestamp_tick_frequency_High", address=0x093C, size=4),
            RegisterInfo(name="Timestamp_tick_frequency_Low", address=0x0940, size=4),
            RegisterInfo(name="Timestamp_control", address=0x0944, size=4),
            RegisterInfo(name="Timestamp_value_latched_High", address=0x0948, size=4),
            RegisterInfo(name="Timestamp_value_latched_Low", address=0x094C, size=4),
            RegisterInfo(name="Discovery_ACK_delay", address=0x0950, size=4),
            RegisterInfo(name="GVCP_Configuration", address=0x0954, size=4),
            RegisterInfo(name="Pending_Timeout", address=0x0958, size=4),
            RegisterInfo(name="Control_Switchover_Key", address=0x095C, size=4),
            RegisterInfo(name="Control_Channel_Privilege", address=0x0A00, size=4),
            RegisterInfo(name="Primary_Application_Port", address=0x0A04, size=4),
            RegisterInfo(name="Primary_Application_IP_address", address=0x0A14, size=4),
            RegisterInfo(name="MCP", address=0x0B00, size=4),
            RegisterInfo(name="MCDA", address=0x0B10, size=4),
            RegisterInfo(name="MCTT", address=0x0B14, size=4),
            RegisterInfo(name="MCRC", address=0x0B18, size=4),
            RegisterInfo(name="MCSP", address=0x0B1C, size=4),
            RegisterInfo(name="Stream_Channel_Port_0", address=0x0D00, size=4),
            RegisterInfo(name="Stream_Channel_Packet_Size_0", address=0x0D04, size=4),
            RegisterInfo(name="SCPD0", address=0x0D08, size=4),
            RegisterInfo(
                name="Stream_Channel_Destination_Address_0", address=0x0D18, size=4
            ),
            RegisterInfo(name="SCSP0", address=0x0D1C, size=4),
            RegisterInfo(name="SCC0", address=0x0D20, size=4),
            RegisterInfo(name="SCCFG0", address=0x0D24, size=4),
            RegisterInfo(name="SCP1", address=0x0D40, size=4),
            RegisterInfo(name="SCPS1", address=0x0D44, size=4),
            RegisterInfo(name="SCPD1", address=0x0D48, size=4),
            RegisterInfo(name="SCDA1", address=0x0D58, size=4),
            RegisterInfo(name="SCSP1", address=0x0D5C, size=4),
            RegisterInfo(name="SCC1", address=0x0D60, size=4),
            RegisterInfo(name="SCCFG1", address=0x0D64, size=4),
            RegisterInfo(name="SCP511", address=0x8CC0, size=4),
            RegisterInfo(name="SCPS511", address=0x8CC4, size=4),
            RegisterInfo(name="SCPD511", address=0x8CC8, size=4),
            RegisterInfo(name="SCDA511", address=0x8CD8, size=4),
            RegisterInfo(name="SCSP511", address=0x8CDC, size=4),
            RegisterInfo(name="SCC511", address=0x8CE0, size=4),
            RegisterInfo(name="SCCFG511", address=0x8CE4, size=4),
            RegisterInfo(name="Manifest_Table", address=0x9000, size=512),
            RegisterInfo(name="ACTION_GROUP_KEY0", address=0x9800, size=4),
            RegisterInfo(name="ACTION_GROUP_MASK0", address=0x9804, size=4),
            RegisterInfo(name="ACTION_GROUP_KEY1", address=0x9810, size=4),
            RegisterInfo(name="ACTION_GROUP_MASK1", address=0x9814, size=4),
            RegisterInfo(name="ACTION_GROUP_KEY127", address=0x9FF0, size=4),
            RegisterInfo(name="ACTION_GROUP_MASK127", address=0x9FF4, size=4),
        ]
        self.set_values()
        self.set_value("Device_Mode", 0x0003)

    def get(
        self, name: str, default: RegisterInfo | None = None
    ) -> RegisterInfo | None:
        for reg in self.registers:
            if reg.name == name:
                return reg
        return default

    def get_value(self, name: str) -> int | bytes:
        reg = self.get(name)
        if reg is not None:
            return reg.value
        raise ValueError(f"Register {name} not found.")

    def get_size(self, name: str) -> int | None:
        reg = self.get(name)
        if reg is not None:
            return reg.size
        return None

    def set_value(self, name: str, value: int | bytes) -> None:
        reg = self.get(name)
        if reg is not None:
            reg.value = value
        else:
            raise ValueError(f"Register {name} not found.")

    def set_values(self) -> None:
        for name, value in self.camera_config.get("RegisterDescription", {}).items():
            try:
                if isinstance(value, str):
                    size = self.get_size(name)
                    if size is not None:
                        self.set_value(name, value.encode("utf-8").ljust(size, b"\x00"))
                    else:
                        self.set_value(name, value.encode("utf-8"))
                elif isinstance(value, int):
                    self.set_value(name, value)
            except ValueError:
                pass

import pathlib
import socket
import time
from typing import Generator

import pytest
from harvesters import core

from src.camera_simulator.gigevision.broadcast import CameraBroadcaster
from src.camera_simulator.gigevision.camera_register import CameraRegister
from src.camera_simulator.gigevision.config_parser import CameraConfig

SERVER_IP = "127.0.0.2"
SERVER_PORT = 3956
UDP_TIMEOUT = 5
TRANSPORT_LAYER_FILE = pathlib.Path(
    "/opt/mvIMPACT_Acquire/lib/x86_64/mvGenTLProducer.cti"
)


class GigEVisionClient:
    def __init__(self, transport_layer_file: pathlib.Path):
        self._transport_layer_file = transport_layer_file
        self._harvester = None

    @property
    def harvester(self):
        if not self._harvester:
            self._harvester = core.Harvester()
            self._harvester.add_cti_file(self._transport_layer_file)
        return self._harvester

    def connect(self) -> None: ...

    def disconnect(self) -> None: ...

    def find_cameras(self) -> list[str]: ...


@pytest.fixture
def gigevision_client() -> Generator[GigEVisionClient, None, None]:
    yield GigEVisionClient(TRANSPORT_LAYER_FILE)


def build_discovery_cmd() -> bytes:
    # GigE Vision DISCOVERY_CMD packet structure:
    # 2 bytes - status (0x4200 = CMD)
    # 2 bytes - command (0x0002 = DISCOVERY_CMD)
    # 2 bytes - length (0x0000, no payload)
    # 2 bytes - request ID
    status = b"\x42\x00"
    command = b"\x00\x02"
    length = b"\x00\x00"
    req_id = b"\x00\x01"
    return status + command + length + req_id


@pytest.fixture(scope="module")
def broadcaster() -> Generator[CameraBroadcaster, None, None]:
    camera_config_path = (
        pathlib.Path(__file__).parent.parent
        / "src"
        / "camera_simulator"
        / "gigevision"
        / "data"
        / "camera_config.yaml"
    )
    camera_config = CameraConfig.from_file(camera_config_path)
    camera_reg = CameraRegister(camera_config=camera_config)
    camera_reg.set_value("Device_MAC_address_High_Network_interface_0", 0x012345)
    camera_reg.set_value("Device_MAC_address_Low_Network_interface_0", 0x678910)

    b = CameraBroadcaster(ip=SERVER_IP, register=camera_reg)
    b.daemon = True
    b.start()
    # Give the thread a moment to bind and enter its receive loop
    time.sleep(0.1)

    yield b

    b.stop()
    b.join(timeout=5)


@pytest.fixture
def udp_client() -> Generator[socket.socket, None, None]:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(UDP_TIMEOUT)
        yield sock

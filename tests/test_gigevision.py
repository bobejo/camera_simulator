import pytest

from tests.conftest import (
    SERVER_IP,
    SERVER_PORT,
    build_discovery_cmd,
)


def test_gigevision_simulator(gigevision_client):
    assert gigevision_client
    assert True


@pytest.mark.usefixtures("broadcaster")
def test_discovery_cmd_returns_ack(udp_client):
    packet = build_discovery_cmd()
    udp_client.sendto(packet, (SERVER_IP, SERVER_PORT))

    data, addr = udp_client.recvfrom(4096)

    assert addr[0] == SERVER_IP
    assert len(data) >= 4


@pytest.mark.usefixtures("broadcaster")
def test_discovery_ack_command_type(udp_client):
    udp_client.sendto(build_discovery_cmd(), (SERVER_IP, SERVER_PORT))
    data, _ = udp_client.recvfrom(4096)

    status = data[0:2]
    command = data[2:4]

    assert status == b"\x00\x00"
    assert command == b"\x00\x03"  # DISCOVERY_ACK


@pytest.mark.usefixtures("broadcaster")
def test_discovery_ack_mac_address(udp_client):
    udp_client.sendto(build_discovery_cmd(), (SERVER_IP, SERVER_PORT))
    data, _ = udp_client.recvfrom(4096)

    # Payload layout (byte offsets):
    # 0:2   status
    # 2:4   command
    # 4:6   major_version  (size=2)
    # 6:8   minor_version  (size=2)
    # 8:12  device_mode    (size=4)
    # 12:15 mac_high       (size=3)
    # 15:18 mac_low        (size=3)
    mac_high = int.from_bytes(data[12:15], "big")
    mac_low = int.from_bytes(data[15:18], "big")

    assert mac_high == 0x012345
    assert mac_low == 0x678910


@pytest.mark.usefixtures("broadcaster")
def test_discovery_ack_source_ip(udp_client):
    udp_client.sendto(build_discovery_cmd(), (SERVER_IP, SERVER_PORT))
    _, addr = udp_client.recvfrom(4096)

    # Check the IP layer — the response must come from the server's bound IP
    src_ip = addr[0]

    assert src_ip == SERVER_IP

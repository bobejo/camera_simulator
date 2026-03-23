import logging
import socket
import threading
import time

from src.camera_simulator.gigevision.camera_register import CameraRegister
from src.camera_simulator.gigevision.commands import CommandType, DiscoveryAck

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CameraBroadcaster(threading.Thread):
    """
    Thread that listens and replies to a camera identification request.
    """

    def __init__(self, ip: str, register: CameraRegister):
        threading.Thread.__init__(self)
        self.ip = ip
        self.register = register
        self._stop_event = threading.Event()

    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            try:
                server_socket.bind((self.ip, 3956))
            except OSError:
                logger.error("Failed to bind on %s, trying again!", self.ip)
                time.sleep(3)
            server_socket.setblocking(False)
            server_socket.settimeout(3)

            logger.debug("Server is started")
            while not self._stop_event.is_set():
                try:
                    data, addr = server_socket.recvfrom(1024)
                    if not data:
                        continue

                    logger.debug("Got request from %s: %s", addr, data)
                    command = data[2:4]

                    if command == CommandType.DISCOVERY_CMD:
                        logger.info("Got DISCOVERY_CMD from %s", addr)
                        packet = DiscoveryAck(register=self.register).payload
                        server_socket.sendto(packet, addr)

                    elif command == CommandType.FORCEIP_CMD:
                        logger.info("Got FORCEIP_CMD from %s", addr)

                    elif command == CommandType.READREG_CMD:
                        logger.info("Got READREG_CMD from %s", addr)

                    elif command == CommandType.WRITEREG_CMD:
                        logger.info("Got WRITEREG_CMD from %s", addr)

                    elif command == CommandType.READMEM_CMD:
                        logger.info("Got READMEM_CMD from %s", addr)

                    elif command == CommandType.WRITEMEM_CMD:
                        logger.info("Got WRITEMEM_CMD from %s", addr)

                    elif command == CommandType.PACKETRESEND_CMD:
                        logger.info("Got PACKETRESEND_CMD from %s", addr)

                    else:
                        logger.info("Got unknown command from %s: %s", addr, data)

                except socket.timeout:
                    pass
                except IndexError:
                    logger.debug("Received unexpected response format")

    def stop(self) -> None:
        self._stop_event.set()

import logging
import pathlib
import signal
import sys

from src.camera_simulator.gigevision.broadcast import CameraBroadcaster
from src.camera_simulator.gigevision.camera_register import CameraRegister
from src.camera_simulator.gigevision.config_parser import CameraConfig


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(module)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    camera_config_path = pathlib.Path(__file__).parent / "data" / "camera_config.yaml"
    camera_config = CameraConfig.from_file(camera_config_path)
    camera_reg = CameraRegister(camera_config=camera_config)

    # Set MAC address since gen_tl looks for it when detecting compatible cameras
    camera_reg.set_value("Device_MAC_address_High_Network_interface_0", 0x012345)
    camera_reg.set_value("Device_MAC_address_Low_Network_interface_0", 0x678910)

    broadcaster = CameraBroadcaster(ip="127.0.0.2", register=camera_reg)

    def handle_signal(signum: int, frame: object) -> None:
        broadcaster.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    broadcaster.start()
    broadcaster.join()


if __name__ == "__main__":
    main()

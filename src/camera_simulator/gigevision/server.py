import pathlib

from src.camera_simulator.gigevision.broadcast import CameraBroadcaster
from src.camera_simulator.gigevision.camera_register import CameraRegister
from src.camera_simulator.gigevision.config_parser import CameraConfig


def main() -> None:
    camera_config_path = pathlib.Path(__file__).parent / "data" / "camera_config.yaml"
    camera_config = CameraConfig.from_file(camera_config_path)
    camera_reg = CameraRegister(camera_config=camera_config)

    # Set MAC address since gen_tl looks for it when detecting compatible cameras
    camera_reg.set_value("Device_MAC_address_High_Network_interface_0", 0x012345)
    camera_reg.set_value("Device_MAC_address_Low_Network_interface_0", 0x678910)

    broadcaster = CameraBroadcaster(ip="127.0.0.2", register=camera_reg)
    broadcaster.start()
    broadcaster.join()


if __name__ == "__main__":
    main()

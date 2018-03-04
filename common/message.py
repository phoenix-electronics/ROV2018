from typing import Tuple

from client.system_info import SystemInfo


class CommandMessage:
    """Command information sent from the server to the client"""

    def __init__(self, motor_speeds: Tuple[int, int, int, int, int, int], camera_index: int) -> None:
        self.motor_speeds = motor_speeds
        self.camera_index = camera_index


class ClientStateMessage:
    """State information sent from the client to the server"""

    def __init__(self, system_info: SystemInfo, arduino_connected: bool) -> None:
        self.system_info = system_info
        self.arduino_connected = arduino_connected

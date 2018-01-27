from typing import Optional, Tuple

import serial
from serial.tools import list_ports


class Arduino:
    ACK_TIMEOUT = 0.1
    SERIAL_RATE = 9600

    def __init__(self) -> None:
        self.connection = None

    def is_connected(self) -> bool:
        return self.connection is not None

    def connect(self) -> None:
        port = self._detect_port()
        if port is not None:
            connection = serial.Serial()
            connection.port = port
            connection.baudrate = self.SERIAL_RATE
            connection.timeout = self.ACK_TIMEOUT
            connection.setDTR(False)
            connection.open()
            self.connection = connection

    def send(self, motor_speeds: Tuple[int, int, int, int, int, int]) -> None:
        pass

    def disconnect(self) -> None:
        if self.is_connected():
            self.connection.close()
        self.connection = None

    @staticmethod
    def _detect_port() -> Optional[str]:
        port = next(list_ports.grep('Arduino'), None)
        if port is not None:
            return port.device

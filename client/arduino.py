from typing import Optional, Tuple

import serial
from serial.tools import list_ports


class Arduino:
    def __init__(self, baud_rate: int = 57600, write_timeout: float = 0.05, enable_dtr: bool = False) -> None:
        self.baud_rate = baud_rate
        self.write_timeout = write_timeout
        self.enable_dtr = enable_dtr
        self.connection = None

    def is_connected(self) -> bool:
        return self.connection is not None and self.connection.isOpen()

    def connect(self) -> None:
        port = self._detect_port()
        if port is not None:
            self.connection = serial.Serial()
            self.connection.port = port
            self.connection.baudrate = self.baud_rate
            self.connection.writeTimeout = self.write_timeout
            self.connection.setDTR(self.enable_dtr)
            self.connection.open()

    def write_speeds(self, motor_speeds: Tuple[int, int, int, int, int, int]) -> None:
        data = '!{}:{}:{}:{}:{}:{};\n'.format(*motor_speeds)
        self.connection.write(data.encode())

    def disconnect(self) -> None:
        if self.is_connected():
            self.connection.close()
        self.connection = None

    @staticmethod
    def _detect_port() -> Optional[str]:
        port = next(list_ports.grep('Arduino'), None)
        if port is not None:
            return port.device

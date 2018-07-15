from typing import Optional, Tuple

import serial
from serial.tools import list_ports


class Arduino:
    """Wrapper for a serial connection to an Arduino"""

    BAUD_RATE = 57600
    WRITE_TIMEOUT = 0.05

    def __init__(self, port: str = None) -> None:
        self.port = port
        self.connection = None

    def is_connected(self) -> bool:
        """Return whether the Arduino is connected"""
        return self.connection is not None and self.connection.is_open

    def connect(self) -> bool:
        """Attempt to connect to the Arduino, searching for a port if one is not specified"""
        port = self.port or self._detect_port()
        if port is not None:
            self.connection = serial.Serial()
            self.connection.port = port
            self.connection.baudrate = self.BAUD_RATE
            self.connection.writeTimeout = self.WRITE_TIMEOUT
            self.connection.dtr = False
            try:
                self.connection.open()
                return True
            except serial.SerialException:
                self.connection = None
        return False

    def write_speeds(self, motor_speeds: Optional[Tuple[int, int, int, int, int, int, int]]) -> None:
        """Write target motor speeds to the Arduino, raising serial.SerialException if the write fails"""
        if motor_speeds is None:
            motor_speeds = (1500, 1500, 1500, 1500, 1500, 1500, 0)
        data = '!{},{},{},{},{},{},{};\n'.format(*motor_speeds)
        self.connection.write(data.encode())

    def disconnect(self) -> None:
        """Close the connection to the Arduino"""
        if self.is_connected():
            self.connection.close()
        self.connection = None

    @staticmethod
    def _detect_port() -> Optional[str]:
        for port in list_ports.grep('Arduino'):
            return port.device

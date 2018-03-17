from typing import Optional

"""Messages contain information sent from the client to the server"""


class SystemInfoMessage:
    """Information about the state of the system"""

    def __init__(self, cpu_usage: float, cpu_temp: Optional[float], mem_usage: float) -> None:
        self.cpu_usage = cpu_usage
        self.cpu_temp = cpu_temp
        self.mem_usage = mem_usage


class ArduinoConnectionMessage:
    """Information about the state of the Arduino connection"""

    def __init__(self, connected: bool) -> None:
        self.connected = connected

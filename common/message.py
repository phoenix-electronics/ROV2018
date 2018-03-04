from client.system_info import SystemInfo

"""Messages contain information sent from the client to the server"""


class SystemInfoMessage:
    """Information about the state of the system"""

    def __init__(self, system_info: SystemInfo) -> None:
        self.system_info = system_info


class ArduinoConnectionMessage:
    """Information about the state of the Arduino connection"""

    def __init__(self, connected: bool) -> None:
        self.connected = connected

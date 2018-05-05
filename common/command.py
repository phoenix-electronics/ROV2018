from typing import Tuple, Optional

"""Commands contain information sent from the server to the client"""


class SetMotorSpeedsCommand:
    """Set the speeds of the motors, or stop the motors if no speeds are provided"""

    def __init__(self, motor_speeds: Optional[Tuple[int, int, int, int, int, int, int]]) -> None:
        self.motor_speeds = motor_speeds

    def __repr__(self) -> str:
        return 'SetMotorSpeedsCommand(motor_speeds={!r})'.format(self.motor_speeds)


class SetCameraCommand:
    """Set the camera used for the video stream"""

    def __init__(self, camera_index: int) -> None:
        self.camera_index = camera_index

    def __repr__(self) -> str:
        return 'SetCameraCommand(camera_index={!r})'.format(self.camera_index)


class PlaySoundCommand:
    """Play a sound file, or stop the currently playing sound if no filename is provided"""

    def __init__(self, filename: Optional[str], volume: float = 1.0) -> None:
        self.filename = filename
        self.volume = volume

    def __repr__(self) -> str:
        return 'PlaySoundCommand(filename={!r}, volume={!r})'.format(self.filename, self.volume)

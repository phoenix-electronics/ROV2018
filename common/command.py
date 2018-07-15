from typing import Tuple, Optional

"""Commands contain information sent from the server to the client"""


class SetMotorSpeedsCommand:
    """Set the speeds of the motors, or stop the motors if no speeds are provided"""

    def __init__(self, motor_speeds: Optional[Tuple[int, int, int, int, int, int, int]]) -> None:
        self.motor_speeds = motor_speeds

    def __repr__(self) -> str:
        return 'SetMotorSpeedsCommand(motor_speeds={})'.format(self.motor_speeds)


class SetCameraCommand:
    """Set the camera used for the video stream"""

    def __init__(self, camera_index: int) -> None:
        self.camera_index = camera_index

    def __repr__(self) -> str:
        return 'SetCameraCommand(camera_index={})'.format(self.camera_index)


class PlaySoundCommand:
    """Stop the currently playing sound (if any), and optionally play a new sound"""

    def __init__(self, filename: Optional[str], vol_mb: int = 0, amp_mb: int = 0) -> None:
        self.filename = filename
        self.vol_mb = vol_mb
        self.amp_mb = amp_mb

    def __repr__(self) -> str:
        return 'PlaySoundCommand(filename={!r}, vol_mb={}, amp_mb={})'.format(self.filename, self.vol_mb, self.amp_mb)

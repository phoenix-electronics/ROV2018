from typing import Tuple, Optional

"""Commands contain information sent from the server to the client"""


class SetMotorSpeedsCommand:
    """Set the speeds of the motors"""

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

import math
from typing import Tuple

from server.joystick import JoystickData


def calculate_motor_speeds(joystick_data: JoystickData) -> Tuple[int, int, int, int, int, int]:
    # Filter out joystick axis values close to zero (deadband)
    axes = [axis if abs(axis) >= 0.05 else 0 for axis in joystick_data.axes]

    # Find the requested forward, strafe, yaw, and vertical motion
    forward_cmd = -axes[1]
    strafe_cmd = axes[0]
    yaw_cmd = axes[2]
    vertical_cmd = (1 - axes[3]) * joystick_data.hat[1] / 2

    # Convert the square joystick input area into a circle
    forward_cmd_circle = forward_cmd * math.sqrt(1 - strafe_cmd ** 2 / 2)
    strafe_cmd_circle = strafe_cmd * math.sqrt(1 - forward_cmd ** 2 / 2)

    # Find the projection of the joystick vectors onto the motor vectors
    rfm_projection = (math.sqrt(3) * forward_cmd_circle + strafe_cmd_circle) / 2
    lfm_projection = (math.sqrt(3) * forward_cmd_circle - strafe_cmd_circle) / 2

    # Calculate the effect of yaw on output
    yaw_effect = math.sqrt(3) / 2 * yaw_cmd

    # Calculate the horizontal and vertical motor speeds
    h_motor_speeds = [
        rfm_projection - yaw_effect,
        lfm_projection - yaw_effect,
        lfm_projection + yaw_effect,
        rfm_projection + yaw_effect
    ]
    v_motor_speeds = [
        vertical_cmd,
        vertical_cmd
    ]

    # Scale the speeds of the horizontal motors down if necessary
    h_motor_speeds_max = max(max(h_motor_speeds), 1)
    h_motor_speeds = [speed / h_motor_speeds_max for speed in h_motor_speeds]

    # Calculate and return the final motor speeds
    motor_speeds = [int(1500 + speed * 500) for speed in h_motor_speeds + v_motor_speeds]
    return tuple(motor_speeds)[:]

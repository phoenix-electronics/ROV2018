import math
from typing import Tuple

from server.joystick import JoystickData


def calculate_motor_speeds(joystick_data: JoystickData) -> Tuple[int, int, int, int, int, int, int]:
    # Filter out joystick axis values close to zero (deadband)
    axes = [axis if abs(axis) >= 0.08 else 0 for axis in joystick_data.axes]

    forwards = -axes[1]
    sideways = axes[0]
    yaw = axes[2] * 0.5
    pitch = (int(joystick_data.buttons[10]) - int(joystick_data.buttons[11])) * (1 - axes[3]) / 2
    vertical = joystick_data.hat[1] * (1 - axes[3]) / 2
    camera_rot = joystick_data.hat[0]

    # Apply a slight pitch to keep the bot level while moving forwards
    pitch += forwards * 0.3

    # Convert the square joystick input area into a circle
    forwards_circle = forwards * math.sqrt(1 - sideways ** 2 / 2)
    sideways_circle = sideways * math.sqrt(1 - forwards ** 2 / 2)

    # Find the projection of the joystick vectors onto the motor vectors
    rfm_projection = (math.sqrt(3) * forwards_circle + sideways_circle) / 2
    lfm_projection = (math.sqrt(3) * forwards_circle - sideways_circle) / 2

    # Calculate the effect of yaw on output
    yaw_effect = math.sqrt(3) / 2 * yaw

    # Calculate the horizontal and vertical_cmd motor speeds
    h_motor_speeds = [
        rfm_projection + yaw_effect,
        lfm_projection - yaw_effect,
        lfm_projection + yaw_effect,
        rfm_projection - yaw_effect
    ]
    v_motor_speeds = [
        vertical - pitch,
        vertical + pitch
    ]

    # Scale the speeds of the horizontal motors down if necessary
    h_motor_speeds_max = max(max(map(abs, h_motor_speeds)), 1)
    h_motor_speeds = [speed / h_motor_speeds_max for speed in h_motor_speeds]

    # Convert the speeds ([-1.0, 1.0]) to values for the ESCs ([1100, 1900])
    motor_speeds = [int(1500 + speed * 400) for speed in h_motor_speeds + v_motor_speeds]

    # Append the camera rotation speed
    motor_speeds.append(camera_rot)

    # Return the speeds
    return tuple(motor_speeds)[:]

import pygame
from typing import List, Optional, Tuple
from common.timer import Timer


class JoystickData:
    def __init__(self, axes: List[float], buttons: List[bool], hat: Tuple[int, int]) -> None:
        self.axes = axes
        self.buttons = buttons
        self.hat = hat


class Joystick:
    """Pygame doesn't provide a way to detect if a joystick has been disconnected.
    After the joystick has been unplugged, pygame will continue to return the state the joystick was last in.
    This is VERY BAD, and could lead to the motors being stuck on or any other number of bad situations.

    In order to get around this, we have to kill the connection every so often and reopen it to make sure that the
    joystick is still connected.
    This interval should be short enough that we can detect the disconnect quickly (and not lose control for too long),
    but not too short, as there is a very large overhead with quitting/initializing the connection.

    Another possible way to detect a disconnect would be to check if the raw axis values from the joystick haven't
    changed in a certain amount of time.
    The values returned from polling the raw axes are ridiculously precise, but not as accurate. This means that two
    consecutive reads will almost certainly return different values, due to inaccuracies in the readings.
    This method is likely the better option, but its reliability has not been tested yet, so we will use the first
    method for now.
    """
    RECONNECT_INTERVAL = 0.25

    def __init__(self) -> None:
        self.reconnect_timer = Timer(self.RECONNECT_INTERVAL)
        self.joystick = None

    def is_connected(self) -> bool:
        return self.joystick is not None

    def _connect(self) -> None:
        if not pygame.joystick.get_init():
            pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.reconnect_timer.restart()

    def _disconnect(self) -> None:
        self.joystick.quit()
        self.joystick = None

    def poll(self) -> Optional[JoystickData]:
        if self.is_connected() and self.reconnect_timer.is_expired():
            self._disconnect()
        if not self.is_connected():
            self._connect()
        if self.is_connected():
            axes = [self.joystick.get_axis(i) for i in range(self.joystick.get_numaxes())]
            buttons = [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]
            hat = self.joystick.get_hat(0)
            return JoystickData(axes, buttons, hat)

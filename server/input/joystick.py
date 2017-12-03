from typing import Tuple, Optional

import pygame

from server.connection.connection import Connection
from server.timer.timer import Timer


class Joystick:
    DEFAULT_RECONNECT_DELAY = 100

    def __init__(self, joystick_id: int = 0) -> None:
        self.joystick_id = joystick_id
        self.connection = Connection()
        self.retry_timer = Timer(self.DEFAULT_RECONNECT_DELAY)
        self.joystick = None
        self.retry_timer.expire()

    def is_connected(self) -> bool:
        return self.connection.is_open()

    def poll(self) -> Optional[Tuple[int, int]]:
        if not self.is_connected():
            self.joystick = None
            if self.retry_timer.is_expired():
                pygame.joystick.quit()
                pygame.joystick.init()
                if pygame.joystick.get_count() > 0:
                    joystick = pygame.joystick.Joystick(self.joystick_id)
                    if joystick:
                        joystick.init()
                        if joystick.get_init():
                            self.joystick = joystick
                            self.connection.open()
                if not self.is_connected():
                    self.retry_timer.restart()
        if self.is_connected():
            return self.joystick.get_axis(0), self.joystick.get_axis(1)

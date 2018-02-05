from typing import List, Tuple

import pygame


class Joystick:
    def __init__(self) -> None:
        self.joystick = None

    def is_connected(self) -> bool:
        return self.joystick is not None

    def connect(self) -> None:
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

    def disconnect(self) -> None:
        self.joystick.quit()
        self.joystick = None

    def read_values(self) -> Tuple[List[float], List[bool], Tuple[int, int]]:
        axes = [self.joystick.get_axis(i) for i in range(self.joystick.get_numaxes())]
        buttons = [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]
        hat = self.joystick.get_hat(0)
        return axes, buttons, hat

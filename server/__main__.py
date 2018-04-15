import os

import pygame

from server import events
from server.joystick import Joystick
from server.server import Server
from server.window import Window

if __name__ == '__main__':
    # Read configuration details from environment
    host = os.getenv('HOST', 'localhost')
    port = int(os.getenv('PORT', '1234'))

    enable_joystick_hotplug = os.getenv('ENABLE_JOYSTICK_HOTPLUG') is not None

    # Initialize Pygame
    pygame.init()

    # Start a Pygame timer to read the joystick's axes (if connected) every 50ms
    pygame.time.set_timer(events.READ_JOYSTICK, 50)

    if enable_joystick_hotplug:
        # Start a Pygame timer to reinitialize the joystick module to check for changes every 1000ms
        pygame.time.set_timer(events.CHECK_JOYSTICK, 1000)

    # Initialize joystick and window
    joystick = Joystick()
    window = Window()
    joystick.connect()
    window.show()

    # Create and run server
    server = Server(host, port, joystick, window)
    try:
        server.run()
    finally:
        window.hide()
        pygame.quit()

import os

import pygame

from common import logging
from server import events
from server.joystick import Joystick
from server.server import Server
from server.window import Window

if __name__ == '__main__':
    # Read configuration details from the environment
    host = os.getenv('HOST', 'localhost')
    port = int(os.getenv('PORT', '1234'))

    enable_joystick_hotplug = os.getenv('ENABLE_JOYSTICK_HOTPLUG') is not None

    # Initialize Pygame
    pygame.init()

    # Start a Pygame timer to read the joystick's axes every 50ms
    pygame.time.set_timer(events.READ_JOYSTICK, 50)

    if enable_joystick_hotplug:
        # Start a Pygame timer to shutdown and reinitialize the joystick system every 1000ms
        pygame.time.set_timer(events.CHECK_JOYSTICK, 1000)

    # Initialize the joystick and window
    joystick = Joystick()
    window = Window()
    joystick.connect()
    window.show()

    # Warn if joystick hotplugging is disabled and a joystick is not detected
    if not enable_joystick_hotplug and not joystick.is_connected():
        logging.warn('Joystick not detected and ENABLE_JOYSTICK_HOTPLUG is not set!')
        logging.warn('Connect a joystick and restart the program to fix this.')

    # Create and run the server
    server = Server(host, port, joystick, window)
    try:
        server.run()
    finally:
        window.hide()
        pygame.quit()

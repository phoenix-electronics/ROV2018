import socket

import pygame

from common import logging
from common.command import SetMotorSpeedsCommand, SetCameraCommand, PlaySoundCommand
from common.message import ArduinoConnectionMessage, SystemInfoMessage
from common.protocol import recv_avail, recv_obj, send_obj
from server import events
from server.joystick import Joystick
from server.motor_vectoring import calculate_motor_speeds
from server.window import Window


class Server:
    SOCKET_TIMEOUT = 0.5

    def __init__(self, host: str, port: int, joystick: Joystick, window: Window) -> None:
        self.host = host
        self.port = port

        self.joystick = joystick
        self.window = window

        self.server_sock = None
        self.client_sock = None
        self.client_addr = None

    def run(self) -> None:
        """Run the server"""
        try:
            # Create, configure, and bind the server socket
            self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_sock.settimeout(self.SOCKET_TIMEOUT)
            self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_sock.bind((self.host, self.port))
            self.server_sock.listen(1)
            logging.info('Server started on {}:{}', self.host or 'INADDR_ANY', self.port)
            while True:
                # Handle Pygame events and update the window while waiting for an incoming connection
                while not recv_avail(self.server_sock):
                    self.handle_event(pygame.event.wait())
                    self.window.update()
                # Once an incoming connection is being made, handle it
                self.handle_connection()
        finally:
            self.server_sock.close()

    def handle_connection(self) -> None:
        """Accept and handle a client connection"""
        try:
            # Accept the incoming connection
            self.client_sock, self.client_addr = self.server_sock.accept()
            logging.info('Client connected: {}', self.client_addr[0])
            # TODO: Update self.window
            while True:
                # Handle Pygame events and update the window
                self.handle_event(pygame.event.wait())
                self.window.update()
                # Receive and handle a message from the client if one is available
                if recv_avail(self.client_sock):
                    message = recv_obj(self.client_sock, self.SOCKET_TIMEOUT)
                    self.handle_message(message)
        except socket.error as err:
            logging.error('Client disconnected: {}', err)
        finally:
            self.client_sock.close()
            self.client_sock = None
            self.client_addr = None
            # TODO: Update self.window

    def handle_message(self, message: object) -> None:
        """Handle a message from the client"""
        if isinstance(message, ArduinoConnectionMessage):
            pass  # TODO: Update self.window
        elif isinstance(message, SystemInfoMessage):
            pass  # TODO: Update self.window

    def handle_event(self, event: pygame.event.EventType) -> None:
        """Handle a Pygame event"""
        if event.type == events.READ_JOYSTICK:
            # Read the joystick's axes if it is connected
            joystick_data = self.joystick.read_values() if self.joystick.is_connected() else None
            # TODO: Update self.window
            # Calculate and send new motor speeds to the client if it is connected
            if self.client_sock is not None:
                motor_speeds = calculate_motor_speeds(joystick_data) if joystick_data is not None else None
                send_obj(self.client_sock, SetMotorSpeedsCommand(motor_speeds))
        elif event.type == events.CHECK_JOYSTICK:
            # Reinitialize the joystick module to check for changes
            pygame.joystick.quit()
            pygame.joystick.init()
            self.joystick.connect()
        elif event.type == pygame.JOYBUTTONDOWN:
            # Handle the button press
            camera_button_min = 6
            camera_button_max = 8
            play_sound_button = 9
            if camera_button_min <= event.button <= camera_button_max:
                # Send a command to change the active camera
                send_obj(self.client_sock, SetCameraCommand(event.button - camera_button_min))
            elif event.button == play_sound_button:
                # Send a command to play the OBS release sound
                send_obj(self.client_sock, PlaySoundCommand('/home/rov/obs_release.wav'))
        elif event.type == pygame.QUIT:
            # Exit when the window is closed
            raise SystemExit

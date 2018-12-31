import socket
from typing import List

import serial

from common import logging
from client.arduino import Arduino
from client.camera_stream import CameraStream
from client.sound_player import SoundPlayer
from client.system_info import get_system_info_message
from common.command import SetMotorSpeedsCommand, SetCameraCommand, PlaySoundCommand
from common.message import ArduinoConnectionMessage
from common.protocol import send_obj, recv_obj
from common.timer import Timer


class Client:
    SOCKET_TIMEOUT = 0.5
    RECONNECT_DELAY = 1.0
    SYSTEM_INFO_INTERVAL = 1.0

    def __init__(self, host: str, port: int, arduino: Arduino, camera_streams: List[CameraStream]) -> None:
        self.host = host
        self.port = port
        self.arduino = arduino
        self.camera_streams = camera_streams
        self.active_camera_stream = None

        self.sound_player = SoundPlayer()

        self.sock = None

    def connect_and_run(self) -> None:
        """Connect to the server and run the client"""
        logging.info('Connecting to server: {}:{}', self.host, self.port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.SOCKET_TIMEOUT)
        try:
            self.sock.connect((self.host, self.port))
        except socket.error as err:
            logging.error('Unable to connect: {} (retrying in {}s)', err, self.RECONNECT_DELAY)
            return
        logging.info("Connected to server")
        # Initialize a timer to periodically send a SystemInfoMessage
        send_system_info_timer = Timer(self.SYSTEM_INFO_INTERVAL, start_expired=True)
        try:
            # Inform the server of the current state of the Arduino connection
            send_obj(self.sock, ArduinoConnectionMessage(self.arduino.is_connected()))
            while True:
                # Send a SystemInfoMessage if send_stats_interval has elapsed
                if send_system_info_timer.is_expired():
                    send_obj(self.sock, get_system_info_message())
                    send_system_info_timer.restart()
                # Receive and handle a command
                command = recv_obj(self.sock, self.SOCKET_TIMEOUT)
                self.handle_command(command)
        except socket.error as err:
            logging.error('Connection closed: {} (reconnecting in {}s)', err, self.RECONNECT_DELAY)
        finally:
            self.sock.close()
            # If the Arduino is connected, try and stop the motors
            if self.arduino.is_connected():
                try:
                    self.arduino.write_speeds(None)
                except serial.SerialException:
                    pass
            # Stop the currently playing sound, if any
            self.sound_player.stop()

    def handle_command(self, command: object) -> None:
        """Handle a command from the server"""
        logging.debug('Server command: {}', command)
        if isinstance(command, SetMotorSpeedsCommand):  # Server requested new motor speeds
            # Try and connect to the Arduino if it is not connected
            if not self.arduino.is_connected() and self.arduino.connect():
                # Inform the server that the Arduino connection state has changed
                send_obj(self.sock, ArduinoConnectionMessage(True))
            # Try and write the motor speeds to the Arduino if it is connected
            if self.arduino.is_connected():
                try:
                    self.arduino.write_speeds(command.motor_speeds)
                except serial.SerialException:
                    # Error writing motor speeds, disconnect and inform the server
                    self.arduino.disconnect()
                    send_obj(self.sock, ArduinoConnectionMessage(False))
        elif isinstance(command, SetCameraCommand):  # Server requested new camera index
            # Set the currently playing camera stream to PAUSED
            self.active_camera_stream.set_paused()
            # Set the the new camera stream to PLAYING
            self.active_camera_stream = self.camera_streams[command.camera_index]
            self.active_camera_stream.set_playing()
        elif isinstance(command, PlaySoundCommand):  # Server requested that a sound be played
            # Stop the currently playing sound, if any
            self.sound_player.stop()
            # If a sound filename was provided, play the sound
            if command.filename is not None:
                self.sound_player.play(command.filename, command.vol_mb, command.amp_mb)

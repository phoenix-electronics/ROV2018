import os
from time import sleep

from client.arduino import Arduino
from client.camera_stream import CameraStream
from client.client import Client

if __name__ == '__main__':
    # Read configuration details from environment
    host = os.getenv('HOST', 'localhost')
    port = int(os.getenv('PORT', '1234'))

    gst_port = int(os.getenv('GST_PORT', '5000'))
    arduino_port = os.getenv('ARDUINO_PORT')

    # Initialize Arduino connection and video stream
    arduino = Arduino(arduino_port)
    camera_stream = CameraStream(host, gst_port)
    arduino.connect()
    camera_stream.set_source(0)

    # Create and run client
    client = Client(host, port, arduino, camera_stream)
    while True:
        client.connect_and_run()
        sleep(client.reconnect_delay)

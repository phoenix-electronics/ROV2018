import os
from time import sleep

from client.arduino import Arduino
from client.camera_stream import CameraStream
from client.client import Client

if __name__ == '__main__':
    # Read configuration details from environment
    host = os.getenv('HOST', 'localhost')  # Server address
    port = int(os.getenv('PORT', '1234'))  # Server port
    gst_port = int(os.getenv('GST_PORT', '5000'))  # GStreamer port

    # Initialize Arduino connection and video stream
    arduino = Arduino()
    camera_stream = CameraStream(host, gst_port)
    arduino.connect()
    camera_stream.set_source(0)

    # Create and run client
    client = Client(host, port, arduino, camera_stream)
    while True:
        client.connect_and_run()
        sleep(client.reconnect_delay)

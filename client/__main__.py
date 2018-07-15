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

    # Initialize Arduino connection
    arduino = Arduino(arduino_port)
    arduino.connect()

    # Initialize camera streams
    camera_stream_settings = [
        ('/dev/video0', (1280, 720), 30),
        ('/dev/video1', (1280, 720), 30),
        ('/dev/video2', (640, 480), 30)
    ]
    camera_streams = [CameraStream(settings[0], settings[1], settings[2], host, gst_port)
                      for settings in camera_stream_settings]

    # Set camera streams to PAUSED so that they are ready to send video
    for stream in camera_streams:
        stream.set_paused()

    # Create the client
    client = Client(host, port, arduino, camera_streams)

    # Set the first camera stream to PLAYING
    camera_streams[0].set_playing()
    client.active_camera_stream = camera_streams[0]

    # Run the client
    while True:
        client.connect_and_run()
        sleep(client.RECONNECT_DELAY)

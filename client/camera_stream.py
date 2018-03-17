import gi
gi.require_version('Gst', '1.0')  # noqa
from gi.repository import Gst

Gst.init(None)


class CameraStream:
    """Wrapper for a GStreamer V4L2 video stream"""

    def __init__(self, host: str = '127.0.0.1', port: int = 5000) -> None:
        self.host = host
        self.port = port
        self.source = None
        self.pipeline = None

    def set_source(self, camera_index: int) -> None:
        """Set the source of the video stream, restarting the stream if necessary"""
        source = '/dev/video{}'.format(camera_index)
        if self.source != source:
            self.source = source
            self.restart()

    def restart(self) -> None:
        """Stop and restart the video stream"""
        if self.pipeline:
            self.pipeline.set_state(Gst.State.NULL)
        pipeline_args = 'v4l2src device="{}" ! video/x-raw, format=I420, width=640, height=480, framerate=30/1 ! ' \
                        'jpegenc ! rtpjpegpay ! udpsink host="{}" port={}' \
            .format(self.source, self.host, self.port)
        self.pipeline = Gst.parse_launch(pipeline_args)
        self.pipeline.set_state(Gst.State.PLAYING)

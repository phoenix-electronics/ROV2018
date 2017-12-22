import gi
gi.require_version('Gst', '1.0')  # noqa
from gi.repository import Gst

Gst.init(None)


class CameraStream:
    def __init__(self, host: str = '127.0.0.1', port: int = 5000) -> None:
        self.host = host
        self.port = port
        self.source = None
        self.pipeline = None

    def set_source(self, source: str) -> None:
        self.source = source
        self.restart()

    def restart(self) -> None:
        if self.pipeline:
            self.pipeline.set_state(Gst.State.NULL)
        pipeline_args = 'v4l2src device="{}" ! video/x-raw, format=I420, width=640, height=480, framerate=15/1 ! ' + \
                        'jpegenc ! rtpjpegpay ! udpsink host="{}" port={}' \
                        .format(self.source, self.host, self.port)
        self.pipeline = Gst.parse_launch(pipeline_args)
        self.pipeline.set_state(Gst.State.PLAYING)

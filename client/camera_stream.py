from typing import Tuple

import gi

gi.require_version('Gst', '1.0')  # noqa
from gi.repository import Gst

Gst.init(None)


class CameraStream:
    """Wrapper for a GStreamer V4L2 video stream"""

    def __init__(self, source: str, resolution: Tuple[int, int], framerate: int, host: str, port: int) -> None:
        self._pipeline = self._create_pipeline(source, resolution, framerate, host, port)

    def set_playing(self) -> None:
        """Sets the video stream state to PLAYING"""
        self._pipeline.set_state(Gst.State.PLAYING)

    def set_paused(self) -> None:
        """Sets the video stream state to PAUSED"""
        self._pipeline.set_state(Gst.State.PAUSED)

    def set_stopped(self) -> None:
        """Sets the video stream state to NULL"""
        self._pipeline.set_state(Gst.State.NULL)

    @staticmethod
    def _create_pipeline(source: str, resolution: Tuple[int, int], framerate: int, host: str, port: int) -> Gst.Element:
        pipeline_args = 'v4l2src device="{}" ! video/x-raw, format=I420, width={}, height={}, framerate={}/1 ! ' \
                        'jpegenc ! rtpjpegpay ! udpsink host="{}" port={}' \
            .format(source, resolution[0], resolution[1], framerate, host, port)
        return Gst.parse_launch(pipeline_args)

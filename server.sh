#!/usr/bin/env sh

##
## This script starts the server and the GStreamer pipeline.
##

export HOST=localhost
export PORT=1234
export GST_PORT=5000
#export JOYSTICK_INDEX=0
#export ENABLE_JOYSTICK_HOTPLUG=1

echo "----------------"
echo "HOST=$HOST"
echo "PORT=$PORT"
echo "GST_PORT=$GST_PORT"
echo "----------------"

gst-launch-1.0 udpsrc port=$GST_PORT \
    ! application/x-rtp,encoding-name=JPEG,payload=26 \
    ! rtpjpegdepay \
    ! jpegdec \
    ! autovideosink &

python3 -m server

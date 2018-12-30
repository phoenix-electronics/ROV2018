#!/usr/bin/env sh

##
## This script starts the server and the GStreamer pipeline.
##

## Address to host the server on.
## See: https://docs.python.org/3/library/socket.html#host-port
export HOST=localhost
export PORT=1234

## Port to receive video on.
## This should match the port set in `client.sh`.
export GST_PORT=5000

## Uncomment to use a specific joystick index.
#export JOYSTICK_INDEX=0

## Uncomment to enable joystick hotplugging.
## This can lead to odd behavior so it is disabled by default.
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

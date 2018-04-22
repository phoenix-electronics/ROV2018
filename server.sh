#!/usr/bin/env sh

export HOST=192.168.0.1
export PORT=1234

echo "----------------"
echo "HOST=$HOST"
echo "PORT=$PORT"
echo "----------------"

gst-launch-1.0 udpsrc port=5000 \
    ! application/x-rtp,encoding-name=JPEG,payload=26 \
    ! rtpjpegdepay \
    ! jpegdec \
    ! autovideosink &

python3 -m server

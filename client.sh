#!/usr/bin/env sh

##
## This script starts the client.
##

export HOST=localhost
export PORT=1234
export GST_PORT=5000
#export ARDUINO_PORT=/dev/ttyUSB0

echo "----------------"
echo "HOST=$HOST"
echo "PORT=$PORT"
echo "GST_PORT=$GST_PORT"
echo "----------------"

python3 -m client

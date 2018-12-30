#!/usr/bin/env sh

##
## This script starts the client.
##

## Server address.
## This should match the address set in `server.sh`.
export HOST=localhost
export PORT=1234

## Port to send video on.
export GST_PORT=5000

## Arduino serial port.
## If not set, the client will try to detect it automatically.
## However, you should probably set it manually if you can.
#export ARDUINO_PORT=/dev/ttyUSB0


echo "----------------"
echo "HOST=$HOST"
echo "PORT=$PORT"
echo "GST_PORT=$GST_PORT"
echo "----------------"

python3 -m client

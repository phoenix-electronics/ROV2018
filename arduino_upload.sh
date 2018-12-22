#!/usr/bin/env sh

##
## This script builds and uploads `arduino/arduino.ino` to the connected board.
##

export ARDUINO_PORT=/dev/ttyUSB0
export ARDUINO_FQBN=arduino:avr:nano:cpu=atmega328

echo "----------------"
echo "ARDUINO_PORT=$ARDUINO_PORT"
echo "ARDUINO_FQBN=$ARDUINO_FQBN"
echo "----------------"

arduino --upload arduino/arduino.ino --port $ARDUINO_PORT --board $ARDUINO_FQBN

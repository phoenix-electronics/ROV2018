#!/usr/bin/env sh

export ARDUINO_PORT=/dev/ttyUSB0
export ARDUINO_BOARD=arduino:avr:nano:cpu=atmega328

echo "----------------"
echo "ARDUINO_PORT=$ARDUINO_PORT"
echo "ARDUINO_BOARD=$ARDUINO_BOARD"
echo "----------------"

arduino --upload arduino/arduino.ino --port $ARDUINO_PORT --board $ARDUINO_BOARD

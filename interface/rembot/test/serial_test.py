#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Testing serial communication between arduio and python
License is available in LICENSE
@author eeshiken
@since 2017-DEC-28
"""
import io
import logging
from time import sleep
import serial

ROOT_LOGGER = logging.getLogger("rembot")
ROOT_LOGGER.setLevel(level=logging.INFO)
LOG_HANDLER = logging.StreamHandler()
LOG_FORMATTER = logging.Formatter(
    fmt='%(asctime)s [%(name)s](%(levelname)s) %(message)s',
    datefmt='%H:%M:%S')
LOG_HANDLER.setFormatter(LOG_FORMATTER)
ROOT_LOGGER.addHandler(LOG_HANDLER)

PY_LOGGER = logging.getLogger("rembot.%s"%__name__)
MCU_LOGGER = logging.getLogger("rembot.arduino")

ser = serial.Serial('COM5', 9600) # Establish the connection on a specific port
counter = 32 # Below 32 everything in ASCII is gibberish

while True:
    counter += 1

    # Convert the decimal number to ASCII then send it to the Arduino
    ser.write(chr(counter).encode('utf-8'))
    # PY_LOGGER.info(counter
    DATA = ser.readline()
    if DATA != b'Ready\r\n':
        out = ord(DATA.decode().rstrip())
    else:
        out = DATA.decode().rstrip()

    MCU_LOGGER.info(out) # Read the newest output from the Arduino
    sleep(.1) # Delay for one tenth of a second
    if counter == 127:
        counter = 32

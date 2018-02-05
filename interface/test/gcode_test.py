#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Testing remote control of the rembot
License is available in LICENSE
@author eeshiken
@since 2018-JAN-27
"""
import io
import logging
from time import sleep
from arduino import Arduino

DEBUG = 1 # True

ROOT_LOGGER = logging.getLogger("rembot")
ROOT_LOGGER.setLevel(level=logging.INFO)
LOG_HANDLER = logging.StreamHandler()
LOG_FORMATTER = logging.Formatter(
    fmt='%(asctime)s [%(name)s](%(levelname)s) %(message)s',
    datefmt='%H:%M:%S')
LOG_HANDLER.setFormatter(LOG_FORMATTER)
ROOT_LOGGER.addHandler(LOG_HANDLER)

PY_LOGGER = logging.getLogger("rembot.gcode_test")
MCU_LOGGER = logging.getLogger("rembot.arduino")

if __name__ == "__main__":
    arduino = Arduino("Gcode_Test")
    PY_LOGGER.info("Beginning test")
    
    """
    Lift Pen - G2 P0
    Reset - G0
    Drop pen - G2 P1
    Left - G1 X10 Y0 F10000
    Down - G1 X10 Y10 F1000
    Right - G1 X0 Y10 F1000
    Up - G1 X0 Y0 F1000
    """
    for cmd in ["G2 P0\n", "G0\n", "G2 P1\n", "G1 X10 Y0 F10000\n", "G1 X10 Y10 F1000\n", "G1 X0 Y10 F1000\n", "G1 X0 Y0 F1000\n", "G2 P0\n", "G0\n" ]:
        arduino.send_str_data(cmd)
        if DEBUG:
            PY_LOGGER.info("Sending {}".format(cmd)) 
        sleep(.1)

        while(arduino.read_str_data() != 'S'): 
            continue

        sleep(.1)
        if DEBUG:
            MCU_LOGGER.info(arduino.read_str_data()) # debug message

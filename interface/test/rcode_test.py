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
    
    # See PROTOCOL.md for commsnd list
    """
    Reset line reset
    """
    for cmd in ["R00\r\n", "R01 x0 X10 y0 Y0\r\n", "R00\r\n"]:
        while(1):
            _m = arduino.read_str_data()
            if _m == '>':
                break
            else:
                MCU_LOGGER.info(_m)
        if DEBUG:
            PY_LOGGER.info("Sending {}".format(cmd))
        
        arduino.send_str_data(cmd)

        sleep(.1)
        
        while(arduino.read_str_data() != 'S'):
            pass

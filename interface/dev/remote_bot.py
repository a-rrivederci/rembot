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
import serial

ROOT_LOGGER = logging.getLogger("rembot")
ROOT_LOGGER.setLevel(level=logging.INFO)
LOG_HANDLER = logging.StreamHandler()
LOG_FORMATTER = logging.Formatter(
    fmt='%(asctime)s [%(name)s](%(levelname)s) %(message)s',
    datefmt='%H:%M:%S')
LOG_HANDLER.setFormatter(LOG_FORMATTER)
ROOT_LOGGER.addHandler(LOG_HANDLER)

PY_LOGGER = logging.getLogger("rembot.remote_bot")
MCU_LOGGER = logging.getLogger("rembot.arduino")

class Arduino(object):
    ''' Rembot communication class '''
    def __init__(self, ability):
        self.name = ability
        self.port = serial.Serial('COM5', 9600)
        self.title = self.read_str_data()

    def send_str_data(self, string):
        ''' Send character string '''
        self.port.write(string.encode('utf-8'))

    def read_str_data(self):
        ''' read string '''
        data = self.port.readline()
        return data.decode().rstrip()

    def read_num_data(self):
        ''' Reads in numerical data from uno  '''
        data = self.port.readline()
        return ord(data.decode().rstrip())

    def __del__(self):
        self.port.close()

if __name__ == "__main__":
    arduino = Arduino("Test")
    _exit = False
    while not _exit:
        cmd = input('Send Command: ')
        PY_LOGGER.info(cmd)
        if cmd == 'e':
            _exit = True
        else:
            arduino.send_str_data(cmd)
            sleep(.1)
            MCU_LOGGER.info(arduino.read_str_data())

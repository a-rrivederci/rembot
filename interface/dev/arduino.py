#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Arduino functionality
License is available in LICENSE
@author eeshiken
@since 2017-DEC-28
"""

import io
import serial

class Arduino(object):
    """ Rembot communication class """
    def __init__(self, ability, port):
        self.name = ability
        self.port = serial.Serial(port, 9600)

    def send_str_data(self, string):
        """ Send character string """
        self.port.write(string.encode('utf-8'))

    def read_str_data(self):
        """ read string """
        data = self.port.readline()
        return data.decode().rstrip()

    def read_num_data(self):
        """ Reads in numerical data from uno  """
        data = self.port.readline()
        return ord(data.decode().rstrip())
    def __del__(self):
        self.port.close()

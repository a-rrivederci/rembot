#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
LineBot ability allows rembot draw an image autonomously

License is available in LICENSE
@author eeshiken
@since 2017-DEC-28
"""


import time
import re

import cv2 as cv
import numpy as np
from math import floor

from .stats import Log
from .comms import Arduino

import serial.tools.list_ports
from PyQt5.QtCore import QObject, pyqtSignal


class Ability(QObject):
    ''' Rembot Ability class'''
    message = pyqtSignal(str) # messages to be passed to the core_ui
    end_FLAG = pyqtSignal() # signal to signify end thread FLAG
    start_time = 0
    assets_path = "interface/rembot/assets/"

    def __init__(self):
        super().__init__()
        self.log = Log(self) # initilize logging

    def process_done(self, ret):
        ''' 
        Signifies the end of a certain bot process 
        @ret 0 or 1 to see if process was killed or naturally ended
        '''
        if ret:
            self.message.emit("Aborting!")
        else:
            self.message.emit("--- %.1f seconds ---" %(time.time() - self.start_time))

class LineBot(Ability):
    ''' Processing and draws a halftone line image '''
    imgpath = None

    def connect(self):
        # Get likely arduino connection
        ret = 1
        seq = re.compile(r'COM[0-9]')
        ports = list(serial.tools.list_ports.comports())
        for portString in ports:
            # If uno is found in string
            if 'Arduino Uno' in str(portString):
                # Find out com port and connect
                port = seq.match(portString).group()
                self.arduino = Arduino(__class__, port)
                ret = 0    
        return ret

    def run(self):
        ''' Template for linebot '''
        if self.connect() == 0:
            self.message.emit("Connected!")
            self.start_time = time.time()
            ret = self.start()
            self.process_done(ret)
            self.end_FLAG.emit()
        else:
            self.message.emit("No ports available")
            self.end_FLAG.emit()
        return

    def start(self):
        ''' Start line bot process '''
        # process image
        halftoned_img = self.line_tone(self.imgpath, 2)
        # Send back output
        cv.imwrite(self.assets_path + "output.png")
        # create gcode
        gcode_list = ["G0\r\n", "G1 X10 Y0\r\n", "G0\r\n"]
        # Send code
        self.send_gcode(gcode_list)

    def line_tone(self, image, window):
        '''
        Converts image into line pattern
        img: (object) png/jpg image
        window: (int) window size
        '''
        
        tone = np.zeros((window, window), dtype=np.uint8)
        # Set all values to white
        # tone[tone == 0] = 255
        # Set horizontal avg as white
        tone[int(tone.shape[0]/2)] = 255

        # Convert image to grayscale
        gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        # Get size of source image
        height, width = gray_image.shape

        # Create new image
        haltone_img = np.zeros((height, width), np.uint8)

        window_pixels = np.zeros((window, window), dtype=np.uint8)

        # Transform to line tone
        for i in range(0, height-window, window):
            for j in range(0, width-window, window):
                # Get pixels from window
                for row, wrow in enumerate(range(i, i+window)):
                    for col, wcol in enumerate(range(j, j+window)):
                        try:
                            window_pixels[row, col] = gray_image[wrow, wcol]
                        except IndexError:
                            print(i, j,row, col, wrow, wcol)

                # Get window average
                saturation = np.sum(window_pixels) / (window*window)

                if saturation > 127:
                    pass
                elif saturation < 127:
                    haltone_img[i:i+window, j:j+window] = tone
            
        return haltone_img

    def send_gcode(self, gcode_list):
        '''
        Count down and end
        gcode_list: list of gcodes to be sent
        '''
        try:
            for code in gcode_list:
                while True:
                    # Read until firmware indicates ready '>'
                    _m = self.arduino.read_str_data()
                    if _m == '>':
                        break
                    else:
                        self.message.emit(_m)

                # Send string code
                self.arduino.send_str_data(code)

                # relax a bit yh
                time.sleep(.1)

                # wait to get 'S'
                while (self.arduino.read_str_data() != 'S'):
                    pass
                
        except Exception as _e:
            self.message.emit(str(_e))
            return 1

        return 0
    
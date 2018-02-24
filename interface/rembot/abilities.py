#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Paintbot ability allows rembot draw an image autonomously

License is available in LICENSE
@author eeshiken
@since 2017-DEC-28
"""


import time
from PyQt5.QtCore import QObject, pyqtSignal

from stats import Log
from comms import Arduino


class Ability(QObject):
    ''' Rembot Ability class'''
    message = pyqtSignal(str)
    finished = pyqtSignal()
    start_time = 0


    def __init__(self):
        super().__init__()
        self.log = Log(self)
        #self.arduino = Arduino('Paintbot')
        self.message.emit("Pairing Bot ...")

    def run_process(self):
        ''' start paint bot process '''
        self.start_time = time.time()
        for i in range(10):
            self.message.emit('Process %s'%i)
            time.sleep(1)
        self.process_done()
        self.finished.emit()

    def process_done(self, ret):
        ''' Signifies the end of a certain paintbot process '''
        if ret:
            self.message.emit("Aborting!")
        else:
            self.message.emit("--- %.1f seconds ---" %(time.time() - self.start_time))

class PaintBot(Ability):
    ''' Processing and painting an image '''

    def run_process(self):
        ''' start paint bot process '''
        self.start_time = time.time()
        ret = self.count_down()
        self.process_done(ret)
        self.finished.emit()

    def count_down(self):
        ''' Count down and end '''
        try:
            self.message.emit(self.arduino.title)

            for _ in range(3):
                self.arduino.send_str_data("c") # connect
                time.sleep(.1)
                self.message.emit("Connecting ...")
                time.sleep(.1)
                if self.arduino.read_str_data() == "C":
                    self.message.emit("Connected!")
                    break

            # Read countdown
            self.arduino.send_str_data('k') # countdown
            while 1:
                time.sleep(.1)
                data = self.arduino.read_str_data()
                self.message.emit(data)

                if data == 'DONE':
                    self.arduino.send_str_data('d')
                    time.sleep(.1)
                    self.arduino.read_str_data() # D
                    break

        except Exception as _e:
            self.message.emit(str(_e))
            return 1

        return 0

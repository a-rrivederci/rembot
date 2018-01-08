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

from system_status import Log


class Ability(QObject):
    ''' Rembot Ability class'''
    message = pyqtSignal(str)
    finished = pyqtSignal()
    start_time = 0

    def __init__(self):
        super().__init__()
        self.log = Log(self)

    def run_process(self):
        ''' start paint bot process '''
        self.start_time = time.time()
        for i in range(10):
            self.message.emit('Process %s'%i)
            time.sleep(1)
        self.process_done()
        self.finished.emit()

    def process_done(self):
        ''' Signifies the end of a certain paintbot process '''
        self.message.emit("--- %.1f seconds ---" %(time.time() - self.start_time))

class PaintBot(Ability):
    ''' Processing and painting an image '''

    def run_process(self):
        ''' start paint bot process '''
        self.start_time = time.time()
        for i in range(10):
            self.message.emit('Process Paint %s'%i)
            time.sleep(1)
        self.process_done()
        self.finished.emit()

class DrawBot(Ability):
    ''' Follows uses input '''

    def run_process(self):
        ''' start paint bot process '''
        self.start_time = time.time()
        for i in range(10):
            self.message.emit('Process Draw %s'%i)
            time.sleep(1)
        self.process_done()
        self.finished.emit()

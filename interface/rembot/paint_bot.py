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


class PaintBot(QObject):
    ''' Processing and painting an image '''
    message = pyqtSignal(str)
    finished = pyqtSignal()
    start_time = 0

    def __init__(self):
        super().__init__()
        self.log = Log(self, __name__)

    def run_process(self):
        ''' start paint bot process '''
        for i in range(10):
            self.message.emit('Process %s'%i)
            time.sleep(1)
        self.process_done()
        self.finished.emit()

    def process_done(self):
        ''' Signifies the end of a certain paintbot process '''
        self.message.emit("--- %s seconds ---" %(time.time() - self.start_time))

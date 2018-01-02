#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
License is available in LICENSE
@brief Rembot system status
@author eeshiken
@since 2017-JAN-01
"""

import io
import sys
import logging
from PyQt5.QtCore import pyqtSignal, QObject


class Log(QObject):
    log_data = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        
        root_logger = logging.getLogger("rembot")
        root_logger.setLevel(level=logging.INFO)
        self.logger_io = io.StringIO()
        log_handler = logging.StreamHandler(self.logger_io)
        log_formatter = logging.Formatter(
            fmt='%(asctime)s [%(name)s](%(levelname)s) %(message)s',
            datefmt='%H:%M:%S')
        log_handler.setFormatter(log_formatter)
        root_logger.addHandler(log_handler)

        self.logger = logging.getLogger("rembot.ui")

    def updateLog(self):
        ''' Update the program log data '''
        log = '' # initialize empty log string
        buffer = self.logger_io.getvalue() # get logger stream
        for i in buffer:  # Remove empty lines
            if i != '\n':
                log += i
        self.logger_io.truncate(0)
        self.logger_io.seek(0)
        print(log) # stdout
        return log
    
    def infoLog(self, msg):
        self.logger.info(msg)
        self.log_data.emit( self.updateLog() )

    def warningLog(self, msg):
        self.logger.warning(msg)
        self.log_data.emit( self.updateLog() )
    
    def errorLog(self, msg):
        self.logger.error(msg)
        self.log_data.emit( self.updateLog() )
    
    def __del__(self):
        self.logger_io.close()

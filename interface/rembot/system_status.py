#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Rembot system status reporting
License is available in LICENSE
@author eeshiken
@since 2017-JAN-01
"""

import io
import logging
from PyQt5.QtCore import pyqtSignal, QObject

class Log(QObject):
    ''' Logging class '''
    log_data = pyqtSignal(str)

    root_logger = logging.getLogger("rembot")
    root_logger.setLevel(level=logging.INFO)
    logger_io = io.StringIO()
    log_handler = logging.StreamHandler(logger_io)
    log_formatter = logging.Formatter(
        fmt='%(asctime)s [%(name)s](%(levelname)s) %(message)s',
        datefmt='%H:%M:%S')
    log_handler.setFormatter(log_formatter)
    root_logger.addHandler(log_handler)

    def __init__(self, parent):
        super().__init__(parent)
        self.logger = logging.getLogger("rembot." + parent.__class__.__name__)\

    def update_log(self):
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

    def info_log(self, msg):
        ''' Information logging '''
        self.logger.info(msg)
        self.log_data.emit(self.update_log())

    def warning_log(self, msg):
        ''' Warning message logging '''
        self.logger.warning(msg)
        self.log_data.emit(self.update_log())

    def error_log(self, msg):
        ''' Error message logging '''
        self.logger.error(msg)
        self.log_data.emit(self.update_log())

    def __del__(self):
        self.logger_io.close()

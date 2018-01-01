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


class Log(object):
    def __init__(self):
        root_logger = logging.getLogger("rembot")
        root_logger.setLevel(level=logging.INFO)
        self.logger_io = io.StringIO()
        log_handler = logging.StreamHandler(self.logger_io)
        log_formatter = logging.Formatter(
            fmt='%(asctime)s [%(name)s](%(levelname)s) %(message)s',
            datefmt='%H:%M:%S')
        log_handler.setFormatter(log_formatter)
        root_logger.addHandler(log_handler)
    
    def setLogger(self, name):
        return logging.getLogger("rembot." + name)

    def updateLog(self):
        ''' Update the program log screen '''
        log = '' # initialize empty log string
        buffer = self.logger_io.getvalue() # get logger stream
        for i in buffer:  # Remove empty lines
            if i != '\n':
                log += i
        self.logger_io.truncate(0)
        self.logger_io.seek(0)
        print(log) # stdout
        return log
    
    def displayInfoLog(self, object, output, msg):
        object.logger.warning(msg)
        output.log_output.append( self.updateLog() ) # interface log

    def displayWarningLog(self, object, output, msg):
        object.logger.warning(msg)
        output.log_output.append( self.updateLog() ) # interface log
    
    def displayErrorLog(self, object, output, msg):
        object.logger.error(msg)
        output.log_output.append( self.updateLog() ) # interface log

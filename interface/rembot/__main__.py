#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
License is available in LICENSE
@brief Rembot main program execution
@author eeshiken
@since 2017-DEC-28
"""

import sys
import logging
from PyQt5.QtWidgets import QMainWindow, QWidget, QDesktopWidget, QApplication, QMessageBox
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor


class MAIN(QMainWindow):
    
    def __init__(self):
        super().__init__()

        # Logging
        root_logger = logging.getLogger("rembot")
        root_logger.setLevel(level=logging.INFO)

        log_handler = logging.StreamHandler()
        log_formatter = logging.Formatter(
            fmt='%(asctime)s [%(name)s](%(levelname)s) %(message)s',
            datefmt='%H:%M:%S'
        )

        log_handler.setFormatter(log_formatter)
        root_logger.addHandler(log_handler)

        # local logger 
        self.logger = logging.getLogger("rembot.main")

        self.initUI()
    
    def initUI(self):    
        ''' Initiates application UI '''
        self.logger.info("REMBOT v0.0.1")
        
        self.rembot = Rembot(self)
        self.setCentralWidget(self.rembot)

        # Status messages
        self.statusbar = self.statusBar()        
        self.rembot.status_message[str].connect(self.statusbar.showMessage)
        
        self.resize(1700, 1200)
        self.center()
        self.setWindowTitle('Rembot')        
        self.show()
        
    def center(self):
        ''' Centers the window on the screen '''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)

    def closeEvent(self, event):
        ''' Close program dialog box '''
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            self.logger.info("Closing Program.")
        else:
            event.ignore()


class Rembot(QWidget):
    status_message = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.logger = logging.getLogger("rembot.ui")
    
        self.initRembotUI()
    
    def initRembotUI(self):
        ''' Rembot UI '''
        self.logger.info("Initializing REMBOT UI")
    
    def connect():
        ''' Connect to Rembot serial device '''

    def start():
        ''' Start image capturing sequence '''
    
    def pause():
        ''' Pause drawing execution '''
    
    def stop():
        ''' Stop image-processing or drawing '''
    
    def quit():
        ''' Quit program '''
    
    def updateStatus(self, msg):
        ''' Update the program statusbar string and log '''
        self.status_message.emit(str(msg))
        self.logger.info(msg)



if __name__ == '__main__':
    """ Run program """
    app = QApplication(sys.argv)
    main = MAIN()
    sys.exit(app.exec_())

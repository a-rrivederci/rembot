#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time, sys
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import (
    QApplication, QPushButton, QTextEdit, QWidget, QVBoxLayout
    )

class Thread(QThread):
    log = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Thread, self).__init__(parent)
        self._items = []

    def setItems(self, items):
        if not self.isRunning():
            self._items[:] = items

    def run(self):
        for item in self._items:
            time.sleep(1)
            self.log.emit('processing: %s' % item)

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui()
        self._worker = Thread(self)
        self._worker.log.connect(self.toLog)
        #self._worker.started.connect(lambda: self.toLog('start'))
        #self._worker.finished.connect(lambda: self.toLog('finished'))

    def process(self):
        items = ['Image%02d.png' % i for i in range(10)]
        self._worker.setItems(items)
        self._worker.start()

    def ui(self):
        self.LogOutputTxt = QTextEdit()
        self.LogOutputTxt.setReadOnly(True)
        startBtn = QPushButton('Start')
        startBtn.clicked.connect(self.start)
        layout = QVBoxLayout()
        layout.addWidget(self.LogOutputTxt)
        layout.addWidget(startBtn)
        self.setLayout(layout)
        self.resize(400, 300)
        self.show()

    def start(self):
        if not self._worker.isRunning():
            self.process()

    def toLog(self, txt):
        self.LogOutputTxt.append(txt)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Widget()
    sys.exit(app.exec_())
#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Rembot main program execution

License is available in LICENSE
@author eeshiken
@since 2017-DEC-28
"""

import sys
from PyQt5.QtWidgets import QApplication
from main_ui import MainUI


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    MAIN = MainUI()
    sys.exit(APP.exec_())

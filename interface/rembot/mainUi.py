#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
License is available in LICENSE
@brief MainUI
@author eeshiken
@since 2017-DEC-28
"""

import logging
from PyQt5.QtWidgets import ( QMainWindow, QDesktopWidget, 
    QApplication, QMessageBox, QSizePolicy, QMenu, QLayout, 
    QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QLineEdit, QGridLayout, 
    QPushButton, QTextBrowser, QAction )
from PyQt5.QtCore import Qt, QMetaObject, QCoreApplication, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap

from rembotUi import RembotUI


class MainUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        
        # Logging
        self.logger = self.RembotUI.log.setLogger(__name__) # set logger mainUi

    def initUI(self):
        ''' Initiates application UI '''
        # MainUI
        self.setObjectName('MainUI') 
        self.resize(1653, 1160)

        # Rembot ui class
        self.RembotUI = RembotUI(self)

        # Set central widget at RembotUI
        self.setCentralWidget(self.RembotUI)

        # Statusbar and Menubar
        # statusbar
        self.statusbar = self.statusBar()        
        self.RembotUI.status_message[str].connect(self.statusbar.showMessage)
        # meunbar
        self.menubar = self.menuBar()
        self.rembot_menu = QMenu(self.menubar)
        self.rembot_menu.setObjectName('rembot_menu')
        self.view_menu = QMenu(self.rembot_menu)
        self.view_menu.setObjectName("view_menu")
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        # meun actions
        self.action_exit = QAction(self)
        self.action_exit.setObjectName("action_exit")
        self.action_about = QAction(self)
        self.action_about.setObjectName("action_about")
        # view menu
        self.action_log = QAction(self)
        self.action_log.setCheckable(True)
        self.action_log.setChecked(True)
        self.action_log.setObjectName("action_log")
        # Add log action to view menu
        self.view_menu.addAction(self.action_log)
        # Add Rembot menu options
        self.rembot_menu.addAction(self.action_about) # about
        self.rembot_menu.addAction(self.view_menu.menuAction()) # view
        self.rembot_menu.addSeparator()
        self.rembot_menu.addAction(self.action_exit) # exit           
        # Add Rembot menu to MainUI Window
        self.menubar.addAction(self.rembot_menu.menuAction())


        # Set sizing
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        # Set Font
        font = QFont()
        font.setFamily("Lucida Console")
        self.setFont(font)
        # Set Icon
        icon = QIcon()
        icon.addPixmap(QPixmap("interface/rembot/assets/icon.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        # MainUI Styles
        self.setLayoutDirection(Qt.LeftToRight)
        self.setStyleSheet("")
        
        # Add text labelling
        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

        # Attach signals
        self.attachEvents()

        # Position and show Window
        self.center()       
        self.show()
    
    def retranslateUi(self):
        ''' UI Text '''
        _translate = QCoreApplication.translate
        self.setWindowTitle('Rembot')
        # Menubar
        self.rembot_menu.setTitle(_translate('MainUI', 'Rembot'))
        self.view_menu.setTitle(_translate('MainUI', 'View'))
        self.action_exit.setText(_translate('MainUI', 'Exit'))
        self.action_exit.setShortcut(_translate('MainUI', 'Ctrl+Q'))
        self.action_about.setText(_translate('MainUI', 'About'))
        self.action_about.setShortcut(_translate('MainUI', 'Ctrl+A'))
        self.action_log.setText(_translate('MainUI', 'Log'))
        self.action_log.setShortcut(_translate('MainUI', 'Ctrl+L'))

    def attachEvents(self):
        ''' Attach MainUI Ui events '''
        ## Menubar
        # self.action_about.triggered.connect()
        self.action_log.toggled['bool'].connect(self.RembotUI.log_box.setVisible)
        self.action_exit.triggered.connect(self.close)
        self.RembotUI.quit_button.clicked.connect(self.close)

    def center(self):
        ''' Centers the window on the screen '''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)

    def closeEvent(self, event):
        ''' Close program dialog box '''
        reply = QMessageBox.question(self, 'Exit ?',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

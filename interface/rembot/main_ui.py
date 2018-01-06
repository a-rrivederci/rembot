#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
MainUI methods
License is available in LICENSE
@author eeshiken
@since 2017-DEC-28
"""

from PyQt5.QtCore import QCoreApplication, QMetaObject, Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (QAction, QDesktopWidget, QMainWindow, QMenu,
                             QMessageBox, QSizePolicy)
from core_ui import CoreUI


class MainUI(QMainWindow):
    ''' Main UI class '''
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.core_ui.update_status("Initializing...") # status update

        self.log = self.core_ui.log
        self.log.info_log("Initializing...") # log
        self.log.info_log("REMBOT v0.0.1") # log

        self.core_ui.update_status("Ready") # status update

    def init_ui(self):
        ''' Initiates application UI '''
        # Rembot ui class
        self.core_ui = CoreUI(self)

        # Set central widget at CoreUI
        self.setCentralWidget(self.core_ui)

        # MainUI
        self.setObjectName('MainUI')
        self.resize(1653, 1160)

        # Statusbar and Menubar
        # statusbar
        self.statusbar = self.statusBar()
        self.core_ui.status_message[str].connect(self.statusbar.showMessage)
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
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        # Set Font
        font = QFont()
        font.setFamily("Lucida Console")
        self.setFont(font)
        # Set Icon
        icon = QIcon()
        icon_image = self.core_ui.images_path + "icon.png"
        icon.addPixmap(QPixmap(icon_image), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        # MainUI Styles
        self.setLayoutDirection(Qt.LeftToRight)
        self.setStyleSheet("")

        # Add text labelling
        self.retranslate_ui()
        QMetaObject.connectSlotsByName(self)

        # Attach signals
        self.attach_events()

        # Position and show Window
        self.center()
        self.show()

    def retranslate_ui(self):
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

    def attach_events(self):
        ''' Attach MainUI Ui events '''
        ## Menubar
        # self.action_about.triggered.connect()
        self.action_log.toggled['bool'].connect(self.core_ui.log_box.setVisible)
        #
        self.action_exit.triggered.connect(self.close)
        self.core_ui.quit_button.clicked.connect(self.close)

    def center(self):
        ''' Centers the window on the screen '''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    def closeEvent(self, event):
        ''' Close program dialog box '''
        self.log.info_log("Exit?") # log
        reply = QMessageBox.question(self, 'Exit ?', "Are you sure to quit?", \
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            self.log.info_log("Goodbye!") # log
        else:
            event.ignore()
            self.log.info_log("Exit Aborted!") # log

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
from PyQt5.QtWidgets import (QAction, QDesktopWidget, QMainWindow, QMenu, QMessageBox, QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout, QLabel)
from core_ui import CoreUI
from stats import Log


class MainUI(QMainWindow):
    ''' Main UI class '''
    def __init__(self):
        super().__init__()
        self.init_ui()

        self.core_ui.update_status("Initializing...") # status update

        # Log class
        self.log = Log(self) # sterr log
        self.log.log_data[str].connect(self.core_ui.to_log) # ui log

        self.log.info_log("Initializing...") # log
        self.log.info_log("REMBOT v2.0.0") # log

        self.core_ui.update_status("Ready") # status update

    def init_ui(self):
        ''' Initiates application UI '''
        self.init_classes()
        self.init_menu_and_statusbar()
        self.add_icon("library.png")
        self.bind_actions()
        self.attach_events()

        # Set central widget at CoreUI
        self.setCentralWidget(self.core_ui)

        # MainUI
        self.setObjectName('MainUI')

        # Add text labelling
        self.retranslate_ui()
        QMetaObject.connectSlotsByName(self)

        # Position and show Window
        self.center()
        self.show()

    def init_classes(self):
        # Rembot ui class
        self.core_ui = CoreUI(self)
        # about dialog
        self.about_dialog = AboutDialog()

    def init_menu_and_statusbar(self):
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

    def add_icon(self, file_name):
        icon = QIcon()
        icon_image = self.core_ui.assets_path + file_name
        icon.addPixmap(QPixmap(icon_image), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

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

    def bind_actions(self):
        '''  Bind menu actions '''
        # Add log action to view menu
        self.view_menu.addAction(self.action_log)
        # Add Rembot menu options
        self.rembot_menu.addAction(self.action_about) # about
        self.rembot_menu.addAction(self.view_menu.menuAction()) # view
        self.rembot_menu.addSeparator()
        self.rembot_menu.addAction(self.action_exit) # exit
        # Add Rembot menu to MainUI Window
        self.menubar.addAction(self.rembot_menu.menuAction())

    def attach_events(self):
        ''' Attach MainUI Ui events '''
        ## Menubar
        self.action_about.triggered.connect(self.open_about_window)
        self.action_log.toggled['bool'].connect(self.core_ui.log_box.setVisible)
        self.action_exit.triggered.connect(self.close)
        ## Buttons
        self.core_ui.quit_button.clicked.connect(self.close)
        ## Status messages
        self.core_ui.status_message[str].connect(self.statusbar.showMessage)

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

    def open_about_window(self):
        ''' Open about window '''
        self.about_dialog.show()

class AboutDialog(QWidget):
    ''' About Interface '''
    def __init__(self):
        super().__init__()
        self.setObjectName("AboutDialog")
        self.resize(849, 472)
        self.about_box = QVBoxLayout(self)
        self.about_box.setObjectName("about_box")
        self.about_system_label = QLabel()
        self.about_system_label.setAlignment(Qt.AlignCenter)
        self.about_system_label.setObjectName("about_system_label")
        self.about_box.addWidget(self.about_system_label)

        self.retranslate_ui()
        QMetaObject.connectSlotsByName(self)

    def retranslate_ui(self):
        ''' Text content '''
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("about_dialog", "Rembot v0.0.1"))
        self.about_system_label.setText(_translate("about_dialog", "REMBOT Interface\nv0.0.1"))

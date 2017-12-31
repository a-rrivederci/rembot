#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
License is available in LICENSE
@brief Rembot main program execution
@author eeshiken
@since 2017-DEC-28
"""

import logging
from PyQt5.QtWidgets import ( QMainWindow, QWidget, QDesktopWidget, 
    QApplication, QMessageBox, QSizePolicy, QMenu, QLayout, 
    QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QLineEdit, QGridLayout, 
    QPushButton, QTextBrowser )
from PyQt5.QtCore import Qt, pyqtSignal, QMetaObject, QCoreApplication, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap, QCursor


class Main(QMainWindow):
    
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
        # MAIN
        self.setObjectName('MAIN') 
        self.resize(1653, 1160)

        # Log Initialization
        self.logger.info("REMBOT v0.0.1") 

        # Rembot ui class
        self.rembot = RembotUI(self)

        # Set central widget at Rembot
        self.setCentralWidget(self.rembot)

        # Statusbar and Menubar
        # statusbar
        self.statusbar = self.statusBar()        
        self.rembot.status_message[str].connect(self.statusbar.showMessage)
        # meunbar
        self.menubar = self.menuBar()
        self.menubar.setObjectName('menubar')
        self.about = QMenu(self.menubar)
        self.about.setObjectName('about')
        self.setMenuBar(self.menubar)
        self.menubar.addAction(self.about.menuAction()) # add about action
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
        # MAIN Styles
        self.setLayoutDirection(Qt.LeftToRight)
        self.setStyleSheet("")

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)
        self.center()
        self.setWindowTitle('Rembot')        
        self.show()
    
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.about.setTitle(_translate("MAIN", "About"))
        
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
            self.logger.info("Closing Program.")
        else:
            event.ignore()

class RembotUI(QWidget):
    status_message = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.logger = logging.getLogger("rembot.ui")
    
        self.initRembotUI()
    
    def initRembotUI(self):
        ''' Rembot UI '''
        # Log Rembot UI initialization
        self.logger.info("Initializing REMBOT UI")
        self.setEnabled(True)
        self.setObjectName("RembotUI")

        # UI Contaier
        self.ui_container = QVBoxLayout(self)
        self.ui_container.setObjectName("ui_container")

        ## Header
        ### Box
        self.header_box = QHBoxLayout()
        self.header_box.setObjectName("header_box")
        self.header_box.setContentsMargins(10, 10, 10, 10)
        ### title
        font = QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(40)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.header_title = QLabel()
        self.header_title.setFont(font)
        self.header_title.setCursor( QCursor(Qt.ArrowCursor) )
        self.header_title.setLayoutDirection( Qt.LeftToRight )
        self.header_title.setStyleSheet("color: rgb(108, 204, 227);")
        self.header_title.setScaledContents(False)
        self.header_title.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.header_title.setContentsMargins(0, 0, 0, 0)
        self.header_title.setObjectName("header_title")
        self.header_box.addWidget(self.header_title) # add title to header
        ### version
        font = QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.version_number = QLabel()
        self.version_number.setFont(font)
        self.version_number.setStyleSheet("color: rgb(85, 85, 85);")
        self.version_number.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.version_number.setObjectName("version_number")
        self.header_box.addWidget(self.version_number) # add version number to header
        
        # Add to UI Container
        self.ui_container.addLayout(self.header_box) # add header box to layout

        # Content
        self.content_box = QHBoxLayout()
        self.content_box.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.content_box.setContentsMargins(10, 10, 10, 10)
        self.content_box.setObjectName("content_box")
        ## Left Box
        self.left_box = QVBoxLayout()
        self.left_box.setSizeConstraint(QLayout.SetFixedSize)
        self.left_box.setContentsMargins(10, 10, 10, 10)
        self.left_box.setObjectName("left_box")
        ### File box
        self.file_box = QHBoxLayout()
        self.file_box.setContentsMargins(10, 10, 10, 10)
        self.file_box.setObjectName("file_box")
        #### File label
        font = QFont()
        font.setPointSize(10)
        self.file_label = QLabel()
        self.file_label.setFont(font)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_label.sizePolicy().hasHeightForWidth())
        self.file_label.setSizePolicy(sizePolicy)
        self.file_label.setObjectName("file_label")
        ### Add label to File box
        self.file_box.addWidget(self.file_label)

        #### File Input
        font = QFont()
        font.setPointSize(20)
        self.file_input = QLineEdit()
        self.file_input.setFont(font)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_input.sizePolicy().hasHeightForWidth())
        self.file_input.setSizePolicy(sizePolicy)
        self.file_input.setMinimumSize(QSize(0, 0))
        self.file_input.setAcceptDrops(True)
        self.file_input.setLayoutDirection(Qt.LeftToRight)
        self.file_input.setText("")
        self.file_input.setFrame(True)
        self.file_input.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.file_input.setObjectName("file_input")
        #### Add File input to File box
        self.file_box.addWidget(self.file_input)

        ### Add File box to Left Box
        self.left_box.addLayout(self.file_box)

        #### Add Button box
        self.button_box = QGridLayout()
        self.button_box.setContentsMargins(10, 10, 10, 10)
        self.button_box.setObjectName("button_box")
        ##### Start Button
        self.start_button = QPushButton()
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
        self.start_button.setSizePolicy(sizePolicy)
        self.start_button.setObjectName("start_button")
        ##### Stop Button
        self.stop_button = QPushButton()
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stop_button.sizePolicy().hasHeightForWidth())
        self.stop_button.setSizePolicy(sizePolicy)
        self.stop_button.setObjectName("stop_button")
        ##### Test Button
        self.test_button = QPushButton()
        self.test_button.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.test_button.sizePolicy().hasHeightForWidth())
        self.test_button.setSizePolicy(sizePolicy)
        self.test_button.setObjectName("test_button")
        ##### Quit Button
        self.quit_button = QPushButton()
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quit_button.sizePolicy().hasHeightForWidth())
        self.quit_button.setSizePolicy(sizePolicy)
        self.quit_button.setObjectName("quit_button")
        #### Add Buttons to Button Box
        self.button_box.addWidget(self.start_button, 0, 0, 1, 1)
        self.button_box.addWidget(self.stop_button, 0, 1, 1, 1)
        self.button_box.addWidget(self.test_button, 1, 0, 1, 1)
        self.button_box.addWidget(self.quit_button, 1, 1, 1, 1)

        ### Add Button box to Left box
        self.left_box.addLayout(self.button_box)

        #### Log Box and Layout
        self.log_box = QGroupBox()
        self.log_box.setFlat(True)
        self.log_box.setObjectName("log_box")
        self.log_layout = QVBoxLayout(self.log_box)
        self.log_layout.setContentsMargins(0, 10, 0, 0)
        self.log_layout.setObjectName("log_layout")
        ##### Log output
        self.log_output = QTextBrowser(self.log_box)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.log_output.sizePolicy().hasHeightForWidth())
        self.log_output.setSizePolicy(sizePolicy)
        self.log_output.setObjectName("log_output")
        #### Add Log Output to Log box | Log layout
        self.log_layout.addWidget(self.log_output)
        ### Add Log box to Left box
        self.left_box.addWidget(self.log_box)

        ## Add Left box to Content box
        self.content_box.addLayout(self.left_box)

        ### Right Box
        self.right_box = QVBoxLayout()
        self.right_box.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.right_box.setContentsMargins(10, 10, 10, 10)
        self.right_box.setObjectName("right_box")
        #### Origninal image box
        self.original_img_box = QGroupBox()
        self.original_img_box.setFlat(True)
        self.original_img_box.setObjectName("original_img_box")
        self.original_img_layout = QVBoxLayout(self.original_img_box)
        self.original_img_layout.setContentsMargins(0, 0, 0, 0)
        self.original_img_layout.setObjectName("original_img_layout")
        ##### Original image
        self.original_img = QLabel(self.original_img_box)
        self.original_img.setText("")
        self.original_img.setPixmap(QPixmap("interface/rembot/assets/default.jpg"))
        self.original_img.setScaledContents(True)
        self.original_img.setObjectName("original_img")
        #### Add Original image to Original image Layout
        self.original_img_layout.addWidget(self.original_img)

        ### Add Original image box to Right box 
        self.right_box.addWidget(self.original_img_box)

        #### Output image box
        self.output_img_box = QGroupBox()
        self.output_img_box.setFlat(True)
        self.output_img_box.setObjectName("output_img_box")
        self.output_img_layout = QHBoxLayout(self.output_img_box)
        self.output_img_layout.setContentsMargins(0, 0, 0, 0)
        self.output_img_layout.setObjectName("output_img_layout")
        ##### Output image
        self.output_img = QLabel(self.output_img_box)
        self.output_img.setText("")
        self.output_img.setPixmap(QPixmap("interface/rembot/assets/default.jpg"))
        self.output_img.setScaledContents(True)
        self.output_img.setObjectName("output_img")
        #### Add Output img to output image layout
        self.output_img_layout.addWidget(self.output_img)

        ### Add Output image box to Right box
        self.right_box.addWidget(self.output_img_box)

        ## Add Right box to Content box
        self.content_box.addLayout(self.right_box)

        # Add Content box to UI Container
        self.ui_container.addLayout(self.content_box) # add content box to layout


        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)
        
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.header_title.setText(_translate("RembotUI", "REMBOT"))
        self.version_number.setText(_translate("RembotUI", ""))
        self.file_label.setText(_translate("RembotUI", "File name"))
        self.file_input.setPlaceholderText(_translate("RembotUI", "image.ext"))
        self.start_button.setText(_translate("RembotUI", "START"))
        self.stop_button.setText(_translate("RembotUI", "STOP"))
        self.test_button.setText(_translate("RembotUI", "TEST"))
        self.quit_button.setText(_translate("RembotUI", "QUIT"))
        self.log_box.setTitle(_translate("RembotUI", "Log"))
        self.original_img_box.setTitle(_translate("RembotUI", "Original Image"))
        self.output_img_box.setTitle(_translate("RembotUI", "Output Image"))

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


def run():
    """ Run program """
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())

if __name__ == '__main__':
    import sys
    run()
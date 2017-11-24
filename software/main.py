'''
 @title main.py
 @brief Rembot main program
 @authors AlvinHo Eeshiken
'''

import sys
import os.path
import time
import pygame
from pygame.locals import *
from pgu import gui
import util

bot = util.Bot("RembrandtBot")

def open_file_browser(arg):
    d = gui.FileDialog()
    d.connect(gui.CHANGE, handle_file_browser_closed, d)
    d.open()
    

def handle_file_browser_closed(dlg):
    if dlg.value: input_file.value = dlg.value

def take_pic(arg):
    global bot
    bot.start_capture()
    time.sleep(.5)

    assert os.path.isfile("images/capture.jpg")
    capture_pic.value = pygame.image.load("images/capture.jpg")
    capture_pic.reupdate()
    capture_pic.repaint()
    time.sleep(.5)
    picture_box.open()

def start_proc(arg):
    global bot
    #begin image processing
    assert os.path.isfile("images/capture.jpg")
    bot.start_processing("images/capture.jpg")
    assert os.path.isfile("images/target_image.png")
    # display image on interface
    raw_pic.value = pygame.image.load("images/target_image.png")
    raw_pic.reupdate()
    raw_pic.repaint()
    gen_cmds()

def gen_cmds():
    global bot
    time.sleep(1)
    bot.bot_gen_cmds() # generate commands

def decline_pic(arg):
    capture_pic.value = pygame.image.load("images/BlackBox.jpg")
    capture_pic.reupdate()
    capture_pic.repaint()

is_drawing = False

def sketch_act(arg):
	global is_drawing
	is_drawing = not is_drawing
	if is_drawing:
		start_button.value = "Pause"
	else:
		start_button.value = "Start"
	start_button.reupdate()
	start_button.repaint()

class QuitDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("Quit")
        
        t = gui.Table()
        
        t.tr()
        t.add(gui.Label("Are you sure you want to quit?"),colspan=2)
        
        t.tr()
        e = gui.Button("Okay")
        e.connect(gui.CLICK,self.send,gui.QUIT)
        t.td(e)
        
        e = gui.Button("Cancel")
        e.connect(gui.CLICK,self.close,None)
        t.td(e)
        
        gui.Dialog.__init__(self,title,t)

class PictureDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("Confirm")
        
        t = gui.Table()
        
        t.tr()
        t.add(gui.Label("Are you sure you want to use this picture?"),colspan=2)
        
        t.tr()
        e = gui.Button("Confirm")
        e.connect(gui.CLICK,self.close,None)
        e.connect(gui.CLICK,start_proc,None)
        t.td(e)
        
        e = gui.Button("Cancel")
        e.connect(gui.CLICK,decline_pic,None)
        e.connect(gui.CLICK,self.close,None)
        t.td(e)
        
        gui.Dialog.__init__(self,title,t)

# capture, sketch, pause,stop, setting
#######################################

app = gui.Desktop()
app.connect(gui.QUIT,app.quit,None)

WIDTH = 1000
HEIGHT = 800
space = 20

main = gui.Container(width=WIDTH, height=HEIGHT) #, background=(220, 220, 220) )

center_style = {'align': -1}
header = gui.Table(width=WIDTH-space*2)
header.tr()
header.td(gui.Label("Remnants of Rembrant", cls="h1"), align=0)
main.add(header, space, space)

picture_box = PictureDialog()
picture_box.connect(QUIT, decline_pic, None)

quit_box = QuitDialog()
quit_box.connect(QUIT,app.quit,None)

capture_button = gui.Button("Capture", width=150, height=30)
capture_button.connect(gui.CLICK, take_pic, None)

start_button = gui.Button("Start", width=150, height=30)
start_button.connect(gui.CLICK, sketch_act, None)

menu = gui.Table(width=(WIDTH-space*2)/2)
menu.tr()
menu.td(capture_button, height=35)#.connect(gui.CLICK, NeedAction, None)
menu.tr()
menu.td(start_button, height=35)
menu.tr()
menu.td(gui.Button("Stop", width=150, height=30), height=35)
menu.tr()
quit_button = gui.Button("Quit", width=150, height=30)
quit_button.connect(gui.CLICK, quit_box.open, None)
menu.td(quit_button)


capture_pic = gui.Image("images/BlackBox.jpg")
raw_pic = gui.Image("images/BlackBox.jpg")

td_style = {'padding_right': 10}
t = gui.Table(width=WIDTH-space)
t.tr()
t.td(capture_pic, align=0)
t.td(raw_pic, align=0)
t.tr()
t.td(gui.Label("Target"), valign=-1, align=0, height=50)
t.td(gui.Label("Raw"), valign=-1, align=0)
t.tr()
t.td(gui.Image("images/BlackBox.jpg"), align=0)
t.td(menu, align=0)
t.tr()
t.td(gui.Label("Progress"), valign=-1, align=0, height=50)


# t.td( gui.Label('File Name:') , style=td_style )
# input_file = gui.Input()
# t.td( input_file, style=td_style )
# b = gui.Button("Browse...")
# t.td( b, style=td_style )
# b.connect(gui.CLICK, open_file_browser, None)


main.add(t, space, 100)

app.run(main)
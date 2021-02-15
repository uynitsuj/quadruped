# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import sys
from ps4thread import PS4Thread
from pynput import keyboard
from IKEngin import Quadruped


class Visualizer(object):
    def __init__(self):
        global x, y, z, yaw, pitch, roll, cl, r
        r = x = y = z = yaw = pitch = roll = cl = 0
        self.robot = Quadruped(ax=self, origin=(0, 0, 100))
        self.traces = dict()
        self.app = QtGui.QApplication(sys.argv)
        self.w = gl.GLViewWidget()
        self.w.opts['distance'] = 700
        self.w.setWindowTitle('pyqtgraph Quadruped')
        self.w.setGeometry(0, 110, 1400, 1000)
        self.w.show()
        self.setup()

    def setup(self):
        gsz=400
        gsp=10
        gx = gl.GLGridItem(color=(255, 255, 255, 60))
        gx.setSize(gsz,gsz,gsz)
        gx.setSpacing(gsp,gsp,gsp)
        gx.rotate(90, 0, 1, 0)
        gx.translate(-gsz/2, 0, gsz/2)
        self.w.addItem(gx)
        gy = gl.GLGridItem(color=(255, 255, 255, 60))
        gy.setSize(gsz,gsz,gsz)
        gy.setSpacing(gsp,gsp,gsp)
        gy.rotate(90, 1, 0, 0)
        gy.translate(0, -gsz/2, gsz/2)
        self.w.addItem(gy)
        gz = gl.GLGridItem(color=(255, 255, 255, 100))
        gz.setSize(gsz,gsz,gsz)
        gz.setSpacing(gsp,gsp,gsp)
        self.w.addItem(gz)


    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def update(self):
        global x, y, z, yaw, pitch, roll, r, cl
        if cl:
            sys.exit(0)
        self.w.clear()
        self.setup()
        self.robot.shift_body_rotation(yaw, pitch, roll)
        self.robot.shift_body_translation(x, y, z)
        #self.robot.reset(r)
        self.robot.draw_body()
        pts = np.array([[-127.5, -110,0], [127.5, -110,0],[127.5, 110,0],[-127.5, 110,0]])
        self.w.addItem(gl.GLScatterPlotItem(pos=pts, color=pg.glColor((4, 5)), size=7))
        self.robot.draw_legs(pts)


    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(1)
        self.start()

#thread callback function
def my_callback(inp):
    global x, y, z, yaw, pitch, roll, r, cl
    yaw, pitch, roll, x, y, z, r, cl = inp
    pass
switch = 'x'
buffer = 0
inc = 5

#keyboard keypress event handler
def on_press(key):
    global switch, buffer, inc, x, y, z, yaw, pitch, roll, cl
    if key == keyboard.Key.esc:
        cl = 1
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['1']:
        x = y = z = yaw = pitch = roll = 0
    if k in ['x']:
        switch = 'x'
    if k in ['y']:
        switch = 'y'
    if k in ['z']:
        switch = 'z'
    if k in ['a']:
        switch = 'a'
    if k in ['p']:
        switch = 'p'
    if k in ['r']:
        switch = 'r'
    if k in ['w']:
        buffer = inc
    if k in ['s']:
        buffer = -inc
    if k in ['w', 's']:
        if switch == 'x':
            x += buffer
        if switch == 'y':
            y += buffer
        if switch == 'z':
            z += buffer
        if switch == 'a':
            yaw += buffer*np.pi/180
        if switch == 'p':
            pitch += buffer*np.pi/180
        if switch == 'r':
            roll += buffer*np.pi/180

if __name__ == '__main__':
    t = 1
    while t:
        num_in = input("Enter 1 for PS4 Joystick Control, or 2 for Keyboard Control: \n")
        if num_in == '1':
            #start joystick listener thread
            cthread = PS4Thread(my_callback)
            t = 0
        elif num_in == '2':
            #start keyboard listener thread
            cthread = keyboard.Listener(on_press=on_press)
            print("Controls: use x, y, z, a, p, r to select",
            " \n(x axis, y axis, z axis, yaw, pitch, roll),\n",
            " and then use 'w' or 's' buttons to increment",
            " or decrement the selected position. \nIf you click '1' on ",
            "your keyboard, it will reset the position.\nIf you click",
            " 'esc' on your keyboard, you will close the visualization")
            print("Use Mouse+Scroll Wheel+Arrow Keys to move camera view")
            cthread.start()
            t = 0
        else:
            pass
    v = Visualizer()
    v.animation()
    cthread.join()

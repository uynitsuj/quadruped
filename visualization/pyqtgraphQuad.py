# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import sys
from IKEngin import Quadruped
from pyPS4Controller.controller import Controller
import threading
import struct

class Visualizer(object):
    def __init__(self):
        global x, y, z, yaw, pitch, roll, r
        r = x = y = z = yaw = pitch = roll = 0
        self.robot = Quadruped(ax=self, origin=(0, 0, 100))
        self.traces = dict()
        self.app = QtGui.QApplication(sys.argv)
        self.w = gl.GLViewWidget()
        self.w.opts['distance'] = 40
        self.w.setWindowTitle('pyqtgraph Quadruped')
        self.w.setGeometry(0, 110, 1920, 1080)
        self.w.show()
        self.setup()

    def setup(self):
        gsz=400
        gx = gl.GLGridItem()
        gx.setSize(gsz,gsz,gsz)
        gx.setSpacing(10,10,10)
        gx.rotate(90, 0, 1, 0)
        gx.translate(-gsz/2, 0, gsz/2)
        self.w.addItem(gx)
        gy = gl.GLGridItem()
        gy.setSize(gsz,gsz,gsz)
        gy.setSpacing(10,10,10)
        gy.rotate(90, 1, 0, 0)
        gy.translate(0, -gsz/2, gsz/2)
        self.w.addItem(gy)
        gz = gl.GLGridItem()
        gz.setSize(gsz,gsz,gsz)
        gz.setSpacing(10,10,10)
        self.w.addItem(gz)


    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def update(self):
        global x, y, z, yaw, pitch, roll, r
        self.w.clear()
        self.setup()
        self.robot.shift_body_rotation(yaw, pitch, roll)
        self.robot.shift_body_translation(x, y, z)
        #self.robot.reset(r)
        #self.robot.IK(1,(115,-85,0))
        #self.robot.IK(2,(115, 85,0))
        self.robot.draw_body()
        pts = np.array([[-115, -85,0], [115, -85,0],[115, 85,0],[-115, 85,0]])
        self.w.addItem(gl.GLScatterPlotItem(pos=pts, color=pg.glColor((4, 5)), size=5))
        self.robot.draw_legs(pts)


    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(1)
        self.start()


class PS4Thread(threading.Thread):

    def __init__(self, input_cbk = None, name='ps4-input-thread'):
        self.input_cbk = input_cbk
        super(PS4Thread, self).__init__(name=name)
        self.start()

    def run(self):
        global x, y, z, yaw, pitch, roll, r
        file = open("/dev/input/js0", "rb")
        while True:
            event = file.read(struct.calcsize("3Bh2b"))
            (*tv_sec, value, button_type, button_id) = struct.unpack("3Bh2b", event)
            self.input_cbk(button_id) #waits to get input + Return
            #print("Button_Type: ", button_type)
            #print("Button_Value: ", value)
            if (button_id == 1 and button_type == 2):
                pitch = value/150000
            if (button_id == 0 and button_type == 2):
                yaw = -value/70000
                #print("L3_y_axis val:", value)
            if (button_id == 5 and button_type == 2):
                roll = -(value+32767)/140000
            if (button_id == 2 and button_type == 2):
                roll = (value+32767)/140000
            if (button_id == 3 and button_type == 2):
                y = value/500
            if (button_id == 4 and button_type == 2):
                x = value/500
            if (button_id == 7 and button_type == 2):
                if value == 32767:
                    z -= 10
                if value == -32767:
                    z += 10
            if (button_id == 0 and button_type == 1 and value == 1):
                r = 1
                z = 0
            if (button_id == 0 and button_type == 1 and value == 0):
                r = 0
            #if (button_id == )

def my_callback(inp):
    #evaluate the keyboard input
    #print('Button_ID: ', inp)
    pass

if __name__ == '__main__':
    kthread = PS4Thread(my_callback)
    v = Visualizer()
    v.animation()

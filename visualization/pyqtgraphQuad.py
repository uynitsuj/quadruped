# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import sys
from ps4thread import PS4Thread
from IKEngin import Quadruped


class Visualizer(object):
    def __init__(self):
        global x, y, z, yaw, pitch, roll
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
        self.w.addItem(gl.GLScatterPlotItem(pos=pts, color=pg.glColor((4, 5)), size=7))
        self.robot.draw_legs(pts)


    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(1)
        self.start()

def my_callback(inp):
    global x, y, z, yaw, pitch, roll
    yaw, pitch, roll, x, y, z = inp
    pass

if __name__ == '__main__':
    cthread = PS4Thread(my_callback)
    v = Visualizer()
    v.animation()

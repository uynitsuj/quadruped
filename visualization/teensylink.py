from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import sys
from ps4thread import PS4Thread
from IKEngin import Quadruped
import serial
import time

serialcomm = serial.Serial('/dev/ttyACM0', 115200, timeout = 0)
serialcomm.bytesize = serial.EIGHTBITS
serialcomm.parity = serial.PARITY_NONE
serialcomm.stopbits = serial.STOPBITS_ONE
serialcomm.timeout = 2
time.sleep(2)


class Visualizer(object):
    def __init__(self):
        global x, y, z, yaw, pitch, roll, cl, r, count
        count = r = x = y = z = yaw = pitch = roll = cl = 0
        self.robot = Quadruped(ax=self, origin=(0, 0, 100))
        self.r2 = Quadruped(ax=self, origin=(0, 0, 100))
        self.px = x
        self.py = y
        self.pz = z
        self.pyaw = yaw
        self.ppitch = pitch
        self.proll = roll
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
        global x, y, z, yaw, pitch, roll, r, cl, count
        count+=1
        del self.w.items [:]
        if cl:
            sys.exit(0)
        self.w.clear()
        self.setup()
        pts = np.array([[-127.5, -110,0], [127.5, -110,0],[127.5, 110,0],[-127.5, 110,0]])
        self.r2.shift_body_rotation(yaw, pitch, roll, 0)
        self.r2.shift_body_translation(x, y, z, 0)
        self.r2.draw_legs(pts, 0)
        if self.r2.flag == 1:
            x = self.px
            y = self.py
            z = self.pz
            yaw = self.pyaw
            pitch = self.ppitch
            roll = self.proll
            self.r2.flag = 0
        else:
            self.robot.shift_body_rotation(yaw, pitch, roll, 1)
            self.robot.shift_body_translation(x, y, z, 1)
            self.px = x
            self.py = y
            self.pz = z
            self.pyaw = yaw
            self.ppitch = pitch
            self.proll = roll
        #self.robot.reset(r)
        self.robot.draw_body()
        #self.w.addItem(gl.GLScatterPlotItem(pos=pts, color=pg.glColor((4, 5)), size=7))
        self.robot.draw_legs(pts, 1)
        FRHM = '#FRHM' + str(-self.robot.joint_angles[1][0]*250/np.pi + 100)
        #print(-self.robot.joint_angles[0][0]*250/np.pi + 100)
        serialcomm.write((FRHM + '\n').encode())
        FRSM = '#FRSM' + str(-self.robot.joint_angles[1][1]*210/np.pi+210)
        #print(-self.robot.joint_angles[0][1]*180/np.pi+200)
        serialcomm.write((FRSM + '\n').encode())
        FRWM = '#FRWM' + str(self.robot.joint_angles[1][2]*200/np.pi+30)
        #print(self.robot.joint_angles[0][2]*180/np.pi+50)
        serialcomm.write((FRWM + '\n').encode())

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
inc = 20

if __name__ == '__main__':
    t = 1
    while t:
        #start joystick listener thread
        cthread = PS4Thread(my_callback)
        t = 0

    v = Visualizer()
    v.animation()
    cthread.join()

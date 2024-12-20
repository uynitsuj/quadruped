import threading
import struct
import sys
from IKEngin import Quadruped
import numpy as np
import serial
import time

class QThread(threading.Thread):
    def __init__(self, input_cbk = None, name='quadruped-thread'):
        self.input_cbk = input_cbk
        super(QThread, self).__init__(name=name)
        self.daemon = True
        time.sleep(2)
        self.r1 = Quadruped(ax=self, origin=(0, 0, 100))
        self.r2 = Quadruped(ax=self, origin=(0, 0, 100))
        self.start()

    def run(self):
        serialcomm = serial.Serial('/dev/ttyACM0', 115200, timeout = 0)
        serialcomm.bytesize = serial.EIGHTBITS
        serialcomm.parity = serial.PARITY_NONE
        serialcomm.stopbits = serial.STOPBITS_ONE
        serialcomm.timeout = 2
        while True:
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
                self.r1.shift_body_rotation(yaw, pitch, roll, 1)
                self.r1.shift_body_translation(x, y, z, 1)
                self.px = x
                self.py = y
                self.pz = z
                self.pyaw = yaw
                self.ppitch = pitch
                self.proll = roll
            print(roll, " ", pitch, " ", yaw, " ", x, " ", y, " ", z)
            #self.robot.reset(r)
            #self.robot.draw_body()
            #self.w.addItem(gl.GLScatterPlotItem(pos=pts, color=pg.glColor((4, 5)), size=7))
            #self.robot.draw_legs(pts, 1)
            BRHM = '#BRHM' + str(-self.robot.joint_angles[0][0]*250/np.pi + 85)
            serialcomm.write((BRHM + '\n').encode())
            BRSM = '#BRSM' + str(-self.robot.joint_angles[0][1]*210/np.pi+197)
            serialcomm.write((BRSM + '\n').encode())
            BRWM = '#BRWM' + str(self.robot.joint_angles[0][2]*198/np.pi+17)
            serialcomm.write((BRWM + '\n').encode())

            BLHM = '#BLHM' + str(int(255-(self.robot.joint_angles[3][0]*250/np.pi + 80)))
            serialcomm.write((BLHM + '\n').encode())
            BLSM = '#BLSM' + str(int(255-(-self.robot.joint_angles[3][1]*210/np.pi+190)))
            serialcomm.write((BLSM + '\n').encode())
            BLWM = '#BLWM' + str(int(255-(self.robot.joint_angles[3][2]*198/np.pi+30)))
            serialcomm.write((BLWM + '\n').encode())

            FLHM = '#FLHM' + str(int(255-(self.robot.joint_angles[2][0]*250/np.pi + 80)))
            serialcomm.write((FLHM + '\n').encode())
            FLSM = '#FLSM' + str(int(255-(-self.robot.joint_angles[2][1]*210/np.pi+200)))
            serialcomm.write((FLSM + '\n').encode())
            FLWM = '#FLWM' + str(int(255-(self.robot.joint_angles[2][2]*198/np.pi+20)))
            serialcomm.write((FLWM + '\n').encode())

            FRHM = '#FRHM' + str(-self.robot.joint_angles[1][0]*250/np.pi + 85)
            serialcomm.write((FRHM + '\n').encode())
            FRSM = '#FRSM' + str(-self.robot.joint_angles[1][1]*210/np.pi+215)
            serialcomm.write((FRSM + '\n').encode())
            FRWM = '#FRWM' + str(self.robot.joint_angles[1][2]*198/np.pi+32)
            serialcomm.write((FRWM + '\n').encode())



import numpy as np
import sys
import threading
from IKEngin2 import Quadruped
from ps4thread import PS4Thread
import serial
import time

serialcomm = serial.Serial('/dev/ttyACM0', 115200, timeout = 0)
serialcomm.bytesize = serial.EIGHTBITS
serialcomm.parity = serial.PARITY_NONE
serialcomm.stopbits = serial.STOPBITS_ONE
serialcomm.timeout = 2

class QThread(threading.Thread):
    def __init__(self, input_cbk = None, name='quadruped-thread'):
        global x, y, z, yaw, pitch, roll, cl, r, count
        count = r = x = y = z = yaw = pitch = roll = cl = 0
        self.input_cbk = input_cbk
        super(QThread, self).__init__(name=name)
        self.daemon = True
        time.sleep(2)
        self.r1 = Quadruped(ax=self, origin=(25, 0, 70))
        self.r2 = Quadruped(ax=self, origin=(25, 0, 70))
        self.px = x
        self.py = y
        self.pz = z
        self.pyaw = yaw
        self.ppitch = pitch
        self.proll = roll
        self.start()

    def run(self):
        
        while True:
            global x, y, z, yaw, pitch, roll, r, cl, count
            count+=1
            if cl:
                sys.exit(0)
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
            #self.r1.draw_legs()
            #print(roll, " ", pitch, " ", yaw, " ", x, " ", y, " ", z)
            #self.r1.reset(r)
            self.r1.draw_body()
            #self.w.addItem(gl.GLScatterPlotItem(pos=pts, color=pg.glColor((4, 5)), size=7))
            self.r1.draw_legs(pts, 1)
            
            BRHM = '#BRHM' + str(-self.r1.joint_angles[0][0]*250/np.pi + 85)
            serialcomm.write((BRHM + '\n').encode())
            BRSM = '#BRSM' + str(-self.r1.joint_angles[0][1]*210/np.pi+197)
            serialcomm.write((BRSM + '\n').encode())
            BRWM = '#BRWM' + str(self.r1.joint_angles[0][2]*198/np.pi+17)
            serialcomm.write((BRWM + '\n').encode())

            BLHM = '#BLHM' + str(int(255-(self.r1.joint_angles[3][0]*250/np.pi + 80)))
            serialcomm.write((BLHM + '\n').encode())
            BLSM = '#BLSM' + str(int(255-(-self.r1.joint_angles[3][1]*210/np.pi+190)))
            serialcomm.write((BLSM + '\n').encode())
            BLWM = '#BLWM' + str(int(255-(self.r1.joint_angles[3][2]*198/np.pi+30)))
            serialcomm.write((BLWM + '\n').encode())

            FLHM = '#FLHM' + str(int(255-(self.r1.joint_angles[2][0]*250/np.pi + 80)))
            serialcomm.write((FLHM + '\n').encode())
            FLSM = '#FLSM' + str(int(255-(-self.r1.joint_angles[2][1]*210/np.pi+200)))
            serialcomm.write((FLSM + '\n').encode())
            FLWM = '#FLWM' + str(int(255-(self.r1.joint_angles[2][2]*198/np.pi+20)))
            serialcomm.write((FLWM + '\n').encode())
            
            FRHM = '#FRHM' + str(-self.r1.joint_angles[1][0]*250/np.pi + 85)
            serialcomm.write((FRHM + '\n').encode())
            FRSM = '#FRSM' + str(-self.r1.joint_angles[1][1]*210/np.pi+215)
            serialcomm.write((FRSM + '\n').encode())
            FRWM = '#FRWM' + str(self.r1.joint_angles[1][2]*198/np.pi+32)
            serialcomm.write((FRWM + '\n').encode())

def ctlr_callback(inp):
    global x, y, z, yaw, pitch, roll, r, cl
    yaw, pitch, roll, x, y, z, r, cl = inp
    pass
switch = 'x'
buffer = 0
inc = 20

def quadruped_callback(inp):
    global x, y, z, yaw, pitch, roll, r, cl
    yaw, pitch, roll, x, y, z, r, cl = inp
    pass

if __name__ == '__main__':
    t = 1
    while t:
        #start joystick listener thread
        cthread = PS4Thread(ctlr_callback)
        rthread = QThread(quadruped_callback)
        t = 0

    cthread.join()
    rthread.join()

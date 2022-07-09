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


#thread callback function
def ctlr_callback(inp):
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
        cthread = PS4Thread(ctlr_callback)
        t = 0

    cthread.join()
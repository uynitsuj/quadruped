import threading
import struct
import sys


class PS4Thread(threading.Thread):

    def __init__(self, input_cbk = None, name='ps4-input-thread'):
        self.input_cbk = input_cbk
        super(PS4Thread, self).__init__(name=name)
        self.daemon = True
        self.start()

    def run(self):
        r = x = y = z = yaw = pitch = roll = cl = 0
        try:
            file = open("/dev/input/js0", "rb")
        except:
            print("No PS4 Controller found")
            r = x = y = z = yaw = pitch = roll = 0
            cl = 1
            self.input_cbk((yaw, pitch, roll, x, y, z, r, cl))
            exit(1)
        print("Controls: \nL Joystick X: yaw\nL Joystick Y: pitch\nR Joystick X: translate body left/right\nR Joystick Y: translate body forward/backward\nL Bumper: roll body\nR Bumper: roll body\nDPad up: translate body up\nDPad down: translate body down\nCircle: close visualization")
        print("Use Mouse+Scroll Wheel+Arrow Keys to move camera view")
        while True:
            #Joystick event handler
            event = file.read(struct.calcsize("3Bh2b"))
            (*tv_sec, value, button_type, button_id) = struct.unpack("3Bh2b", event)
            if (button_id == 1 and button_type == 2):
                pitch = -value/150000
            if (button_id == 0 and button_type == 2):
                yaw = -value/70000
            if (button_id == 5 and button_type == 2):
                roll = (value+32767)/140000
            if (button_id == 2 and button_type == 2):
                roll = -(value+32767)/140000
            if (button_id == 3 and button_type == 2):
                y = -value/500
            if (button_id == 4 and button_type == 2):
                x = -value/500
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
            if (button_id == 1 and button_type == 1 and value == 1):
                cl = 1
            self.input_cbk((yaw, pitch, roll, x, y, z, r, cl))
            #print(yaw, " ", pitch, " ", roll, " ", x, " ", y, " ", z, " ", r, " ", cl)
            file.flush()

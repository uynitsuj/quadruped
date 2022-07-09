import threading
import struct
import sys
import numpy as np

class QThread(threading.Thread):
    def __init__(self, input_cbk = None, name='quadruped-thread'):
        self.input_cbk = input_cbk
        super(QThread, self).__init__(name=name)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            



#!/usr/bin/python


import math
import random
import socket
import time

ip = "localhost"
#ip = "114.116.82.53"

class DBConn:
    def __init__(self, port):
        self.port = port
        self.connect()

    def connect(self):
        self.socket = socket.socket()
        self.socket.connect((ip, self.port))

    def send(self, data):
        try:
            if not self.socket:
                self.connect()
            self.socket.send("put " + data + "\n")
            print data
        except socket.error:
            self.socket.close()
            self.socket = None


s1 = DBConn( 4460)

def contruct_time_and_value(value, scale):

    return "%10d " % time.time() + "%1.3f" % ((value + 0.7) * scale * random.uniform(0.9, 1))

x = 0.0
y = 0.0
scale_x = 0.0
scale_y = 1.0
while True:
    y_ = y
    y = math.sin(x)
    data = "temperature " + contruct_time_and_value(math.sin(x), scale_y, 1.6)
    s1.send(data)
    data = "temperature " + contruct_time_and_value(math.sin(x), scale_y)
    x += 0.7
    if y_ < 0 and y > 0:
        scale_x += 0.05
        scale_y = (math.cos(scale_x) + 2) * 30
    time.sleep(1)


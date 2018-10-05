#!/usr/bin/python

import Tkinter
import tkMessageBox
import os
from threading import Thread

from bottle import request, run, post

root = Tkinter.Tk()
root.withdraw()

level_up = 0

@post('/facetime')
def hello():
    global level_up

    if request.json["state"] != "alerting":
        return

    os.system('open /Users/yunxinwu/Documents/face_time_voice_ywu_first_item.app')
    level_up = 0
    tkMessageBox.showwarning("Warning", "Reduced speed of the equipment!")

@post('/raise')
def hello():
    global level_up
    level_up = 400

def data_gen():
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
    s2 = DBConn(14460)

    #s1 = DBConn(4242)
    #s2 = DBConn(4242)

    def contruct_time_and_value(value, scale, factor=1):
        level_up_local = 0

        if factor != 1:
            level_up_local = level_up
            scale = scale * factor

        return "%10d " % time.time() + "%1.3f" % ((value + 0.7) * scale * random.uniform(0.9, 1) + level_up_local)

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
        s2.send(data)
        data =    "pressure " + contruct_time_and_value(math.cos(x), scale_y, 1.6)
        s1.send(data)
        data =    "pressure " + contruct_time_and_value(math.cos(x), scale_y)
        s2.send(data)
        x += 0.7
        if y_ < 0 and y > 0:
            scale_x += 0.05
            scale_y = (math.cos(scale_x) + 2) * 30
        time.sleep(1)

thread = Thread(target = data_gen)
thread.start()
run(host='localhost', port=4461, debug=True)

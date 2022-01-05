#!/usr/bin/env python3

import time
import math
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
t=0

while True:
    linear = 100
    angular = 50 * math.sin(math.radians(t))
    t+=1

    left = (linear + angular) * 1024 / 138
    right = (linear - angular) * 1024 / 138
    msg = "{},{},{}\r".format(left,
                              right,
                              0)
    sock.sendto(str.encode(msg), ('192.168.247.103', 4210))
    time.sleep(1/150)

from setup import *
import PingPi
import socket
import os
import time
import math
from datetime import datetime
import netifaces as ni

ni.ifaddresses('br0')
IPAddr = ni.ifaddresses('enp2s0')[ni.AF_INET][0]['addr']

# os.system('setup.py')
# hostname = socket.gethostname()
# IPAddr = socket.gethostbyname(hostname)

old = 0
now = datetime.now()
current_time_H = now.strftime("%H")
current_time_M = now.strftime("%M")

time_per_set = 60/N #from setup

while int(current_time_H)<=100 :
    now = datetime.now()
    current_time_H = now.strftime("%H")
    current_time_M = now.strftime("%M")
    current_set=math.floor(int(current_time_M)/time_per_set)
    if (old != current_time_H) :
        for i in range(0,len(S[current_set])) :
            if IPAddr == S[current_set][i][0] :
               PingPi.ton(S[current_set][i][0],S[current_set][i][1],Name[current_set][i])
               old = current_time_H

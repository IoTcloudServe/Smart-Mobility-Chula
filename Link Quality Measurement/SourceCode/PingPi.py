from pythonping import ping
import socket
from datetime import datetime
import math
import csv
import time
import netifaces as ni

def ton(A,B,C) :
    file = []
    for i in range (0,100) :
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S:%f")
        current_time_M = now.strftime("%M")
        x = ping(B, size=56, count=1)
        file.append([C,A,B,current_time,x.rtt_avg_ms])
        time.sleep(1)
#print('testping:')

    with open(str(C)+'_'+str(current_time)+'.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(file)
    csvFile.close()
    #print("save")

#str(current_time_M)+C+'test.csv',

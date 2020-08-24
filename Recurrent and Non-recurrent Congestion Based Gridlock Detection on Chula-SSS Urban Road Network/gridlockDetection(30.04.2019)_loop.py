import os, sys

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
sys.path.append(os.path.join('c:', os.sep, 'whatever', 'path', 'to', 'sumo', 'tools'))

import traci
import sumolib
import numpy as np
import csv
import pathlib
import glob
import math
import matplotlib.pyplot as plt
import pandas as pd
import lxml.etree as ET
from xml.etree import ElementTree
import xml.etree.cElementTree as eleTree

from datetime import datetime
import time

import numpy as np

sumoBinary = sumolib.checkBinary('sumo-gui')
#sumoBinary = sumolib.checkBinary('sumo') # to run without sumo gui


sumoCmd = [sumoBinary,
           "--no-internal-links",'true', #true
           "--ignore-junction-blocker",'-1',
            '--start','true',
           '--quit-on-end','true',
           #"--random",'true',
           "-c", "sathorn_w.sumo.cfg",
           #'-a',"sathon_wide_tls_20160418_edited.add(smallPOI).xml",
           '-a',"sathon_wide_tls_20160418_edited.add(LargePOI)_extendDetectorLength.xml",
           #'-a',"sathon_wide_tls_20160418_edited.add(LargePOI)_extendDetectorLength_upstream_100m.xml",
           '--time-to-teleport',"-1",
           #'--step-length', '2',
           #'--seed',"23423"
           '--seed',"10"
           ]

#sumoCmd = [sumoBinary, "-c", "sathorn_w.sumo.cfg",'-a',"sathon_wide_tls_20160418_edited.add.xml",'--time-to-teleport',"-1"]
#sumoCmd = [sumoBinary, "-c", "sathorn_w.sumo.cfg"]
traci.start(sumoCmd)

POIEdges1={
          'L30':'99.68',
          'L10059':'537.99',
          'L58#1':'371.54',
          'L58#2':'13.43',
          'L60':'104.34',
          'L73':'159.19',
          'L10149#1':'88.09',
          'L10149#2':'13.48',
          'L138':'112.16',
          'L133.25':'118.71',
          'L10130':'246.38',
          #'L49':'271.31',
          'L10189':'171.59',
          #'L179':'313.44',
          #'L10188':'282.95',
          #'L64':'277.38',
          #'L10032':'161.93',
          #'L40':'515.18',
          #'L30032':'339.44',
          #'L135':'98.77',
          #'L140#2':'78.13',
          #'L197#2':'68.75'
          }
#=======================================================================================
def createFile1(detDicionary):
    #to get the current directory
    dirpath = os.getcwd()

    for k,v in detDicionary.items():
        csvForEachEdgeID=open(dirpath+'/CSVData_forLoop/'+k+'.csv','w',newline='')
        writer=csv.writer(csvForEachEdgeID)
        writer.writerow(["Time","Edge","EdgeLength","JamLength","Density","MeanSpeed","MeanOccupancy","Status"])
    loopcsv=open(dirpath+'/CSVData_forLoop/loopCSV.csv','w',newline='')
    writer=csv.writer(loopcsv)
    writer.writerow(["Time","EdgeLength","JamLength","Density","MeanSpeed","MeanOccupancy","Status"])
#=======================================================================================


#main function
def main():
    step = 21600
    detDicionary=groupDetector()
    createFile1(detDicionary)
    while step< 32400: # 32400
        traci.simulationStep()
        retrieveData(detDicionary)
        #print('================================================================================')
        step += 1
    traci.close()

#==========================================================================================


def retrieveData(detDicionary):
    #this code segment is trying to detect the number of vehicles on each edge from detectors via traci online
    #===================================================================================================
    cursimtime = traci.simulation.getCurrentTime()/1000
        #print(cursimtime)
    loopLength=0
    jamLoop=0
    densityLoop=0
    meanspeedLoop=0
    meanOccupancyLoop=0

    allState=[]

    for key, value in detDicionary.items():#key is Edge ID and values are det list on the Edge
        detList_inEachEdge=value
        jamlengthinMeter=0
        density=0
        weighted_meanSpeed=0
        meanOccupancy=0
        #print(detList_inEachEdge)
        for det in detList_inEachEdge:
            lanelength = traci.lane.getLength(det)
            jamlengthinMeter+=traci.lanearea.getJamLengthMeters(det)
            density+=traci.lanearea.getLastStepVehicleNumber(det)
            weighted_meanSpeed+=float(traci.lanearea.getLastStepMeanSpeed(det))* int(traci.lanearea.getLastStepVehicleNumber(det))
            meanOccupancy+=traci.lanearea.getLastStepOccupancy(det)

        jamlengthinMeter=jamlengthinMeter/len(detList_inEachEdge)
        density= density/len(detList_inEachEdge)
        weighted_meanSpeed= weighted_meanSpeed/len(detList_inEachEdge)
        meanOccupancy= meanOccupancy/len(detList_inEachEdge)


        loopLength+=lanelength
        jamLoop+=jamlengthinMeter
        densityLoop+=density
        meanspeedLoop+=weighted_meanSpeed
        meanOccupancyLoop+=meanOccupancy

        dirpath = os.getcwd()
        path=dirpath+'/CSVData_forLoop/*.csv'
        files=glob.glob(path)

        #check road state
        if key=='L58#2' or 'L10149#2':
            condition1=0.40*lanelength
        else:
            condition1=0.80*lanelength
        #condition2 = 0.40 * lanelength
        if (jamlengthinMeter > condition1  and (weighted_meanSpeed >= 0 and weighted_meanSpeed <= (
                                5 / 3.6))):

            state="1"  # congested
            #print(laneID,jamlengthinMeter,meanSpeed,state)
            allState.append(1)
        else:
            state="0" # free flow
            allState.append(0)
            #print(laneID, jamlengthinMeter, meanSpeed, state)


        print(key)
        for name in files:
            if(name==dirpath+'/CSVData_forLoop\\'+str(key)+'.csv'):
                file=open(name,'a',newline='')
                writer = csv.writer(file)
                with file:
                    writer.writerow([cursimtime,key,lanelength,jamlengthinMeter,density,weighted_meanSpeed, meanOccupancy,state])
                file.close()
                break

        #writeFile(cursimtime,key,lanelength,jamlengthinMeter,density,weighted_meanSpeed, meanOccupancy)


    condition=all(state == 1 for state in allState)
    if(condition== True):
        loopState=1
    else:
        loopState = 0
    writeLoopData(cursimtime,loopLength,jamLoop,densityLoop,meanspeedLoop, meanOccupancyLoop,loopState)
    #===================================================================================================




def writeLoopData(cursimtime,loopLength,jamLoop,densityLoop,meanspeedLoop, meanOccupancyLoop,loopState):
    dirpath = os.getcwd()
    file=open(dirpath+'/CSVData_forLoop/loopCSV.csv','a',newline='')
    writer = csv.writer(file)
    with file:
        writer.writerow([cursimtime,loopLength,jamLoop,densityLoop,meanspeedLoop, meanOccupancyLoop,loopState])
    file.close()




#this code segment is trying to group e2 detectors
#========================================================================================
def groupDetector():
    detlist = traci.lanearea.getIDList()
    detDicionary={}
    det_in_eachCluster=[]

    for detID in detlist:
        laneID=traci.lanearea.getLaneID(detID)#to get lane ID of detector
        edgeID=traci.lane.getEdgeID(laneID)#to get the edge ID of detector via laneID

        if(len(detDicionary))==0: #new entry with new key and value
            det_in_eachCluster.append(detID)
            detDicionary[edgeID]=det_in_eachCluster

        else:# not new entry but old key and new value
            det_in_eachCluster=[]

            if(detDicionary.__contains__(edgeID)):
                oldlist= detDicionary.get(edgeID)
                if detID not in oldlist:
                    detDicionary[edgeID].append(detID)

            else: # not new entry but new key and value
                det_in_eachCluster.append(detID)
                detDicionary[edgeID]=det_in_eachCluster
    '''
    for key,value in detDicionary.items():
        print(key,value)
    '''
    return detDicionary
#========================================================================================


#this function is to get the time string like h:m:s
#=======================================================================================
def getTime(time):
    time=time%(24*3600)
    hours=time//3600
    time%=3600
    minutes=time//60
    time%=60
    seconds=time
    periods=[('hours',int(hours)),('minutes',int(minutes)),('seconds',int(seconds))]
    time_string=':'.join('{}'.format(value) for name,value in periods)
    return time_string

#========================================================================================



if __name__=="__main__":
    main()


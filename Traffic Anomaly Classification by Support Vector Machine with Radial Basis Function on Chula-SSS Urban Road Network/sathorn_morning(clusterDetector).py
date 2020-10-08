import os, sys

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
sys.path.append(os.path.join('c:', os.sep, 'whatever', 'path', 'to', 'sumo', 'tools'))

import traci
import sumolib
import csv
import pathlib
import glob

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from datetime import datetime, timedelta
from pandas import DataFrame
from pandas import concat

import glob
import lxml.etree as ET
import xml.etree.cElementTree as eleTree

import operator # this library is for sorting dictionary
sumoBinary = sumolib.checkBinary('sumo-gui')
sumoCmd = [sumoBinary,
           "--no-internal-links",'true',
           "--ignore-junction-blocker",'1',
           '--start','false',
           '--quit-on-end','false',
           #"--random",'true',
           "-c", "sathorn_w.sumo.cfg",
           #'-a',"sathon_wide_tls_20160418_edited.add(cover_wholeLane)_withoutLaneclose.xml",
           '-a',"sathon_wide_tls_20160418_edited.add(cover_wholeLane)_withLaneClose_20mins.xml",
           '--time-to-teleport',"-1",
           '--seed',"50",
           #'--no-warnings','true'
           ]

#sumoCmd = [sumoBinary, "-c", "sathorn_w.sumo.cfg",'-a',"sathon_wide_tls_20160418_edited.add.xml",'--time-to-teleport',"-1"]
#sumoCmd = [sumoBinary, "-c", "sathorn_w.sumo.cfg"]
traci.start(sumoCmd)

# initialization of POIlanes
POIlanes={1:['L179_0'],
          2:['L10188_0'],
          3:['L10130_0','L10130_1','L10130_2','L10130_3'],#'L10130_0',
          4:['L49_0','L49_1','L49_2'],
          5:['L10189_0','L10189_1','L10189_2','L10189_3'],#'L10189_0',
          6:['L239_0','L239_1','L239_2','L239_3'],
          7:['L249_0','L249_1','L249_2','L249_3'],
          8:['L232_0','L232_1','L232_2','L232_3'],
          9:['L10009_0','L10009_1','L10009_2'],
          10:['L60_0','L60_1'],
          11:['L73_0','L73_1'],
          12:['L10149#1_0','L10149#1_1'],
          13:['L10149#2_1','L10149#2_2'],#,'L10149#2_0'
          14:['L138_0','L138_1','L138_2'],
          15:['L133.25_0','L133.25_1','L133.25_2','L133.25_3'],
          16:['L135_0','L135_1','L135_2'],
          17:['L140#1_0','L140#1_1','L140#1_2'],
          18:['L140#2_3'],
          19:['L64_1','L64_2','L64_3'],
          20:['L10032_0'],
          21:['L40493_0','L40493_1','L40493_2','L40493_3'],
          22:['L30_0','L30_1','L30_2','L30_3'],
          23:['L72_0','L72_1','L72_2','L72_3'],
          #24:['L10059_0'],
          24:['L58#1_0','L58#1_1']
          }

POIEdges=['L179','L10188','L10130','L49','L10189','L239','L249','L232','L10009','L60','L73','L10149#1',
            'L10149#2','L138','L133.25','L135','L140#1','L140#2','L64','L10032','L40493','L30','L72','L58#1']



#to setup e2 Detectors in xml file by code
#========================================================================================
'''
root = ET.Element('additionals')

for key,value in POIlanes.items():
    for laneid in value:
        len_Of_lane=traci.lane.getLength(laneid)
        initial_Pos=0.00
        subelement=ET.Element('e2Detector')
        subelement.set('id',laneid)
        subelement.set('lane',laneid)
        subelement.set('pos',str(initial_Pos))
        subelement.set('length',str(len_Of_lane))
        subelement.set('freq','120.00')
        subelement.set('file','output/Alle2Detector.xml')
        subelement.set('cont','0')
        subelement.set('timeThreshold','1.00')
        subelement.set('speedThreshold','1.39')
        subelement.set('jamThreshold','10.00')
        root.append(subelement)

tree=ET.ElementTree(root)
filename="sathon_morning_Great_e2.add.xml"
tree.write(filename, xml_declaration=True,pretty_print=True)'''
#========================================================================================




#this code segment is trying to group e2 detectors
#========================================================================================

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

'''for key,value in detDicionary.items():
    print(key,value)'''
#========================================================================================




#1. to create respective output files for each edge
#========================================================================================

for key,value in detDicionary.items():
    myfile = open('csvOutputUsingDetector/'+str(key)+'.csv', 'w',newline='')
    writer = csv.writer(myfile)
    writer.writerow(["Time","Edge ID","Edge Length","Jam Length","Density","Mean Speed","Mean Occupancy","Road State"])

#========================================================================================






#2. to create respective output files for each edge
#========================================================================================

for edge in POIEdges:
    myfile = open('csvOutputNotUsingDetector/'+edge+'.csv', 'w',newline='')
    writer = csv.writer(myfile)
    writer.writerow(["Time","Travel Time","Mean Speed","Occupancy","Density"])
#========================================================================================



# to get the traffic light IDs
#========================================================================================
tlsList=[]
tlsList=traci.trafficlight.getIDList()
#print(len(tlsList))

controlLanes=[]
controlLinks=[]

for tlsID in tlsList:
    controlLanes=traci.trafficlight.getControlledLanes(tlsID)
    controlLinks=traci.trafficlight.getControlledLinks(tlsID)
    '''print('***************** controlled lanes of '+tlsID+' ************************')
    for laneID in controlLanes:
        print(laneID)'''
    print('***************** controlled links of '+tlsID+' ************************')
    for laneID in controlLinks:
        print(laneID)
    controlLanes=[]
    controlLinks=[]
#========================================================================================




#This function is to write output to each detector file
#========================================================================================

def writeFile(cursimtime,edgeID,lanelength,jamlengthinMeter,density,meanSpeed, meanOccupancy):


    path='csvOutputUsingDetector/*.csv'
    files=glob.glob(path)

    #check road state
    condition1=0.95*lanelength
    condition2 = 0.40 * lanelength
    if (jamlengthinMeter > condition1 ):

        state="2"  # congested
        #print(laneID,jamlengthinMeter,meanSpeed,state)

    elif (meanSpeed < 2.0 and (condition2<= jamlengthinMeter <= condition1)):
        state="1" # moderate
        #print(laneID, jamlengthinMeter, meanSpeed, state)

    else:
        state="0" # free flow
        #print(laneID, jamlengthinMeter, meanSpeed, state)

    for name in files:

        if(name=='csvOutputUsingDetector\\'+edgeID+'.csv'):

            file=open(name,'a',newline='')
            writer = csv.writer(file)
            with file:
                writer.writerow([cursimtime,edgeID,lanelength,jamlengthinMeter,density,meanSpeed, meanOccupancy,state])
            file.close()

            break

#========================================================================================




#main functin
def main():
    #when I try to stop vehicle before starting the simulation, I face the error  like Vehicle 43.0 is not known
    #traci.vehicle.setStop('43.0',edgeID='L10189',laneIndex=1,pos=100,startPos=50,duration=600);
    step = 21600
    while step< 32400:
        traci.simulationStep()

        #this is trying to stop vehicle
        #===================================================================================================
        '''
        if(step==21600):
            traci.vehicle.setStop('5.0', edgeID='L10130', laneIndex=2,pos=50,duration=1200);
            routeID=traci.vehicle.getRouteID('5.0')
            roadID=traci.vehicle.getRoadID('5.0')
            print('vid 5.0 :'+routeID,roadID)
            print('========================================')
        if(step==22500):
            traci.vehicle.setStop('94.0', edgeID='L10130', laneIndex=2,pos=50,duration=1200);
            routeID=traci.vehicle.getRouteID('94.0')
            roadID=traci.vehicle.getRoadID('94.0')
            print('vid 94.0 :'+routeID,roadID)
            print('========================================')
        if(step==23400):
            traci.vehicle.setStop('168.0', edgeID='L10130', laneIndex=2,pos=50,duration=1200);
            routeID=traci.vehicle.getRouteID('168.0')
            roadID=traci.vehicle.getRoadID('168.0')
            print('vid 168.0 :'+routeID,roadID)
            print('========================================')
        if(step==24300):
            traci.vehicle.setStop('242.0', edgeID='L10130', laneIndex=2,pos=50,duration=1200);
            routeID=traci.vehicle.getRouteID('242.0')
            roadID=traci.vehicle.getRoadID('242.0')
            print('vid 242.0 :'+routeID,roadID)
            print('========================================')
        '''
        #===================================================================================================


        '''
        #this code segment is trying to detect the number of vehicles on each edge from detectors via traci online
        #===================================================================================================
        cursimtime = getTime(traci.simulation.getCurrentTime()/1000)
            #print(cursimtime)

        for key, value in detDicionary.items():#key is Edge ID and values are det list on the Edge
            detList_inEachEdge=value
            jamlengthinMeter=0
            density=0
            meanSpeed=0
            meanOccupancy=0
            #print(detList_inEachEdge)
            for det in detList_inEachEdge:


                lanelength = traci.lane.getLength(det)
                jamlengthinMeter+=traci.lanearea.getJamLengthMeters(det)
                density+=traci.lanearea.getLastStepVehicleNumber(det)
                meanSpeed+=traci.lanearea.getLastStepMeanSpeed(det)
                meanOccupancy+=traci.lanearea.getLastStepOccupancy(det)

            jamlengthinMeter=jamlengthinMeter/len(detList_inEachEdge)
            #density= density/len(detList_inEachEdge)
            meanSpeed= meanSpeed/len(detList_inEachEdge)
            meanOccupancy= meanOccupancy/len(detList_inEachEdge)

            writeFile(cursimtime,key,lanelength,jamlengthinMeter,density,meanSpeed, meanOccupancy)

        #===================================================================================================




        #this code segment is trying to get the information of POIEdges via traci online
        #===================================================================================================
        density=0
        meanSpeed=0
        travelTime=0
        Occupancy=0
        for edge in POIEdges:

            travelTime=traci.edge.getTraveltime(edge)
            meanSpeed=traci.edge.getLastStepMeanSpeed(edge)
            Occupancy=traci.edge.getLastStepOccupancy(edge)
            density=traci.edge.getLastStepVehicleNumber(edge)

            path='csvOutputNotUsingDetector/*.csv'
            files=glob.glob(path)
            for name in files:

                if(name=='csvOutputNotUsingDetector\\'+edge+'.csv'):

                    file=open(name,'a',newline='')
                    writer = csv.writer(file)
                    with file:
                        writer.writerow([cursimtime,travelTime,meanSpeed,Occupancy,density])
                    file.close()

                    break
        #===================================================================================================
        '''
        step += 1
    traci.close()




#this function is to get the time string like h:m:s
#========================================================================================

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


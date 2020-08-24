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

import plotly
from plotly.offline import init_notebook_mode
import plotly.graph_objs as go
plotly.offline.init_notebook_mode(connected=True)
from datetime import datetime
import time


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
           #'-a',"sathon_wide_tls_20160418_edited.add(LargePOI)_extendDetectorLength.xml",
           '-a',"sathon_wide_tls_20160418_edited.add(LargePOI)_extendDetectorLength_upstream_100m.xml",
           '--time-to-teleport',"-1",
           #'--step-length', '2',
           #'--seed',"23423"
           '--seed',"10"
           ]

#sumoCmd = [sumoBinary, "-c", "sathorn_w.sumo.cfg",'-a',"sathon_wide_tls_20160418_edited.add.xml",'--time-to-teleport',"-1"]
#sumoCmd = [sumoBinary, "-c", "sathorn_w.sumo.cfg"]
traci.start(sumoCmd)

POIEdges={
          'L49':'271.31',
          'L10189':'171.59',
          'L179':'313.44',
          'L10188':'282.95',
          'L10130':'246.38',
          'L64':'277.38',
          'L133.25':'118.71',
          'L138':'112.16',
          'L10149#1':'88.09',
          'L10149#2':'13.48',
          'L58#1':'371.54',
          'L58#2':'13.43',
          'L10032':'161.93',
          'L30':'99.68',
          'L40':'515.18',
          'L30032':'339.44',
          'L135':'98.77',
          'L140#2':'78.13',
          'L197#2':'68.75'
          }

cluster={
'cluster_185_186':['L58#2','L30032'],
'cluster_159_32_6_7':['L138'],
'cluster_43_44':['L133.25','L49','L64'],
'cluster_46_47':['L40','L197#2','L10189'],
'cluster_83_84':['L10149#2']
                }

POICluster=['cluster_185_186','cluster_159_32_6_7','cluster_43_44','cluster_46_47','cluster_83_84']

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

#====================================================================
def setUpLaneAreaDetector():

    root = ET.Element('additionals')
    net = sumolib.net.readNet('sathorn_w_fixed_20160404.net.xml')

    for key,value in POIEdges.items():
        edgeID = net.getEdge(key)
        numOfLane=edgeID.getLaneNumber()
        edgeLength=edgeID.getLength()
        for lane_index in range(numOfLane):
            initial_Pos=0.00
            subelement=ET.Element('e2Detector')
            subelement.set('id',key+'_'+str(lane_index))
            subelement.set('lane',key+'_'+str(lane_index))
            subelement.set('pos',str(initial_Pos))
            subelement.set('endPos','0.00')
            subelement.set('friendlyPos','True')
            subelement.set('length',str(edgeLength))
            subelement.set('freq','2.00')
            subelement.set('file','output/Alle2Detector.xml')
            subelement.set('cont','0')
            subelement.set('timeThreshold','1.00')
            subelement.set('speedThreshold','1.39')
            subelement.set('jamThreshold','10.00')

            root.append(subelement)

    tree=ET.ElementTree(root)
    filename="sathon_morning_Great_e2.add.xml"
    tree.write(filename, xml_declaration=True,pretty_print=True)


#====================================================================


# retrieving controlled lanes and controlled links from traffic light IDs
#========================================================================================
def getControlledLaneAndLinks():
    tlsList=[]
    #tlsList=traci.trafficlights.getIDList()
    #print(len(tlsList)) # there are 10 intersections in our Sathorn model

    tls_Cluster={}
    controlLanes=[]
    controlLinks=[]

    for tlsID in POICluster:

        Lanes=traci.trafficlights.getControlledLanes(tlsID)
        #print(Lanes)
        for lane in Lanes:
            if lane not in controlLanes:
                controlLanes.append(lane)
        #controlLinks=traci.trafficlights.getControlledLinks(tlsID)
        '''
        print('***************** controlled lanes of '+tlsID+' ************************')
        for laneID in controlLanes:
            print(laneID)


        print('***************** controlled links of '+tlsID+' ************************')
        for laneID in controlLinks:
            print(laneID)
        '''
        tls_Cluster[tlsID] = [controlLanes, traci.trafficlights.getControlledLinks(tlsID)]
    '''
    for key,value in tls_Cluster.items():
        #print(key,value[0])
        print(key,value[1])
        print('=======================================================')
    '''
    return tls_Cluster
#========================================================================================


#=======================================================================================
def createFile1():
    #to get the current directory
    dirpath = os.getcwd()
    detDicionary=groupDetector()
    for k,v in detDicionary.items():
        csvForEachEdgeID=open(dirpath+'/CSVData/'+k+'.csv','w',newline='')
        writer=csv.writer(csvForEachEdgeID)
        writer.writerow(["Time","ClusterID","Upstream","LaneLength","Downstream","UpstreamJamLength","UpstreamMeanSpeed","DownstreamJamLength","DownstreamMeanSpeed","TLS","Status"])
#=======================================================================================


#main function
def main():
    #setUpLaneAreaDetector()
    detDicionary=groupDetector()
    step = 21600

    createFile1() # to create file for each link
    createFile3() # to keep for flow

    while step< 32400: # 32400
        traci.simulationStep()
        #stateForEachDetector=retrieveForEachDetector()
        retrieveForEachDetector(detDicionary)
        flow_in_criticalRegion()
        #print(stateForEachDetector)
        #print('================================================================================')
        step += 1
    traci.close()

    createFile2()
    detection()
    plotClusterCongestion()
    plotClusterMeanSpeed()
    plot_ClusterCongestionState()
    #plotCongestion_withMatplot()
    plot_flow_inCriticalRegion()

#==========================================================================================

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


def retrieveForEachDetector(detDicionary):
    #to retrieve control traffic light cluster by given laneID
    tls_Cluster= getControlledLaneAndLinks()
    stateForEachDetector={}
    detlist = traci.lanearea.getIDList()


    #print(len(detlist)) # 41
    dirpath = os.getcwd()
    path=dirpath+'/CSVData/*.csv'
    files=glob.glob(path)
    dummy_dictionary={}
    for key,value in tls_Cluster.items():
        control_links=value[1]
        rygstate=traci.trafficlights.getRedYellowGreenState(key) # rgy state for each cluster
        #print(key,control_links)

        detector_list_1=[]
        detector_list_2=[]

        for control_link in control_links: # for each control link that are controlled by cluster

            #print(control_link)

            for links in control_link: # each control link has tuple (upstream,downstream, clusterID)

                #print(links)
                #print('******************')
                # L133 is too short, it is replaced by L133.25
                #==============================================
                lst = list(links) # change tuple to list
                if lst[1]=='L133_0': lst[1]='L133.25_2'
                if lst[1]=='L133_1': lst[1]='L133.25_3'
                links=tuple(lst)
                #==============================================


                det_key= [x for x in detDicionary.keys()]
                detectors=[x for x in detDicionary.values()]

                #print(det_key,detectors)

                if links[0]in detlist and links[1] in detlist:


                    # this code block is to combine only upstream detectors because some upstream's length has less than 50 meters
                    # so, to cover 50 m we set up detectors on two consecutive lanes such as L58#2_1 and L58#1_0
                    #====================================================================================
                    extra_weighted_meanSpeed_1=0.00
                    extra_weighted_meanSpeed_2=0.00
                    extra_weighted_meanSpeed_3=0.00

                    extra_jamlength_1=0.00
                    extra_jamlength_2=0.00
                    extra_jamlength_3=0.00

                    if links[0]=='L58#2_1':
                        extra_weighted_meanSpeed_1= (int(traci.lanearea.getLastStepVehicleNumber ('L58#1_0')) *\
                                            float(traci.lanearea.getLastStepMeanSpeed ('L58#1_0')))+\
                                            (int(traci.lanearea.getLastStepVehicleNumber ('L58#1_1')) *\
                                            float(traci.lanearea.getLastStepMeanSpeed ('L58#1_1')))

                        extra_jamlength_1=float(traci.lanearea.getJamLengthMeters('L58#1_0')) +\
                                            float(traci.lanearea.getJamLengthMeters('L58#1_1'))

                    if links[0]=='L10149#2_1':
                        extra_weighted_meanSpeed_2= (int(traci.lanearea.getLastStepVehicleNumber ('L10149#1_0')) *\
                                            float(traci.lanearea.getLastStepMeanSpeed ('L10149#1_0')))+\
                                            (int(traci.lanearea.getLastStepVehicleNumber ('L10149#1_1')) *\
                                            float(traci.lanearea.getLastStepMeanSpeed ('L10149#1_1')))

                        extra_jamlength_2=float(traci.lanearea.getJamLengthMeters('L10149#1_0')) +\
                                            float(traci.lanearea.getJamLengthMeters('L10149#1_1'))

                    if links[0]=='L197#2_1':
                        extra_weighted_meanSpeed_3= (int(traci.lanearea.getLastStepVehicleNumber ('L197#1_0')) *\
                                            float(traci.lanearea.getLastStepMeanSpeed ('L197#1_0')))+\
                                            (int(traci.lanearea.getLastStepVehicleNumber ('L197#1_1')) *\
                                            float(traci.lanearea.getLastStepMeanSpeed ('L197#1_1')))+\
                                             (int(traci.lanearea.getLastStepVehicleNumber ('L197#1_2')) *\
                                            float(traci.lanearea.getLastStepMeanSpeed ('L197#1_2')))+\
                                             (int(traci.lanearea.getLastStepVehicleNumber ('L197#1_3')) *\
                                            float(traci.lanearea.getLastStepMeanSpeed ('L197#1_3')))


                        extra_jamlength_3=float(traci.lanearea.getJamLengthMeters('L197#1_0')) +\
                                            float(traci.lanearea.getJamLengthMeters('L197#1_1'))+\
                                        float(traci.lanearea.getJamLengthMeters('L197#1_2')) +\
                                            float(traci.lanearea.getJamLengthMeters('L197#1_3'))

                    extra_length=0.00
                    if links[0]=='L58#2_1':
                        extra_length = float(traci.lane.getLength('L58#1_0'))
                    if links[0]=='L10149#2_1':
                        extra_length = float(traci.lane.getLength('L10149#1_0'))
                    if links[0]=='L197#2_1':
                        extra_length = float(traci.lane.getLength('L197#1_0'))
                    #====================================================================================


                    # this code block is to sum up occupancy for upstream (links[0]) and downstream (links[1])
                    #====================================================================================
                    laneID_1=traci.lanearea.getLaneID(links[0])#to get lane ID of detector
                    edgeID_1=traci.lane.getEdgeID(laneID_1)#to get the edge ID of detector via laneID
                    lanelength = float(traci.lane.getLength(links[0]))+extra_length
                    index_1= det_key.index((edgeID_1))
                    detector_list_1= detectors[index_1]
                    upstreamJamLength=0.00
                    for d in detector_list_1:
                        upstreamJamLength+=float(traci.lanearea.getJamLengthMeters(d))
                    upstreamJamLength=math.ceil((upstreamJamLength+extra_jamlength_1+extra_jamlength_2+extra_jamlength_3)/int(len(detector_list_1)))


                    upstream_weighted_meanSpeed=0.00
                    for d in detector_list_1:
                        #print(traci.lanearea.getLastStepVehicleNumber (d))
                        #print(traci.lanearea.getLastStepMeanSpeed(d))
                        #print('*************************************')
                        upstream_weighted_meanSpeed+=int(traci.lanearea.getLastStepVehicleNumber (d)) *\
                                            float(traci.lanearea.getLastStepMeanSpeed (d))
                    upstream_weighted_meanSpeed=(upstream_weighted_meanSpeed+extra_weighted_meanSpeed_1+extra_weighted_meanSpeed_2+extra_weighted_meanSpeed_3)/int(len(detector_list_1))



                    laneID_2=traci.lanearea.getLaneID(links[1])#to get lane ID of detector
                    edgeID_2=traci.lane.getEdgeID(laneID_2)#to get the edge ID of detector via laneID
                    index_2= det_key.index((edgeID_2))
                    detector_list_2= detectors[index_2]
                    downstreamJamLength=0.00
                    for d in detector_list_2:
                         downstreamJamLength+=float(traci.lanearea.getJamLengthMeters(d))
                    downstreamJamLength=math.ceil(downstreamJamLength/int(len(detector_list_2)))

                    downstream_weighted_meanSpeed = 0.00
                    for d in detector_list_2:
                        downstream_weighted_meanSpeed += int(traci.lanearea.getLastStepVehicleNumber (d)) *\
                                            float(traci.lanearea.getLastStepMeanSpeed (d))
                    downstream_weighted_meanSpeed = downstream_weighted_meanSpeed / int(len(detector_list_2))
                    #====================================================================================

                    index=control_links.index(control_link)
                    current_tls=rygstate[index] # current traffic state of control link
                    cur_time=int(traci.simulation.getCurrentTime()/1000)
                    #cur_time=getTime(float(traci.simulation.getCurrentTime()/1000))
                    #cur_time = (datetime.strptime(str(cur_time),'%H:%M:%S')).time() # to save time in datatime format

                    #print(edgeID_1,detector_list_1)
                    #print(edgeID_2,detector_list_2)

                    '''
                    # 1. upstream==> speed, downstream ==> speed
                    if ((current_tls != 'r') and (upstream_weighted_meanSpeed >= 0 and upstream_weighted_meanSpeed <= (
                            5 / 3.6))and ((downstream_weighted_meanSpeed >= 0 and downstream_weighted_meanSpeed <= (
                            5 / 3.6)))):
                        status = 1  # gridlock
                    else:
                        status = 0  # no gridlock

                    # 2. upstream==> speed, downstream ==> jam
                    if ((current_tls != 'r') and (upstream_weighted_meanSpeed >= 0 and upstream_weighted_meanSpeed <= (
                            5 / 3.6))and downstreamJamLength > (0.80 * 50)):
                        status = 1  # gridlock
                    else:
                        status = 0  # no gridlock
                    
                    # 3. upstream ==> speed, downstream ==> (speed +jam)
                    if ((current_tls != 'r') and (upstream_weighted_meanSpeed >= 0 and upstream_weighted_meanSpeed <= (
                            5 / 3.6))and (downstreamJamLength > (0.80 * 50) and (downstream_weighted_meanSpeed >= 0 and downstream_weighted_meanSpeed <= (
                            5 / 3.6)))):
                        status = 1  # gridlock
                    else:
                        status = 0  # no gridlock
                    
                    # 4. upstream ==> jam , downstream ==> speed
                    if ((current_tls != 'r' ) and (upstreamJamLength > (0.80 * 50)) and (downstream_weighted_meanSpeed >= 0 and downstream_weighted_meanSpeed <= (
                            5 / 3.6))):
                        status = 1  # gridlock
                    else:
                        status = 0  # no gridlock
                    
                    # 5. upstream ==> jam , downstream ==> jam
                    if ((current_tls != 'r') and (upstreamJamLength > (0.80 * 50)) and (downstreamJamLength > (0.80 * 50) )):
                        status = 1  # gridlock
                    else:
                        status = 0  # no gridlock
                    
                    # 6. upstream ==> jam , downstream ==> (speed+jam)
                    if ((current_tls != 'r') and (upstreamJamLength > (0.80 * 50)) and ((
                            downstreamJamLength > (0.80 * 50)) and (downstream_weighted_meanSpeed >= 0 and downstream_weighted_meanSpeed <= (
                            5 / 3.6)))):
                        status = 1  # gridlock
                    else:
                        status = 0  # no gridlock
                    
                    # 7. upstream ==> (speed + jam), downstream ==> speed
                    if ((current_tls != 'r') and (upstreamJamLength > (0.80 * 50) and (upstream_weighted_meanSpeed >= 0 and upstream_weighted_meanSpeed <= (
                            5 / 3.6)))  and (downstream_weighted_meanSpeed >= 0 and downstream_weighted_meanSpeed <= (
                            5 / 3.6))):
                        status = 1  # gridlock
                    else:
                        status = 0  # no gridlock
                    
                    # 8. upstream ==> (speed + jam), downstream ==> jam
                    if ((current_tls != 'r') and (upstreamJamLength > (0.80 * 50) and (
                            upstream_weighted_meanSpeed >= 0 and upstream_weighted_meanSpeed <= (5 / 3.6))) and (downstreamJamLength > (0.80 * 50))):
                        status = 1  # gridlock
                    else:
                        status = 0  # no gridlock
                    '''
                    # 9. upstream ==> (speed + jam), downstream ==> (speed+jam)
                    if ((current_tls != 'r') and (upstreamJamLength > (0.80 * 50) and (
                            upstream_weighted_meanSpeed >= 0 and upstream_weighted_meanSpeed <= (5 / 3.6))) and (
                            downstreamJamLength > (0.80 * 50) and (downstream_weighted_meanSpeed >= 0 and downstream_weighted_meanSpeed <= (
                            5 / 3.6)))):
                        status = 1  # gridlock
                    else:
                        status = 0  # no gridlock


            # this code block is to write csv file
            #=====================================================================================
                    if (cur_time,edgeID_1) not in dummy_dictionary:

                        dummy_list=[]
                        dummy_list.append(cur_time)
                        dummy_list.append(edgeID_1) # edgeID_1 is upstream
                        dummy_list.append(lanelength)
                        dummy_list.append(edgeID_2) # edgeID_2 is downstream
                        dummy_list.append(upstreamJamLength)
                        dummy_list.append(upstream_weighted_meanSpeed)
                        dummy_list.append(downstreamJamLength)
                        dummy_list.append(downstream_weighted_meanSpeed)
                        dummy_list.append(current_tls)
                        dummy_list.append(status)
                        dummy_dictionary[(cur_time,edgeID_1)]=dummy_list

    #print(dummy_dictionary)
    for k,v in dummy_dictionary.items():
        dummy_path_1=dirpath+'/CSVData\\'+str(k[1])+'.csv'
        if dummy_path_1 in files:
            file=open(dummy_path_1,'a',newline='')
            writer = csv.writer(file)
            with file:
                writer.writerow([v[0],key,v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],v[9]])
            file.close()
#=============================================================================================================================



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


#===============================================================================================
def createFile2():
    #to get the current directory
    dirpath = os.getcwd()
    for k,v in cluster.items():
        csvForEachCluster=open(dirpath+'/CongestionDataForEachCluster/'+k+'.csv','w',newline='')
        writer=csv.writer(csvForEachCluster)
        writer.writerow(["Time","Status"])

    allClusterCongestion=open(dirpath+'/CongestionDataForEachCluster/allClusterCongestion.csv','w',newline='')
    writer=csv.writer(allClusterCongestion)
    writer.writerow(["Time","Status"])
#===============================================================================================


def detection():
    dirpath = os.getcwd()
    names =  ["Time","ClusterID","Upstream","LaneLength","Downstream","UpstreamJamLength","UpstreamMeanSpeed","DownstreamJamLength","DownstreamMeanSpeed","TLS","Status"]

    # this code block is to group data for plotting
    #====================================================================================
    rowcount=1
    while rowcount<10801:
        dummy_dictionary2={}
        status_list=[]
        for cluster_ID,edges in cluster.items():
            for edge in edges:
                filepath=dirpath+'/CSVData/'+edge+'.csv'
                if os.path.isfile(filepath):
                    df = pd.read_csv(filepath,names=names, header=None)
                    if(len(dummy_dictionary2))==0: #new entry with new key and value
                        status_list.append(int(df['Status'].loc[rowcount]))
                        #time =sum(int(x) * 60 ** i for i,x in enumerate(reversed(str(df['Time'].loc[rowcount]).split(":"))))
                        #dummy_dictionary2[(time,cluster_ID)]=status_list
                        dummy_dictionary2[(int(df['Time'].loc[rowcount]),cluster_ID)]=status_list

                    else:# not new entry but old key and new value
                        status_list=[]
                        #time =sum(int(x) * 60 ** i for i,x in enumerate(reversed(str(df['Time'].loc[rowcount]).split(":"))))

                        if(dummy_dictionary2.__contains__((int(df['Time'].loc[rowcount]),cluster_ID))):
                            oldlist= dummy_dictionary2.get((int(df['Time'].loc[rowcount]),cluster_ID))
                            oldlist.append(int(df['Status'].loc[rowcount]))
                            dummy_dictionary2[(int(df['Time'].loc[rowcount]),cluster_ID)]=oldlist

                        else: # not new entry but new key and value
                            #time =sum(int(x) * 60 ** i for i,x in enumerate(reversed(str(df['Time'].loc[rowcount]).split(":"))))
                            status_list.append(int(df['Status'].loc[rowcount]))
                            dummy_dictionary2[(int(df['Time'].loc[rowcount]),cluster_ID)]=status_list


        #print(dummy_dictionary2)
        clusterCongestion = {}
        i=1
        for k,v in dummy_dictionary2.items():

            condition=any(state == 1 for state in v)
            if(condition== True):
                clusterCongestion[(k[0],k[1])]=1
            else:
                clusterCongestion[(k[0], k[1])] = 0


        #to save congestion state for each cluster
        #=================================================================
        dirpath = os.getcwd()
        path=dirpath+'/CongestionDataForEachCluster/*.csv'
        files=glob.glob(path)
        gridlock_time=[]
        gridlock_plot=[]
        for cluster_key,state in clusterCongestion.items():
            #======================================================================
            dummy_path_1=dirpath+'/CongestionDataForEachCluster\\'+str(cluster_key[1])+'.csv'
            if dummy_path_1 in files:
                file=open(dummy_path_1,'a',newline='')
                writer = csv.writer(file)
                with file:
                    writer.writerow([cluster_key[0],state])
                    print(cluster_key[0],cluster_key[1],state)

                file.close()
            # ======================================================================

        print(clusterCongestion.values())
        print('================================================')
        condition = all(lock == 1 for lock in clusterCongestion.values())
        file=open(dirpath+'/CongestionDataForEachCluster/allClusterCongestion.csv','a',newline='')
        writer = csv.writer(file)
        if (condition == True):
            writer.writerow([k[0],1])
        else:
            writer.writerow([k[0],0])

        # =================================================================
        rowcount+=1 # time interval to detect

#===================================================================================================






#=========================================================================================================
def plotClusterCongestion():
    dirpath = os.getcwd()
    names =   ["Time","ClusterID","Upstream","LaneLength","Downstream","UpstreamJamLength","UpstreamMeanSpeed","DownstreamJamLength","DownstreamMeanSpeed","TLS","Status"]
    #==========================================================================================
    fichier_html_graphs=open(dirpath+"/plotClusterCongestion/AllCluster.html",'w')
    fichier_html_graphs.write("<html><head></head><body style=\"margin:0\">"+"\n")
    for k,v in cluster.items():

        COLORS = ['rgb(0,128,0)',
          'rgb(0, 0, 0)',
          'rgb( 0, 0, 255)',
          'rgb(255,0,0)',]
        upstream_trace=[]
        for edgeID in v:
            filepath=dirpath+'/CSVData/'+edgeID+'.csv'
            if os.path.isfile(filepath):
                df = pd.read_csv(filepath,names=names, header=None)

                trace = go.Scatter(x=df['Time'], y=df['UpstreamJamLength'], mode = 'lines',name=edgeID+'(upstream)',
                                     line = dict(color =  COLORS[v.index(edgeID)],width = 1)
                                    )
                upstream_trace.append(trace)
                downstream_trace= go.Scatter(x=df['Time'], y=df['DownstreamJamLength'], mode = 'lines',name=str(df['Downstream'].values[1])+'(downstream)',
                                     line = dict(color =  ('rgb(255,0,0)'),width = 1)
                            )
        upstream_trace.append(downstream_trace)
        data = upstream_trace



        # Edit the layout
        layout = go.Layout(title = '<b>Congestion in: '+str(k)+'</b>',
                      titlefont=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                        ),
                      xaxis = dict(title = 'Time',tickangle=270,color='#000000',tickfont=dict(color='#000000')),
                      yaxis = dict(title = 'Jam',color='#000000',range=[0,150],tickfont=dict(color='#000000')),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      )

        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename=dirpath+'/plotClusterCongestion/'+str(k)+'.html',auto_open=False)
        fichier_html_graphs.write("<object data=\""+str(k)+'.html'+"\" width=\"1500\" height=\"500\" style=\"margin: 0px 0px\"></object>")
    fichier_html_graphs.write("</body></html>")
    print("CHECK YOUR DASHBOARD.html In the current directory")
#==========================================================================================



#=========================================================================================================
def plotClusterMeanSpeed():
    dirpath = os.getcwd()
    names =   ["Time","ClusterID","Upstream","LaneLength","Downstream","UpstreamJamLength","UpstreamMeanSpeed","DownstreamJamLength","DownstreamMeanSpeed","TLS","Status"]
    #==========================================================================================
    fichier_html_graphs=open(dirpath+"/plotClusterMeanSpeed/AllCluster.html",'w')
    fichier_html_graphs.write("<html><head></head><body style=\"margin:0\">"+"\n")
    for k,v in cluster.items():

        COLORS = ['rgb(0,128,0)',
          'rgb(0, 0, 0)',
          'rgb( 0, 0, 255)',
          'rgb(255,0,0)',]
        upstream_trace=[]
        for edgeID in v:
            filepath=dirpath+'/CSVData/'+edgeID+'.csv'
            if os.path.isfile(filepath):
                df = pd.read_csv(filepath,names=names, header=None)

                trace = go.Scatter(x=df['Time'], y=df['UpstreamMeanSpeed'], mode = 'lines',name=edgeID+'(upstream)',
                                     line = dict(color =  COLORS[v.index(edgeID)],width = 1)
                                    )
                upstream_trace.append(trace)
                downstream_trace= go.Scatter(x=df['Time'], y=df['DownstreamMeanSpeed'], mode = 'lines',name=str(df['Downstream'].values[1])+'(downstream)',
                                     line = dict(color =  ('rgb(255,0,0)'),width = 1)
                            )
        upstream_trace.append(downstream_trace)
        data = upstream_trace



        # Edit the layout
        layout = go.Layout(title = '<b>Mean Speed in: '+str(k)+'</b>',
                      titlefont=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                        ),
                      xaxis = dict(title = 'time',tickangle=270,color='#000000',tickfont=dict(color='#000000')),
                      yaxis = dict(title = 'mean speed',color='#000000',range=[0,60],tickfont=dict(color='#000000')),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      )

        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename=dirpath+'/plotClusterMeanSpeed/'+str(k)+'.html',auto_open=False)
        fichier_html_graphs.write("<object data=\""+str(k)+'.html'+"\" width=\"1500\" height=\"500\" style=\"margin: 0px 0px\"></object>")
    fichier_html_graphs.write("</body></html>")
    print("CHECK YOUR DASHBOARD.html In the current directory")
#==========================================================================================




#===========================================================================================
def plotCongestion_withMatplot():
    x = []
    y = []
    dirpath = os.getcwd()
    path=dirpath+'/CongestionDataForEachCluster/*.csv'
    files=glob.glob(path)
    i=1
    for f in files:
        head, tail = os.path.split(f)
        with open(f,'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            next(plots) # to skip header
            for row in plots:

                x.append((row[0]))
                y.append((row[1]))

                f = plt.figure(i,figsize=(10, 5))
                plt.scatter(x,y,c="b")
                plt.title('Congestion in '+ tail)
                plt.ylabel('state of congestion')
                plt.xlabel('time')
                plt.xticks(rotation=45)
                plt.yticks([-0.5,-0.25,0,0.25,0.5,0.75,1.0,1.25,1.5])
                plt.draw()
                #plt.show()
                index_Of_underscore1=int(tail.find('.'))# to get the position of first underscore
                filename=tail[0:((index_Of_underscore1))]
                plt.savefig(filename)
                i=i+1

    path=dirpath+'/CongestionDataForEachCluster/allClusterCongestion.csv'
    with open(path,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        next(plots) # to skip header
        for row in plots:

            x.append(int(row[0]))
            y.append(int(row[1]))
            f = plt.figure(i,figsize=(10, 5))
            plt.scatter(x, y, c="b")
            plt.title('Gridlock Detection')
            plt.ylabel('gridlock state')
            plt.xlabel('Time')
            plt.xticks(rotation=45)
            plt.yticks([-0.5, -0.25, 0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5])
            plt.draw()
            plt.savefig('grid')
            #plt.show()
#==============================================================================================


def plot_ClusterCongestionState():
    dirpath = os.getcwd()
    names =   ["Time","Status"]
    #==========================================================================================
    fichier_html_graphs=open(dirpath+"/plotClusterCongestionStatus/AllCluster.html",'w')
    fichier_html_graphs.write("<html><head></head><body style=\"margin:0\">"+"\n")
    path=dirpath+'/CongestionDataForEachCluster/*.csv'
    files=glob.glob(path)
    for f in files:
        head, tail = os.path.split(f)
        index_Of_underscore1=int(tail.find('.'))# to get the position of first underscore
        filename=tail[0:((index_Of_underscore1))]

        df = pd.read_csv(f,names=names, header=None)
        #print(df)
        trace=go.Scatter(x=df['Time'], y=df['Status'],mode='markers',name=str(filename),
                         marker = dict(
                          color = 'rgb(0,0,160)',
                          size = 6)
                         )

        data = [trace]
        # Edit the layout

        if filename=='allClusterCongestion':
            title1=''
            title2='gridlock status'
        else:
            title1='<b>Congestion in: '+str(filename)+'</b>'
            title2='congestion status'


        layout = go.Layout(title = title1,
                      titlefont=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                        ),
                      xaxis = dict(title = 'time',tickangle=270,color='#000000',tickfont=dict(color='#000000')),
                      yaxis = dict(title = title2,color='#000000',range=[-0.5,1.5],tickfont=dict(color='#000000')),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      )

        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename=dirpath+'/plotClusterCongestionStatus/'+str(filename)+'.html',auto_open=False)
        fichier_html_graphs.write("<object data=\""+str(filename)+'.html'+"\" width=\"1500\" height=\"500\" style=\"margin: 0px 0px\"></object>")
    fichier_html_graphs.write("</body></html>")
    print("CHECK YOUR DASHBOARD.html In the current directory")

    #==========================================================================================


#===============================================================================================
def createFile3():
    #to get the current directory
    dirpath = os.getcwd()
    for k,v in POIEdges1.items():
        csvForEachCluster=open(dirpath+'/flowDataCSV/'+str(k)+'.csv','w',newline='')
        writer=csv.writer(csvForEachCluster)
        writer.writerow(["Time","NumberOfFlow"])

    allClusterCongestion=open(dirpath+'/flowDataCSV/allFlowInCriticalRegion.csv','w',newline='')
    writer=csv.writer(allClusterCongestion)
    writer.writerow(["Time","NumberOfFlow"])
#===============================================================================================


#===============================================================================================
def flow_in_criticalRegion():
    dirpath = os.getcwd()
    path=dirpath+'/flowDataCSV/*.csv'
    files=glob.glob(path)
    vCount=0
    vTotal=0
    for edge,state in POIEdges1.items():
        #======================================================================
        dummy_path_1=dirpath+'/flowDataCSV\\'+str(edge)+'.csv'
        if dummy_path_1 in files:
            file=open(dummy_path_1,'a',newline='')
            writer = csv.writer(file)
            vCount=traci.edge.getLastStepVehicleNumber(edge)
            vTotal+=vCount
            with file:
                writer.writerow([int(traci.simulation.getCurrentTime()/1000),vCount])
            file.close()

    file=open(dirpath+'/flowDataCSV/allFlowInCriticalRegion.csv','a',newline='')
    writer = csv.writer(file)
    with file:
        writer.writerow([int(traci.simulation.getCurrentTime()/1000),vTotal])
    file.close()
#=============================================================================================




#=============================================================================================
def plot_flow_inCriticalRegion():
    dirpath = os.getcwd()
    names =   ["Time","NumberOfFlow"]
    #==========================================================================================
    fichier_html_graphs=open(dirpath+"/plotCriticalRegion/CriticalRegion.html",'w')
    fichier_html_graphs.write("<html><head></head><body style=\"margin:0\">"+"\n")
    path=dirpath+'/flowDataCSV/*.csv'
    files=glob.glob(path)
    for f in files:
        head, tail = os.path.split(f)
        index_Of_underscore1=int(tail.find('.'))# to get the position of first underscore
        filename=tail[0:((index_Of_underscore1))]

        df = pd.read_csv(f,names=names, header=None)
        trace=go.Scatter(x=df['Time'], y=df['NumberOfFlow'],mode='lines+markers',name=str(filename),
                         marker = dict(
                          color = 'rgb(255,140,0)',
                          size = 2)
                         )

        data = [trace]
        # Edit the layout

        if filename=='allFlowInCriticalRegion':
            title=''
        else: title='<b>Congestion in: '+str(filename)+'</b>'
        layout = go.Layout(title = title,
                      titlefont=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                        ),
                      xaxis = dict(title = 'time',tickangle=270,color='#000000',tickfont=dict(color='#000000')),
                      yaxis = dict(title = 'vehicles/s',color='#000000',range=[0,800],tickfont=dict(color='#000000')),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      )

        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename=dirpath+'/plotCriticalRegion/'+str(filename)+'.html',auto_open=False)
        fichier_html_graphs.write("<object data=\""+str(filename)+'.html'+"\" width=\"1500\" height=\"500\" style=\"margin: 0px 0px\"></object>")
    fichier_html_graphs.write("</body></html>")
    print("CHECK YOUR DASHBOARD.html In the current directory")

#==========================================================================================


if __name__=="__main__":
    main()


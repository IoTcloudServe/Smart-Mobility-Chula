from xml.etree import ElementTree
import csv
import pandas as pd

from pandas import Series
from matplotlib import pyplot
import numpy as np
import glob
import os, sys
from datetime import datetime
import matplotlib.pyplot as plt

#import plotly.plotly as py
import plotly
from plotly.offline import init_notebook_mode
import plotly.graph_objs as go
#plotly.offline.init_notebook_mode(connected=True)
from tkinter import *
from operator import itemgetter

from multiprocessing.pool import ThreadPool

import time


POIEdges={'L179':'313.44',
          'L10188':'282.95',
          'L10130':'246.38',
          'L49':'271.31',
          'L10189':'171.59',
          'L239':'36.12',
          'L249':'54.98',
          'L232':'82.62',
          'L10009':'427.63',
          'L60':'104.34',
          'L73':'159.19',
          'L10149#1':'88.09',
          'L10149#2':'13.48',
          'L138':'112.16',
          'L133.25':'118.71',
          'L135':'98.77',
          'L140#1':'77.64',
          'L140#2':'78.13',
          'L64':'277.38',
          'L10032':'161.93',
          'L40493':'157.78',
          'L30':'99.68',
          'L72':'100.12',
          'L58#1':'371.54'
          }

POIlanes={'L179':['L179_0'],
          'L10188':['L10188_0'],
          'L10130':['L10130_0','L10130_1','L10130_2','L10130_3'],#'L10130_0',
          'L49':['L49_0','L49_1','L49_2'],
          'L10189':['L10189_0','L10189_1','L10189_2','L10189_3'],#'L10189_0',
          'L239':['L239_0','L239_1','L239_2','L239_3'],
          'L249':['L249_0','L249_1','L249_2','L249_3'],
          'L232':['L232_0','L232_1','L232_2','L232_3'],
          'L10009':['L10009_0','L10009_1','L10009_2'],
          'L60':['L60_0','L60_1'],
          'L73':['L73_0','L73_1'],
          'L10149#1':['L10149#1_0','L10149#1_1'],
          'L10149#2':['L10149#2_1','L10149#2_2'],#,'L10149#2_0'
          'L138':['L138_0','L138_1','L138_2'],
          'L133.25':['L133.25_0','L133.25_1','L133.25_2','L133.25_3'],
          'L135':['L135_0','L135_1','L135_2'],
          'L140#1':['L140#1_0','L140#1_1','L140#1_2'],
          'L140#2':['L140#2_3'],
          'L64':['L64_1','L64_2','L64_3'],
          'L10032':['L10032_0'],
          'L40493':['L40493_0','L40493_1','L40493_2','L40493_3'],
          'L30':['L30_0','L30_1','L30_2','L30_3'],
          'L72':['L72_0','L72_1','L72_2','L72_3'],
          #24:['L10059_0'],
          'L58#1':['L58#1_0','L58#1_1']
          }



ControlledLanes={
'cluster_118_119_120_121':['L7_1','L7_2','L7_3','L7_4','L176_0','L176_1','L176_2','L176_3','L10199_0','L10199_1','L10199_2','L10199_3','L10199_4','L10017_0','L10017_1','L10017_2'],
'cluster_134_135_136_138':['L30767_0','L30767_1','L30767_2','L61_0','L61_1','L61_2','L61_3','L27_0','L27_1','L27_2','L27_3','L10223_0','L10223_1','L10223_2','L10223_3'],
'cluster_13_14':['L25_0','L25_1','L25_2','L25_3','L10186_0','L10186_1','L243_0','L243_1','L243_2','L243_3','L243_4'],
'cluster_159_32_6_7':['L10219_0','L10219_1','L10219_2','L134_0','L134_1','L134_2','L10032_0','L10032_1','L10032_2','L10032_3','L138_0','L138_1','L138_2'],
'cluster_15_16_17_18':['L70_0','L70_1','L70_2','L70_3','L70_4','L148_0','L148_1','L148_2','L53_0','L53_1','L53_2','L53_3','L53_4','L143_0','L143_1','L143_2'],
'cluster_185_186':['L58#2_0','L58#2_1','L58#2_2','L30940_0','L30940_1','L30032_0','L30032_1'],
'cluster_20_21_22_23':['L97_0','L97_1','L97_2','L97_3','L10217_0','L10217_1','L10217_2','L10217_3','L10217_4','L220_0','L220_1','L220_2','L220_3','L220_4','L240_0','L240_1','L240_2','L240_3','L240_4'],
'cluster_43_44':['L49_0','L49_1','L49_2','L64_0','L64_1','L64_2','L64_3','L133.25_0','L133.25_1','L133.25_2','L133.25_3'],
'cluster_46_47':['L40_0','L40_1','L40_2','L40_3','L197#2_0','L197#2_1','L197#2_2','L197#2_3','L197#2_4','L10189_0','L10189_1','L10189_2','L10189_3','L239_0','L239_1','L239_2','L239_3'],
'cluster_83_84':['L132_0','L132_1','L132_2','L67_0','L67_1','L10149#2_0','L10149#2_1','L10149#2_2']
                }



# to check critical density
'''
#====================================================================================================
def checkDensity(time,edgeID,det_dictionary):
    tempTime = '00:00:02'
    FMT = '%H:%M:%S' # FMT is format
    tdelta = datetime.strptime(str(time), FMT) - datetime.strptime(tempTime, FMT)


    #print(tdelta,time,edgeID)
    if ((str(tdelta)!='6:00:00') and (str(tdelta)!='8:59:59')):
        format_time = datetime.strptime(str(tdelta),'%H:%M:%S')
        tdelta=format_time.time()
        dataList1=det_dictionary.get((tdelta,edgeID))
        dataList2=det_dictionary.get((time,edgeID))

        if(float(dataList2[1])<= float(dataList1[6])):
            dataList2[6]=dataList1[6]
            #print('less than or equal case:')
            #print(dataList2[1],dataList1[6])

        elif(float(dataList2[1])> float(dataList1[6])):
            dataList2[6]=dataList2[1]
            #print('greater than case:')
            #print(dataList2[1],dataList1[6])


        det_dictionary[(tdelta,edgeID)]=dataList1
        det_dictionary[(time,edgeID)]=dataList2

    if ((str(time)=='09:00:01')):
        tempTime = '09:00:00'
        format_time = datetime.strptime(str(tempTime),'%H:%M:%S')# 9:00:00
        tdelta=format_time.time()
        #print('hello')
        format_time = datetime.strptime(str(time),'%H:%M:%S')#9:00:01
        time=format_time.time()
        dataList1=det_dictionary.get((tdelta,edgeID))
        dataList2=det_dictionary.get((time,edgeID))

        dataList2[6]=dataList1[6]

        det_dictionary[(time,edgeID)]=dataList2

    return det_dictionary
'''
#====================================================================================================






#this function is read output xml file from all detectors with offline mode
#========================================================================================
def readWithoutAccident():
    #to get the current directory
    dirpath = os.getcwd()
    with open(dirpath+'/dataset/NormalCase/seed50_Correct_5min/Alle2Detector.xml','rt')as f:
        tree=ElementTree.parse(f)
    det_dictionary={}
    for node in tree.iter('interval'):
        infoList=[]

        count=0
        densityPerLane=0
        meanSpeed=0
        meanOccupancy=0
        jamlengthinMeter=0

        timeInterval=node.attrib.get('end')
        detID=node.attrib.get('id')
        densityPerLane=node.attrib.get('nVehSeen')
        meanSpeed=node.attrib.get('meanSpeed')
        meanOccupancy=node.attrib.get('meanOccupancy')
        jamlengthinMeter=node.attrib.get('meanMaxJamLengthInMeters')

        format_time = datetime.strptime(getTime(float(timeInterval)),'%H:%M:%S')
        time=format_time.time()

        index_Of_underscore1=int(detID.find('_'))# to get the position of first underscore
        edgeID=detID[0:((index_Of_underscore1))]




        lanelength=0
        if(POIEdges.__contains__(edgeID)):
            lanelength=float(POIEdges.get(edgeID))

        #weighted_meanSpeed= int(densityPerLane)* float(meanSpeed)

        if float(meanSpeed) == -1.00:
            print('>>>>>>>>',float(meanSpeed))
            meanSpeed = float(0)



        infoList.append(jamlengthinMeter)
        infoList.append(densityPerLane)
        #infoList.append(weighted_meanSpeed)
        infoList.append(float(meanSpeed))
        infoList.append(meanOccupancy)
        infoList.append(1)
        infoList.append(detID)

        #criticalDensity=densityPerLane
        #infoList.append(criticalDensity)

        #Speed (metres per sec) = flow (vehicle per sec) / density (veh per metre), Ajarn chaodit
        flow= int(densityPerLane) * float(meanSpeed)#flow per lane
        infoList.append(flow)


        if(len(det_dictionary))==0: #new entry with new key and value
            det_dictionary[(time,edgeID)]=infoList
            #det_dictionary= checkDensity(time,edgeID,det_dictionary) # this statement is to update maximum density

        else:# not new entry but old key and new value
            newList=[]
            if(det_dictionary.__contains__((time,edgeID))):
                oldList= det_dictionary.get((time,edgeID))

                newList.append(float(infoList[0])+float(oldList[0])) #jam length
                newList.append(float(infoList[1])+float(oldList[1]))#density
                newList.append(float(infoList[2])+float(oldList[2]))#meanspeed
                newList.append(float(infoList[3])+float(oldList[3]))#meanoccupancy
                newList.append(int(infoList[4])+int(oldList[4]))#number of lane
                newList.append(infoList[5]+','+oldList[5])# detector IDs
                #newList.append(float(infoList[6])+float(oldList[6])) # critical density
                newList.append(float(infoList[6])+float(oldList[6])) # flow for all cells


                det_dictionary[(time,edgeID)]=newList
                #det_dictionary= checkDensity(time,edgeID,det_dictionary) # this statement is to update maximum density

            else: # not new entry but new key and value

                det_dictionary[(time,edgeID)]=infoList
                #det_dictionary= checkDensity(time,edgeID,det_dictionary) # this statement is to update maximum density

    f.close()
    '''
    for keys,values in det_dictionary.items():
        print(keys,values)
    '''
    return det_dictionary
#========================================================================================




#this function is read output xml file from all detectors with offline mode
#========================================================================================
def readWithAccident():

    #to get the current directory
    dirpath = os.getcwd()
    with open(dirpath+'/dataset/AccidentCase/LaneClosure/L10130/seed50_20min/1,2,3 close/Alle2Detector.xml','rt')as f:

        tree=ElementTree.parse(f)

    det_dictionary={}
    for node in tree.iter('interval'):
        infoList=[]

        count=0
        densityPerLane=0
        meanSpeed=0
        meanOccupancy=0
        jamlengthinMeter=0

        timeInterval=node.attrib.get('end')
        detID=node.attrib.get('id')
        densityPerLane=node.attrib.get('nVehSeen')
        meanSpeed=node.attrib.get('meanSpeed')
        meanOccupancy=node.attrib.get('meanOccupancy')
        jamlengthinMeter=node.attrib.get('meanMaxJamLengthInMeters')

        format_time = datetime.strptime(getTime(float(timeInterval)),'%H:%M:%S')
        time=format_time.time()

        index_Of_underscore1=int(detID.find('_'))# to get the position of first underscore
        edgeID=detID[0:((index_Of_underscore1))]




        lanelength=0
        if(POIEdges.__contains__(edgeID)):
            lanelength=float(POIEdges.get(edgeID))

        #weighted_meanSpeed= int(densityPerLane)* float(meanSpeed)
        if float(meanSpeed) == -1.00:
            print('>>>>>>>>',float(meanSpeed))
            meanSpeed = float(0)


        infoList.append(jamlengthinMeter)
        infoList.append(densityPerLane)
        #infoList.append(weighted_meanSpeed)
        infoList.append(float(meanSpeed))
        infoList.append(meanOccupancy)
        infoList.append(1)
        infoList.append(detID)

        #criticalDensity=densityPerLane
        #infoList.append(criticalDensity)

        #Speed (metres per sec) = flow (vehicle per sec) / density (veh per metre), Ajarn chaodit
        flow= int(densityPerLane) * float(meanSpeed)#flow per lane
        infoList.append(flow)


        if(len(det_dictionary))==0: #new entry with new key and value
            det_dictionary[(time,edgeID)]=infoList
            #det_dictionary= checkDensity(time,edgeID,det_dictionary) # this statement is to update maximum density

        else:# not new entry but old key and new value
            newList=[]
            if(det_dictionary.__contains__((time,edgeID))):
                oldList= det_dictionary.get((time,edgeID))

                newList.append(float(infoList[0])+float(oldList[0])) #jam length
                newList.append(float(infoList[1])+float(oldList[1]))#density
                newList.append(float(infoList[2])+float(oldList[2]))#meanspeed
                newList.append(float(infoList[3])+float(oldList[3]))#meanoccupancy
                newList.append(int(infoList[4])+int(oldList[4]))#number of lane
                newList.append(infoList[5]+','+oldList[5])# detectors
                #newList.append(float(infoList[6])+float(oldList[6])) # critical density
                newList.append(float(infoList[6])+float(oldList[6])) # flow for all cells


                det_dictionary[(time,edgeID)]=newList
                #det_dictionary= checkDensity(time,edgeID,det_dictionary) # this statement is to update maximum density

            else:# not new entry but new key and value
                det_dictionary[(time,edgeID)]=infoList
                #det_dictionary= checkDensity(time,edgeID,det_dictionary) # this statement is to update maximum density
    f.close()
    '''
    for keys,values in det_dictionary.items():
        print(keys,values)
    '''
    return det_dictionary
#========================================================================================



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





#1. to create respective output files for each edge
#========================================================================================
def createFile():
    for key,value in POIEdges.items():
        for eachEdge in value:
            #to get the current directory
            dirpath = os.getcwd()
            myfile1 = open(dirpath+'/dataset/NormalCase/seed50_Correct_5min/'+str(key)+'.csv', 'w',newline='')
            myfile2 = open(dirpath+'/dataset/AccidentCase/LaneClosure/L10130/seed50_20min/1,2,3 close/'+str(key)+'.csv', 'w',newline='')

            writer1 = csv.writer(myfile1)
            writer1.writerow(["Time","Edge ID","Edge Length","NumberOfLane","Lane Name","Jam Length","Density","Mean Speed","Mean Occupancy","Flow","Road State(basedOnJamLength)"])

            writer2 = csv.writer(myfile2)
            writer2.writerow(["Time","Edge ID","Edge Length","NumberOfLane","Lane Name","Jam Length","Density","Mean Speed","Mean Occupancy","Flow","Road State(basedOnJamLength)","Road State(basedOnFlow)"])
#========================================================================================





#this function is to write csv for each edge in WithoutAccident Case
#========================================================================================
def writeFileWithoutAccident(det_dictionary):
    #to get the current directory
    dirpath = os.getcwd()
    path=dirpath+'/dataset/NormalCase/seed50_Correct_5min/*.csv'


    files=glob.glob(path)

    for key,value in det_dictionary.items():

        if(POIEdges.__contains__(key[1])):
            laneLength=float(POIEdges.get(key[1]))

        infoList=value

        jamLength=infoList[0]
        density=infoList[1]
        meanSpeed=infoList[2]
        meanOccupancy=infoList[3]
        numOfLane=infoList[4]
        laneList=infoList[5] # detectors
        flow=infoList[6]



        meanSpeed=float(meanSpeed)/int(numOfLane)
        meanOccupancy=float(meanOccupancy)/int(numOfLane)
        jamlengthinMeter=float(jamLength)/int(numOfLane)
        density= int(round(int(density)/int(numOfLane)))



        #flow=int(density)*float(meanSpeed)
        #flow=int(density)
        flow=float(flow)/int(numOfLane)


        condition1=0.95*laneLength
        condition2 = 0.40 * laneLength
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
            #print(str(dirpath)+'/dataset/NormalCase/seed10\\'+key[1]+'.csv')
            #print(name)
            #print('==============================================')
            if(name==str(dirpath)+'/dataset/NormalCase/seed50_Correct_5min\\'+key[1]+'.csv'):
                    file=open(name,'a',newline='')
                    writer = csv.writer(file)
                    with file:
                        writer.writerow([key[0],key[1],laneLength,numOfLane,laneList,jamlengthinMeter,density,meanSpeed,meanOccupancy,flow,state])
                    file.close()

                    break
#========================================================================================



#this function is to write csv for each edge in WithAccident Case
#========================================================================================
def writeFileWithAccident(det_dictionary):
    dirpath = os.getcwd()
    path=dirpath+'/dataset/AccidentCase/LaneClosure/L10130/seed50_20min/1,2,3 close/*.csv'
    files=glob.glob(path)


    #to_checkLink={'L10130':'accident','L49':'up','L64':'up','L133.25':'up','L10189':'down'} # this is only accident link and one-hop up/down link
    to_checkLink={'L10130':'accident','L49':'up','L64':'up','L133.25':'up','L10189':'down','L10032':'up','L138':'up','L72':'down','L30':'down'}
    anomaly_state='NaN' #for non-accident link
    linkType=""

    for key,value in det_dictionary.items():
        if(POIEdges.__contains__(key[1])):
            laneLength=float(POIEdges.get(key[1]))

        infoList=value

        jamLength=infoList[0]
        density=infoList[1]
        meanSpeed=infoList[2]
        meanOccupancy=infoList[3]
        numOfLane=infoList[4]
        laneList=infoList[5] # detectors
        flow=infoList[6]


        meanSpeed=float(meanSpeed)/int(numOfLane)
        meanOccupancy=float(meanOccupancy)/int(numOfLane)
        jamlengthinMeter=float(jamLength)/int(numOfLane)
        density= int(round(int(density)/int(numOfLane)))

        # Speed (metres per sec) = flow (vehicle per sec) / density (veh per metre), Ajarn chaodit
        #flow=int(density)*float(meanSpeed)
        #flow=int(density)
        flow=float(flow)/int(numOfLane)





        condition1=0.95*laneLength
        condition2 = 0.40 * laneLength
        if (jamlengthinMeter > condition1 ):

            state="2"  # congested
            #print(laneID,jamlengthinMeter,meanSpeed,state)

        elif (meanSpeed < 2.0 and (condition2<= jamlengthinMeter <= condition1)):
            state="1" # moderate
            #print(laneID, jamlengthinMeter, meanSpeed, state)

        else:
            state="0" # free flow
            #print(laneID, jamlengthinMeter, meanSpeed, state)


        #************************* to check anomaly ****************************************
        if to_checkLink.__contains__(key[1]):
            linkType=to_checkLink.get(key[1])
            #print(key[1],linkType)
            anomaly_state=checkAnomaly_WhenWriteFile(key[1],linkType,key[0],flow,meanSpeed,jamlengthinMeter)
        else:
            anomaly_state="NaN" #for non-accident link

        #*****************************************************************



        for name in files:

            if(name==dirpath+'/dataset/AccidentCase/LaneClosure/L10130/seed50_20min/1,2,3 close\\'+key[1]+'.csv'):

                    file=open(name,'a',newline='')
                    writer = csv.writer(file)
                    with file:
                        writer.writerow([key[0],key[1],laneLength,numOfLane,laneList,jamlengthinMeter,density,meanSpeed,meanOccupancy,flow,state,anomaly_state])
                    file.close()

                    break
#========================================================================================






# def readAccData(edgeName,row,linkType):
#     #to check anomaly
#     #===================================================================
#     names = ["Time","Edge ID","Edge Length","NumberOfLane","Lane Name","Jam Length","Density","Critical Density","Mean Speed","Mean Occupancy","Flow","Road State"]
#     dirpath = os.getcwd()
#     withoutACC=dirpath+'/dataset/NormalCase/seed50_Correct_2s/'+edgeName+'.csv'
#     withACC=dirpath+'/dataset/AccidentCase/LaneClosure/L10130/seed50_20min/1,2 close/'+edgeName+'.csv'
#
#     flow=0.0
#     flowCondition1=0.0
#     flowCondition2=0.0
#     infoList=[]
#     state=0#'Normal'
#
#     if os.path.isfile(withoutACC):
#         df = pd.read_csv(withoutACC,names=names, skiprows=1)
#         max_flow=df['Flow'].max()
#         notACCflow=df['Flow'].loc[row]
#
#         # if you are trying to check anomaly case by using critical density, you can use critical density as below.
#         #criticalDensity=df['Critical Density'].max()
#
#     if os.path.isfile(withACC):
#         df = pd.read_csv(withACC,names=names, skiprows=1)
#         meanSpeed=df['Mean Speed'].loc[row]
#
#         flow=df['Flow'].loc[row]
#
#
#         if (linkType=='accident'):
#             flowCondition1=1/3 * float(max_flow)
#             if ((flow <=flowCondition1) and (float(meanSpeed)<=1.0)):
#                 state=1#'Abnormal'
#             infoList.append(df["Time"].loc[row])
#             infoList.append(df["Edge ID"].loc[row])
#             infoList.append(flow)
#             infoList.append(meanSpeed)
#             infoList.append(state)
#
#         if (linkType=='up'):
#             if (float(notACCflow)>= float(flow)):
#                 state=1#'Abnormal'
#             infoList.append(df["Time"].loc[row])
#             infoList.append(df["Edge ID"].loc[row])
#             infoList.append(flow)
#             infoList.append(meanSpeed)
#             infoList.append(state)
#
#         if (linkType=='down'):
#             flowCondition1=1/3 * float(max_flow)
#             if ((flow <=flowCondition1) and (float(meanSpeed)<=1.0)):
#                 state=1#'Abnormal'
#             infoList.append(df["Time"].loc[row])
#             infoList.append(df["Edge ID"].loc[row])
#             infoList.append(flow)
#             infoList.append(meanSpeed)
#             infoList.append(state)
#     return infoList
#     #===================================================================


def readUpAndDownFile(accidentLink,linktype):
    names = ["Lane Name","One Hop","Two Hop","Three Hop","Four Hop"]
    oneHop=[]
    dirpath = os.getcwd()
    with open(dirpath+'/upAndDown/'+linktype+'.csv', 'r', newline='') as csvDataFile:
        csvReader = csv.DictReader(csvDataFile)
        for index, row in enumerate(csvReader):
            if (row['Lane Name']==accidentLink):
                #print(index)
                oneHop.append(row['One Hop'])
                break
    return oneHop


#this code segment is trying to check anomaly case in any lane
#=======================================================================================
# def checkAnomlay():
#     row=0
#     total_rows=5400
#
#     accInfoList=[]
#     upInfoList=[]
#     downInfoList=[]
#
#     #read up and down link
#     accidentLink='L10130'
#     upLink=readUpAndDownFile(accidentLink,'up')
#     upLink= upLink[0].split(',')
#     #print(upLink)
#
#
#     downLink=readUpAndDownFile(accidentLink,'down')
#     downLink= downLink[0].split(',')
#     #print(downLink)
#
#     dirpath = os.getcwd()
#     accLink = open(dirpath+'/AnomalyCheckData/'+accidentLink+'.csv', 'w',newline='')
#     writer1 = csv.writer(accLink)
#     writer1.writerow(["Time","Edge ID","Flow","Mean Speed","Road State"])
#
#
#     for eachEdge in upLink:
#         upstream = open(dirpath+'/AnomalyCheckData/'+eachEdge+'.csv', 'w',newline='')
#         writer2 = csv.writer(upstream)
#         writer2.writerow(["Time","Edge ID","Flow","Mean Speed","Road State"])
#
#     for eachEdge in downLink:
#         downstream = open(dirpath+'/AnomalyCheckData/'+eachEdge+'.csv', 'w',newline='')
#         writer3 = csv.writer(downstream)
#         writer3.writerow(["Time","Edge ID","Flow","Mean Speed","Road State"])
#
#     start=time.strftime("%H:%M:%S")
#     print('Detection start :',start)
#     while(row<=total_rows):
#
#         #checking anomaly for accident link, up link and down link
#         accinfoList=readAccData(accidentLink,row,'accident')
#
#         path=dirpath+'/AnomalyCheckData/*.csv'
#         files=glob.glob(path)
#         for name in files:
#             if(name==dirpath+'/AnomalyCheckData\\'+accidentLink+'.csv'):
#                 file=open(name,'a',newline='')
#                 writer = csv.writer(file)
#                 with file:
#                     writer.writerow([accinfoList[0],accinfoList[1],accinfoList[2],accinfoList[3],accinfoList[4]])
#                 break
#
#
#         for up_link in upLink:
#             upInfoList=readAccData(up_link,row,'up')
#
#             path=dirpath+'/AnomalyCheckData/*.csv'
#             files=glob.glob(path)
#             for name in files:
#                 if(name==dirpath+'/AnomalyCheckData\\'+up_link+'.csv'):
#                     file=open(name,'a',newline='')
#                     writer = csv.writer(file)
#                     with file:
#                         writer.writerow([upInfoList[0],upInfoList[1],upInfoList[2],upInfoList[3],upInfoList[4]])
#                     break
#
#         for down_link in downLink:
#             downInfoList=readAccData(down_link,row,'down')
#             path=dirpath+'/AnomalyCheckData/*.csv'
#             files=glob.glob(path)
#             for name in files:
#                 if(name==dirpath+'/AnomalyCheckData\\'+down_link+'.csv'):
#                     file=open(name,'a',newline='')
#                     writer = csv.writer(file)
#                     with file:
#                         writer.writerow([downInfoList[0],downInfoList[1],downInfoList[2],downInfoList[3],downInfoList[4]])
#                     break
#
#         row+=1
#
#     end=time.strftime("%H:%M:%S")
#     print('Detection end :',end)
#     #duration=end-start
#     #print('Duration :',duration)
# #=======================================================================================




#========================================================================================
def checkAnomaly_WhenWriteFile(edgeName,linkType,time,flow,meanSpeed,jamlengthinMeter):
    names = ["Time","Edge ID","Edge Length","NumberOfLane","Lane Name","Jam Length","Density","Mean Speed","Mean Occupancy","Flow","Road State(basedOnJamLength)"]
    dirpath = os.getcwd()
    withoutACC=dirpath+'/dataset/NormalCase/seed50_Correct_5min/'+edgeName+'.csv'
    anomaly_state=0#Normal

    if os.path.isfile(withoutACC):
        df = pd.read_csv(withoutACC,names=names, skiprows=1)
        #max_flow=df['Flow'].max()
        #max_jamLength=df['Jam Length'].max()

        #print(edgeName,max_flow)
        row=df.loc[(df['Time'] == str(time))]
        non_AccidentFlow=row['Flow']
        non_AccidentMeanSpeed=row['Mean Speed']

    if (linkType=='accident'):
        if ( (float(flow)<= float(non_AccidentFlow)) and ((float(meanSpeed)< float(non_AccidentMeanSpeed)) and float(meanSpeed)<=5/3.6)):
        #if(( float(meanSpeed) <= 5/3.6) and (float(flow) < 1.0)):
            anomaly_state=1#'Abnormal'


    if (linkType=='up'):
        #if (float(meanSpeed)< float(non_AccidentMeanSpeed)):
        #if(( float(meanSpeed) <= 5/3.6) and (float(flow) < 1.0)):
        if ( (float(flow)<= float(non_AccidentFlow)) and ((float(meanSpeed)< float(non_AccidentMeanSpeed)) and float(meanSpeed)<=5/3.6)):
            anomaly_state=1#'Abnormal'


    if (linkType=='down'):
        #if ( (float(flow)<= float(non_AccidentFlow)) and (float(meanSpeed)< float(non_AccidentMeanSpeed))):
        if ( (float(flow)<= float(non_AccidentFlow)) and ((float(meanSpeed)< float(non_AccidentMeanSpeed)) and float(meanSpeed)<=5/3.6)):
        #if(( float(meanSpeed) <= 5/3.6) and (float(flow) < 1.0)):
            anomaly_state=1#'Abnormal'

    return anomaly_state
#=========================================================================================

#main functin
#========================================================================================
def main():
     createFile()
     det_dictionary=readWithoutAccident()
     writeFileWithoutAccident(det_dictionary)

     det_dictionary=readWithAccident()
     writeFileWithAccident(det_dictionary)

#========================================================================================





if __name__=="__main__":
    main()



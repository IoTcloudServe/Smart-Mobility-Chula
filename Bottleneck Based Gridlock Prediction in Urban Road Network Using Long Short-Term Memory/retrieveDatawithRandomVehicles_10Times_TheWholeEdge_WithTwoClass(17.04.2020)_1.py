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
import pandas as pd
import random
from datetime import datetime, timedelta
import os
from random import randint as r

def createFile(POIEdges,percentage,frequency,outputFile):
    # to get the current directory
    dirpath = 'c:'
    for freq in frequency:
        for pcent in percentage:
            for road,links in POIEdges.items():

                myfile1 = open(
                    dirpath + '/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID/' +outputFile+'/'+ road + '_' + str(freq) + '_' + pcent + '.csv', 'w', newline='')

                writer1 = csv.writer(myfile1)

                heading = ["Time","Time(s)",*links, "Total Vehicles", "Mean Speed (km/h)","Low Mean Speed","Persistently Low Mean Speed Indicator"]
                writer1.writerow(
                    heading)
                myfile1.close()


def parseFloat(str):
    try:
        return float(str)
    except:
        str = str.strip()
        if str.endswith("%"):
            return float(str.strip("%").strip()) / 100
        raise Exception("Don't know how to parse %s" % str)


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


#main functin
def main():

    POIEdges = {    'Sathorn_Thai_1':['L197#1','L197#2'],
                    'Sathorn_Thai_2': ['L30', 'L58#1','L58#2'],
                    'Charoenkrung_1': ['L30032'],
                    'Charoenkrung_2': ['L60', 'L73', 'L10149#1','L10149#2'],
                    'Charoenkrung_3': ['L67'],
                    'Silom_1': ['L138'],
                    'Silom_2': ['L133.25'],
                    'Silom_3': ['L49'],
                    'Mehasak':['L64'],
                    'Surasak': ['L10130', 'L10189'],
                    'Charoen_Rat': ['L40']
                }
    percentage = ['1%', '5%', '10%', '15%', '20%', '25%', '30%', '35%', '40%', '45%', '50%','100%']
    frequency = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    randomlist = []
    dirpath = 'c:/'


    path = dirpath + 'RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID/random.csv'
    myfile1 = open(path,'w', newline='')
    writer1 = csv.writer(myfile1)
    heading = ["Output File","random seed"]
    writer1.writerow(heading)
    myfile1.close()


    for outputFile in range(0,10):
        random_number = random.randint(50, 23423)

        #################### this code block is to keep random seed number permanently####################
        random_df = pd.read_csv(path)
        # print(random_df.columns)
        randomlist = random_df['random seed'].values.tolist()



        if len(randomlist) >=0:
            while random_number in randomlist:
                random_number = random.randint(50, 23423)

        #randomlist.append(r)

        myfile = open(path, 'a', newline='')
        writer = csv.writer(myfile)
        with myfile:

            writer.writerow([(outputFile+1),random_number])
            myfile.close()
        ##################################################################################################

        print(randomlist)

        print('Random Seed Number : ', random_number)
        os.mkdir(dirpath + 'RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID/'+ str(outputFile+1))

        createFile(POIEdges, percentage, frequency, str(outputFile+1))

        # sumoBinary = sumolib.checkBinary('sumo-gui')
        sumoBinary = sumolib.checkBinary('sumo')
        sumoCmd = [sumoBinary,
                   "--no-internal-links", 'true',
                   "--ignore-junction-blocker", '1',
                   '--start', 'true',
                   '--quit-on-end', 'true',
                   # "--random",'true',
                   "-c", "sathorn_w.sumo.cfg",
                   # '-a',"sathon_wide_tls_20160418_edited.add(upperSurasak)_withoutLaneclose.xml",
                   '-a', "sathon_wide_tls_20160418_edited.add.xml",
                   '--time-to-teleport', "-1",
                   '--seed', str(random_number),
                   '--no-warnings','true'
                   ]

        # sumoCmd = [sumoBinary, "-c", "sathorn_w.sumo.cfg",'-a',"sathon_wide_tls_20160418_edited.add.xml",'--time-to-teleport',"-1"]
        # sumoCmd = [sumoBinary, "-c", "sathorn_w.sumo.cfg"]
        traci.start(sumoCmd)


        step = 21600
        import time
        start_time = time.time()

        while step <= 32400:
            traci.simulationStep()
            for freq in frequency:

                if step % freq == 0:

                    for pcent in percentage:

                        percent = parseFloat(pcent)
                        for road, links in POIEdges.items():
                            temp = []
                            vList = []

                            for link in links:
                                IDs = list(traci.edge.getLastStepVehicleIDs(link))
                                vList.extend(IDs)
                                # print(vList)

                                temp.append(len(list(traci.edge.getLastStepVehicleIDs(link))))

                            ###### This code segment has issues about replicated vehicle IDs##########
                            # random_v = []
                            # g = (r(0, len(vList) - 1) for _ in range(int(len(vList) * (percent))))
                            # for i in g:
                            #     random_v.append(vList[i])
                            # print(percent,random_v)
                            ##########################################################################

                            random_v = random.sample(vList, int(len(vList) * (percent)))
                            # print(percent,random_v)
                            totalSpeed = 0.0
                            for v in random_v:
                                totalSpeed += float(traci.vehicle.getSpeed(v))

                            if (len(random_v)) > 0:
                                meanSpeed = float(totalSpeed / int(len(random_v)))
                            else:
                                meanSpeed = -1.00


                            format_time = datetime.strptime(getTime(float(step)), '%H:%M:%S')
                            time = format_time.time()

                            if meanSpeed * 3.6 <= 5 and meanSpeed >= 0:
                                low_meanSpeed = 1
                            else:
                                low_meanSpeed = 0

                            persistent_low_meanSpeed = 0

                            myfile = open(
                                dirpath + '/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID/' + str(
                                    outputFile + 1) + '/' + road + '_' + str(
                                    freq) + '_' + pcent + '.csv', 'a', newline='')

                            writer = csv.writer(myfile)

                            with myfile:

                                writer.writerow(
                                    [time, step, *temp, int(len(random_v)), meanSpeed, low_meanSpeed,
                                     persistent_low_meanSpeed])
                                myfile.close()

            step += 1
        traci.close()
        import time
        print("--- %s seconds ---" % (time.time() - start_time))

if __name__=="__main__":
    main()


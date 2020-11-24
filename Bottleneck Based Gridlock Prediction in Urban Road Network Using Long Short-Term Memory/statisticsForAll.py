import csv
import os
import pandas as pd
import math
import numpy as np

POIEdges = {'Sathorn_Thai_1': ['L197#1', 'L197#2'],
            'Sathorn_Thai_2': ['L30', 'L58#1', 'L58#2'],
            'Charoenkrung_1': ['L30032'],
            'Charoenkrung_2': ['L60', 'L73', 'L10149#1', 'L10149#2'],
            'Charoenkrung_3': ['L67'],
            'Silom_1': ['L138'],
            'Silom_2': ['L133.25'],
            'Silom_3': ['L49'],
            'Mehasak': ['L64'],
            'Surasak': ['L10130', 'L10189'],
            'Charoen_Rat': ['L40']
            }
percentage = ['100%','1%','5%','10%','15%','20%','25%','30%','35%','40%','45%','50%']
resolution = ['1','5','10','15','20','25','30','35','40','45','50','55','60']


def createFileForMean(fileNo):
    # to get the current directory
    dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'
    os.mkdir(dirpath + '/' + str(fileNo) + '/statistics')
    for time_resolution in resolution:

        myfile1 = open(
            dirpath + '/'+str(fileNo)+'/statistics/' + str(time_resolution) + '_mean.csv', 'w', newline='')
        writer1 = csv.writer(myfile1)
        #print(len(percentage))
        heading = ["Road Name",*percentage]
        writer1.writerow(heading)
        myfile1.close()

def createFileForStd(fileNo):
    # to get the current directory
    dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'
    for freq in resolution:
        myfile1 = open(
            dirpath + '/'+str(fileNo)+'/statistics/' + str(freq) + '_std.csv', 'w', newline='')
        writer1 = csv.writer(myfile1)
        # print(len(percentage))
        heading = ["Road Name", *percentage]
        writer1.writerow(heading)
        myfile1.close()

def parseFloat(str):
    try:
        return float(str)
    except:
        str = str.strip()
        if str.endswith("%"):
            return float(str.strip("%").strip()) / 100
        raise Exception("Don't know how to parse %s" % str)


def statisticsForResolution_And_Percentage(fileNo):
    dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'

    ###############################################
    #https://www.geeksforgeeks.org/program- mplement-standard-error-mean/
    # arr[] = {78.53, 79.62, 80.25, 81.05, 83.21, 83.46}
    # mean = (78.53 + 79.62 + 80.25 + 81.05 + 83.21 + 83.46) / 6
    # = 486.12 / 6
    # = 81.02
    # Sample Standard deviation = sqrt((78.53 – 81.02)
    # 2 + (79.62 - 81.02)
    # 2 + ...
    # + (83.46 – 81.02)
    # 2 / (6 – 1))
    # = sqrt(19.5036 / 5)
    # = 1.97502
    # Standard error of mean = 1.97502 / sqrt(6)
    # = 0.8063
    ###############################################
    for time_resolution in resolution:
        for edge, value in POIEdges.items():

            meanSpeed = []
            std = []
            for pcent in percentage:

                path = dirpath + '/'+str(fileNo)+'/' + edge + '_' + time_resolution + '_' + pcent + '.csv'
                if (os.path.exists(path)):
                    link_df = pd.read_csv(path)
                    meanSpeed.append(link_df['Mean Speed (km/h)'].mean())
                    std.append(link_df['Mean Speed (km/h)'].std())


            myfile = open(
                dirpath + '/'+str(fileNo)+'/statistics/' + str(time_resolution) + '_mean.csv', 'a', newline='')
            writer = csv.writer(myfile)
            with myfile:
                writer.writerow([edge, *meanSpeed])
                myfile.close()

            myfile = open(
                dirpath + '/'+str(fileNo)+'/statistics/' + str(time_resolution) + '_std.csv', 'a', newline='')
            writer = csv.writer(myfile)
            with myfile:
                writer.writerow([edge, *std])
                myfile.close()

def stasticsforLoop(fileNo):
    dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'

    for time_resolution in resolution:
        ###################for standard deviation###############################
        temp_1 =[]
        temp_1.append('Mean of standard deviation for all edges')  

        temp_2 = []
        temp_2.append('Standard Error of Mean')
        path = dirpath + '/'+str(fileNo)+'/statistics/' + str(time_resolution) + '_std.csv'
        if (os.path.exists(path)):
            road_df = pd.read_csv(path)
            for column in (list(road_df)):
                if column !='Road Name':

                    #print('Number of roads :', len(road_df))
                    temp_1.append(road_df[column].sum()/len(road_df)) # Mean of standard deviation for all edges

                    percent = parseFloat(column)
                    #print(time_resolution,column, road_df[column].sum())
                    #print(len(road_df))
                    temp_2.append((road_df[column].sum()/len(road_df))/math.sqrt(percent))# standard error of mean for all edges

            road_df.loc[len(road_df)] = temp_1
            road_df.loc[len(road_df)+1] = temp_2
            road_df.to_csv(dirpath + '/'+str(fileNo)+'/statistics/' + str(time_resolution) + '_std.csv',
                           index=False)

        ##################for mean ###############################

        temp = []
        temp.append('Mean Speed for all edges')
        path = dirpath + '/'+str(fileNo)+'/statistics/' + str(time_resolution) + '_mean.csv'
        if (os.path.exists(path)):
            road_df = pd.read_csv(path)
            for column in (list(road_df)):
                if column != 'Road Name':
                    temp.append(road_df[column].sum() / len(road_df))

            road_df.loc[len(road_df)] = temp
            road_df.to_csv(dirpath + '/'+str(fileNo)+'/statistics/' + str(time_resolution) + '_mean.csv',
                           index=False)


def readTotal(fileNo):
    dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'


    ####################for mean ###########################################
    myfile1 = open(
        dirpath + '/'+str(fileNo)+'/statistics/All_mean.csv', 'w', newline='')
    writer1 = csv.writer(myfile1)
    heading = ["Time Resolution",*percentage]
    writer1.writerow(heading)

    for time_resolution in resolution:
        temp =[]
        path = dirpath + '/'+str(fileNo)+'/statistics/' + str(time_resolution) + '_mean.csv'
        if (os.path.exists(path)):
            time_df = pd.read_csv(path)
            temp =  time_df.iloc[-1,:].values.tolist()
            #print(temp)
            temp.pop(0)
        writer1.writerow([time_resolution,*temp])

    myfile1.close()

    ##################for standard deviation #################################

    myfile1 = open(
        dirpath + '/'+str(fileNo)+'/statistics/All_std.csv', 'w', newline='')
    writer1 = csv.writer(myfile1)
    heading = ["Time Resolution", *percentage]
    writer1.writerow(heading)

    for time_resolution in resolution:
        temp = []
        path = dirpath + '/'+str(fileNo)+'/statistics/' + str(time_resolution) + '_std.csv'
        if (os.path.exists(path)):
            time_df = pd.read_csv(path)
            temp = time_df.iloc[-2,:].values.tolist()

            temp.pop(0)
        writer1.writerow([time_resolution,*temp])

    myfile1.close()

    ###################for standard error of mean################################################

    myfile1 = open(
        dirpath + '/'+str(fileNo)+'/statistics/All_stdError.csv', 'w', newline='')
    writer1 = csv.writer(myfile1)
    heading = ["Time Resolution", *percentage]
    writer1.writerow(heading)

    for time_resolution in resolution:
        temp = []
        path = dirpath + '/'+str(fileNo)+'/statistics/' + str(time_resolution) + '_std.csv'
        if (os.path.exists(path)):
            time_df = pd.read_csv(path)
            temp = time_df.iloc[-1, :].values.tolist()

            temp.pop(0)
        writer1.writerow([time_resolution, *temp])

    myfile1.close()


def plotAllMean(fileNo):
    import pandas as pd
    import matplotlib.pyplot as plt

    dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'
    path = dirpath + '/'+str(fileNo)+'/statistics/All_mean.csv'

    if (os.path.exists(path) ):
        mean_all_df = pd.read_csv(path)

        colors = ['#CB4335', '#808000', '#616A6B', '#009E73', '#ABB2B9', '#E69F00', '#800000']
        #percentage.pop(0)
        names = percentage
        #https://stackoverflow.com/questions/29498652/plot-bar-graph-from-pandas-dataframe
        mean_df = mean_all_df.set_index("Time Resolution")

        ax = mean_df[[*names]].plot(kind='bar', figsize=(15, 10), legend=True, color=colors)
        ax.set_xlabel("Time resolution", fontsize=20, fontname='Times New Roman')
        ax.set_ylabel("Mean", fontsize=20, fontname='Times New Roman')
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'family': 'Times New Roman', 'size': 20})
        # plt.legend(prop={'family' :'Times New Roman'})
        plt.xticks(fontsize=20, fontname='Times New Roman', rotation=0)
        plt.yticks(fontsize=20, fontname='Times New Roman')
        # plt.rcParams.update({'font.family':'Times New Roman'})
        plt.tight_layout()
        plt.savefig(
            dirpath + '/'+str(fileNo)+'/statistics/All_mean.png',
            width=1800, height=500)



def plotAllStd(fileNo):
    import pandas as pd
    import matplotlib.pyplot as plt

    dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'
    path = dirpath + '/'+str(fileNo)+'/statistics/All_std.csv'
    if (os.path.exists(path)):
        std_all_df = pd.read_csv(path)
        #colors = ['#E69F00', '#56B4E9', '#F0E442', '#009E73', '#D55E00', '#2E4053', '#0000FF']
        colors = ['#CB4335', '#808000', '#616A6B', '#009E73', '#ABB2B9', '#E69F00', '#0000FF']
        #percentage.pop(0)
        names = percentage
        #https://stackoverflow.com/questions/29498652/plot-bar-graph-from-pandas-dataframe
        df = std_all_df.set_index("Time Resolution")

        ax = df[[*names]].plot(kind='bar', figsize=(15, 10), legend=True, color=colors)
        ax.set_xlabel("Time resolution", fontsize=20, fontname='Times New Roman')
        ax.set_ylabel("Standard deviation", fontsize=20, fontname='Times New Roman')
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'family': 'Times New Roman', 'size': 20})
        # plt.legend(prop={'family' :'Times New Roman'})
        plt.xticks(fontsize=20, fontname='Times New Roman', rotation=0)
        plt.yticks(fontsize=20, fontname='Times New Roman')
        # plt.rcParams.update({'font.family':'Times New Roman'})
        plt.tight_layout()
        plt.savefig(
            dirpath + '/'+str(fileNo)+'/statistics/All_std.png',
            width=1800, height=500)

def plotAllStandardErrorOfMean(fileNo):
    import pandas as pd
    import matplotlib.pyplot as plt

    dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'
    path = dirpath + '/'+str(fileNo)+'/statistics/All_stdError.csv'
    if (os.path.exists(path)):
        stderror_all_df = pd.read_csv(path)
        #colors = ['#E69F00', '#56B4E9', '#F0E442', '#009E73', '#D55E00', '#2E4053', '#0000FF']
        #colors = ['#CB4335', '#808000', '#616A6B', '#009E73', '#ABB2B9', '#E69F00', '#0000FF']
        colors = ['#FFA07A', '#FF7F50', '#FFFFE0', '#98FB98', '#E0FFFF', '#B0E0E6', '#E6E6FA', '#FFC0CB',
                  '#F0FFF0', '#DCDCDC', '#8B0000', '#FF8C00', '#FFFF00', '#6B8E23', '#008080',
                  '#483D8B', '#4B0082', '#C71585', '#000000', '#800000']
        names = percentage
        #https://stackoverflow.com/questions/29498652/plot-bar-graph-from-pandas-dataframe
        df = stderror_all_df.set_index("Time Resolution")

        ax = df[[*names]].plot(kind='bar',figsize=(15, 10), legend=True, color=colors)
        ax.set_xlabel("Time Resolution", fontsize=20, fontname ='Times New Roman')
        ax.set_ylabel("Standard Error of Mean", fontsize=20, fontname ='Times New Roman')
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'family' :'Times New Roman','size':20})
        #plt.legend(prop={'family' :'Times New Roman'})
        plt.xticks(fontsize=20, fontname = 'Times New Roman',rotation=0)
        plt.yticks(fontsize=20,fontname = 'Times New Roman')
        #plt.rcParams.update({'font.family':'Times New Roman'})
        plt.tight_layout()
        plt.savefig(
            dirpath + '/'+str(fileNo)+'/statistics/All_stdError.png',
            width=1800, height=500)


def plotLineChart_AllStandardErrorOfMean(fileNo):
    import pandas as pd
    import matplotlib.pyplot as plt

    dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'
    path = dirpath + '/'+str(fileNo)+'/statistics/All_stdError.csv'
    if (os.path.exists(path)):
        stderror_all_df = pd.read_csv(path)
        #colors = ['#E69F00', '#56B4E9', '#F0E442', '#009E73', '#D55E00', '#2E4053', '#0000FF']
        #colors = ['#CB4335', '#808000', '#616A6B', '#009E73', '#ABB2B9', '#E69F00', '#0000FF']

        colors =['#FFA07A','#FF7F50','#FFFFE0','#98FB98','#E0FFFF','#B0E0E6','#E6E6FA','#FFC0CB',
                 '#F0FFF0','#DCDCDC','#8B0000','#FF8C00', '#FFFF00', '#6B8E23', '#008080',
                 '#483D8B', '#4B0082', '#C71585', '#000000', '#800000']
        names = percentage
        #https://stackoverflow.com/questions/29498652/plot-bar-graph-from-pandas-dataframe
        df = stderror_all_df.set_index("Time Resolution")

        ax = df[[*names]].plot(kind='line',figsize=(15, 10), legend=True, color=colors)
        ax.set_xlabel("Time Resolution", fontsize=20, fontname ='Times New Roman')
        ax.set_ylabel("Standard Error of Mean", fontsize=20, fontname ='Times New Roman')
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'family' :'Times New Roman','size':20})
        #plt.legend(prop={'family' :'Times New Roman'})
        plt.xticks(fontsize=20, fontname = 'Times New Roman',rotation=0)
        plt.yticks(fontsize=20,fontname = 'Times New Roman')
        #plt.rcParams.update({'font.family':'Times New Roman'})
        plt.tight_layout()
        plt.savefig(
            dirpath + '/'+str(fileNo)+'/statistics/All_stdError_Line.png',
            width=1800, height=500)
################################################################


def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

# def detectionMetric():
#     dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'
#     resolution = ['60']
#
#     myfile1 = open(
#         dirpath + '/'+str(fileNo)+'/statistics/detectionMetric.csv', 'w', newline='')
#     writer1 = csv.writer(myfile1)
#     # print(len(percentage))
#     heading = ["Samples","NDPG","NTPG","NPFA","NTPA","DR_PG","FAR_PG","NDG","NTG","NFA","NTA","DR_G","FAR_G"]
#     writer1.writerow(heading)
#
#     #############################
#     #NTPG =  Number of total potential gridlock
#     #NDPG =  Number of detected potential gridlock
#     #NTPA =  Number of total potential gridlock alarm
#     #NPFA =  Number of potential gridlock false alarm
#     #DR_PG =  Detected rate of potential gridlock
#     #FAR_PG = False alarm rate of potential gridlock
#
#     # NTG =  Number of total gridlock
#     # NDG =  Number of detected gridlock
#     # NTA =  Number of total gridlock alarm
#     # NFA =  Number of gridlock false alarm
#     # DR_G =  Detected rate of gridlock
#     # FAR_G = False alarm rate of gridlock
#     #############################
#
#     actual_data = pd.read_csv(dirpath + '/'+str(fileNo)+'/cluster/60_100%_AllCluster.csv')
#
#
#     NTPG_list =  actual_data[actual_data['Gridlock']==1]
#     #print(NTPG_list)
#     NTPG =  len(NTPG_list)
#     actual_potential_Index = actual_data.query('Gridlock == 1').index.tolist()
#
#
#     NTG_list = actual_data[actual_data['Gridlock']==2]
#     NTG = len(NTG_list)
#     actual_gridlock_Index = actual_data.query('Gridlock == 2').index.tolist()
#
#
#
#     for time_resolution in resolution:
#         #percentage.pop(0)
#         #print(percentage)
#
#         for pcent in percentage:
#             predicted_data = pd.read_csv(dirpath + '/'+str(fileNo)+'/cluster/' + time_resolution + '_' + pcent + '_AllCluster.csv')
#
#             ####################### for potential gridlock ####################
#             predicted_potential_Index = predicted_data.query('Gridlock == 1').index.tolist()
#             NDPG = len(set(actual_potential_Index) & set(predicted_potential_Index))
#             NTPA =  len(predicted_potential_Index)
#             NPFA = len(diff(predicted_potential_Index,actual_potential_Index))
#
#             DR_PG = 0
#             FAR_PG = 0
#
#             if NTPG  !=0 and NTPA !=0:
#                 DR_PG =  (NDPG/NTPG) *100
#                 FAR_PG = (NPFA/NTPA) *100
#
#
#             #####################for gridlock #################################
#             predicted_gridlock_Index = predicted_data.query('Gridlock == 2').index.tolist()
#             NDG = len(set(actual_gridlock_Index) & set(predicted_gridlock_Index))
#             NTA = len(predicted_gridlock_Index)
#             NFA = len(diff(predicted_gridlock_Index, actual_gridlock_Index))
#
#             DR_G = 0
#             FAR_G = 0
#
#             if NTG != 0 and NTA != 0:
#                 DR_G = (NDG / NTG) * 100
#                 FAR_G = (NFA / NTA) * 100#

#             ##################writing file#####################
#             writer1.writerow([pcent,NDPG,NTPG,NPFA,NTPA,DR_PG,FAR_PG,NDG,NTG,NFA,NTA,DR_G,FAR_G])
#
#     myfile1.close()


def detectionMetricForEachLabel(fileNo):
    dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'
    resolution = ['60'] # To evaluate gridlock detection, I use only 60s time resoultion with various sample size 

    for label in range(5):

        myfile1 = open(
            dirpath + '/'+str(fileNo)+'/statistics/detectionMetricForLabel_'+str(label+1)+'.csv', 'w', newline='')
        writer1 = csv.writer(myfile1)
        # print(len(percentage))
        heading = ["Samples","ND_"+str(label+1),"NT_"+str(label+1),"NFA_"+str(label+1),"NTA_"+str(label+1),"DR_"+str(label+1),"FAR_"+str(label+1)]
        writer1.writerow(heading)

        ############################################
        # NT =  Number of total respective level
        # ND =  Number of detected respective level
        # NTA =  Number of total  respective alarm
        # NFA =  Number of  respective false alarm
        # DR =  Detected rate of respective level
        # FAR = False alarm rate of respective level
        ############################################

        actual_data = pd.read_csv(dirpath + '/'+str(fileNo)+'/cluster/60_100%_AllCluster.csv')


        NT_list =  actual_data[actual_data['Gridlock']==(label+1)]
        NT =  len(NT_list)

        actual_Index = actual_data[actual_data['Gridlock'] ==(label+1)].index.tolist()
        for time_resolution in resolution:
            for pcent in percentage:
                predicted_data = pd.read_csv(dirpath + '/'+str(fileNo)+'/cluster/' + time_resolution + '_' + pcent + '_AllCluster.csv')

                #################################################
                predicted_Index = predicted_data[predicted_data['Gridlock'] ==(label+1)].index.tolist()
                ND = len(set(actual_Index) & set(predicted_Index))
                NTA =  len(predicted_Index)
                NFA = len(diff(predicted_Index,actual_Index))

                DR = 0
                FAR = 0

                if NT!=0 and NTA !=0:
                    DR =  (ND/NT) *100
                    FAR = (NFA/NTA) *100
                ##################writing file####################

                writer1.writerow([pcent,ND,NT,NFA,NTA,DR,FAR])
        myfile1.close()

def plotDetectionRate(fileNo):
    import pandas as pd
    import matplotlib.pyplot as plt

    dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'

    for label in range(5):
        path = dirpath + '/'+str(fileNo)+'/statistics/detectionMetricForLabel_'+str(label+1)+'.csv'
        if (os.path.exists(path)):
            all_df = pd.read_csv(path)
            #colors = ['#616A6B','#ABB2B9']
            colors = ['#616A6B']

            #names = ["DR_PG", "DR_G"]
            names = ["DR_"+str(label+1)]
            #https://stackoverflow.com/questions/29498652/plot-bar-graph-from-pandas-dataframe
            df = all_df.set_index("Samples")

            ax = df[[*names]].plot(kind='bar',figsize=(15, 10), legend=True, color=colors, width =0.8)
            ax.set_xlabel("Data Samples", fontsize=20, fontname ='Times New Roman')
            ax.set_ylabel("Detection Rate (%)", fontsize=20, fontname ='Times New Roman')
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'family' :'Times New Roman','size':20})

            ################################################################################
            #https://robertmitchellv.com/blog-bar-chart-annotations-pandas-mpl.html
            # create a list to collect the plt.patches data
            totals = []

            # find the values and append to list
            for i in ax.patches:
                totals.append(i.get_height())

            # set individual bar lables using above list
            for i in ax.patches:
                # get_x pulls left or right; get_height pushes up or down
                ax.text(i.get_x() - .001, i.get_height() + .5, \
                        str(int(round((i.get_height())))) + '%', fontsize=10,
                        color='red')
            ################################################################################

            #plt.legend(prop={'family' :'Times New Roman'})
            plt.xticks(fontsize=20, fontname = 'Times New Roman',rotation=0)
            plt.yticks(fontsize=20,fontname = 'Times New Roman')
            #plt.rcParams.update({'font.family':'Times New Roman'})
            plt.tight_layout()
            plt.savefig(
                dirpath + '/'+str(fileNo)+'/statistics/DetectionRate_'+str(label+1)+'_.png',
                width=1800, height=500)

def plotFalseAlarmRate(fileNo):
    import pandas as pd
    import matplotlib.pyplot as plt

    dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'

    for label in range(5):
        # print('False Alarm rate for class label :'+str(label+1))
        path = dirpath + '/'+str(fileNo)+'/statistics/detectionMetricForLabel_'+str(label+1)+'.csv'
        if (os.path.exists(path)):
            all_df = pd.read_csv(path)
            #colors = ['#009E73', '#E69F00']
            colors = ['#009E73']

            #names = ["FAR_PG","FAR_G"]
            names = ["FAR_"+str(label+1)]
            #https://stackoverflow.com/questions/29498652/plot-bar-graph-from-pandas-dataframe
            df = all_df.set_index("Samples")

            ax = df[[*names]].plot(kind='bar',figsize=(15, 10), legend=True, color=colors, width =0.8)
            ax.set_xlabel("Data Samples", fontsize=20, fontname ='Times New Roman')
            ax.set_ylabel("False Alarm Rate (%)", fontsize=20, fontname ='Times New Roman')
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'family' :'Times New Roman','size':20})

            ################################################################################
            #https://robertmitchellv.com/blog-bar-chart-annotations-pandas-mpl.html
            # create a list to collect the plt.patches data
            totals = []

            # find the values and append to list
            for i in ax.patches:
                totals.append(i.get_height())

            # set individual bar lables using above list
            for i in ax.patches:
                # get_x pulls left or right; get_height pushes up or down
                ax.text(i.get_x() - .001, i.get_height() + .5, \
                        str(int(round((i.get_height())))) + '%', fontsize=10,
                        color='red')
            ################################################################################

            #plt.legend(prop={'family' :'Times New Roman'})
            plt.xticks(fontsize=20, fontname = 'Times New Roman',rotation=0)
            plt.yticks(fontsize=20,fontname = 'Times New Roman')
            #plt.rcParams.update({'font.family':'Times New Roman'})
            plt.tight_layout()
            plt.savefig(
                dirpath + '/'+str(fileNo)+'/statistics/FalseAlarmRate_'+str(label+1)+'_.png',
                width=1800, height=500)
#========================================================================================

def StandardErrorofMeanforEachEdge_TimeResolutionFileIndex(): # In my dataset, I used edge and road interchangeably, but both are same.
    dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'
    for time_resolution in resolution:
        temp_df = pd.DataFrame()
        temp_df['Road Name']= POIEdges.keys()
        for pcent in percentage:
            temp_1 = list()

            for edge, value in POIEdges.items():

                percent = parseFloat(pcent)

                temp_2 = list()
                for fileNo in range(1, 101):
                    path = dirpath + '/' + str(fileNo) + '/statistics/' + time_resolution + '_std.csv'
                    if (os.path.exists(path)):
                        df = pd.read_csv(path)
                        #print(df[df['Road Name'] == edge][pcent].values[0])
                        temp_2.append(df[df['Road Name'] == edge][pcent].values/math.sqrt(percent)) # standard error of mean of speed of vehicles on this edge

                temp_1.append(np.mean(temp_2))

            temp_df[pcent] = temp_1

        temp_df.to_csv(dirpath + '/StandardErrorOfMeanForAllEdges/' + str(time_resolution) + '_std_ForAllEdges.csv',
                   index=False)


def plotStandardErrorOfMeanForEachLink_TimeResolutionFileIndex():
    import pandas as pd
    import matplotlib.pyplot as plt

    dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID/'
    print(dirpath)
    percentage.pop(0)
    for time_resoultion in resolution:
        path = dirpath + '/StandardErrorOfMeanForAllEdges/StandardErrorOfMeanForEachLink_TimeResolutionFileIndex/'+str(time_resoultion)+'_std_ForAllEdges.csv'
        if (os.path.exists(path)):
            stderror_all_df = pd.read_csv(path)
            colors = ['#CD5C5C', '#808080', '#808000', '#0000FF', '#000080', '#BDB76B', '#3CB371', '#D8BFD8']


            names = percentage
            #https://stackoverflow.com/questions/29498652/plot-bar-graph-from-pandas-dataframe
            df = stderror_all_df.set_index("Road Name")
            #print(df)
            ax = df[[*names]].plot(kind='bar',figsize=(15, 10), legend=True, color=colors)
            ax.set_xlabel("Link Name", fontsize=20, fontname ='Times New Roman')
            ax.set_ylabel("Standard Error of Mean", fontsize=20, fontname ='Times New Roman')
            ax.legend(title = "Samples", loc='center left', bbox_to_anchor=(1, 0.5),prop={'family' :'Times New Roman','size':20})
            #plt.legend(prop={'family' :'Times New Roman'})
            plt.xticks(fontsize=20, fontname = 'Times New Roman',rotation=90)
            plt.yticks(fontsize=20,fontname = 'Times New Roman')
            plt.title('Standard Error of Mean Speed of Vehicles on each Link with time resoultion '+time_resoultion +'s',fontsize=20, fontname='Times New Roman')
            #plt.rcParams.update({'font.family':'Times New Roman'})
            plt.tight_layout()
            plt.savefig(dirpath + '/StandardErrorOfMeanForAllEdges/' + str(time_resoultion) + '_std_ForAllEdges.png',
                width=1800, height=500)

def StandardErrorofMeanforEachEdge_SamplesFileIndex(): # In my dataset, I used edge and road interchangeably, but both are same.
    dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'
    for pcent in percentage:
        temp_df = pd.DataFrame()
        temp_df['Road Name']= POIEdges.keys()

        for time_resolution in resolution:
            temp_1 = list()

            for edge, value in POIEdges.items():

                percent = parseFloat(pcent)

                temp_2 = list()
                for fileNo in range(1, 101):
                    path = dirpath + '/' + str(fileNo) + '/statistics/' + time_resolution + '_std.csv'
                    if (os.path.exists(path)):
                        df = pd.read_csv(path)
                        #print(df[df['Road Name'] == edge][pcent].values[0])
                        temp_2.append(df[df['Road Name'] == edge][pcent].values/math.sqrt(percent)) # standard error of mean of speed of vehicles on this edge

                temp_1.append(np.mean(temp_2))

            temp_df[time_resolution] = temp_1

        temp_df.to_csv(dirpath + '/StandardErrorOfMeanForAllEdges/' + str(pcent) + '_std_ForAllEdges.csv',
                   index=False)


def plotStandardErrorOfMeanForEachLink_SamplesFileIndex():
    import pandas as pd
    import matplotlib.pyplot as plt

    dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID/'

    percentage.insert(0,'100%')
    for pcent in percentage:

        path = dirpath + '/StandardErrorOfMeanForAllEdges/StandardErrorOfMeanForEachLink_SamplesFileIndex/'+pcent+'_std_ForAllEdges - Copy.csv'

        if (os.path.exists(path)):
            print(percentage)
            stderror_all_df = pd.read_csv(path)
            colors = ['#CD5C5C', '#808080', '#808000', '#0000FF', '#000080', '#BDB76B', '#3CB371', '#D8BFD8',
                      '#483D8B', '#dfbec3', '#C0C0C0', '#000000', '#800000']


            names = resolution
            #https://stackoverflow.com/questions/29498652/plot-bar-graph-from-pandas-dataframe
            df = stderror_all_df.set_index("Road Name")
            #print(df)
            ax = df[[*names]].plot(kind='bar',figsize=(15, 10), legend=True, color=colors)
            ax.set_xlabel("Link Name", fontsize=20, fontname ='Times New Roman')
            ax.set_ylabel("Standard Error of Mean", fontsize=20, fontname ='Times New Roman')
            ax.legend(title ="Time Resolution (s)", loc='center left', bbox_to_anchor=(1, 0.5),prop={'family' :'Times New Roman','size':20})
            #plt.legend(prop={'family' :'Times New Roman'})
            plt.xticks(fontsize=20, fontname = 'Times New Roman',rotation=90)
            plt.yticks(fontsize=20,fontname = 'Times New Roman')
            plt.title('Standard Error of Mean Speed of Vehicles on each Link with time resoultion '+ pcent,fontsize=20, fontname='Times New Roman')
            #plt.rcParams.update({'font.family':'Times New Roman'})
            plt.tight_layout()
            plt.savefig(dirpath + '/StandardErrorOfMeanForAllEdges/' + pcent + '_std_ForAllEdges.png',
                width=1800, height=500)

#main functin
#========================================================================================
def main():
    # for fileNo in range(1,101):
    #     print(fileNo ,'is working ')
    #     createFileForMean(fileNo)
    #     createFileForStd(fileNo)
    #     statisticsForResolution_And_Percentage(fileNo)
    #     stasticsforLoop(fileNo)
    #     readTotal(fileNo)
    #     plotAllMean(fileNo)
    #     plotAllStd(fileNo)
    #     plotAllStandardErrorOfMean(fileNo)
    #     plotLineChart_AllStandardErrorOfMean(fileNo)
    #     # detectionMetric()
    #     detectionMetricForEachLabel(fileNo)
    #     plotDetectionRate(fileNo)
    #     plotFalseAlarmRate(fileNo)
    # StandardErrorofMeanforEachEdge_TimeResolutionFileIndex()
    # plotStandardErrorOfMeanForEachLink_TimeResolutionFileIndex()
    # StandardErrorofMeanforEachEdge_SamplesFileIndex()
    plotStandardErrorOfMeanForEachLink_SamplesFileIndex()

if __name__=="__main__":
    main()
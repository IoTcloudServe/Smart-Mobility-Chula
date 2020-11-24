import csv
import os
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt

percentage = ['1%','5%','10%','15%','20%','25%','30%','35%','40%','45%','50%']
setting = {'1': ['10','20','10'], # setting 1 (epoch:10, batch_size:20,neurons:10)
            '2': ['10','20','20'],
            '3': ['50','20','10'],
            '4': ['10','50','10'],
            '5': ['50','10','10'],
            '6': ['10','10','1']
            }
time_lagged_observation =['1','5','10','15','30','60']

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

def detectionMetricForEachLabel():

    dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'
    resolution = ['60'] # To evaluate gridlock detection, I use only 60s time resoultion with various sample size

    myfile1 = open(
        dirpath + '/LSTMExperimentResults_DR_FAR_AfterDefense/All_DR_FAR.csv', 'w', newline='')
    writer1 = csv.writer(myfile1)
    # print(len(percentage))
    heading = ['epoch','batch_size','neurons','samples','time_lagged_observation','DR_1','FAR_1','DR_2','FAR_2','DR_3','FAR_3',
               'DR_4','FAR_4','DR_5','FAR_5']
    writer1.writerow(heading)


    for key, value in setting.items():
        for percent in percentage:
            for history in time_lagged_observation:

                data = pd.read_csv(dirpath + '/LSTMExperimentResults_AfterDefense/'+percent+'_'+history+'min_'+value[0]+'epochs_'+value[1]+'batch_size_'+value[2]+'neurons.csv')
                temp = data['predicted'].tolist()
                temp_convert = [np.round(num) for num in temp]
                data['round_predicted'] = temp_convert
                DR_FAR =[]
                for label in range(5):
                    ############################################
                    # NT =  Number of total respective level
                    # ND =  Number of detected respective level
                    # NTA =  Number of total  respective alarm
                    # NFA =  Number of  respective false alarm
                    # DR =  Detected rate of respective level
                    # FAR = False alarm rate of respective level
                    ############################################

                    NT_list =  data[data['actual']==(label+1)]
                    NT =  len(NT_list)
                    actual_Index = data[data['actual'] ==(label+1)].index.tolist()

                    #################################################
                    predicted_Index = data[data['round_predicted'] ==(label+1)].index.tolist()
                    ND = len(set(actual_Index) & set(predicted_Index))
                    NTA =  len(predicted_Index)
                    NFA = len(diff(predicted_Index,actual_Index))

                    DR = 0
                    FAR = 0
                    if NT!=0 and NTA !=0:
                        DR =  (ND/NT) *100
                        FAR = (NFA/NTA) *100
                       ##################writing file####################
                        DR_FAR.append(DR)
                        DR_FAR.append(FAR)

                writer1.writerow([value[0],value[1],value[2],percent,history,*DR_FAR])


def plotDetectionRate():
    percentage = ['1%','5%', '10%', '15%', '20%', '25%', '30%', '35%', '40%', '45%', '50%']
    setting = {'1': ['10', '20', '10'],  # setting 1 (epoch:10, batch_size:20,neurons:10)
               '2': ['10', '20', '20'],
               '3': ['50', '20', '10'],
               '4': ['10', '50', '10'],
               '5': ['50', '10', '10'],
               '6': ['10','10','1']
               }
    time_lagged_obeservation = ['1', '5', '10', '15', '30', '60']

    dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'
    data = pd.read_csv(dirpath + '/LSTMExperimentResults_DR_FAR_AfterDefense/All_DR_FAR.csv')

    for key, value in setting.items():
        for history in time_lagged_obeservation:

            filter_df = data[(data['epoch'] == int(value[0])) & (data['batch_size']== int(value[1]))
                        & (data['neurons']== int(value[2])) & (data['time_lagged_observation']== int(history))
            ]

            # print(filter_df['samples'])
            # filter_df = filter_df.astype(float)
            # filter_df = filter_df.astype({"DR_1": 'float', "DR_2": 'float',"DR_3": 'float',"DR_4": 'float',"DR_5": 'float'})

            colors = ['#CD5C5C', '#808080', '#808000', '#BDB76B', '#3CB371']

            names = ["DR_1", "DR_2", "DR_3", "DR_4", "DR_5"]
            # https://stackoverflow.com/questions/29498652/plot-bar-graph-from-pandas-dataframe
            filter_df = filter_df.set_index("samples")

            ax = filter_df[[*names]].plot(kind='bar', figsize=(15, 10), legend=True, color=colors, width=0.8)
            ax.set_xlabel("Samples", fontsize=20, fontname='Times New Roman')
            ax.set_ylabel("Detection Rate (%)", fontsize=20, fontname='Times New Roman')
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'family': 'Times New Roman', 'size': 20})

            ################################################################################
            # https://robertmitchellv.com/blog-bar-chart-annotations-pandas-mpl.html
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

            # plt.legend(prop={'family' :'Times New Roman'})
            plt.xticks(fontsize=20, fontname='Times New Roman', rotation=0)
            plt.yticks(fontsize=20, fontname='Times New Roman')
            # plt.rcParams.update({'font.family':'Times New Roman'})
            plt.tight_layout()
            plt.savefig(
                dirpath + '/LSTMExperimentResults_DR_FAR_AfterDefense/detectionRateFor_epoch_' + value[0] +
                '_batch_' + value[1] + '_neuron_' + value[2] + '_' + history + '_min.png', width=1800, height=500)

def plotFalseAlarmRate():
    percentage = ['1%','5%', '10%', '15%', '20%', '25%', '30%', '35%', '40%', '45%', '50%']
    setting = {'1': ['10', '20', '10'],  # setting 1 (epoch:10, batch_size:20,neurons:10)
               '2': ['10', '20', '20'],
               '3': ['50', '20', '10'],
               '4': ['10', '50', '10'],
               '5': ['50', '10', '10'],
               '6': ['10', '10', '1']
               }
    time_lagged_obeservation = ['1', '5', '10', '15', '30', '60']

    dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'
    data = pd.read_csv(dirpath + '/LSTMExperimentResults_DR_FAR_AfterDefense/All_DR_FAR.csv')

    for key, value in setting.items():
        for history in time_lagged_obeservation:

            filter_df = data[(data['epoch'] == int(value[0])) & (data['batch_size']== int(value[1]))
                        & (data['neurons']== int(value[2])) & (data['time_lagged_observation']== int(history))
            ]

            # print(filter_df['samples'])

            # filter_df = filter_df.astype(
            #     {"FAR_1": 'float', "FAR_2": 'float', "FAR_3": 'float', "FAR_4": 'float', "FAR_5": 'float'})

            colors = ['#CD5C5C', '#808080', '#808000', '#BDB76B', '#3CB371']

            names = ["FAR_1", "FAR_2", "FAR_3", "FAR_4", "FAR_5"]
            # https://stackoverflow.com/questions/29498652/plot-bar-graph-from-pandas-dataframe
            filter_df = filter_df.set_index("samples")

            ax = filter_df[[*names]].plot(kind='bar', figsize=(15, 10), legend=True, color=colors, width=0.8)
            ax.set_xlabel("Samples", fontsize=20, fontname='Times New Roman')
            ax.set_ylabel("False Alarm Rate (%)", fontsize=20, fontname='Times New Roman')
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'family': 'Times New Roman', 'size': 20})

            ################################################################################
            # https://robertmitchellv.com/blog-bar-chart-annotations-pandas-mpl.html
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

            # plt.legend(prop={'family' :'Times New Roman'})
            plt.xticks(fontsize=20, fontname='Times New Roman', rotation=0)
            plt.yticks(fontsize=20, fontname='Times New Roman')
            # plt.rcParams.update({'font.family':'Times New Roman'})
            plt.tight_layout()
            plt.savefig(
                dirpath + '/LSTMExperimentResults_DR_FAR_AfterDefense/falseAlarmRateFor_epoch_'+value[0]+
                '_batch_'+value[1]+'_neuron_'+value[2]+'_'+history+'_min.png', width=1800, height=500)


#main functin
#========================================================================================
def main():
    detectionMetricForEachLabel()
    plotDetectionRate()
    plotFalseAlarmRate()

if __name__=="__main__":
    main()
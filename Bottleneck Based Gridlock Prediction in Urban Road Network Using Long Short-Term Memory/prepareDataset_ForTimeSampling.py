import numpy as np
import pandas as pd
from pandas import DataFrame
import glob
import os
from pandas import read_csv
from datetime import datetime
import shutil

cluster=['cluster_185_186','cluster_159_32_6_7','cluster_43_44','cluster_46_47','cluster_83_84']
# load dataset


percentage = ['1%','5%','10%','15%','20%','25%','30%','35%','40%','45%','50%','100%']
time_resolution = ['60']

dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'
for number in range (0, 100):
    #os.makedirs(dirpath + '/outputFile_'+str(number+1)+'/dataset')
    # if os.path.isdir(dirpath + '/outputFile_' + str(number + 1) + '/datasetForTimeSampling'):
    #     shutil.rmtree(dirpath + '/outputFile_' + str(number + 1) + '/datasetForTimeSampling', ignore_errors=True)
    # os.mkdir(dirpath + '/' + str(number + 1) + '/datasetForTimeSampling')
    os.mkdir(dirpath + '/' + str(number + 1) + '/datasetForTimeSampling/15mins')
    for percent in percentage:
        #for resolution in time_resolution:
        df = pd.DataFrame()
        for c in cluster:
			#path = dirpath + '/outputFile_'+str(number)+'/cluster/' + resolution + '_' + percent + '_' + c + '.csv'
            path = dirpath + '/'+str(number+1)+'/cluster/60_' + percent + '_' + c + '.csv'
            # print(path)
            clusters = glob.glob(path)
            #print(clusters)
            for i, fname in enumerate(clusters):
                with open(fname, 'rb') as infile:
                    dataset = pd.read_csv(fname, header=0, sep=',')
                    # print(dataset.columns)
                    index = 0
                    temp_list = list()
                    while(index <= len(dataset)):
                        print(index )
                        temp_list.append(dataset.loc[index,'Cluster Congestion'])
                        index += 15# for every 5 minutes

                    df[c] = temp_list
                    #print(df.head())

        # to read gridlock
        dataset = pd.read_csv(
            dirpath + '/'+str(number+1)+'/cluster/60_' + percent + '_AllCluster.csv', header=0,
			sep=',')
        index = 0
        temp_list = list()
        while (index <= len(dataset)):
            temp_list.append(dataset.loc[index, 'Gridlock'])
            index += 15# for every 5 minutes
        df['gridlock'] = temp_list

        # to read time
        index = 0
        temp_list = list()
        while (index <= len(dataset)):
            temp_list.append(dataset.loc[index, 'Time(s)'])
            index += 15 # for every 5 minutes

        df.insert(0, 'time(s)', temp_list)
        #print(df.columns)
        df.to_csv(dirpath + '/'+str(number+1)+'/datasetForTimeSampling/15mins/60_' + percent + '_combine.csv',
				  index=False)
import csv

import os, sys
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import numpy as np
import matplotlib.font_manager



#==================================================================================================
def plotClusterCongestionState():
    dirpath = 'C:\RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'

    fig, ax = plt.subplots(1, 1, figsize=(12, 5), sharex=True, sharey=True)
    ticks_font = matplotlib.font_manager.FontProperties(family='times new roman', style='normal', size=12,
                                                        weight='normal', stretch='normal')

    path = dirpath + '/LSTMExperimentResults_AfterDefense/5%_1min_10epochs_50batch_size_10neurons - Copy.csv'
    df = pd.read_csv(path)
    # print(df.columns)
    temp = df['predicted'].tolist()
    temp_convert = [np.round(num) for num in temp]
    df['round_predicted'] = temp_convert
    # df = pd.DataFrame(df, columns=['actual', 'round_predicted'])
    # df = df.astype(int)
    # df = df.set_index(pd.DatetimeIndex(df['Time']))

    ax.plot(df['round_predicted'], label='predicted', linewidth=0.5, color='r')
    ax.plot(df['actual'], label='actual', linewidth=0.5, color='b')
    # leg = ax.legend(loc="upper left", prop={'family': 'times new roman', 'size': 14}, handlelength=0,
    #                    handletextpad=0, fancybox=True)
    leg = ax.legend(loc="upper left", prop={'family': 'times new roman', 'size': 14})
    # for item in leg.legendHandles:
    #     item.set_visible(False)
    # ax[i].legend(loc="upper left")

    # ax.xaxis_date()
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    # ax[i].title.set_text(key)

    for label in ax.get_xticklabels():
        label.set_fontproperties(ticks_font)
    for label in ax.get_yticklabels():
        label.set_fontproperties(ticks_font)


    # plt.yticks(np.arange(0, 6, 1.0))
    plt.xlabel('Time (min)', fontsize=16, fontname='Times New Roman')
    plt.ylabel('Gridlock Labels', fontsize=16, fontname='Times New Roman')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),
               prop={'family': 'Times New Roman', 'size': 16})
    fig.tight_layout()
    plt.savefig(
        dirpath + '/LSTMExperimentResults_AfterDefense/5%_1min_10epochs_50batch_size_10neurons-actualAndpredict.png',
        width=2000, height=500)
    plt.show()

    for ax in fig.get_axes():
        ax.label_outer()

    plt.close()

#main functin
#========================================================================================
def main():
    plotClusterCongestionState()

if __name__=="__main__":
    main()
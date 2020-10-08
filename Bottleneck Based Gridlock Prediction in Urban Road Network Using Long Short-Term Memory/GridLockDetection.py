import csv
import pathlib
import glob
import os, sys
import pandas as pd
from itertools import groupby
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.io as pio
import plotly
import plotly.offline as py
import plotly.graph_objs as go
import numpy as np
import matplotlib.font_manager

cluster = {
        'cluster_185_186': ['Sathorn_Thai_2', 'Charoenkrung_1'],
        'cluster_83_84': ['Charoenkrung_2', 'Charoenkrung_3'],
        'cluster_159_32_6_7': ['Silom_1'],
        'cluster_43_44': ['Silom_2', 'Silom_3', 'Mehasak'],
        'cluster_46_47': ['Sathorn_Thai_1', 'Charoen_Rat', 'Surasak']
    }
downstream_road = { 'Charoenkrung_1':'Charoenkrung_2',
                    'Sathorn_Thai_2':'Charoenkrung_2',
                    'Charoenkrung_2': 'Silom_1',
                    'Charoenkrung_3': 'Silom_1',
                    'Silom_1': 'Silom_2',
                    'Silom_2':'Surasak',
                    'Silom_3': 'Surasak',
                    'Mehasak': 'Surasak',
                    'Surasak':'Sathorn_Thai_2',
                    'Sathorn_Thai_1': 'Sathorn_Thai_2',
                    'Charoen_Rat': 'Sathorn_Thai_2'
}
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


#percentage = ['1%','5%','10%','15%','20%','25%','30%','35%','40%','45%','50%','55%','60%','65%','70%','75%','80%','85%','90%','95%','100%']
percentage = ['1%','5%','10%','15%','20%','25%','30%','35%','40%','45%','50%','100%']
resolution = ['1','5','10','15','20','25','30','35','40','45','50','55','60']


def checkLowMeanSpeed_forEachLink(outputFile):
    dirpath = os.getcwd()
    for edge, value in POIEdges.items():
        for time_resolution in resolution:
            for pcent in percentage:
                path =  dirpath + '/'+str(outputFile+1)+'/' + edge + '_'+time_resolution+'_'+pcent+'.csv'
                if (os.path.exists(path)):
                    link_df = pd.read_csv(path)
                    # consecutive_indices = []
                    where = 0  # need this to keep track of original indices
                    for key, group in groupby(link_df['Low Mean Speed']):
                        # length = sum(1 for item in group)
                        length = len([*group])
                        if key == 1 and length >= float(600/int(time_resolution)) :  # greater than 10 minutes
                            items = [where + i for i in range(length)]
                            # print(f'{key}:{items}')

                            min_index = min(items)
                            max_index = max(items)
                            # print(min_index,max_index)
                            # start_time = datetime.strptime(normal.loc[min_index, 'time'], '%H:%M:%S').time()
                            # end_time = datetime.strptime(normal.loc[max_index, 'time'], '%H:%M:%S').time()

                            link_df.loc[min_index:max_index]['Persistently Low Mean Speed Indicator'] = 1

                        where += length
                    link_df.to_csv(dirpath + '/'+str(outputFile+1)+'/' + edge + '_'+time_resolution+'_'+pcent+'.csv',index = False)
#==================================================================================================



#==================================================================================================
def checkLowMeanSpeed_forUpDownPair(outputFile):
    for time_resolution in resolution:
        for pcent in percentage:
            for key, value in cluster.items():
                # to get the current directory
                dirpath = os.getcwd()
                temp_df = pd.DataFrame()

                for upstream in value:
                    upstream_path = dirpath + '/'+str(outputFile+1)+'/' + upstream + '_' + time_resolution + '_' + pcent + '.csv'
                    upstream_df = pd.read_csv(upstream_path)
                    temp_df['Time'] = upstream_df['Time']
                    temp_df['Time(s)'] = upstream_df['Time(s)']

                    downstream = downstream_road.get(upstream)
                    downstream_path = dirpath + '/'+str(outputFile+1)+'/' + downstream + '_' + time_resolution + '_' + pcent + '.csv'
                    downstream_df = pd.read_csv(downstream_path)

                    col = upstream + '_' + downstream
                    temp_list = []
                    for index in range(len(upstream_df)):
                        if (upstream_df.loc[index]['Persistently Low Mean Speed Indicator'] == 1 and downstream_df.loc[index][
                            'Persistently Low Mean Speed Indicator'] == 1):
                            temp_list.append(1)
                            # print(time_resolution,upstream,downstream)
                        else:
                            temp_list.append(0)

                    temp_df[col] = temp_list
                temp_df.to_csv(
                    dirpath + '/'+str(outputFile+1)+'/cluster/' + time_resolution + '_' + pcent + '_' + key + '.csv',
                    index=False)
#==================================================================================================




#==================================================================================================
def detectClusterCongestion(outputFile):
    # to get the current directory
    dirpath = os.getcwd()
    for time_resolution in resolution:
        for pcent in percentage:
            for key, value in cluster.items():

                cluster_path = dirpath + '/'+str(outputFile+1)+'/cluster/' + time_resolution + '_' + pcent + '_' + key + '.csv'
                cluster_df = pd.read_csv(cluster_path)
                temp = []
                for idx, row in cluster_df.iterrows():
                    # print(key, value)
                    # print(row[1:])
                    if row[2:].any() == 1:
                        temp.append(1)
                    else:
                        temp.append(0)
                cluster_df['Cluster Congestion'] = temp

                cluster_df.to_csv(
                    dirpath + '/'+str(outputFile+1)+'/cluster/' + time_resolution + '_' + pcent + '_' + key + '.csv',
                    index=False)
#==================================================================================================




#==================================================================================================
def detectGridlock(outputFile):
    # to get the current directory
    dirpath = os.getcwd()
    for time_resolution in resolution:
        # print( list(cluster.keys())[0] )
        for pcent in percentage:
            cluster_path = dirpath + '/'+str(outputFile+1)+'/cluster/' + time_resolution + '_' + pcent + '_' + \
                           list(cluster.keys())[0] + '.csv'
            cluster_df = pd.read_csv(cluster_path)
            temp_1 = []
            temp_df = pd.DataFrame()
            temp_df['Time'] = cluster_df['Time']
            temp_df['Time(s)'] = cluster_df['Time(s)']

            temp_df['Gridlock'] = 0 * len(cluster_df)
            for idx, row in cluster_df.iterrows():

                temp_2 = []
                for key, value in cluster.items():
                    cluster_path = dirpath + '/'+str(outputFile+1)+'/cluster/' + time_resolution + '_' + pcent + '_' + key + '.csv'
                    cluster_df = pd.read_csv(cluster_path)
                    if (cluster_df.loc[idx]['Cluster Congestion'] == 1):
                        temp_2.append(1)
                    else:
                        temp_2.append(0)

                ############### Six Class Labels###########################
                if (sum(temp_2) == len(cluster)):
                    temp_1.append(5)   # level 5
                elif sum(temp_2) == len(cluster) * 0.8:
                    temp_1.append(4)  # level 4
                elif sum(temp_2) == len(cluster) * 0.6:
                    temp_1.append(3)  # level 3
                elif sum(temp_2) == len(cluster) * 0.4:
                    temp_1.append(2)  # level 2
                elif sum(temp_2) == len(cluster) * 0.2:
                    temp_1.append(1)  # level 1
                else:  #
                    temp_1.append(0)  # no gridlock

            temp_df['Gridlock'] = temp_1
            temp_df.to_csv(dirpath + '/'+str(outputFile+1)+'/cluster/' + time_resolution + '_' + pcent + '_AllCluster.csv',
                           index=False)
#==================================================================================================




#==================================================================================================
def plotClusterCongestionState(outputFile):
    dirpath = os.getcwd()
    for time_resolution in resolution:
        for pcent in percentage:
            fig, ax = plt.subplots(len(cluster) + 1, 1, figsize=(12, 10), sharex=True, sharey=True)
            ticks_font = matplotlib.font_manager.FontProperties(family='times new roman', style='normal', size=12,
                                                                weight='normal', stretch='normal')
            i = 0
            for key, value in cluster.items():
                cluster_path = dirpath + '/'+str(outputFile+1)+'/cluster/' + time_resolution + '_' + pcent + '_' + key + '.csv'
                cluster_df = pd.read_csv(cluster_path)
                cluster_df = cluster_df.set_index(pd.DatetimeIndex(cluster_df['Time']))

                ax[i].plot(cluster_df['Cluster Congestion'], label=key, color='b')
                leg = ax[i].legend(loc="upper left", prop={'family': 'times new roman', 'size': 14}, handlelength=0,
                                   handletextpad=0, fancybox=True)
                for item in leg.legendHandles:
                    item.set_visible(False)
                # ax[i].legend(loc="upper left")

                ax[i].xaxis_date()
                ax[i].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
                # ax[i].title.set_text(key)

                for label in ax[i].get_xticklabels():
                    label.set_fontproperties(ticks_font)
                for label in ax[i].get_yticklabels():
                    label.set_fontproperties(ticks_font)

                i += 1

            allcluster_path = dirpath + '/'+str(outputFile+1)+'/cluster/' + time_resolution + '_' + pcent + '_AllCluster.csv'
            allcluster_df = pd.read_csv(allcluster_path)
            allcluster_df = allcluster_df.set_index(pd.DatetimeIndex(allcluster_df['Time']))

            ax[i].plot(allcluster_df['Gridlock'], label='Gridlock Status', color='r')
            leg = ax[i].legend(loc="upper left", prop={'family': 'times new roman', 'size': 14}, handlelength=0,
                               handletextpad=0, fancybox=True)
            for item in leg.legendHandles:
                item.set_visible(False)
            # ax[i].legend(loc="upper left")
            ax[i].xaxis_date()
            ax[i].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
            # ax[i].title.set_text('AllCluster')
            for label in ax[i].get_xticklabels():
                label.set_fontproperties(ticks_font)
            for label in ax[i].get_yticklabels():
                label.set_fontproperties(ticks_font)

            # plt.yticks(np.arange(allcluster_df['Gridlock'].min(), allcluster_df['Gridlock'].max() + 1, 1.0))

            plt.yticks(np.arange(0, 6, 1.0))
            plt.xlabel('Time', fontsize=16, fontname='Times New Roman')

            plt.savefig(
                dirpath + '/'+str(outputFile+1)+'/cluster/images/' + time_resolution + '_' + pcent + '_EachCluster.png',
                width=1800, height=500)
            # plt.show()

            for ax in fig.get_axes():
                ax.label_outer()
            fig.tight_layout()
            plt.close()
# ==================================================================================================

def plotMeanSpeed(outputFile):
    dirpath = os.getcwd()

    for key, value in cluster.items():
        data = []
        fichier_html_graphs = open(dirpath + '/'+str(outputFile+1)+'/plotMeanSpeed/1_100%/' +  key + ".html", 'w')
        fichier_html_graphs.write("<html><head></head><body style=\"margin:0\">" + "\n")

        upstreamkey = ''
        colors = ['RGB(128, 128, 0)','RGB(0, 0, 255)','RGB(255, 0, 0)']
        index = 0
        for upstream in value:
            upstream_path = dirpath + '/'+str(outputFile+1)+'/' + upstream + '_1_100%.csv'
            upstream_df = pd.read_csv(upstream_path)
            upstream_df.loc[:,'Mean Speed (km/h)']*=3.6
            trace = go.Scatter(x=upstream_df['Time'], y=upstream_df['Mean Speed (km/h)'], mode='lines', name=upstream,
                                line=dict(color=(colors[index]), width=2)
                                )
            upstreamkey = upstream
            data.append(trace)
            index +=1

        downstream = downstream_road.get(upstreamkey)
        downstream_path = dirpath + '/'+str(outputFile+1)+'/' + downstream + '_1_100%.csv'
        downstream_df = pd.read_csv(downstream_path)
        downstream_df.loc[:, 'Mean Speed (km/h)'] *= 3.6
        trace = go.Scatter(x=downstream_df['Time'], y=downstream_df['Mean Speed (km/h)'], mode='lines', name=downstream,
                           line=dict(color=('RGB(0, 0, 0)'), width=2)
                           )

        data.append(trace)
        # Edit the layout
        layout = go.Layout(title='<b></b>',
                           titlefont=dict(
                               family='Courier New, monospace',
                               size=22,
                               color='#000000'
                           ),
                           legend=dict(traceorder='normal', font=dict(family='times', size=22, color='#000')),
                           xaxis=dict(title='Time', tickangle=0, titlefont=dict(family='Times New Roman',size=20, color='#000000'),
                                      tickfont=dict(family='Times New Roman', size=19, color='#000'), tickmode='linear',
                                      dtick=1800),
                           yaxis=dict(title='Mean Speed (km/h)',titlefont=dict(family='Times New Roman',size=20, color='#000000'), range=[0, 50], dtick=5,
                                      tickfont=dict(family='Times New Roman', size=19, color='#000000'),
                                      ),
                           paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)',

                           )
        fig = go.Figure(data=data, layout=layout)

        plotly.offline.plot(fig, filename=dirpath + '/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID/'+str(outputFile+1)+'/plotMeanSpeed/1_100%/' +  key + '.html', auto_open=False)

        # Save image
        pio.write_image(fig, dirpath + '/'+str(outputFile+1)+'/plotMeanSpeed/1_100%/images/' + key + '.png', width=1800,
                        height=700)
        fichier_html_graphs.write(
            "  <object data=\"" + key + '.html' + "\" width=\"1800\" height=\"400\" style=\"margin: 0px 0px\"></object>")



#main function
#========================================================================================
def main():
    dirpath = os.getcwd()
    for outputFile in range(0, 100):
        os.mkdir(dirpath + 'RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID/' + str(outputFile + 1) + '/cluster')
        os.mkdir(dirpath + 'RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID/' + str(outputFile + 1) + '/cluster/images')
        checkLowMeanSpeed_forEachLink(outputFile)
        checkLowMeanSpeed_forUpDownPair(outputFile)
        detectClusterCongestion(outputFile)
        detectGridlock(outputFile)
        plotMeanSpeed(outputFile)


if __name__=="__main__":
    main()
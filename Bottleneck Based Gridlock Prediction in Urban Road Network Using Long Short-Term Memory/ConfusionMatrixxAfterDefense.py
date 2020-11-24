import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np
percentage = ['1%','5%','10%','15%','20%','25%','30%','35%','40%','45%','50%']
setting = {'1': ['10','20','10'], # setting 1 (epoch:10, batch_size:20,neurons:10)
            '2': ['10','20','20'],
            '3': ['50','20','10'],
            '4': ['10','50','10'],
            '5': ['50','10','10'],
            '6': ['10','10','1']
            }
time_lagged_observation =['1','5','10','15','30','60']

def confusionMatrix():

    dirpath = 'c:/RetrieveOnly100%DATAFROMSUMO_RANDOMSEED(One time)-DATASET-WithoutReplicatedVID'
    for key, value in setting.items():
        for percent in percentage:
            for history in time_lagged_observation:
                fig = plt.figure()
                data = pd.read_csv(
                    dirpath + '/LSTMExperimentResults_AfterDefense/' + percent + '_' + history + 'min_' + value[
                        0] + 'epochs_' + value[1] + 'batch_size_' + value[2] + 'neurons.csv')
                temp = data['predicted'].tolist()
                temp_convert = [np.round(num) for num in temp]
                data['round_predicted'] = temp_convert
                df = pd.DataFrame(data, columns=['actual','round_predicted'])
                df = df.astype(int)
                confusion_matrix = pd.crosstab(df['actual'], df['round_predicted'], rownames=['Actual Gridlock Labels'], colnames=['Predicted Gridlock Labels'])
                ax = plt.subplot()
                # sn.set(font_scale=3.0)  # Adjust to fit
                sn.heatmap(confusion_matrix, annot=True,ax=ax, cmap="Blues", fmt="g")
                plt.xticks(fontsize=18, fontname='Times New Roman')
                plt.yticks(fontsize=18, fontname='Times New Roman')
                # plt.legend(prop={'family': 'Times New Roman'})
                plt.rcParams.update({'font.family': 'Times New Roman','font.size': '20'})
                plt.tight_layout()
                plt.savefig(
                    dirpath + '/LSTMExperimentResults_DR_FAR_AfterDefense/ConfusionMatrix/confusiontMatrixFor_epoch_' + value[0] +
                    '_batch_' + value[1] + '_neuron_' + value[2] + '_'+ percent+'_' + history + '_min.png', width=1800, height=500)
                fig.clf()
#main functin
#========================================================================================
def main():
    confusionMatrix()

if __name__=="__main__":
    main()
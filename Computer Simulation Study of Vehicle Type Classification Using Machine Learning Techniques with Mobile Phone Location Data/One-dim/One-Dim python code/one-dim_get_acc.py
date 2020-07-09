import pandas as pd
import numpy as np
import csv
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

# list of file name, included cdt and avg velo
# for each congestion level within the same traffic light signal inter-spacing and cell tower inter-spacing
file_velo = [
             'C_TLS1000/Cell_50/1VeloC50_TLS1000_G150-vph1400-2hr.csv',
             'C_TLS1000/Cell_50/2VeloC50_TLS1000_G150-vph2800-2hr.csv',
             'C_TLS1000/Cell_50/3VeloC50_TLS1000_G100-vph1400-2hr.csv',
             'C_TLS1000/Cell_50/4VeloC50_TLS1000_G50-vph1400-2hr.csv',
             'C_TLS1000/Cell_50/5VeloC50_TLS1000_G150-vph4200-2hr.csv',
             'C_TLS1000/Cell_50/6VeloC50_TLS1000_G100-vph2800-2hr.csv',
             ]

# list for collecting train and test accuracy
RF_train_acc = []
RF_test_acc = []
SVM_lin_train_acc = []
SVM_lin_test_acc = []
KNN_train_acc = []
KNN_test_acc = []

# list for collecting the accuracy for each algorithm
RF =[]
SVM = []
KNN = []

# list for collecting variance of accuracy
VAR_RF = []
VAR_KNN = []
VAR_SVM = []

# list for collecting confusion matrix
Confusion_RF =[]
Confusion_SVM = []
Confusion_KNN = []

# list of accuracy, compared between 2 classes
C_RF_MC_CAR =[]
C_SVM_MC_CAR = []
C_KNN_MC_CAR = []
C_KNN_MC_TRAIN = []
C_KNN_CAR_TRAIN = []
C_RF_MC_TRAIN = []
C_RF_CAR_TRAIN = []
C_SVM_MC_TRAIN = []
C_SVM_CAR_TRAIN = []

# sum of confusion matrix for each algorithm
sum_conf_RF = np.zeros(shape=(3,3), dtype=int)
sum_conf_KNN = np.zeros(shape=(3,3), dtype=int)
sum_conf_SVM = np.zeros(shape=(3,3), dtype=int)

# for each file in list
for a in range(len(file_velo)):
    # to collect the classification accuracy of each algorithm
    temp_rf = []
    temp_knn = []
    temp_svm = []

    # to collect the confusion matrix of each algorithm
    confusion_temp_svm = np.zeros(shape=(3,3), dtype=int)
    confusion_temp_rf = np.zeros(shape=(3,3), dtype=int)
    confusion_temp_knn = np.zeros(shape=(3,3), dtype=int)

    for j in range(10):
        # to reorganize the cell dwelled time data to dataframe
        # included vehicle ID as an index, vehicle class as an output label,
        # and cell dwelled time at each cell as an input features
        df = pd.read_csv(file_velo[a], index_col=7)
        df.drop(['C_y', 'C_x', 'Avg Velocity'], axis=1, inplace=True)
        df = df.groupby(['ID', 'Class', 'Cell_ID'])['CDT'].max().unstack()
        df.drop(['Cell_001'], axis=1, inplace=True)
        df = df.drop(df[df.isna().sum(axis=1) > 3].index, inplace=False)
        df = df.fillna(df.mean())
        df = df.reset_index()
        df.set_index('ID', inplace=True)

        # split the data to train and test data set
        X_train, X_test, y_train, y_test = train_test_split(df.drop('Class', axis=1), df['Class'], test_size=0.2)
        # to prevent y_test set without Skytrain
        while 'rail_urban' not in list(y_test):
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
            if 'rail_urban' in list(y_test):
                break

        # Random Forest
        clf_rf = RandomForestClassifier()
        clf_rf.fit(X_train2, y_train2)
        train_pred_rf = clf_rf.predict(X_train)
        test_pred_rf = clf_rf.predict(X_test)
        RF_test_acc.append((y_test == test_pred_rf).sum() / len(y_test))
        RF_train_acc.append((y_train == train_pred_rf).sum() / len(y_train))
        temp_rf.append((y_test == test_pred_rf).sum() / len(y_test))
        confusion_temp_rf += confusion_matrix(y_test, test_pred_rf)

        # K-Nearest Neighbor
        clf_knn = KNeighborsClassifier()
        clf_knn.fit(X_train, y_train)
        train_pred_knn = clf_knn.predict(X_train)
        test_pred_knn = clf_knn.predict(X_test)
        KNN_test_acc.append((y_test == test_pred_knn).sum() / len(y_test))
        KNN_train_acc.append((y_train == train_pred_knn).sum() / len(y_train))
        temp_knn.append((y_test == test_pred_knn).sum() / len(y_test))
        confusion_temp_knnt += confusion_matrix(y_test, test_pred_knn)

        # Support Vector Machine with Linear Kernel
        scaler = StandardScaler()
        scaler.fit(df.drop('Class', axis=1))
        X_train_Scaled = scaler.transform(X_train)
        X_test_Scaled = scaler.transform(X_test)
        clf_svm = SVC(kernel='linear')
        clf_svm.fit(X_train_Scaled, y_train)
        train_pred_svm = clf_svm.predict(X_train_Scaled)
        test_pred_svm = clf_svm.predict(X_test_Scaled)
        SVM_lin_test_acc.append((y_test == test_pred_svm).sum() / len(y_test))
        SVM_lin_train_acc.append((y_train == train_pred_svm).sum() / len(y_train))
        temp_svm.append((y_test == test_pred_svm).sum() / len(y_test))
        confusion_temp_svm += confusion_matrix(y_test, test_pred_svm)

    RF.append(np.mean(temp_rf))
    SVM_Scaled.append(np.mean(temp_svm))
    KNN.append(np.mean(temp_knn))

    VAR_KNN.append(np.var(temp_knn))
    VAR_RF.append(np.var(temp_rf))
    VAR_SVM.append(np.var(temp_svm))

    Confusion_RF.append(confusion_temp_rf)
    Confusion_SVM.append(confusion_temp_svm)
    Confusion_KNN.append(confusion_temp_knn)

    sum_conf_RF += confusion_temp_rf
    sum_conf_SVM += confusion_temp_svm
    sum_conf_KNN += confusion_temp_knn

for i in Confusion_SVM_CDT_Scaled:
    C_SVM_CDT_Scaled_MC_CAR.append((i[0][0]+i[1][1])/(i[0][0]+i[0][1]+i[1][0]+i[1][1]))
    C_SVM_CDT_Scaled_MC_TRAIN.append((i[0][0] + i[2][2]) / (i[0][0] + i[2][2] + i[0][2] + i[2][0]))
    C_SVM_CDT_Scaled_CAR_TRAIN.append((i[1][1] + i[2][2]) / (i[1][1] + i[2][2] + i[1][2] + i[2][1]))

for i in Confusion_RF_CDT:
    C_RF_CDT_MC_CAR.append((i[0][0]+i[1][1])/(i[0][0]+i[0][1]+i[1][0]+i[1][1]))
    C_RF_CDT_MC_TRAIN.append((i[0][0]+i[2][2])/(i[0][0]+i[2][2]+i[0][2]+i[2][0]))
    C_RF_CDT_CAR_TRAIN.append((i[1][1]+i[2][2])/(i[1][1]+i[2][2]+i[1][2]+i[2][1]))

for i in Confusion_KNN_CDT:
    C_KNN_CDT_MC_CAR.append((i[0][0]+i[1][1])/(i[0][0]+i[0][1]+i[1][0]+i[1][1]))
    C_KNN_CDT_MC_TRAIN.append((i[0][0] + i[2][2]) / (i[0][0] + i[2][2] + i[0][2] + i[2][0]))
    C_KNN_CDT_CAR_TRAIN.append((i[1][1] + i[2][2]) / (i[1][1] + i[2][2] + i[1][2] + i[2][1]))

with open('C_TLS1000/Cell_250/accuracy_10times-0.2.csv', mode='w', newline='') as csv_acc:
    writer_acc = csv.writer(csv_acc)
    writer_acc.writerow(['RF_CDT', 'KNN_CDT', 'SVM_CDT_Scaled',
                         'C_RF_CDT_MC_CAR', 'C_KNN_CDT_MC_CAR', 'C_SVM_CDT_Scaled_MC_CAR',
                         'C_RF_CDT_MC_TRAIN', 'C_KNN_CDT_MC_TRAIN', 'C_SVM_CDT_Scaled_MC_TRAIN',
                         'C_RF_CDT_CAR_TRAIN', 'C_KNN_CDT_CAR_TRAIN', 'C_SVM_CDT_Scaled_CAR_TRAIN',
                         'Var_RF_CDT', 'Var_KNN_CDT', 'Var_SVM_CDT_Scaled',
                         'Confusion_RF', 'Confusion_KNN', 'Confusion_SVM'])
    writer_acc.writerow(RF_CDT)
    writer_acc.writerow(KNN_CDT)
    writer_acc.writerow(SVM_CDT_Scaled)
    writer_acc.writerow(C_RF_CDT_MC_CAR)
    writer_acc.writerow(C_KNN_CDT_MC_CAR)
    writer_acc.writerow(C_SVM_CDT_Scaled_MC_CAR)
    writer_acc.writerow(C_RF_CDT_MC_TRAIN)
    writer_acc.writerow(C_KNN_CDT_MC_TRAIN)
    writer_acc.writerow(C_SVM_CDT_Scaled_MC_TRAIN)
    writer_acc.writerow(C_RF_CDT_CAR_TRAIN)
    writer_acc.writerow(C_KNN_CDT_CAR_TRAIN)
    writer_acc.writerow(C_SVM_CDT_Scaled_CAR_TRAIN)
    writer_acc.writerow(VAR_RF)
    writer_acc.writerow(VAR_KNN)
    writer_acc.writerow(VAR_SVM)
    writer_acc.writerow(Confusion_RF_CDT)
    writer_acc.writerow(Confusion_KNN_CDT)
    writer_acc.writerow(Confusion_SVM_CDT_Scaled)
# calculate the classification accuracy for each simulation in each case of C value

import pandas as pd
import numpy as np
import csv

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

# list of dataframe file name
file_cdt = ['df_cdt/cell500/cell500_case1_data_00',
'df_cdt/cell500/cell500_case1_data_01',
'df_cdt/cell500/cell500_case1_data_02',
'df_cdt/cell500/cell500_case1_data_03',
'df_cdt/cell500/cell500_case1_data_04',
'df_cdt/cell500/cell500_case1_data_05',
'df_cdt/cell500/cell500_case1_data_06',
'df_cdt/cell500/cell500_case1_data_07',
'df_cdt/cell500/cell500_case1_data_08',
'df_cdt/cell500/cell500_case1_data_10',
'df_cdt/cell500/cell500_case1_data_11',
'df_cdt/cell500/cell500_case1_data_12',
'df_cdt/cell500/cell500_case1_data_13',
'df_cdt/cell500/cell500_case1_data_14',
'df_cdt/cell500/cell500_case1_data_15',
'df_cdt/cell500/cell500_case1_data_16',
'df_cdt/cell500/cell500_case1_data_17',
'df_cdt/cell500/cell500_case1_data_18',
'df_cdt/cell500/cell500_case1_data_19',
'df_cdt/cell500/cell500_case1_data_20',
'df_cdt/cell500/cell500_case1_data_21',
'df_cdt/cell500/cell500_case1_data_22',
'df_cdt/cell500/cell500_case1_data_23',
'df_cdt/cell500/cell500_case1_data_24',
'df_cdt/cell500/cell500_case1_data_25',
'df_cdt/cell500/cell500_case1_data_26',
'df_cdt/cell500/cell500_case1_data_27',
'df_cdt/cell500/cell500_case1_data_28',
'df_cdt/cell500/cell500_case1_data_29',
'df_cdt/cell500/cell500_case1_data_30']

# list of train, test accuracy and confusion matrix for each hyperparameter setting
SVM_train_acc_C_01 = []
SVM_test_acc_C_01 = []
SVM_train_acc_C_05 = []
SVM_test_acc_C_05 = []
SVM_train_acc_C_1 = []
SVM_test_acc_C_1 = []
SVM_train_acc_C_10 = []
SVM_test_acc_C_10 = []
SVM_train_acc_C_50 = []
SVM_test_acc_C_50 = []
SVM_train_acc_C_100 = []
SVM_test_acc_C_100 = []
SVM_train_acc_C_5 = []
SVM_test_acc_C_5 = []

SVM_C_01 = []
SVM_C_05 = []
SVM_C_1 = []
SVM_C_5 = []
SVM_C_10 = []
SVM_C_50 = []
SVM_C_100 = []

Confusion_SVM_C_01 = []
Confusion_SVM_C_05 = []
Confusion_SVM_C_1 = []
Confusion_SVM_C_5 = []
Confusion_SVM_C_10 = []
Confusion_SVM_C_50 = []
Confusion_SVM_C_100 = []

conf_svm_C_01 = np.zeros(shape=(3,3), dtype=int)
conf_svm_C_05 = np.zeros(shape=(3,3), dtype=int)
conf_svm_C_1 = np.zeros(shape=(3,3), dtype=int)
conf_svm_C_5 = np.zeros(shape=(3,3), dtype=int)
conf_svm_C_10 = np.zeros(shape=(3,3), dtype=int)
conf_svm_C_50 = np.zeros(shape=(3,3), dtype=int)
conf_svm_C_100 = np.zeros(shape=(3,3), dtype=int)

# for each simulation
for a in range(len(file_cdt)):
    print('start file: {}'.format(a))
    temp_svm_C_01 = []
    temp_svm_C_05 = []
    temp_svm_C_1 = []
    temp_svm_C_5 = []
    temp_svm_C_10 = []
    temp_svm_C_50 = []
    temp_svm_C_100 = []

    confusion_temp_svm_C_01 = np.zeros(shape=(3, 3), dtype=int)
    confusion_temp_svm_C_05 = np.zeros(shape=(3, 3), dtype=int)
    confusion_temp_svm_C_1 = np.zeros(shape=(3, 3), dtype=int)
    confusion_temp_svm_C_5 = np.zeros(shape=(3, 3), dtype=int)
    confusion_temp_svm_C_10 = np.zeros(shape=(3, 3), dtype=int)
    confusion_temp_svm_C_50 = np.zeros(shape=(3, 3), dtype=int)
    confusion_temp_svm_C_100 = np.zeros(shape=(3, 3), dtype=int)

    df = pd.read_csv(file_cdt[a]+'.csv')
    X = df.drop(['ID', 'Class'], axis=1)
    y = df.Class

    # set the number of loop for each simulation
    # fit the model and calculate the classification accuracy
    for j in range(3):
        print('round: {}'.format(j))

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        scaler = StandardScaler()
        scaler.fit(X)
        X_train_scaled = scaler.transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        print('start C 0.1')

        svm_clf = SVC(kernel='linear', C=0.1)
        svm_clf.fit(X_train_scaled, y_train)
        train_pred_svm = svm_clf.predict(X_train_scaled)
        test_pred_svm = svm_clf.predict(X_test_scaled)
        SVM_test_acc_C_01.append((y_test==test_pred_svm).mean())
        SVM_train_acc_C_01.append((y_train==train_pred_svm).mean())
        temp_svm_C_01.append((y_test==test_pred_svm).mean())
        confusion_temp_svm_C_01 += confusion_matrix(y_test, test_pred_svm)

        print('start C 0.5')

        svm_clf = SVC(kernel='linear', C=0.5)
        svm_clf.fit(X_train_scaled, y_train)
        train_pred_svm = svm_clf.predict(X_train_scaled)
        test_pred_svm = svm_clf.predict(X_test_scaled)
        SVM_test_acc_C_05.append((y_test == test_pred_svm).mean())
        SVM_train_acc_C_05.append((y_train == train_pred_svm).mean())
        temp_svm_C_05.append((y_test == test_pred_svm).mean())
        confusion_temp_svm_C_05 += confusion_matrix(y_test, test_pred_svm)

        print('start C 1')

        svm_clf = SVC(kernel='linear', C=1)
        svm_clf.fit(X_train_scaled, y_train)
        train_pred_svm = svm_clf.predict(X_train_scaled)
        test_pred_svm = svm_clf.predict(X_test_scaled)
        SVM_test_acc_C_1.append((y_test == test_pred_svm).mean())
        SVM_train_acc_C_1.append((y_train == train_pred_svm).mean())
        temp_svm_C_1.append((y_test == test_pred_svm).mean())
        confusion_temp_svm_C_1 += confusion_matrix(y_test, test_pred_svm)

        print('start C 5')

        svm_clf = SVC(kernel='linear', C=5)
        svm_clf.fit(X_train_scaled, y_train)
        train_pred_svm = svm_clf.predict(X_train_scaled)
        test_pred_svm = svm_clf.predict(X_test_scaled)
        SVM_test_acc_C_5.append((y_test == test_pred_svm).mean())
        SVM_train_acc_C_5.append((y_train == train_pred_svm).mean())
        temp_svm_C_5.append((y_test == test_pred_svm).mean())
        confusion_temp_svm_C_5 += confusion_matrix(y_test, test_pred_svm)

        print('start C 10')

        svm_clf = SVC(kernel='linear', C=10)
        svm_clf.fit(X_train_scaled, y_train)
        train_pred_svm = svm_clf.predict(X_train_scaled)
        test_pred_svm = svm_clf.predict(X_test_scaled)
        SVM_test_acc_C_10.append((y_test == test_pred_svm).mean())
        SVM_train_acc_C_10.append((y_train == train_pred_svm).mean())
        temp_svm_C_10.append((y_test == test_pred_svm).mean())
        confusion_temp_svm_C_10 += confusion_matrix(y_test, test_pred_svm)

        print('start C 50')

        svm_clf = SVC(kernel='linear', C=50)
        svm_clf.fit(X_train_scaled, y_train)
        train_pred_svm = svm_clf.predict(X_train_scaled)
        test_pred_svm = svm_clf.predict(X_test_scaled)
        SVM_test_acc_C_50.append((y_test == test_pred_svm).mean())
        SVM_train_acc_C_50.append((y_train == train_pred_svm).mean())
        temp_svm_C_50.append((y_test == test_pred_svm).mean())
        confusion_temp_svm_C_50 += confusion_matrix(y_test, test_pred_svm)
        #
        print('start C 100')

        svm_clf = SVC(kernel='linear', C=100)
        svm_clf.fit(X_train_scaled, y_train)
        train_pred_svm = svm_clf.predict(X_train_scaled)
        test_pred_svm = svm_clf.predict(X_test_scaled)
        SVM_test_acc_C_100.append((y_test == test_pred_svm).mean())
        SVM_train_acc_C_100.append((y_train == train_pred_svm).mean())
        temp_svm_C_100.append((y_test == test_pred_svm).mean())
        confusion_temp_svm_C_100 += confusion_matrix(y_test, test_pred_svm)

        print('end C 100')


    SVM_C_01.append(np.mean(temp_svm_C_01))
    SVM_C_05.append(np.mean(temp_svm_C_05))
    SVM_C_1.append(np.mean(temp_svm_C_1))
    SVM_C_5.append(np.mean(temp_svm_C_5))
    SVM_C_10.append(np.mean(temp_svm_C_10))
    SVM_C_50.append(np.mean(temp_svm_C_50))
    SVM_C_100.append(np.mean(temp_svm_C_100))

    Confusion_SVM_C_01.append(confusion_temp_svm_C_01)
    Confusion_SVM_C_05.append(confusion_temp_svm_C_05)
    Confusion_SVM_C_1.append(confusion_temp_svm_C_1)
    Confusion_SVM_C_5.append(confusion_temp_svm_C_5)
    Confusion_SVM_C_10.append(confusion_temp_svm_C_10)
    Confusion_SVM_C_50.append(confusion_temp_svm_C_50)
    Confusion_SVM_C_100.append(confusion_temp_svm_C_100)

    conf_svm_C_01 += confusion_temp_svm_C_01
    conf_svm_C_05 += confusion_temp_svm_C_05
    conf_svm_C_1 += confusion_temp_svm_C_1
    conf_svm_C_5 += confusion_temp_svm_C_5
    conf_svm_C_10 += confusion_temp_svm_C_10
    conf_svm_C_50 += confusion_temp_svm_C_50
    conf_svm_C_100 += confusion_temp_svm_C_100

    print('end file: {}'.format(a))


with open('df_cdt/cell500/accuracy_cell500_3times_all_C.csv', mode='w', newline='') as csv_acc:
    writer_acc = csv.writer(csv_acc)
    writer_acc.writerow(SVM_C_01)
    writer_acc.writerow(SVM_C_05)
    writer_acc.writerow(SVM_C_1)
    writer_acc.writerow(SVM_C_5)
    writer_acc.writerow(SVM_C_10)
    writer_acc.writerow(SVM_C_50)
    writer_acc.writerow(SVM_C_100)
    writer_acc.writerow(Confusion_SVM_C_01)
    writer_acc.writerow(Confusion_SVM_C_05)
    writer_acc.writerow(Confusion_SVM_C_1)
    writer_acc.writerow(Confusion_SVM_C_5)
    writer_acc.writerow(Confusion_SVM_C_10)
    writer_acc.writerow(Confusion_SVM_C_50)
    writer_acc.writerow(Confusion_SVM_C_100)
    writer_acc.writerow(conf_svm_C_01)
    writer_acc.writerow(conf_svm_C_05)
    writer_acc.writerow(conf_svm_C_1)
    writer_acc.writerow(conf_svm_C_5)
    writer_acc.writerow(conf_svm_C_10)
    writer_acc.writerow(conf_svm_C_50)
    writer_acc.writerow(conf_svm_C_100)

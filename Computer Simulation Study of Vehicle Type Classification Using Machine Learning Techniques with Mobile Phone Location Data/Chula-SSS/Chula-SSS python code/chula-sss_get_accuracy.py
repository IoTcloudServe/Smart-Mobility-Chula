import pandas as pd
import numpy as np
import csv

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

# For cell tower inter-spacing 100 meters
# list of dataframe file name
file_cdt = ['df_cdt/cell100/cell100_case1_data_00',
		'df_cdt/cell100/cell100_case1_data_01',
		'df_cdt/cell100/cell100_case1_data_02',
		'df_cdt/cell100/cell100_case1_data_03',
		'df_cdt/cell100/cell100_case1_data_04',
		'df_cdt/cell100/cell100_case1_data_05',
		'df_cdt/cell100/cell100_case1_data_06',
		'df_cdt/cell100/cell100_case1_data_07',
		'df_cdt/cell100/cell100_case1_data_08',
		'df_cdt/cell100/cell100_case1_data_10',
		'df_cdt/cell100/cell100_case1_data_11',
		'df_cdt/cell100/cell100_case1_data_12',
		'df_cdt/cell100/cell100_case1_data_13',
		'df_cdt/cell100/cell100_case1_data_14',
		'df_cdt/cell100/cell100_case1_data_15',
		'df_cdt/cell100/cell100_case1_data_16',
		'df_cdt/cell100/cell100_case1_data_17',
		'df_cdt/cell100/cell100_case1_data_18',
		'df_cdt/cell100/cell100_case1_data_19',
		'df_cdt/cell100/cell100_case1_data_20',
		'df_cdt/cell100/cell100_case1_data_21',
		'df_cdt/cell100/cell100_case1_data_22',
		'df_cdt/cell100/cell100_case1_data_23',
		'df_cdt/cell100/cell100_case1_data_24',
		'df_cdt/cell100/cell100_case1_data_25',
		'df_cdt/cell100/cell100_case1_data_26',
		'df_cdt/cell100/cell100_case1_data_27',
		'df_cdt/cell100/cell100_case1_data_28',
		'df_cdt/cell100/cell100_case1_data_29',
		'df_cdt/cell100/cell100_case1_data_30']

# list of train and test accuracy for each algorithm
RF_train_acc = []
RF_test_acc = []
KNN_train_acc = []
KNN_test_acc = []
SVM_train_acc = []
SVM_test_acc = []

# list of test accuracy for each algorithm
RF = []
KNN = []
SVM = []

# list of confusion matrix for each algorithm for all prediction times
Confusion_RF = []
Confusion_KNN = []
Confusion_SVM = []

# list of confusion matrix for each simulation for each algorithm
conf_rf = np.zeros(shape=(3,3), dtype=int)
conf_knn = np.zeros(shape=(3,3), dtype=int)
conf_svm = np.zeros(shape=(3,3), dtype=int)

# for each file in file list
for a in range(len(file_cdt)):
    # list to collect the test accuracy for each simulation
    temp_rf = []
    temp_knn = []
    temp_svm = []
    # list to collect confusion matrix for each simulation
    confusion_temp_rf = np.zeros(shape=(3,3), dtype=int)
    confusion_temp_svm = np.zeros(shape=(3,3), dtype=int)
    confusion_temp_knn = np.zeros(shape=(3,3), dtype=int)

    # read dataframe from file and determine the input features and output label
    df = pd.read_csv(file_cdt[a]+'.csv')
    X = df.drop(['ID', 'Class'], axis=1)
    y = df.Class

    for j in range(10):
        # Split train-test dataset with test size 0.2
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        # hyperparameters for each algorithm are determined by grid search

        # Random Forest Algorithm
        # for cell tower inter-spacing 100 m
        rf_clf = RandomForestClassifier(n_estimators=100, max_features='sqrt', n_jobs=-1)

        # # for cell tower inter-spacing 250 m
        # rf_clf = RandomForestClassifier(n_estimators=100, max_features=0.1, n_jobs=-1)
        #
        # # for cell tower inter-spacing 500 m
        # rf_clf = RandomForestClassifier(n_estimators=90, max_features='sqrt', n_jobs=-1)

        # Fit the model and predict the output
        rf_clf.fit(X_train, y_train)
        train_pred_rf = rf_clf.predict(X_train)
        test_pred_rf = rf_clf.predict(X_test)
        RF_test_acc.append((y_test == test_pred_rf).mean())
        RF_train_acc.append((y_train == train_pred_rf).mean())
        temp_rf.append((y_test == test_pred_rf).mean())
        confusion_temp_rf += confusion_matrix(y_test, test_pred_rf)

        # K-Nearest Neighbor Algorithm
        # for cell tower inter-spacing 100 m
        knn_clf = KNeighborsClassifier(n_neighbors=7, n_jobs=-1)

        # # for cell tower inter-spacing 250 and 500 m
        # knn_clf = KNeighborsClassifier(n_neighbors=17, n_jobs=-1)

        # Fit the model and predict the output
        knn_clf.fit(X_train, y_train)
        train_pred_knn = knn_clf.predict(X_train)
        test_pred_knn = knn_clf.predict(X_test)
        KNN_test_acc.append((y_test==test_pred_knn).mean())
        KNN_train_acc.append((y_train==train_pred_knn).mean())
        temp_knn.append((y_test==test_pred_knn).mean())
        confusion_temp_knn += confusion_matrix(y_test, test_pred_knn)

        # Scale the value before using SVM
        scaler = StandardScaler()
        scaler.fit(X)
        X_train_scaled = scaler.transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Fit the model and predict the output
        svm_clf = SVC(kernel='linear', C=1)
        svm_clf.fit(X_train_scaled, y_train)
        train_pred_svm = svm_clf.predict(X_train_scaled)
        test_pred_svm = svm_clf.predict(X_test_scaled)
        SVM_test_acc.append((y_test==test_pred_svm).mean())
        SVM_train_acc.append((y_train==train_pred_svm).mean())
        temp_svm.append((y_test==test_pred_svm).mean())
        confusion_temp_svm += confusion_matrix(y_test, test_pred_svm)


    # average the result from n loops (n=10)

    RF.append(np.mean(temp_rf))
    SVM.append(np.mean(temp_svm))
    KNN.append(np.mean(temp_knn))

    Confusion_RF.append(confusion_temp_rf)
    Confusion_SVM.append(confusion_temp_svm)
    Confusion_KNN.append(confusion_temp_knn)

    conf_rf += confusion_temp_rf
    conf_knn += confusion_temp_knn
    conf_svm += confusion_temp_svm

# save the result in file
with open('df_cdt/cell100/accuracy_cell100_10times.csv', mode='w', newline='') as csv_acc:
    writer_acc = csv.writer(csv_acc)
    writer_acc.writerow(['RF_acc', 'KNN_acc', 'SVM_acc',
                         'Confusion_RF', 'Confusion_KNN', 'Confusion_SVM',
                         'Confusion_RF_sum', 'Confusion_KNN_sum', 'Confusion_SVM_sum'])
    writer_acc.writerow(RF)
    writer_acc.writerow(KNN)
    writer_acc.writerow(SVM)
    writer_acc.writerow(Confusion_RF)
    writer_acc.writerow(Confusion_KNN)
    writer_acc.writerow(Confusion_SVM)
    writer_acc.writerow(conf_rf)
    writer_acc.writerow(conf_knn)
    writer_acc.writerow(conf_svm)


import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler


np.random.seed(42)

# concatenated dataframe file for all simulation
# set the file name and path
# reorganize dataframe and split data
df = pd.read_csv('df_cdt/cell250/cell250_case1_all_data.csv')
X = df.drop(['Class', 'ID'], axis=1)
y = df.Class
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# set the hyperparameter for searching for each algorithm
clf_rf = RandomForestClassifier(n_jobs=-1)
param_grid_rf = {'n_estimators': np.arange(40,110,10),
			  'max_features': [0.1, 0.2, 0.3, 0.4, 'sqrt', 'log2']}

gs_rf = GridSearchCV(clf_rf, param_grid_rf, verbose=2, cv=5, n_jobs=-1)
gs_rf.fit(X_train, y_train)

result_rf = pd.DataFrame(gs_rf.cv_results_)
result_rf.to_csv('df_cdt/cell250/cell250_gridsearch_rf.csv', index=False)


clf_knn = KNeighborsClassifier(n_jobs=-1)
param_grid_knn = {'n_neighbors': np.arange(3,17,2)}

gs_knn = GridSearchCV(clf_knn, param_grid_knn, verbose=3, cv=5, n_jobs=-1)
gs_knn.fit(X_train, y_train)

result_knn = pd.DataFrame(gs_knn.cv_results_)
result_knn.to_csv('df_cdt/cell250/cell250_gridsearch_knn_extended1.csv', index=False)

# scaling data before using svm
scaler = StandardScaler()
scaler.fit(X)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# gridsearch in svm should be avoided
clf_svm = SVC()
param_grid_svm = {'kernel': ['linear'],
				  'C': [1, 5, 10, 50, 100]}

gs_svm = GridSearchCV(clf_svm, param_grid_svm, verbose=3, cv=5, n_jobs=-1)
gs_svm.fit(X_train_scaled, y_train)

result_svm = pd.DataFrame(gs_svm.cv_results_)
result_svm.to_csv('df_cdt/cell250/cell250_gridsearch_svm_21.csv', index=False)

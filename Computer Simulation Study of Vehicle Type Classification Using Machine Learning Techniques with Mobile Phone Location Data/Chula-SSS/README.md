# Chula-SSS Vehicle Type Classification

1. Run chula-sss_get_raw.py or download on https://drive.google.com/drive/folders/1TFTM5Pc_OESkaVsAE2klWzyicE6xhuYl?usp=sharing to get raw data file as csv file including vehicle ID (ID), vehicle type (Class), time in second (Time), x-coordinate in meter (PositionX), and y-coordinate in meter (PositionY)

2. Run chula-sss_get_cell_position.py to get the location of cell tower, changing cell_dist variable for varying the cell tower inter-spacing

3. Run chula-sss_get_df.py to convert raw data to cell-dwelled time within the dataframe (as in Figure 4) and save to csv file, preparing for modeling

4. Run chula-sss_gridsearch.py to find the best hyperparameters (as in Table 4) for random forest and k-nearest neighbor algorithms

5. Run chula-sss_get_accuracy.py to get the classification accuracy of random forest and k-nearest neighbor algorithms (as in Figure 7) using the best hyperparameters from the previous step

6. Run chula-sss_svm_acc.py to get the best hyperparameter (as in Table 4) and classification accuracy of support vector machine algorithm (as in Figure 7)

One-Dim Vehicle Type Classification

1. Run one-dim_get_raw.py to get the raw data, 
	including vehicle ID (ID), vehicle type (Class), time in second (Time), 
	x-coordinate in meter (PositionX), and y-coordinate in meter (PositionY)
2. Run one-dim_get_cdt.py to convert the data to cell-dwelled time data 
	including vehicle ID (ID), cell tower in x-coordinate (C_x), 
	cell tower in y-coordinate (C_y), average velocity (Avg Velocity), 
	time stamp (Time Stamp), cell-dwelled time (CDT), vehicle type (Class), 
	and cell tower ID (Cell_ID)
3. Run one-dim_get_accuracy.py to convert the cell-dwelled time data 
	to dataframe and using random forest, k-nearest neighbor, 
	and support vector machines algorithms to find the classification accuracy (as in Figure 5)

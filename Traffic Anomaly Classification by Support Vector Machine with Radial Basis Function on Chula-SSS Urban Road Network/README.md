Installation:

	python 3.5 
	PyCharm 5 


Main Files 
============================================================================================
1) sathon_wide_tls_20160418_edited.add(cover_wholeLane)_withLaneClose_20mins.xml 	- to create incidents in SUMO 

2) sathorn_morning(clusterDetector).py 												- to retrieve data 

3) checkAnomalyOfflineMode_Specific_withFlow.py										- to check anomaly and write file
	
	- writeFileWithAccident()
	- checkAnomaly_WhenWriteFile()
	
4) AnomalyDetection.ipynb															- for anomaly detection using support vector machine 	


Dataset
============================================================================================
IncidentDetection/ 

	1) dataset/NormalCase/
		- seed50_Correct_2s		- for data collection interval with 2 s

	2) dataset/AccidentCase/LaneClosure/L10130/seed50_20min/
		-2s interval
			- 1 close		- for one-lane closure
			- 1,2 close 		- for two-lane closure
			- 1,2,3 close		- for three-lane closure

Remark
============================================================================================
Here, sumo configurations are same as with the original Chula-SSS. 


Paper
============================================================================================
Ei Ei Mon, Hideya Ochiai, Chaiyachet Saivichit, Chaodit Aswakul, "Traffic Anomaly Classification by Support Vector Machine with Radial Basis Function on Chula-SSS Urban Road Network," 
Proceedings of 2019 the 9th International Workshop on Computer Science and Engineering WCSE_2019_SPRING, pp. 73-80, Yangon, Myanmar, February 27-March 1, 2019.

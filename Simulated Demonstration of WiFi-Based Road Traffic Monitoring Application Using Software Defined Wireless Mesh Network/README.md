# Simulated Demonstration of WiFi-Based Road Traffic Monitoring Application Using Software Defined Wireless Mesh Network

<p align="center">
<strong> Software-defined wireless mesh network </strong> 
<p align="center">
<p align="center">
  <img width="460" height="300" src="https://github.com/IoTcloudServe/Smart-Mobility-Chula/blob/master/Simulated%20Demonstration%20of%20WiFi-Based%20Road%20Traffic%20Monitoring%20Application%20Using%20Software%20Defined%20Wireless%20Mesh%20Network/outdoor_ex.PNG">
</p>

  Software-defined wireless mesh network (SDWMN) is developed and installed on Phayathai road in front of Chulalongkorn University for sending traffic image to two traffic police boxes. The system consists of 6 Raspberry Pi nodes (PI1 – PI6) equipped with a camera that is installed on the cross over bridge connected with wireless links and two gateways that are installed inside the traffic police boxes to present the police traffic photography. 

<p align="center">
## <strong> Wifi packet measurement  </strong> 
<p align="center">
 
<p align="center">
  <img width="460" height="300" src="https://github.com/IoTcloudServe/Smart-Mobility-Chula/blob/master/Simulated%20Demonstration%20of%20WiFi-Based%20Road%20Traffic%20Monitoring%20Application%20Using%20Software%20Defined%20Wireless%20Mesh%20Network/sniff_ssid.PNG">
</p>
  This experiment uses a raspberry pi 4 model B as a node for measuring WIFI packets. The experiment is performed in the actual site where SDWMN is installed on Phayathai Road. During installation, the SDWMN node connects to the internet in order to synchronize the time in every node with NTP (network time protocol) program. Actual data collect from WIFI packet wireless communication measurement by using RSSI [9] module python program to develop the software. With this program, the WIFI in sensing range will be searched and perceive the received signal power. The software will be set in the SDWMN equipment to record SSID, received signal power and detected timestamp. The program scans and records the WIFI packet every 10 seconds.

<p align="center">
<strong> Simulation of Wifi packet measurement by SUMO  </strong> 
<p align="center">
 
<p align="center">
  <img width="460" height="300" src="https://github.com/IoTcloudServe/Smart-Mobility-Chula/blob/master/Simulated%20Demonstration%20of%20WiFi-Based%20Road%20Traffic%20Monitoring%20Application%20Using%20Software%20Defined%20Wireless%20Mesh%20Network/sdwmn_sumo.PNG">
</p>

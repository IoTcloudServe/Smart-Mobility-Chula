![Heading Collaboration](https://github.com/IoTcloudServe/the-3rd-collaboration-community-meeting/blob/master/Agenda/Heading.png)

<h1>
<p align="center">
<strong> Simulated Demonstration of WiFi-Based Road Traffic Monitoring Application Using Software Defined Wireless Mesh Network </strong>
<p align="center">
</h1> 

<h3>
<p align="center">
<strong> Software-defined wireless mesh network </strong>
<p align="center">
</h3> 
 
<p align="center">
  <img width="460" height="300" src="https://github.com/IoTcloudServe/Smart-Mobility-Chula/blob/master/Simulated%20Demonstration%20of%20WiFi-Based%20Road%20Traffic%20Monitoring%20Application%20Using%20Software%20Defined%20Wireless%20Mesh%20Network/outdoor_ex.PNG">
</p>

&nbsp; Software-defined wireless mesh network (SDWMN) is developed and installed on Phayathai road in front of Chulalongkorn University for sending traffic image to two traffic police boxes. The system consists of 6 Raspberry Pi nodes (PI1 – PI6) equipped with a camera that is installed on the cross over bridge connected with wireless links and two gateways that are installed inside the traffic police boxes to present the police traffic photography. 

<h3>
<p align="center">
<strong> Wifi packet measurement  </strong>
</p>
</h3>
 
<p align="center">
  <img width="460" height="300" src="https://github.com/IoTcloudServe/Smart-Mobility-Chula/blob/master/Simulated%20Demonstration%20of%20WiFi-Based%20Road%20Traffic%20Monitoring%20Application%20Using%20Software%20Defined%20Wireless%20Mesh%20Network/sniff_ssid.PNG">
</p>

&nbsp; This experiment uses a raspberry pi 4 model B as a node for measuring WIFI packets. The experiment is performed in the actual site where SDWMN is installed on Phayathai Road. During installation, the SDWMN node connects to the internet in order to synchronize the time in every node with NTP (network time protocol) program. Actual data collect from WIFI packet wireless communication measurement by using RSSI module python program to develop the software. With this program, the WIFI in sensing range will be searched and perceive the received signal power. The software will be set in the SDWMN equipment to record SSID, received signal power and detected timestamp. The program scans and records the WIFI packet every 10 seconds.

<h3>
<p align="center">
<strong> Simulation of Wifi packet measurement by SUMO  </strong>
</p>
</h3>

<p align="center">
  <img width="460" height="300" src="https://github.com/IoTcloudServe/Smart-Mobility-Chula/blob/master/Simulated%20Demonstration%20of%20WiFi-Based%20Road%20Traffic%20Monitoring%20Application%20Using%20Software%20Defined%20Wireless%20Mesh%20Network/sdwmn_sumo.PNG">
</p>

&nbsp; In this research, the SUMO program is used to create a traffic model. This program can determine the position of the vehicle on the simulated road at any time. Then, using Python to create a wifi package measurement by using the Free space propagation model.

<details>
    <summary>Click Here for SUMO</summary>
  <p align="center">
  <img width="400" height="250" src="https://github.com/IoTcloudServe/Smart-Mobility-Chula/blob/master/Simulated%20Demonstration%20of%20WiFi-Based%20Road%20Traffic%20Monitoring%20Application%20Using%20Software%20Defined%20Wireless%20Mesh%20Network/SUMOgif.gif">
</p>
  
&nbsp; SUMO is a free and open source traffic simulation suite. It is available since 2001 and allows modelling of intermodal traffic systems including road vehicles, public transport and pedestrians. Included with SUMO is a wealth of supporting tools which automate core tasks for the creation, the execution and evaluation of traffic simulations, such as network import, route calculations, visualization and emission calculation. SUMO can be enhanced with custom models and provides various APIs to remotely control the simulation.

<h6><a href="https://www.eclipse.org/sumo/">>>Click Here for visit SUMO website<<</a></h6>
<h6><a href="https://github.com/IoTcloudServe/Smart-Mobility-Chula/tree/master/Computer%20Simulation%20Study%20of%20Vehicle%20Type%20Classification%20Using%20Machine%20Learning%20Techniques%20with%20Mobile%20Phone%20Location%20Data/One-dim">>>Click Here for One dimention road simulation<<</a></h6>

</details>



<details>
    <summary>Click Here for Free space propagation</summary>
    <p align="center">
  <img width="500" height="300" src="https://github.com/IoTcloudServe/Smart-Mobility-Chula/blob/master/Simulated%20Demonstration%20of%20WiFi-Based%20Road%20Traffic%20Monitoring%20Application%20Using%20Software%20Defined%20Wireless%20Mesh%20Network/friis.PNG">
</p>
  
&nbsp; The free space propagation model assumes a transmit antenna and a receive antenna to be located in an otherwise empty environment. Neither absorbing obstacles nor reflecting surfaces are considered. In particular, the influence of the earth surface is assumed to be entirely absent.
</details>

<a href="https://202.28.193.103/login"><h1 align="center">
<img width="10%" alt="registration" src ="https://github.com/IoTcloudServe/Smart-Mobility-Chula/blob/master/Simulated%20Demonstration%20of%20WiFi-Based%20Road%20Traffic%20Monitoring%20Application%20Using%20Software%20Defined%20Wireless%20Mesh%20Network/icon-demo.png" /></h1>
</a>

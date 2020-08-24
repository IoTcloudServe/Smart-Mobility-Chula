from __future__ import absolute_import
from __future__ import print_function

import os
import random
import sys
import optparse
import csv
import math
import numpy as np

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary
import traci

file_raw = 'C_TLS500/2Raw1D_TLS1500_G100-vph2800-2hr.csv'
file_tlp = 'C_TLS500/6Teleport_TLS1500_G100-vph2800-2hr.csv'

list = []
tlp = []

def get_tlp():
    tlpID = traci.simulation.getStartingTeleportIDList()
    list = []
    if tlpID != tuple():
        for i in tlpID:
            list.append(i)
    return list


def run():
    # waiting until 6:30
    while traci.simulation.getCurrentTime() <= 23400000:
        traci.simulationStep()
    # collect data since 6:30 to 8:30
    while traci.simulation.getCurrentTime() <= 30600000:
        traci.simulationStep()
        # get simulation time
        time = traci.simulation.getTime()
        # get the teleported vehicle
        tlp += get_tlp()
        tlp = list(set(tlp))
        # get the vehicle id, type, time, coordinate position and keep them in list
        for i in traci.vehicle.getIDList():
            # get the position of vehicle
            # get (x, y) coordinate
            pos = traci.vehicle.getPosition(i)
            # append list of the data into list
            # list includes vehicle ID, vehicle type, time, x coordinate, and y coordinate
            list.append([i, traci.vehicle.getVehicleClass(i), time, pos[0], pos[1]])

    # save to raw data file
    with open(file_raw, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['ID', 'Class', 'Time', 'PositionX', 'PositionY'])
        writer.writerows(list)

    # save teleported vehicle data
    with open(file_tlp, mode='w') as tlp_file:
        writer2 = csv.writer(tlp_file)
        writer2.writerow(tlpset)

    traci.close()
    sys.stdout.flush()

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')


    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "1Dim/OneDim.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()

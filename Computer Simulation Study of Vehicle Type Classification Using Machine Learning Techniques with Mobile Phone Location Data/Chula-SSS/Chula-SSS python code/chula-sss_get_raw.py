# collect coordinate position, time, vehicle type of all vehicles inside the considered area
# using coil loop to detect vehicle inside the considered area

from __future__ import absolute_import
from __future__ import print_function

import os
import random
import sys
import optparse
import csv
import math
import numpy as np

# raw data file name
file_raw = 'raw_data_20.csv'

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa

# Check the vehicle ID, passed the induction loop
# INPUT: induction loop coil ID
# OUTPUT: list of vehicle ID, passed the coil in current simulation step
def check_coil_loop(ID):
    vehID = traci.inductionloop.getLastStepVehicleIDs(ID)
    list = []
    if vehID != tuple():
        for i in vehID:
            list.append(i)
    return list

# To get the teleported vehicle ID
# OUTPUT: list of vehicle ID, teleporting in current simulation step
def get_tlp():
    tlpID = traci.simulation.getStartingTeleportIDList()
    list = []
    if tlpID != tuple():
        for i in tlpID:
            list.append(i)
    return list


def run():
    list_in = []
    tlp = []
    raw_list = []
    # When time < 32400
    while traci.simulation.getTime() <= 32400:
        traci.simulationStep()

        # list of detector, detecting in-out vehicle
        # as in the .add.xml file
        # Check the vehicle ID, passed the coil loop into the considered area
        for j in range(3):
            list_in += check_coil_loop('in_%02d' %j)
        for j in range(7, 26):
            list_in += check_coil_loop('in_%02d' %j)
        for j in range(30, 47):
            list_in += check_coil_loop('in_%02d' %j)
        list_in = list(set(list_in))

        # Check the vehicle ID, passed the coil loop out of the considered area,
        list_out = []
        for j in range(64):
            list_out += check_coil_loop('out_%02d' %j)
        list_out = list(set(list_out))
        # get the teleported vehicle ID
        tlp += get_tlp()
        tlp = list(set(tlp))

        # Check the out of the considered area vehicle ID
        # and the teleported vehicle
        # then, remove that vehicle ID from the ID list within the considered area
        for j in list_out:
            if j in list_in:
                list_in.remove(j)
        for j in list_in:
            if j in tlp:
                list_in.remove(j)
        # get the simulation time
        time = traci.simulation.getTime()
        for j in list_in:
            # collect the vehicle ID, vehicle Type, time, X coordinate, and Y coordinate into the list
            pos = traci.vehicle.getPosition(j)
            raw_list.append([j, traci.vehicle.getVehicleClass(j), time, pos[0], pos[1]])

    # write the data list into csv file
    with open(file_raw, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['ID', 'Class', 'Time', 'PositionX', 'PositionY'])
        writer.writerows(raw_list)

    tlp = set(tlp)
    # save the teleported vehicle ID into csv file
    with open('tlp_data.csv', mode='w', newline='') as csv_tlp:
        writer_tlp = csv.writer(csv_tlp)
        writer_tlp.writerow(tlp)

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
        sumoBinary = checkBinary('sumo')

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "Chula_SSS_BTS_MC/bts_added.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()


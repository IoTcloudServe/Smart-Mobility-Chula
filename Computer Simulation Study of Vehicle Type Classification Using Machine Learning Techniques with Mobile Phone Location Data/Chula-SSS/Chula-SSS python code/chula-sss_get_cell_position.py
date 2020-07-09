# Collect cell tower position, using bts
# Output: cell tower position along the railway

from __future__ import absolute_import
from __future__ import print_function

import os
import random
import sys
import optparse
import csv
import math
import numpy as np

# Determine the file name of the cell position raw file and
# cell position file with the determined cell tower inter-spacing
file_cell_pos_raw = 'cell_pos_raw.csv'
file_cell_pos = 'cell_100_pos_ver2.csv'

def get_dist(x1, x2, y1, y2):
    dist = np.sqrt(((x1-x2)**2)+((y1-y2)**2))
    return dist

def get_x(x2, y1 , y2, cell_dist):
    x = np.sqrt(cell_dist**2 - (y1-y2)**2) + x2
    return x

# For SUMO simulation
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa

def run():
    list_pos = []
    # when simulation time less than 23000
    while traci.simulation.getTime() <= 23000:
        traci.simulationStep()
        # vehicle can be changed to collect the cell tower position in the other path
        if 'flow_BTSSl_1.0' in traci.vehicle.getIDList():
            list_pos.append(traci.vehicle.getPosition('flow_BTSSl_1.0'))
    # collect the position data and save to cell position raw file
    with open(file_cell_pos_raw, mode='w', newline='') as csv_cell:
        writer_cell = csv.writer(csv_cell)
        writer_cell.writerows(list_pos)

    # initiate the parameter value
    cell_dist = 100
    cell_pos = []
    # set the scope of map
    x_old = 4700.602929086564
    y_old = 5281.0876122968075
    cell_pos.append([x_old, y_old, 'A'])

    # get the position data
    with open(file_cell_pos_raw) as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        next(read_csv, None)
        for row in read_csv:
            # separate the map into 4 part
            # using the condition to calculate the cell tower position
            # with the constant value of inter-spacing
            x = float(row[0])
            y = float(row[1])
            if x >= 6050 and y < 5470:
                # 0.92 from setting the speed of vehicle to 10
                # and the highest resolution is around 8 meters
                d = get_dist(x, x_old, y, y_old)
                if d >= 0.92 * cell_dist:
                    x_adj = get_x(x_old, y, y_old, cell_dist)
                    x_old = x_adj
                    y_old = y
                    cell_pos.append([x_old, y_old, 'B'])
            elif x >= 7000 and y >= 5950 and x <= 8000:
                d = get_dist(x, x_old, y, y_old)
                if d >= 0.92 * cell_dist:
                    x_adj = get_x(x_old, y, y_old, cell_dist)
                    x_old = x_adj
                    y_old = y
                    cell_pos.append([x_old, y_old, 'D'])
            elif x >= 4600 and x <= 6050:
                d = get_dist(x, x_old, y, y_old)
                if d >= 0.92 * cell_dist:
                    x_adj = get_x(x_old, y, y_old, cell_dist)
                    x_old = x_adj
                    y_old = y
                    cell_pos.append([x_old, y_old, 'A'])
            elif x >= 4600:
                d = get_dist(x, x_old, y, y_old)
                if d >= 0.92 * cell_dist:
                    y_adj = get_x(y_old, x, x_old, cell_dist)
                    x_old = x
                    y_old = y_adj
                    cell_pos.append([x_old, y_old, 'C'])

    # save the converted data into the cell tower position file
    with open(file_cell_pos, mode='w', newline='') as csv_cell:
        writer_cell = csv.writer(csv_cell)
        writer_cell.writerows(cell_pos)


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
    traci.start([sumoBinary, "-c", "Collect_cell_pos/bts_added.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()
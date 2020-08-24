# Input: teleport file and raw data file
# Output: cell dwelled time with velocity file, timestamp file

import csv
import math

# determine the cell tower inter-spacing
dist_betw_C = 100
# cell tower list
C = []

# list of raw file
file_raw = [
            'C_TLS1000/1Raw1D_TLS1000_G150-vph1400-2hr.csv',
            'C_TLS1000/2Raw1D_TLS1000_G150-vph2800-2hr.csv',
            'C_TLS1000/3Raw1D_TLS1000_G100-vph1400-2hr.csv',
            'C_TLS1000/4Raw1D_TLS1000_G50-vph1400-2hr.csv',
            'C_TLS1000/5Raw1D_TLS1000_G150-vph4200-2hr.csv',
            'C_TLS1000/6Raw1D_TLS1000_G100-vph2800-2hr.csv',
            ]

# list of teleported vehicle file
file_tlp = [
            'C_TLS1000/1Teleport_TLS1000_G150-vph1400-2hr.csv',
            'C_TLS1000/2Teleport_TLS1000_G150-vph2800-2hr.csv',
            'C_TLS1000/3Teleport_TLS1000_G100-vph1400-2hr.csv',
            'C_TLS1000/4Teleport_TLS1000_G50-vph1400-2hr.csv',
            'C_TLS1000/5Teleport_TLS1000_G150-vph4200-2hr.csv',
            'C_TLS1000/6Teleport_TLS1000_G100-vph2800-2hr.csv',
            ]

# list of timestamp file
# using timestamp to find cell dwelled time
file_tst = [
            'C_TLS1000/Cell_50/1TimestampC50_TLS1000_G150-vph1400-2hr.csv',
            'C_TLS1000/Cell_50/2TimestampC50_TLS1000_G150-vph2800-2hr.csv',
            'C_TLS1000/Cell_50/3TimestampC50_TLS1000_G100-vph1400-2hr.csv',
            'C_TLS1000/Cell_50/4TimestampC50_TLS1000_G50-vph1400-2hr.csv',
            'C_TLS1000/Cell_50/5TimestampC50_TLS1000_G150-vph4200-2hr.csv',
            'C_TLS1000/Cell_50/6TimestampC50_TLS1000_G100-vph2800-2hr.csv',
            ]

# calculate the velocity and cell dwelled time to process in machine learning algorithms
file_velo = [
             'C_TLS1000/Cell_50/1VeloC50_TLS1000_G150-vph1400-2hr.csv',
             'C_TLS1000/Cell_50/2VeloC50_TLS1000_G150-vph2800-2hr.csv',
             'C_TLS1000/Cell_50/3VeloC50_TLS1000_G100-vph1400-2hr.csv',
             'C_TLS1000/Cell_50/4VeloC50_TLS1000_G50-vph1400-2hr.csv',
             'C_TLS1000/Cell_50/5VeloC50_TLS1000_G150-vph4200-2hr.csv',
             'C_TLS1000/Cell_50/6VeloC50_TLS1000_G100-vph2800-2hr.csv',
             ]

# find the cell tower location in (x, y) coordinate and cell ID
c = 0
for i in range(int(3000/dist_betw_C+1)):
    c += 1
    C.append((i*dist_betw_C-1500, 0, 'Cell_%03d' %c))

# for each file in raw data file
for a in range(len(file_raw)):
    # read data from raw data file
    # collect vehicle ID in vehicleList
    # collect location data and time in Vehicle
    with open(file_raw[a]) as csv_file:
        Vehicle = []
        VehicleList = []
        read_csv = csv.reader(csv_file, delimiter=',')
        list = []
        next(read_csv, None)
        for row in read_csv:
            newid = row[0]
            if newid not in VehicleList:
                VehicleList.append(newid)
                Vehicle.append([newid, [], [], [], row[1]])
            j = VehicleList.index(newid)
            Vehicle[j][1].append(float(row[2]))  # added time to Vehicle list in column 3 (0 1 2)
            Vehicle[j][2].append(float(row[3]))
            Vehicle[j][3].append(float(row[4]))

    # read data from teleport vehicle
    with open(file_tlp[a]) as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        TLPlist = []
        for row in read_csv:
            for i in row:
                i = str(i.strip())
                TLPlist.append(i)

    # convert raw data to timestamp data and save to file
    with open(file_tst[a], mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['ID', 'Class', 'C_x', 'C_y', 'TimeStamp', 'Cell_ID'])

        # for each vehicle
        for i in Vehicle:
            # calculate for the closest cell
            list = []
            time = range(len(i[2]))
            # for all time
            for ii in time:  # for ii in range of time
                # calculate the distance and compare to cell tower inter-spacing
                # check that if vehicle in the detectable range from the first cell tower
                if math.sqrt((i[2][ii] - C[0][0]) ** 2 + (i[3][ii] - C[0][1]) ** 2) <= dist_betw_C:
                    list.append([i[0], i[4], C[0][0], C[0][1], i[1][ii], C[0][2]])
                    count = ii
                    # for each cell tower
                    for j in range(len(C) - 1):
                        # for each time step
                        for k in range(len(i[1]) - 1 - count):
                            # if the next cell tower is closer than the present cell tower
                            # get the time to be timestamp at the next cell tower
                            # and move to the next cell tower (in for j in range(len(C)-1) loop)
                            if ((i[2][k + 1 + count] - C[j + 1][0]) ** 2 + (
                                    i[3][k + 1 + count] - C[j + 1][1]) ** 2) <= (
                                    (i[2][k + 1 + count] - C[j][0]) ** 2 + (i[3][k + 1 + count] - C[j][1]) ** 2) \
                                    and ((i[2][k + 1 + count] - C[j + 1][0]) ** 2 + (
                                    i[3][k + 1 + count] - C[j + 1][1]) ** 2) < dist_betw_C ** 2:
                                list.append([i[0], i[4], C[j + 1][0], C[j + 1][1], i[1][k + 1 + count], C[j + 1][2]])
                                count += k + 1
                                # go to the next cell tower
                                break
                    writer.writerows(list)
                    list = []
                    break


                elif math.sqrt((i[2][ii] - C[-1][0]) ** 2 + (
                        i[3][ii] - C[-1][1]) ** 2) <= dist_betw_C:
                    list.append([i[0], i[4], C[-1][0], C[-1][1], i[1][ii], C[-1][2]])
                    count = ii
                    for j in range(len(C) - 1):
                        for k in range(len(i[1]) - 1 - count):
                            if ((i[2][k + 1 + count] - C[-2 - j][0]) ** 2 + (
                                    i[3][k + 1 + count] - C[-2 - j][1]) ** 2) <= (
                                    (i[2][k + 1 + count] - C[-1 - j][0]) ** 2 + (
                                    i[3][k + 1 + count] - C[-1 - j][1]) ** 2) \
                                    and ((i[2][k + 1 + count] - C[-2 - j][0]) ** 2 + (
                                    i[3][k + 1 + count] - C[-2 - j][1]) ** 2) < dist_betw_C ** 2:
                                list.append([i[0], i[4], C[-2 - j][0], C[-2 - j][1], i[1][k + 1 + count], C[-2 - j][2]])
                                count += k + 1
                                break
                    writer.writerows(list)
                    list = []
                    break

    # open the timestamp data and convert timestamp to cell dwelled time and average velocity
    with open(file_tst[a]) as csv_file:
        id = 'vehicle ID check'
        read_csv = csv.reader(csv_file, delimiter=',')
        next(read_csv, None)
        list = []
        # get the value for each row
        for row in read_csv:
            # check for the teleportation of vehicle
            if row[0] not in TLPlist:
                # for the new vehicle ID
                # get the new value for each parameter
                if id != row[0]:
                    id = row[0]
                    type = row[1]
                    Cell_ID = row[5]
                    x_coor = float(row[2])
                    y_coor = float(row[3])
                    time = float(row[4])
                # for the same vehicle ID
                # calculate the cell dwelled time and average velocity of vehicle at each cell tower
                elif id == row[0]:
                    CDT = float(row[4]) - time
                    velo = math.sqrt((float(row[2]) - x_coor) ** 2 + (float(row[3]) - y_coor) ** 2) / CDT
                    if velo > 15 and type != 'rail_urban':
                        print(id, type, Cell_ID, velo)
                    else:
                        list.append([id, x_coor, y_coor, velo, time - 21600, CDT, type, Cell_ID])
                    x_coor = float(row[2])
                    y_coor = float(row[3])
                    Cell_ID = row[5]
                    time = float(row[4])

    # save converted data to file
    with open(file_velo[a], mode='w', newline='') as csv_velo:
        writer = csv.writer(csv_velo)
        writer.writerow(['ID', 'C_x', 'C_y', 'Avg Velocity', 'Time Stamp', 'CDT', 'Class', 'Cell_ID'])
        writer.writerows(list)



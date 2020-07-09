import numpy as np
import pandas as pd
import csv

def distance(x1, x2, y1, y2):
    dist = np.sqrt((x1-x2)**2+(y1-y2)**2)
    return dist

# function with
# INPUT: x, y coordinate of vehicle
# OUTPUT: cell ID
def find_cell(inn):
    # extract x, y coordinate from input
    x, y = inn

    # search for x, y index for cell tower
    index_x = (cell_pos_x > (x - cell_dist)) & (cell_pos_x < (x + cell_dist))
    index_y = (cell_pos_y > (y - cell_dist)) & (cell_pos_y < (y + cell_dist))
    index = index_x & index_y

    # get the position of x, y coordinate and ID of cell tower
    pos_x = list(cell_pos_x[index])
    pos_y = list(cell_pos_y[index])
    cell_list = list(cell_pos_id[index])

    # list of distance between each cell tower and the input position of vehicle
    dist = []
    for i in range(len(pos_x)):
        dist.append(distance(x, pos_x[i], y, pos_y[i]))
    dist.append(cell_dist * 2)

    # get the minimum distance's cell tower ID
    if np.min(dist) <= cell_dist:
        cell_id = cell_list[dist.index(np.min(dist))]
    else:
        cell_id = 'out'

    # return cell tower ID as output of this function
    return cell_id

# list of raw data file name
file_raw = ['sathorn_data/collected_data/raw_data_03.csv',
            'sathorn_data/collected_data/raw_data_04.csv',
            'sathorn_data/collected_data/raw_data_05.csv',
            'sathorn_data/collected_data/raw_data_06.csv',
            'sathorn_data/collected_data/raw_data_07.csv']

# list of cell dwelled time data
file_cdt_case1_cell100 = ['sathorn_data/df_tst/cell100/cell100_case1_data_03.csv',
                         'sathorn_data/df_tst/cell100/cell100_case1_data_04.csv',
                         'sathorn_data/df_tst/cell100/cell100_case1_data_05.csv',
                         'sathorn_data/df_tst/cell100/cell100_case1_data_06.csv',
                         'sathorn_data/df_tst/cell100/cell100_case1_data_07.csv']

file_cdt_case2_cell100 = ['sathorn_data/df_tst/cell100/cell100_case2_data_03.csv',
                         'sathorn_data/df_tst/cell100/cell100_case2_data_04.csv',
                         'sathorn_data/df_tst/cell100/cell100_case2_data_05.csv',
                         'sathorn_data/df_tst/cell100/cell100_case2_data_06.csv',
                         'sathorn_data/df_tst/cell100/cell100_case2_data_07.csv']

# determine the cell tower inter-spacing HERE
cell_dist = 100
# cell position file which match with cell_dist
file_cell = 'cell_100_pos.csv'

# get the value from cell position file into numpy array
with open(file_cell) as csv_cell:
    read_csv = csv.reader(csv_cell, delimiter=',')
    cell_pos = []
    cell_pos_x = []
    cell_pos_y = []
    cell_pos_id = []
    # next(read_csv, None)
    for row in read_csv:
        cell_pos.append([float(row[0]), float(row[1]), row[2]])
        cell_pos_x.append(float(row[0]))
        cell_pos_y.append(float(row[1]))
        cell_pos_id.append(row[2])
cell_pos_x = np.array(cell_pos_x)
cell_pos_y = np.array(cell_pos_y)
cell_pos_id = np.array(cell_pos_id)

# get the dataframe with cell ids as the columns and cdt as the data points
# case 1 is the cell dwelled time for each direction
# case 2 is the cell dwelled time sorted by the first to the last cell
for ii in range(len(file_raw)):
    # read raw data from csv file
    df = pd.read_csv(file_raw[ii], delimiter=',')
    # calculate cell tower ID from x, y coordinate using function
    df['Cell_ID'] = df[['PositionX', 'PositionY']].apply(find_cell, axis=1)
    # reorganize dataframe
    df = df.drop(df[df.Cell_ID == 'out'].index)
    df = df.groupby(['ID', 'Class', 'Cell_ID']).Time.min().reset_index()
    df = df.sort_values(['ID', 'Time']).reset_index().drop('index', axis=1)
    # find vehicle ID list
    id_list = df.ID.unique()
    # generate new dataframe to be output dataframe
    df_new = pd.DataFrame([['ID', 'Class', 'Cell_ID', 'Time']])
    df_new.columns = ['ID', 'Class', 'Cell_ID', 'Time']
    df_new = df_new.drop(0)
    # for each vehicle ID in list
    for i in id_list:
        Temp = df.loc[df.ID == i, ['ID', 'Class', 'Cell_ID', 'Time']]
        Temp['Index'] = Temp.reset_index().index
        Temp['time_shift'] = Temp.Time.shift(periods=-1, fill_value=0)
        Temp['cell_shift'] = Temp.Cell_ID.shift(periods=-1, fill_value='none')
        di = (Temp.Cell_ID >= Temp.cell_shift).mean()
        # check the vehicle direction
        if di >= 0.5:
            Temp['Cell_ID'] = '2_' + Temp['Cell_ID']
        else:
            Temp['Cell_ID'] = '1_' + Temp['Cell_ID']
        df_new = pd.concat([df_new, Temp])
    # calculate cell dwelled time for each cell ID
    df_new['CDT'] = df_new['time_shift'] - df_new['Time']

    # save dataframe for case 1
    df_save = df_new.loc[df4.CDT > 0]
    df_save = df_save.groupby(['ID', 'Class', 'Cell_ID']).CDT.mean().unstack().reset_index().fillna(0)
    df_save.to_csv(file_cdt_case1_cell100[ii], index=False)

    # save dataframe for case 2
    df_save = df_new.loc[df4.CDT > 0]
    df_save = df_save.groupby(['ID', 'Class', 'Index']).CDT.mean().unstack().reset_index().fillna(0)
    df_save.to_csv(file_cdt_case2_cell100[ii], index=False)
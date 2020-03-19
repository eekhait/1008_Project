import pandas as pd


# THIS PART CONCERNS WITH:
# THE CSV FILES AND EXTRACTING DATA FROM THEM
# --------------------------------- #
# Indexes of the Complete_Punggol_Graph.csv file:
# Columns: 0-Code, 1-Name, 2-Type, 3-Latitude, 4-Longitude, 5-Buses, 6-ConnectedWalks, 7-ConnectedDistances
# Columns: 8-1197 to refer to nodes     (+7 difference from corresponding node in rows)
# Rows: 1-1190 to refer to nodes
# --------------------------------- #
# How to use pandas dataframe (treat it as a 2D array/excel file):
# mainGraph.at[row,column]
# --------------------------------- #
mainGraph = pd.read_csv('Complete_Punggol_Graph.csv', sep=',', header=None)
mainGraph[0] = mainGraph[0].apply(str)  # converts column to be string-only (rather than int+str)
startIndex = 1
endIndex = len(mainGraph.index)
# --------------------------------- #


def get_distance_to_from(point_a, point_b):
    index_a = get_node_index(point_a)+7
    index_b = get_node_index(point_b)
    return mainGraph.at[index_b, index_a]


def get_long_lat(target):
    index = get_node_index(target)
    return [round(float(mainGraph.at[index, 3]), 3), round(float(mainGraph.at[index, 4]), 3)]


def get_lat_long(target):
    index = get_node_index(target)
    return [round(float(mainGraph.at[index, 4]), 3), round(float(mainGraph.at[index, 3]), 3)]


def get_node_index(target):
    # Start location codes are from index 1 to 1190
    low = startIndex
    high = endIndex
    mid = (startIndex+endIndex)//2
    while target != str(mainGraph.at[mid, 0]):
        if target < str(mainGraph.at[mid, 0]):    # if target is in smaller half
            high = mid
            if mid == (low+high)//2:
                return -1
            mid = (low+high)//2
        elif target > str(mainGraph.at[mid, 0]):    # if target is in larger half
            low = mid
            if mid == (low+high)//2:
                return -1
            mid = (low+high)//2
    return mid


def get_nearest_bus_stops(target, distance):
    pass


def get_nearest_lrt(target):
    if len(target) == 3:
        return target
    else:
        index = get_node_index(target)
        node = ""
        distance = 3000
        for i in range(endIndex+7-14, endIndex+7):
            if 0 < int(mainGraph.at[index, i]) < distance:
                node = mainGraph.at[0, i]
        return str(node)


def is_adjacent_walk(start_node, end_node):
    pass


def is_adjacent_bus(start_node, end_node):
    pass


def is_adjacent_lrt(start_node, end_node):
    pass


# ----------------------------------
# THIS PART CONCERNS WITH ALGORITHMS:
# ----------------------------------
def take_walk(start_node, end_node):
    start_node = str(start_node)
    end_node = str(end_node)
    # if start and end are connected
    if is_adjacent_walk(start_node, end_node):
        return [start_node, end_node]
    else:
        pass


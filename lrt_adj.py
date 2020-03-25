import pandas as pd
import csv
import math

from PyQt5.QtCore.QJsonValue import Null

import main_graph as m_graph

lrtData = pd.read_csv('Punggol_LRT_Routing.csv', sep=',', header=None)


def round_up(n, decimals=0):
    # this is to round up even is 0.1 above
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


def bfs_route(graph, start, end):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        if node == end:
            return path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)


def cal_distance(adj_list_val, result):
    distance = 0
    # e.g. PE1, PE2, PE3
    for i in range(len(result) - 1):  # number of time to run
        for y in range(len(adj_list_val[result[i]])):  # e.g. adj_list_val['PE1'] return number of list value
            if result[i + 1] in adj_list_val[result[i]][
                y]:  # e.g. check if PE2 is in  adj_list_val['PE1'][0] or  adj_list_val['PE1'][1] LISTING
                distance += int(adj_list_val[result[i]][y][result[
                    i + 1]])  # e.g. adj_list_val['PE1'][0][['PE2'] will return the distance weightage
    return distance


def take_lrt(start_node, end_node):
    start_node = str(start_node)
    end_node = str(end_node)
    walk_start_node = []
    walk_end_node = []
    lrt_name = []  # Store the LRT NAME
    lrt_code = []  # Store the LRT CODE
    adj_list = {}  # Store the Adj list
    adj_list_val = {}  # Store the Adj list with value
    with open('Punggol_LRT_Routing.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        first = True
        for row in reader:
            if (first == True):
                for i in range(len(row)):
                    first = False
            else:
                # for i in range(0, len(row)):
                #     # key_value = {row[0]: row[2].split()}  # This is to create the Adj
                lrt_name.append(row[1])  # Append the LRT NAME into the lrt_name
                lrt_code.append(row[0])  # Append the LRT CODE into the lrt_code
                keys = row[2].split(", ")
                values = row[3].split(", ")
                add_value = []
                for i in range(len(keys)):
                    add_value.append({keys[i]: values[i]})  # Create a list of dict e.g. 'PE1' : 1010
                adj_list_val[row[0]] = add_value  # Append the linked code into the list
                adj_list[row[0]] = row[2].split(", ")  # Append the linked code into the list

    if len(start_node) != 3:
        temp_string_start_node = start_node
        start_node = m_graph.get_nearest_lrt(start_node)
        walk_start_node = m_graph.take_walk(temp_string_start_node, start_node)

    if len(end_node) != 3:
        temp_string_end_node = end_node
        end_node = m_graph.get_nearest_lrt(end_node)
        walk_end_node = m_graph.take_walk(temp_string_end_node, end_node)


    print(walk_start_node)
    print(walk_start_node[0])
    print(walk_start_node[1])
    print(start_node)
    print(end_node)

    # Convert the LRT NAME INTO LRT CODE
    for i in range(len(adj_list)):
        if lrt_name[i] == start_node:
            start_node = lrt_code[i]  # Convert start_node Into LRT CODE
            break

    for i in range(len(adj_list)):
        if lrt_name[i] == end_node:
            end_node = lrt_code[i]  # Convert end_noce Into LRT CODE
            break

    # if start and end are connected
    if m_graph.is_adjacent_lrt(adj_list, start_node, end_node):
        result = [start_node, end_node]
        distance = cal_distance(adj_list_val, result)
        timing = round_up((distance / 12.5) / 60)

        if walk_start_node != Null:
            result = walk_start_node[1] + result
            timing = walk_start_node[0] + timing

        if walk_end_node != Null:
            result = result + walk_end_node[1]
            timing = timing + walk_start_node[1]

        # average SG MRT 45km/h == 12.5m/s
        # Calculate the timing Second in minutes,
        print("OutPut: ", [int(timing), [result]])
        return [int(timing), [result]]
    else:
        result = (bfs_route(adj_list, start_node, end_node))
        distance = cal_distance(adj_list_val, result)
        # average timing stop at each mrt is 2min
        mrt_stopping = 2 * int(len(result) - 1)
        # Calculate the timing Second in minutes,
        timing = round_up((distance / 12.5) / 60) + mrt_stopping
        return [int(timing), [result]]

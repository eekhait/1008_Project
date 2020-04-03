import pandas as pd
import main_graph as m_graph
import csv
import sys
import math
import numpy as np


# Columns: 0-Code, ....... pending
busData = pd.read_csv('Punggol_Bus_Routing.csv', sep=',', header=None)
# Columns: 0-Code, ....... pending
busData2 = pd.read_csv('Punggol_Bus_Routing_Type2.csv', sep=',',header=None)
punggol = pd.read_csv('Complete_Punggol_Graph.csv',sep=',',header=None)
punggol1 = pd.read_csv('Punggol_complete_graph2.csv',sep=',',header=None)

bus_speed = 50000/60
bus_waiting_time = 5
'''
Test Cases
start = "65141"
end = "65339"
new_start = "828858"
new_end = "821266"
'''
def busStopCode1(data):
    start = (punggol[0] == data)
    return start

def busStopCode2(data):
    start = punggol1[0] == data
    return start

def connected(data):
    connected1 = punggol[busStopCode1(data)]
    if connected1.empty is True:
        connected1 = punggol1[busStopCode2(data)]
    hg = []
    test = pd.DataFrame(connected1[6].str.split(',').tolist())
    test1 = pd.DataFrame((connected1[7].str.split(',').tolist()))
    if test.empty == True:
        print("no such route For Buses")
        sys.exit()
    if test1.empty == True:
        print ("no such route For buses")
        sys.exit()
    ht =[]
    if len(data) == 5:
        ht.append(int(data))
   # print(int(test1[0].values))
    try:
        niii = max(test1.columns.values)
    except ValueError:
        niii = (test1.columns.values)
    for i in test.iterrows():
        for k in range (0, niii):
            if int(test1[k].values) <= 360:
                #for connected nodes and distance
                hg.append(((int(test[k].values)),(int(test1[k].values))))
                #just for connected nodes
                ht.append(int((test[k].values)))

    return ht

# For finding starting bus Stop( See csv for column 1 and compare to check for bus stop code)
def busStopCode(data):
    startStop = busData2[1] == data
    return startStop

# For finding starting bus Stop( See csv for column 2 and compare to check for bus stop code)
def endStopCode(data):
    endStop = busData2[2] == data
    return endStop

def busNoInserter(data):
    busNo = busData2[0] == data
    return busNo

#For finding the starting point of the bus
def busStopCode_startfinder(data):
    length = len(data)
    new_array =[]
    isa =0
    for i in range(0,length):
        test_test = busStopCode(str(data[i]))
        test_test1 = busData2[test_test]
        if test_test1.empty == False:
            new_array.append(test_test1)
    return new_array

#For findin the ending point of the bus
def busStopCode_endfinder(data):
    length = len(data)
    new_array =[]
    isa =0
    for i in range(0,length):
        test_test = endStopCode(str(data[i]))
        test_test1 = busData2[test_test]
        if test_test1.empty == False:
            new_array.append(test_test1)
    return new_array

# Checking the routes taken by the buses to see if there is a route to the ending bus stop.
def take_bus(start_node, end_node,data):
    bus_route = (busNoInserter(data)) & ((busStopCode(start_node) |  endStopCode(end_node)))
    asd =[]
    asd.append(start_node)
    bus_distance = 0
    lol = np.int64(0)
    lol1 = np.int64(0)
    #bus_route = (bus_route[0]) >= 1 & (bus_route[0] <=3)
    route = busData2[bus_route]
    if len(route) < 2:
        pass
    else:
        if route.empty == True:
            pass
        else:
            lol = route.index.values[0]
            try:
                lol1= route.index.values[1]
            except IndexError:
                lol1 = lol
            for i in range (lol,lol1+1):
                if busData2.at[lol,6] != busData2.at[lol1,6]:
                    pass
                else:
                    bus_distance += int(busData2.at[i,3])
                    asd.append(busData2.at[i,2])

    if len(asd) < 2:
        asd = []
        return None


    return (data,asd, math.ceil(bus_distance/bus_speed + bus_waiting_time + (lol1-lol)))


#For appending all the routes that could be taken and return the one with the least time
def route_finder(new_start, new_end):
    starting = busStopCode_startfinder(connected(new_start))
    ending = busStopCode_endfinder(connected(new_end))
    str1 = ' '
    str2 = ' '
    k = []
    n = []
    for i in range (0,len(starting)):
        bus_to_take = starting[i][0].values
        asd = (starting[i][1].values)
        #bus_to_take , indices = np.unique(asd,return_counts=True)
        for l in bus_to_take:
            try:
                a ,indices= np.unique((starting[i][1].values),return_counts=True)
                b, indices = np.unique((ending[i][2].values),return_counts= True)
                str1 = str1.join(a)
                str2 = str2.join(b)
                if take_bus(str1,str2,l) is None:
                    pass
                else:
                    p = list(take_bus(str1,str2,l))
                    n.append((take_bus(str1,str2,l))[2])
                    k.append(p)

            except IndexError:
                "Do Nothing"
    df = pd.DataFrame(k)

    if df.empty == True:
        print("No common bus nearby start and end points. Please restart with another option. ")
        sys.exit()

    route = df[2] == min(n)
    optimised_route = df[route]
    optimised_route[0], optimised_route[2] = optimised_route[2], optimised_route[0]
    pop = optimised_route.head(1)

    first_route = []
    lol = pd.DataFrame(pop[1].tolist())

    starting_walk = m_graph.take_walk(new_start,lol[0].values[0])
    lemon =[]
    if ((starting_walk[0]) == 0):
        pass
    else:
        first_route=starting_walk[1]
        first_route.pop(len(first_route)-1)

    for i in range(1,len(starting_walk)):
        lemon.append(False)


    for i in range (0,len(lol)):
        for l in lol:
            first_route.append((lol[l][i]))
            lemon.append(True)

    length = max(lol)
    Last_Point = lol[length].values[0]
    ending_walk = m_graph.take_walk(Last_Point, new_end)


    if len(ending_walk) <= 2:
        end_route = ending_walk[1]
        end_route.pop(0)

        lemon.append(False)
    else:
        new = np.array(ending_walk[1])
        counter = 1
        for i in range(1, len(new)):
            first_route.append(new[counter])
            lemon.append(False)
            counter = counter + 1

    k = []
    # all route here
    for i, l in optimised_route.iterrows():
        k.append((l[0], l[1], l[2]))
    route = []
    test1 = pop
    route.append(test1[0][0]) # time taken is fine
    route[0] += starting_walk[0]
    route[0] += ending_walk[0]
    print("first_route:", first_route)
    route.append(first_route)
    route.append(lemon) # lemon is fine
    print("")
    route.append(test1[2][0]) # bus number is fine
    return (route)

# print("BUS ROUTE: ", route_finder("828858","65009"))



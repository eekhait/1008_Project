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
#Complete_graph = pd.read_csv('Complete_Punggol_Graph.csv' , sep=',', header=None,)
bus_speed = 50000/60
bus_waiting_time = 5
start = "65141"
end = "65339"
new_start = "828858"
new_end = "821266"
#busData.set_index("3")
#print (busData[:])
#print (busData[[2,3]])
#print (busData.loc[[5 ,7 , 9],:])

#busStop2 = (busData[3] == "65009")
#print(busStop2)
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
            if int(test1[k].values) <=200:
                #for connected nodes and distance
                hg.append(((int(test[k].values)),(int(test1[k].values))))
                #just for connected nodes
                ht.append(int((test[k].values)))
    #connected = connected1[7] <= 200;
    return ht

#print ("New Conneccted ", connected(new_start))
#print ("New end ", connected(new_end))
#print(m_graph.take_walk(start,end))
# test test find route
'''
connected1 = punggol[busStopCode1(new_start)]
connected2 =punggol[busStopCode1(new_end)]
new_route2 = (busStopCode1(new_start) | busStopCode1(new_end))
new_route2 = punggol[new_route2]
print (new_route2)
'''


def busStopCode(data):
    startStop = busData2[1] == data
    return startStop

def endStopCode(data):
    endStop = busData2[2] == data
    return endStop
#bus = busStopCode(start) | endStopCode(end)
def busNoInserter(data):
    busNo = busData2[0] == data
    return busNo

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

def take_bus(start_node, end_node,data):
    bus_route = (busNoInserter(data)) & (busStopCode(start_node) |  endStopCode(end_node))
    asd = [start_node]
    bus_distance = 0
    lol = np.int64(0)
    lol1 = np.int64(0)
    #bus_route = (bus_route[0]) >= 1 & (bus_route[0] <=3)
    route = busData2[bus_route]
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
    # This is for distance measuring
    #print (math.ceil(bus_distance/bus_speed + bus_waiting_time + (lol1-lol)))

    if len(asd) < 1:
        asd = []
        return None


    return (data,asd, math.ceil(bus_distance/bus_speed + bus_waiting_time + (lol1-lol)))
    #for i in busData:
        #print(col[2])
   # for key, value in busData.iteritems():
        #print(key,value)

#print(take_bus("65141", "65009","43"))
print(busStopCode_startfinder(connected(new_start)))

def route_finder(new_start, new_end):
    starting = busStopCode_startfinder(connected(new_start))
    print(starting)
    ending = busStopCode_startfinder(connected(new_end))
    print(ending)
    str1 = ' '
    str2 = ' '
    k = []
    n = []
    for i in range (0,len(starting)):
        bus_to_take = starting[i][0].values
        asd = (starting[i][1].values)
        bus_to , indices = np.unique(asd,return_counts=True)
        for l in bus_to_take:
        #buses.append(bus_to_take[5])
            try:
                a ,indices= np.unique((starting[i][1].values),return_counts=True)
                b, indices = np.unique((ending[i][2].values),return_counts= True)
                str1 = str1.join(a)
                str2 = str2.join(b)
                if take_bus(str1,str2,l) is None:
                    pass
                else:
                    p = list((take_bus(str1,str2,l)))
                    n.append((take_bus(str1,str2,l))[2])
                    k.append(p)


                #k.append(take_bus(str1,str2,l)[2])
                #print((take_bus(str1,str2,l)))
            except IndexError:
                "Do Nothing"
    df = pd.DataFrame(k)
    print(df)
    if df.empty == True:
        print("no such route for buses")
        sys.exit()
    route = df[2] == min(n)
    optimised_route = df[route]
    name = pd.DataFrame(optimised_route[1].tolist())
    optimised_route[0], optimised_route[2] = optimised_route[2], optimised_route[0]
    pop = optimised_route.head(1)
    #pop.loc[0], pop.loc[2] = pop.loc[2], pop.loc[0]
    first_route = []
    lol = pd.DataFrame(pop[1].tolist())

    starting_walk = m_graph.take_walk(new_start,lol[0].values[0])
    print(starting_walk)
    if ((starting_walk[0]) == 0):
        pass
    else:
        first_route.append(starting_walk[0])
    for i in range (0,len(lol)):
        for l in lol:
            first_route.append((lol[l][i]))
    ending_walk = m_graph.take_walk(lol[1].values[0], new_end)
    if len(ending_walk) <2:
        first_route.append(ending_walk[1])
    else:
        new = np.array(ending_walk[1])
        #for m in ending_walk:
        #ending_list = (str(ending_walk[1])).strip('[]')
        counter = 1
        for i in range (1,len(new)):
            first_route.append(new[counter])
            counter = counter + 1
    for i, l in pop.iterrows():
        p = [l[0], l[1], l[2]]

    k = []
    # all route here
    for i ,l in optimised_route.iterrows():
        k.append((l[0],l[1],l[2]))
    #print (k)

    return first_route


print(m_graph.take_walk("65431", end))
route_finder(new_start,new_end)

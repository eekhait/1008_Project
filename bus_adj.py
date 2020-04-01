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
#Complete_graph = pd.read_csv('Complete_Punggol_Graph.csv' , sep=',', header=None,)
bus_speed = 50000/60
bus_waiting_time = 5
start = "65009"
end = "65221"
new_start = "821260"
new_end = "821266"
#busData.set_index("3")
#print (busData[:])
#print (busData[[2,3]])
#print (busData.loc[[5 ,7 , 9],:])

#busStop2 = (busData[3] == "65009")
#print(busStop2)
def busStopCode1(data):
    start = punggol[0] == data;
    return start

def connected(data):

    connected1 = punggol[busStopCode1(data)]
    hg = []
    test = pd.DataFrame(connected1[6].str.split(',').tolist())
    test1 = pd.DataFrame((connected1[7].str.split(',').tolist()))
    ht =[]
    if len(data) == 5:
        ht.append(data)
   # print(int(test1[0].values))
    niii = max(test1.columns.values)
    for i in test.iterrows():
        for k in range (0, niii):
            if int(test1[k].values) <=200:
                #for connected nodes and distance
                hg.append(((int(test[k].values)),(int(test1[k].values))))
                #just for connected nodes
                ht.append(int(test[k].values))
    #connected = connected1[7] <= 200;
    return ht

print (connected(start))
print (connected(end))

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

#print (busStopCode_startfinder(connected(new_start)))
#print (busStopCode_endfinder(connected(new_end)))

#print (lol)
#print ()
#print (busNo("3"))
#print (busData2[bus])
#print(busData[(busStopCode(start))])
#print (busData2.loc[1:2,1])

def take_bus(start_node, end_node,data):
    bus_route = (busNoInserter(data)) & (busStopCode(start_node) |  endStopCode(end_node))
    asd = [start_node]
    bus_distance = 0
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
            bus_distance += int(busData2.at[i,3])
            asd.append(busData2.at[i,2])
    # This is for distance measuring
    #print (math.ceil(bus_distance/bus_speed + bus_waiting_time + (lol1-lol)))
    return (data,asd, math.ceil(bus_distance/bus_speed + bus_waiting_time + (lol1-lol)))
    #for i in busData:
        #print(col[2])
   # for key, value in busData.iteritems():
        #print(key,value)

#print(take_bus(start, end,busNumber))

def route_finder(new_start, new_end):
    starting = busStopCode_startfinder(connected(new_start))
    starting_busNo = starting[0][0]
    ending = busStopCode_endfinder(connected(new_end))
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
                p = list((take_bus(str1,str2,l)))
                n.append((take_bus(str1,str2,l))[2])
                k.append(p)

                #k.append(take_bus(str1,str2,l)[2])
                #print((take_bus(str1,str2,l)))
            except IndexError:
                "Do Nothing"

    df = pd.DataFrame(k)
    route = df[2] == min(n)
    optimised_route = df[route]
    name = pd.DataFrame(optimised_route[1].tolist())
    optimised_route[0], optimised_route[2] = optimised_route[2], optimised_route[0]
    pop = optimised_route.head(1)
    #pop.loc[0], pop.loc[2] = pop.loc[2], pop.loc[0]
    first_route = []
    lol = pd.DataFrame(pop[1].tolist())
    for i in range (0,len(lol)):
        for l in lol:
            first_route.append((lol[l][i]))
    p = []
    #if len(new_start) == 6:
     #   if len(new_end) == 6:
      #      for i, l in pop.iterrows():
       #         p = [l[0], new_start,l[1],new_end, l[2]]
    #else:
    for i, l in pop.iterrows():
        p = [l[0], l[1], l[2]]

    print (p)
    k = []
    # all route here
    for i ,l in optimised_route.iterrows():
        k.append((l[0],l[1],l[2]))
    #print (k)

    return p

route_finder(new_start,new_end)

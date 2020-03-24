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
    return int(mainGraph.at[index_b, index_a])


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
        for i in range(endIndex+7-14, endIndex+7):  # start and end of LRT columns in csv
            if 0 < int(mainGraph.at[index, i]) < distance:
                node = mainGraph.at[0, i]
        return str(node)


def get_adjacent_walks(start_node):
    start_index = get_node_index(start_node)
    connected_nodes = mainGraph.at[start_index, 6].split(', ')
    return connected_nodes


def is_adjacent_walk(start_node, end_node):
    start_index = get_node_index(start_node)
    connected_nodes = mainGraph.at[start_index, 6].split(', ')
    if end_node in connected_nodes:
        return True
    else:
        return False


def is_adjacent_bus(start_node, end_node):
    pass


def is_adjacent_lrt(adj_list, start_node, end_node):
    # Check If Are Both LRT are directly connected!
    for i in (adj_list):
        if start_node == i:  # To check if able to found the KEY
            if end_node in adj_list[i]:  # To check if both Start_Node & End_Node are directly connected
                return 1  # If Yes, return 1
            else:
                return 0  # If No, return 0
            break

# ----------------------------------
# THIS PART CONCERNS WITH ALGORITHMS:
# ----------------------------------
class AStarStack:
    def __init__(self):
        self.top = -1
        self.data = []
        self.total_distance = 0

    def show_stack(self):
        print("start")
        for i in self.data:
            print(i)
        print("end")

    def push(self, node):
        self.top += 1
        self.data.append(node)
        if self.top > 0:    # if there is at least two elements...
            self.total_distance += get_distance_to_from(self.data[self.top], self.data[self.top-1])

    def pop(self):
        if self.top > -1:
            node = self.data[self.top]
            if self.top > 0:
                self.total_distance -= get_distance_to_from(self.data[self.top], self.data[self.top-1])
            del self.data[self.top]
            self.top -= 1
            return node

    def is_empty(self):
        if self.top < 0:
            return True
        else:
            return False

    def peek(self):
        if not self.is_empty():
            return self.data[self.top]

    def peek_distance(self):
        if not self.is_empty():
            return self.total_distance

    def copy_from(self, a_stack):
        for x in a_stack.data:
            self.push(x)


class AStarQueue:
    def __init__(self):
        self.top = -1
        self.data = []

    def show_line(self):
        for i in self.data:
            print("START")
            i.show_stack()
            print("END")

    def enqueue(self, node):
        self.top += 1
        self.data.append(node)

    def dequeue(self):
        if self.top > -1:
            temp = self.data[0]
            del self.data[0]
            self.top -= 1
            return temp

    def is_empty(self):
        if self.top < 0:
            return True
        else:
            return False

    def peek(self):
        if not self.is_empty():
            return self.data[0]


def take_walk(start_node, end_node):
    start_node = str(start_node)
    end_node = str(end_node)
    # if start and end are connected
    if is_adjacent_walk(start_node, end_node):
        return [start_node, end_node]
    else:   # this part begins like the word ladder
        # initialization of queue and first stack (of just start node)
        # also initialization of visited nodes
        star_queue = AStarQueue()
        star_stack = AStarStack()
        star_stack.push(start_node)
        star_queue.enqueue(star_stack)
        visited_nodes = {}
        counter = 0
        # while end node is not reached
        while star_queue.data[0].peek() != end_node:
            # dequeue the first stack
            temp_stack = star_queue.dequeue()
            mid_node = temp_stack.peek()
            # add all adjacent nodes to mid_node in separate stacks
            # move stacks to queue
            for i in get_adjacent_walks(mid_node):
                # create new stack with each adjacent node
                temper_stack = AStarStack()
                temper_stack.copy_from(temp_stack)
                temper_stack.push(str(i))
                # temper_stack.show_stack()
                # if node is visited before
                if i in visited_nodes:
                    # only enqueue if new path/stack is shorter than old path
                    if temper_stack.total_distance < visited_nodes[i]:
                        star_queue.enqueue(temper_stack)
                        visited_nodes[i] = temper_stack.total_distance
                # if node is new, enqueue normally
                elif i not in visited_nodes:
                    # enqueue the stack
                    star_queue.enqueue(temper_stack)
                    visited_nodes[i] = temper_stack.total_distance
        return [star_queue.data[0].total_distance, star_queue.data[0].data]


print(take_walk('65009', '820199'))



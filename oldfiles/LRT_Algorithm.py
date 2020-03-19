from collections import deque
import csv


class Graph:
    def __init__(self, lists):
        self.lists = lists

    def get_neighbours(self, i):
        return self.lists[i]

    import csv
    cove_lrt, meridian_lrt, coraledge_lrt, riviera_lrt, kadaloor_lrt, oasis_lrt, damai_lrt, punggol_lrt, samkee_lrt, tecklee_lrt, punggolpoint_lrt, samudera_lrt, nibong_lrt, sumang_lrt, sooteck_lrt = ([] for i in range(15))

    with open('LRT.csv') as file:
        lrt = list(csv.reader(file))
        cove_lrt.append(lrt[1])
        meridian_lrt.append(lrt[2])
        coraledge_lrt.append(lrt[3])
        riviera_lrt.append(lrt[4])
        kadaloor_lrt.append(lrt[5])
        oasis_lrt.append(lrt[6])
        damai_lrt.append(lrt[7])
        punggol_lrt.append(lrt[8])
        samkee_lrt.append(lrt[9])
        tecklee_lrt.append(lrt[10])
        punggolpoint_lrt.append(lrt[11])
        samudera_lrt.append(lrt[12])
        nibong_lrt.append(lrt[13])
        sumang_lrt.append(lrt[14])
        sooteck_lrt.append(lrt[15])

    #heuristic function for all nodes
    def heuristic(self, n):
        Heuristic = {
            'Punggol_MRT': 1,
            'SamKee_LRT': 1,
            'SooTeck_LRT': 1,
            'PunggolPoint_LRT': 1,
            'Samudera_LRT': 1,
            'Sumang_LRT': 1,
            'Nibong_LRT': 1,
            'Damai_LRT': 1,
            'Kadaloor_LRT': 1,
            'Riviera_LRT': 1,
            'CoralEdge_LRT': 1,
            'Meridian_LRT': 1,
            'Oasis_LRT': 1,
            'Cove_LRT': 1,
        }
        return Heuristic[n]

    def astar_algorithm(self, start_node, stop_node):
        # open_list is a list of nodes which have been visited, but who's neighbors
        # haven't all been inspected, starts off with the start node
        # closed_list is a list of nodes which have been visited
        # and who's neighbors have been inspected
        open_list = set([start_node])
        closed_list = set([])

        # cdist contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        cdist = {}

        cdist[start_node] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start_node] = start_node

        while len(open_list) > 0:
            n = None

            # find a node with the lowest value of f() - evaluation function
            for i in open_list:
                if n == None or cdist[i] + self.heuristic(i) < cdist[n] + self.heuristic(n):
                    n = i;

            if n == None:
                print('Path does not exist!')
                return None

            # if the current node is the stop_node
            # then we begin reconstructing the path from it to the start_node
            if n == stop_node:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start_node)

                reconst_path.reverse()
                print('Path found: {}'.format(reconst_path))
                return reconst_path

            # for all neighbors of the current node do
            for (m, weight) in self.get_neighbours(n):
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    cdist[m] = cdist[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if cdist[m] > cdist[n] + weight:
                        cdist[m] = cdist[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None

lists = {
    # LRT on Punggol East
    'Punggol_MRT': [('SamKee_LRT', 0.589), ('SooTeck_LRT', 0.605), ('Damai_LRT', 0.690), ('Cove_LRT', 0.763)],
    'SamKee_LRT': [('Punggol_MRT', 0.589), ('PunggolPoint_LRT', 0.815)],
    'PunggolPoint_LRT': [('SamKee_LRT', 0.815), ('Samudera_LRT', 0.513)],
    'Samudera_LRT': [('PunggolPoint_LRT', 0.513), ('Nibong_LRT', 0.493)],
    'Nibong_LRT': [('Samudera_LRT', 0.493), ('Sumang_LRT', 0.429)],
    'Sumang_LRT': [('Nibong_LRT', 0.429), ('SooTeck_LRT', 0.478)],
    'SooTeck_LRT': [('Sumang_LRT', 0.478), ('Punggol_MRT', 0.605)],

    # LRT on Punggol West
    'Damai_LRT': [('Punggol_MRT', 0.690), ('Oasis_LRT', 0.563)],
    'Oasis_LRT': [('Damai_LRT', 0.563), ('Kadaloor_LRT', 0.515)],
    'Kadaloor_LRT': [('Oasis_LRT', 0.515), ('Riviera_LRT', 0.558)],
    'Riviera_LRT': [('Kadaloor_LRT', 0.558), ('CoralEdge_LRT', 0.386)],
    'CoralEdge_LRT': [('Riviera_LRT', 0.386), ('Meridian_LRT', 0.530)],
    'Meridian_LRT': [('CoralEdge_LRT', 0.530), ('Cove_LRT', 0.443)],
    'Cove_LRT': [('Meridian_LRT', 0.443), ('Punggol_MRT', 0.763)],
}

graph1 = Graph(lists)
graph1.astar_algorithm('Samudera_LRT', 'Riviera_LRT')

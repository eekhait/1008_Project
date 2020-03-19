import pandas as pd
import main_graph as m_graph

lrtData = pd.read_csv('Punggol_LRT_Routing.csv', sep=',', header=None)


def take_lrt(start_node, end_node):
    start_node = str(start_node)
    end_node = str(end_node)
    # if start and end are connected
    if m_graph.is_adjacent_lrt(start_node, end_node):
        return [start_node, end_node]
    else:
        pass

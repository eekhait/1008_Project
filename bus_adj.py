import pandas as pd
import main_graph as m_graph


# Columns: 0-Code, ....... pending
busData = pd.read_csv('Punggol_Bus_Routing.csv', sep=',', header=None)
# Columns: 0-Code, ....... pending
busData2 = pd.read_csv('Punggol_Bus_Routing_Type2.csv', sep=',',header=None)


def take_bus(start_node, end_node):
    start_node = str(start_node)
    end_node = str(end_node)
    # if start and end are connected
    if m_graph.is_adjacent_bus(start_node, end_node):
        return [start_node, end_node]
    else:
        pass

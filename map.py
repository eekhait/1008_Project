import folium
import io
import sys
import main_graph as m_graph
import bus_adj as bus_graph
import lrt_adj as lrt_graph
from PyQt5 import QtWidgets, QtWebEngineWidgets
import csv

# ----------------------------------
# THIS PART CONCERNS WITH UI
# EVERYTHING COMES TOGETHER HERE
# ----------------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Create map object, set default location, map theme & zoom
    m = folium.Map(location=[1.4046357, 103.9090000], tiles="Stamen Terrain", zoom_start=14.5)
    # Global tooltip, hover info
    tooltip = 'Click For More Info'

    # ASKS FOR INPUT/OUTPUT HERE, EVERYTHING TAKEN IN AS STRING (Irvyn)
    def check(start):
        with open('Complete_Punggol_Graph.csv', 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if start == row[0] or start == row[1]:
                    location.append(row[0])
                    name.append(row[1])
            return location, name

    def confirmation(msg):
        while True:
            answer = input(msg).upper()
            if answer in ('Y', 'N'):
                return answer
            else:
                print('Not a valid input, please try again')

    def transportation(tp):
        while True:
            mode = input(tp).upper()
            if mode in ('L', 'B', 'W', 'M'):
                return mode
            else:
                print('Not a valid input, please try again')

    print("\nWelcome to Punggol Pathfinder")
    print(
        "Valid inputs are: \033[1m Postal codes, bus stop numbers, train station names, train station codes. \033[0m")

    while True:
        name = []
        # User start and end code will be stored in here
        location = []
        # User choosen mode will stored in here
        mode = []
        result_path = []
        # Prompt user for start and destination point
        start = input("\nWhere are you coming from?\n")
        end = input("Where is your destination?\n")

        # Calls function to check if input is valid by comparing with CSV
        if check(start) == None or check(end) == None:
            print("Location not valid, please try again\n")
            continue
        else:
            sp = name[0]
            ep = name[1]

            if sp:
                print("Start location: ", sp)
            else:
                print("Start location: ", start)
            if ep:
                print("Destination: ", ep)
            else:
                print("Destination: ", end)

            answer = confirmation("\nConfirm start location and destination? [Y/N] \n")
            if answer == 'N':
                print("Let\'s try again")
            elif answer == 'Y':
                mode = transportation("Select mode of transport: LRT (L), Bus (B), Walk (W), or Mixed (M)\n")
                if mode == 'L':
                    # Call Lrt algorithm here
                    result_path = lrt_graph.take_lrt(start, end)
                elif mode == 'B':
                    # Call Bus algorithm here
                    print("Bus")
                elif mode == 'W':
                    # Call Walk algorithm here
                    result_path = m_graph.take_walk(location[0], location[1])
                elif mode == 'M':
                    # Call Mixed algorithm here
                    print("Mixed")
                break

    # print(location)
    # print(mode)

    # lastly... (current path is placeholder)
    caseL = [10, ['65151', 'PE1', 'PE2', 'PE3','820127']]
    caseB = [15, ['820269', '820270', '820271', '65009', '65221', '820294'], ['0', '0', '0', '3', '3', '0']]

    print("\nYou can reach XXX from XXX via...")
    print("")   # loop through result_path array and print in one line

    # (khai)
    # THIS PART IS WHERE THE MAP GETS POPULATED WITH NODES AND EDGES ---------------------------------------------

    # Adding of markers and edges for Single Transport Routes
    def singleTransportPlot(paths, markerColor, lineColor, markerIcon):
        marker_coords = []
        edge_coords = []
        for i in paths:
            # this loop creates a list of coordinates to add markers/nodes with
            marker_coords.append(m_graph.get_lat_long(i))
            edge_coords.append(m_graph.get_long_lat(i))

        for i in range(0, len(marker_coords)):
            folium.Marker([marker_coords[i][1], marker_coords[i][0]], icon=folium.Icon(color=markerColor,icon=markerIcon, prefix='fa'), popup=i, tooltip=result_path[i]).add_to(m)
        folium.PolyLine(edge_coords, color=lineColor).add_to(m)

    # Set icon for different transportation types
    def iconMaker(length):
        if length == 3:
            return "train"
        elif (length == 5):
            return "bus"
        elif length == 6:
            return "blind"

    # Set color based on transportation type
    def setColor(length):
        if length == 3:
            return "purple"
        elif (length == 5):
            return "green"
        elif length == 6:
            return "grey"    
    
    # Set route based on different transport
    def routePlotting(MOT, paths):
        if (MOT == "L"):
            marker_coords = []
            edge_coords = []
            changes_Indicator = 0

            for i in range(0, len(paths[1])):
                marker_coords.append(m_graph.get_lat_long(paths[1][i]))

                current_node = paths[1][i]
                if i+1 < len(paths[1]):
                    next_node = paths[1][i+1]
                
                edge_coords.append(m_graph.get_long_lat(current_node))

                if len(current_node) == 3 and len(next_node) == 3:
                    folium.Marker([marker_coords[i][1], marker_coords[i][0]], icon=folium.Icon(color="darkred",icon=iconMaker(len(current_node)), prefix='fa'), popup=i, tooltip=result_path[1][i]).add_to(m)
                    edge_coords.append(m_graph.get_long_lat(next_node))
                    folium.PolyLine(edge_coords, color="purple").add_to(m)
                    edge_coords = []
                else:
                    folium.Marker([marker_coords[i][1], marker_coords[i][0]], icon=folium.Icon(color="darkred",icon=iconMaker(len(current_node)), prefix='fa'), popup=i, tooltip=result_path[1][i]).add_to(m)
                    edge_coords.append(m_graph.get_long_lat(next_node))
                    folium.PolyLine(edge_coords, color="grey").add_to(m)
                    edge_coords = []                    
        elif (MOT == "B"):
            marker_coords = []
            edge_coords = []
            changes_Indicator = 0

            for i in range(0, len(paths[1])):
                marker_coords.append(m_graph.get_lat_long(paths[1][i]))

                current_node = paths[1][i]
                if i+1 < len(paths[1]):
                    next_node = paths[1][i+1]
                
                edge_coords.append(m_graph.get_long_lat(current_node))

                if len(current_node) == 5 and len(next_node) == 5:
                    folium.Marker([marker_coords[i][1], marker_coords[i][0]], icon=folium.Icon(color="darkred",icon=iconMaker(len(current_node)), prefix='fa'), popup=i, tooltip=result_path[1][i]).add_to(m)
                    edge_coords.append(m_graph.get_long_lat(next_node))
                    folium.PolyLine(edge_coords, color="green").add_to(m)
                    edge_coords = []
                else:
                    folium.Marker([marker_coords[i][1], marker_coords[i][0]], icon=folium.Icon(color="darkred",icon=iconMaker(len(current_node)), prefix='fa'), popup=i, tooltip=result_path[1][i]).add_to(m)
                    edge_coords.append(m_graph.get_long_lat(next_node))
                    folium.PolyLine(edge_coords, color="grey").add_to(m)
                    edge_coords = []   
        elif (MOT == "W"):
            singleTransportPlot(paths, "darkred", "grey", "male") 
        elif (MOT == "M"):
            marker_coords = []
            edge_coords = []
            changes_Indicator = 0

            for i in range(0, len(paths[1])):
                marker_coords.append(m_graph.get_lat_long(paths[1][i]))

                current_node = paths[1][i]
                if i+1 < len(paths[1]):
                    next_node = paths[1][i+1]
                
                edge_coords.append(m_graph.get_long_lat(current_node))

                if len(current_node) == len(next_node):
                    folium.Marker([marker_coords[i][1], marker_coords[i][0]], icon=folium.Icon(color="darkred",icon=iconMaker(len(current_node)), prefix='fa'), popup=i, tooltip=result_path[1][i]).add_to(m)
                    edge_coords.append(m_graph.get_long_lat(next_node))
                    folium.PolyLine(edge_coords, color=setColor(len(current_node))).add_to(m)
                    edge_coords = []
                elif len(current_node) != len(next_node):
                    if changes_Indicator == 1:
                        folium.Marker([marker_coords[i][1], marker_coords[i][0]], icon=folium.Icon(color="darkred",icon=iconMaker(len(current_node)), prefix='fa'), popup=i, tooltip=result_path[1][i]).add_to(m)
                        edge_coords.append(m_graph.get_long_lat(next_node))
                        folium.PolyLine(edge_coords, color=setColor(len(next_node))).add_to(m)
                        edge_coords = []
                        changes_Indicator -= 1
                    else:
                        folium.Marker([marker_coords[i][1], marker_coords[i][0]], icon=folium.Icon(color="darkred",icon=iconMaker(len(current_node)), prefix='fa'), popup=i, tooltip=result_path[1][i]).add_to(m)
                        edge_coords.append(m_graph.get_long_lat(next_node))
                        folium.PolyLine(edge_coords, color=setColor(len(current_node))).add_to(m)
                        edge_coords = []
                        changes_Indicator +=1

    # Call Set routes and pass in mode of transport and routes
    # Sample Input: [Coming From: PE1], [Coming From: ]
    routePlotting(mode, location)

    # Initialization of the map
    data = io.BytesIO()             # creates a temporary 'container' for html code
    m.save(data, close_file=False)  # folium html code is saved inside data variable
    w = QtWebEngineWidgets.QWebEngineView()     # then the rest of the code is the map running
    w.setHtml(data.getvalue().decode())
    w.resize(840, 680)
    w.show()
    sys.exit(app.exec_())

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
        def lrt(start):
        with open('csv\Punggol_LRT_Routing.csv', 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if start == row[0] or start == row[1]:
                    location.append(row[0])
                    return location
                else:
                    with open('csv\Complete_Punggol_Graph.csv') as g:
                        reader2 = csv.reader(g, delimiter=',')
                        for row2 in reader2:
                            if start == row2[0]:
                                location.append(row2[0])
                                return location
                            else:
                                with open('csv\Punggol_Buildings.csv') as h:
                                    reader3 = csv.reader(h, delimiter=',')
                                    for row3 in reader3:
                                        if start == row3[0] or start == row2[1]:
                                            location.append(row3[1])
                                            return location

    def confirmation(msg):
        while True:
            answer = input(msg)
            answer = answer.upper()
            if answer in ('Y', 'N'):
                return answer
            else:
                print('Not a valid input, please try again')

    def transportation(tp):
        while True:
            mode = input(tp)
            mode = mode.upper()
            if mode in ('L', 'B', 'W', 'M'):
                return mode
            else:
                print('Not a valid input, please try again')

    print("\nWelcome to Punggol Pathfinder")
    print(
        "Valid inputs are: \033[1m Postal codes, buss tops numbers, train station names, train station codes. \033[0m")

    while True:
        # User start and end code will be stored in here
        location = []
        # User choosen mode will stored in here
        mode = []
        # Prompt user for start and destination point
        start = input("\nWhere are you coming from?\n")
        end = input("Where is your destination?\n")

        # Calls function to check if input is valid by comparing with CSV
        if lrt(start) == None or lrt(end) == None:
            print("Location not valid, please try again\n")
            continue
        else:
            print("Start location: ", start, "\nDestination: ", end)
            answer = confirmation("\nConfirm start location and destination? [Y/N] \n")
            if answer == 'N':
                print("Let\'s try again")
            elif answer == 'Y':
                mode = transportation("Select mode of transport: LRT (L), Bus (B), Walk (W), or Mixed (M)\n")
                if mode == 'L':
                    # Call Lrt algorithm here
                    print("Lrt")
                elif mode == 'B':
                    # Call Bus algorithm here
                    print("Bus")
                elif mode == 'W':
                    # Call Walk algorithm here
                    print("Walk")
                elif mode == 'M':
                    # Call Mixed algorithm here
                    print("Mixed")
                break

    print(location)
    print(mode)

    # search if inputs are codes/names
        # if codes, no change
        # if names, convert to code
    # if L... (Alfred)
        # call LRT function
        # store results of node under result_path
        # closest LRT to START is XXX, closest LRT to END is XXX
                # algorithm hereee
                # explain route (start station, station 2, ..., end station)
                    # maybe prepend/append walk to start and end stations
    # elif B... (Bryan)
        # call bus function
        # store reults of node under result_path
            #  get closest bus stops and their available buses
    # elif W... (Russ)
        # call walk function
        # store reults of node under result_path
    # elif M (Russ)
        # call mixed function
        # store reults of node under result_path
    # else: invalid (Irvyn)
        # ask for input again


    # lastly... (current path is placeholder)
    result_path = [30, ['PE1', 'PE2', 'PE3', 'PE4', 'PE5', 'PE6', 'PE7', 'PTC', 'PW1', 'PW3', 'PW4', 'PW5', 'PW6', 'PW7']]
    caseL = [10, ['65151', 'PE1', 'PE2', 'PE3','820127']]
    caseB = [15, ['820269', '820270', '820271', '65009', '65221', '820294'], ['0', '0', '0', '3', '3', '0']]
    caseW = [30, ['65009', '65159', '820288', '65341']]

    print("\nYou can reach XXX from XXX via...")
    print("")   # loop through result_path array and print in one line

    # (khai/tamm)
    # THIS PART IS WHERE THE MAP GETS POPULATED WITH NODES AND EDGES
    marker_coords = []
    edge_coords = []
    for i in result_path:
        # this loop creates a list of coordinates to add markers/nodes with
        marker_coords.append(m_graph.get_lat_long(i))
        edge_coords.append(m_graph.get_long_lat(i))

    # Adding of markers and edges to map
    for i in range(0, len(marker_coords)):
        folium.Marker([marker_coords[i][1], marker_coords[i][0]], popup=i, tooltip=result_path[i]).add_to(m)
    folium.PolyLine(edge_coords, color="red").add_to(m)

    # CREATE A FUNCTION THAT USES DIFFERENT COLORS FOR DIFFERENT MODES OF TRANSPORT
    # MODIFY THE CODE ABOVE
    # if only one more of transport, no biggie
        # if lrt...
        # elif bus...
        # elif walk...
        # elif mixed...
            # take in edge_coords
            # split edge_coords to how many times the transport mode changes according to mode array
            # basically you will get a list of arrays
            # also hardcode a list of 4 colours to choose from (walk, lrt, bus1, bus2)
            # prevcolor = "" (blank)
            # for each sub-array in array:
                # if lrt/walk...
                    #folium.PolyLine(sub_array, color="1/2").add_to(m) #rmbr to push the color out
                # if bus
                    # bus will alternate between two similar colours
                    # if color == precolor:
                        # folium.PolyLine(sub_array, color="4").add_to(m) #rmbr to push the color out
                    # else:
                        # folium.PolyLine(sub_array, color="3").add_to(m) #rmbr to push the color out
                # prevcolor = color used


    # Initialization of the map
    data = io.BytesIO()             # creates a temporary 'container' for html code
    m.save(data, close_file=False)  # folium html code is saved inside data variable
    w = QtWebEngineWidgets.QWebEngineView()     # then the rest of the code is the map running
    w.setHtml(data.getvalue().decode())
    w.resize(840, 680)
    w.show()
    sys.exit(app.exec_())

import folium
import io
import sys
import main_graph as m_graph
import bus_adj as bus_graph
import lrt_adj as lrt_graph
from PyQt5 import QtWidgets, QtWebEngineWidgets


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
    start = ""
    end = ""
    mode = ""
    user_input = ""
    print("Welcome to Punggol Pathfinder")
    print("Valid inputs are: Postal codes, bus stop numbers, train station names, train station codes.")
    print("Where are you coming from?")
    print("INPUT HERE")
    print("Where is your destination?")
    print("INPUT HERE")
    print("Path is " + "START " + "to " + "END" + ". Correct? Y/N")
    print("INPUT HERE")
    print("Select mode of transport: LRT (L), Bus (B), Walk (W), or Mixed (M)?")
    print("INPUT HERE")

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

import folium
import io
import sys
from PyQt5 import QtWidgets, QtWebEngineWidgets


def create_edges_json(array):
    # This function creates a .json file to draw edges between nodes.
    # The array it receives should be in the format -> [[lat,long],...,[lat,long]]
    f = open("overlay.json", "w")   # 'w' will overwrite any existing content
    list_to_str = ', '.join([str(elem) for elem in array]) # join elements of array with comma
    f.write("{\"type\": \"FeatureCollection\", \"features\": [ { \"type\": \"Feature\", \"properties\": {}, "
            "\"geometry\": { \"type\": \"LineString\", \"coordinates\": [")
    f.write(list_to_str)
    f.write("]}}]}")
    f.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Create map object, set default location, map theme & zoom
    m = folium.Map(location=[1.4046357, 103.9090000], tiles="Stamen Terrain", zoom_start=14.5)
    # Global tooltip, hover info
    tooltip = 'Click For More Info'

    # Static Array, pending data of routes
    testArray = [[103.899582, 1.405146], [103.904666, 1.414444]]
    create_edges_json(testArray)            # calls function to create json file based on coordinates given
    for i in range(0, len(testArray)):      # creates markers on map based on coordinates given
        # Set coordinates location, popup information, tooltip color etc
        folium.Marker([testArray[i][1], testArray[i][0]],   # function works in reverse order of [long,lat]
                      popup=i, tooltip=tooltip).add_to(m)

    # GeoJson overlay
    folium.GeoJson('overlay.json', name='Punggol').add_to(m)   # line plotting

    # Initialization of the map
    data = io.BytesIO()
    m.save(data, close_file=False)
    w = QtWebEngineWidgets.QWebEngineView()
    w.setHtml(data.getvalue().decode())
    w.resize(840, 680)
    w.show()
    sys.exit(app.exec_())

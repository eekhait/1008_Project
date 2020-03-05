import folium
import os
import json
import io
import sys
from PyQt5 import QtWidgets, QtWebEngineWidgets

def setCoordinates(array):
    f = open("overlay.json", "w") 
    listToStr = ', '.join([str(elem) for elem in array]) #join elements of array with comma
    f.write("{\"type\": \"FeatureCollection\", \"features\": [ { \"type\": \"Feature\", \"properties\": {}, \"geometry\": { \"type\": \"LineString\", \"coordinates\": [")
    f.write(listToStr)
    f.write("]}}]}")
    f.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    data = io.BytesIO()
    
    # Create map object, set default location, map theme & zoom
    m = folium.Map(location=[1.4046357,103.9090000],tiles="Stamen Toner", zoom_start=14.5)

    # Global tooltip, hover info
    tooltip = 'Click For More Info'

    # Add coordinates to json file
    # Static Array, pending data of routes
    array = [[103.899582, 1.405146],[103.904666, 1.414444],[103.907902, 1.402316],[103.918416, 1.403702],[103.913274, 1.394577]]
    # Call function and append new route data
    setCoordinates(array)

    # Location Data from json
    overlay = os.path.join('data', 'overlay.json')

    # Loop to repackage from [lat, long] to [long, lat]
    for i in range(0, len(array)):  
        # Set coordinates location, popup information, tooltip color etc
        folium.Marker([array[i][1],array[i][0]],
                popup= i,
                tooltip=tooltip).add_to(m)

    # Geojson overlay
    folium.GeoJson(overlay, name='Punggol').add_to(m)   # line plotting

    m.save(data, close_file=False)

    w = QtWebEngineWidgets.QWebEngineView()
    w.setHtml(data.getvalue().decode())
    w.resize(840, 680)
    w.show()
    sys.exit(app.exec_())

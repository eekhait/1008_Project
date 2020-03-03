import folium
import os
import json
import io
import sys
from PyQt5 import QtWidgets, QtWebEngineWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    data = io.BytesIO()
    
    # Create map object, set default location, map theme & zoom
    m = folium.Map(location=[1.4046357,103.9090000],tiles="Stamen Toner", zoom_start=14.5)

    # Global tooltip, hover info
    tooltip = 'Click For More Info'

    # Location Data from json
    overlay = os.path.join('data', 'overlay.json')

    # Static Array, pending data of routes
    array = [[103.899582, 1.405146],[103.904666, 1.414444],[103.907902, 1.402316],[103.918416, 1.403702],[103.913274, 1.394577]]   

    # Loop to repackage from [lat, long] to [long, lat]
    for i in range(0, len(array)):    
        markerCoordinates = []
        markerCoordinates.append(array[i][1])   
        markerCoordinates.append(array[i][0])

        # Set coordinates location, popup informations, tooltip color etc
        folium.Marker(markerCoordinates,
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

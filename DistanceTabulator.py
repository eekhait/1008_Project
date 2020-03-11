import pandas as pd
from geopy.distance import geodesic

# Take note:
# Latitude is vertical (How 'north-south' a place is)
# Longitude is horizontal (How 'east-west' a place is)
distance_table = pd.read_csv("Punggol Coordinates.csv", header=None)

# to mimic cell selection in pandas dataframe, for iteration
# iloc[horizontal, vertical]
# iloc[1123, 1119]  <--- most bottom right value
# 0,0           0,1     0,2         0,3         0,4...
# postal_code   Street  Latitude    Longitude   820136...

# FOR EVERY ROW... (Skips header row)
for i in range(1, 1191):  # 1191
    # FOR EVERY COLUMN... (Skips first 4 already-populated columns)
    nearbyNodes = []
    for j in range(6, 1196):
        # Assign distance between nodes in meters
        distance = 1000 * round(geodesic((distance_table.iloc[i, 2], distance_table.iloc[i, 3]),
                                         (distance_table.iloc[j-5, 2], distance_table.iloc[j-5, 3])).km, 3)
        distance_table.iloc[i, j] = distance
        if 0 < distance < 180:
            nearbyNodes.append(str(distance_table.iloc[j-5, 0]))
    distance_table.iloc[i, 5] = str(nearbyNodes)
    # Prints progress of population per row
    print(round(i / 1191 * 100, 2))

# Create new csv
distance_table.to_csv('Complete_Punggol_Graph.csv', header=False, index=False)

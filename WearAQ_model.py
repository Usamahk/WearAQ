import pandas as pd
import numpy as np
from pyKriging import kriging

from scipy.spatial import KDTree

# =============================================================================
# Locations
# =============================================================================

# Read in locations - for this example using data from workshop 1. Can find data
# in the 'data' folder

w_airbeam = pd.read_csv("WearAQ_workshop_1.xlsx - PM10.csv")
w_airbeam = w_airbeam.drop(['Timestamp'], axis = 1)

# Initialize workshop locations - in this example, here are the locations for
# workshop 1

locations = np.array([[-0.004744, 51.509824],
                      [-0.003672, 51.510358],
                      [-0.002685, 51.511079],
                      [-0.003586, 51.511400],
                      [-0.004272, 51.510899],
                      [-0.005056, 51.510445]])

# Find closest readings  to locations

coords = np.array([w_airbeam['geo:lat'],w_airbeam['geo:long']]).T # Extract Lon/lat in array

tree = KDTree(coords) # set up k-d tree
num_readings = 1 # set number of readings to take

nearest_neighbour = np.empty((0,3), int)

for i in range(len(locations)):
    idx = tree.query_ball_point([locations[i,0], locations[i,1]],r=0.0003)
    temp = w_airbeam.iloc[idx]
    temp = np.array(temp.tail(num_readings))
    
    nearest_neighbour = np.append(nearest_neighbour, temp, axis = 0).astype(None)

# Compile in array

closest = pd.DataFrame(nearest_neighbour)
closest = closest.rename(columns = {0:'lat',1:'lon', 2:'Value'})

X = np.array([closest['lat'],closest['lon']]).T
y = np.array(closest['Value'])

# clean by adding an offset point to artificially create a stronger pull

offset_lon1 = -0.000003
offset_lat1 = -0.000001

for i in range(len(X)):
    lon1 = X[i,0] + offset_lon1
    lat1 = X[i,1] + offset_lat1
    loc1 = np.array([lon1,lat1])
    
    X = np.append(X,[loc1], axis=0)
    y = np.append(y,[y[i]])
   
# Run through kriging model

optimizer = 'ga'

print('Setting up the Kriging Model')
k = kriging(X, y)

k.train(optimizer = optimizer)

new_loc = []

# infill points to improve models accuracy

for i in range(3):
    newpoints = k.infill(1, method='error')
    for point in newpoints:
        print('Adding point {}'.format(point))
        k.addPoint(point, y[0])
    k.train(optimizer=optimizer)
    new_loc.append({'lon':point[0],'lat':point[1]})

new_loc = pd.DataFrame(new_loc)


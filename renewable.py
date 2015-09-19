# -*- coding: utf-8 -*-
# Sean Tully - 19 Sept 2015
# Tested on archlinux x86_64 with python 2.7.10, sqlite 3.8.11, numpy 1.9.2

import sqlite3      # sqlite3 required to import data from database file
import numpy as np  # numpy required for array structure, maths functions

# Read data from renewable.db file and save into a numpy array
# Assumption: Data is in the form lat° N, long° W
conn = sqlite3.connect('renewable.db')
locs = np.array(conn.execute('SELECT * FROM location').fetchall())
ports = np.array(conn.execute('SELECT * FROM ports').fetchall())
conn.close()

# Function to find central angle between two points on the surface of a sphere
# coord1, coord2 are of the form [latitude, longitude, (ignored data)]
def getCentralAngle(coord1, coord2):
    phi1 = coord1[0] * np.pi / 180.0  # latitude0 in radians
    phi2 = coord2[0] * np.pi / 180.0  # latitude1 in radians
    dphi = phi2 - phi1                # latitude difference, in radians
    dtheta = (coord2[1] - coord1[1]) * np.pi / 180.0  # longitude diff, radians
    a = (np.sin(dphi/2))**2 + np.cos(phi1)*np.cos(phi2)*(np.sin(dtheta/2))**2
    return 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

# Get arrays of location-location and location-port angles
locLocAngle = np.array([[getCentralAngle(i,j) for j in locs] for i in locs])
locPortAngle = np.array([[getCentralAngle(i,j) for j in ports] for i in locs])

# Evaluate costs and identify minimum
# rawcosts is a 1D array with a value for each location
# finishedcosts is a 2D array for each location x port combination
# totalcosts is a 2D array for each location x port combination
rawcosts = np.sum(locLocAngle * locs[:,2], axis=1)    # sum of (angle x tonnage)
finishedcosts = np.sum(locs[:,2]) * locPortAngle      # (sum of tonnage) x angle
totalcosts = rawcosts[:, np.newaxis] + finishedcosts  # total = raw + finished
# Get index of the location-port combination corresponding to minimum cost
optimum = np.unravel_index(totalcosts.argmin(), totalcosts.shape)
print 'Optimum Locations:'
print 'Plant:\t%.2f° N, %.2f° W' % (locs[optimum[0]][0], locs[optimum[0]][1])
print 'Port:\t%.2f° N, %.2f° W' % (ports[optimum[1]][0], ports[optimum[1]][1])

# Test getCentralAngle function:
# Distance from London to New York should be approx 5570 km
#earthMeanRadius = 6371 # km
#london = np.array([51.5072,0.1275])
#newyork = np.array([40.7127,74.0059])
#testdist = earthMeanRadius * getCentralAngle(london,newyork)
#print testdist

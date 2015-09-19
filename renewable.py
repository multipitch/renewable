# -*- coding: utf-8 -*-
"""    Copyright (C) 2015  Sean Tully

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
# Tested on archlinux x86_64 with python 2.7.10, sqlite 3.8.11, numpy 1.9.2

import sqlite3
import numpy as np

# Read data from renewable.db file and save into a numpy array
# Assumption: Data is in the form lat° N, long° W
conn = sqlite3.connect('renewable.db')
locs = np.array(conn.execute('SELECT * FROM location').fetchall())
ports = np.array(conn.execute('SELECT * FROM ports').fetchall())
conn.close()

def central_angle(coord1, coord2):
    """Get central angle between two points on the surface of a sphere
    
    Keyword arguments:
    coord1 (numpy.array): first two columns are lat, long in degrees
    coord2 (numpy.array): first two columns are lat, long in degrees
           
    Returns:
    float: central angle in radians
    """
    phi1 = coord1[0] * np.pi / 180.0  # lat1 in radians
    phi2 = coord2[0] * np.pi / 180.0  # lat2 in radians
    dphi = phi2 - phi1                # lat difference, in radians
    dtheta = (coord2[1] - coord1[1]) * np.pi / 180.0  # long diff, in radians
    a = (np.sin(dphi / 2)) ** 2 + \
        np.cos(phi1) * np.cos(phi2) * (np.sin(dtheta / 2)) ** 2
    return 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

# Get arrays of location-location and location-port angles
loc_loc_angle = np.array([[central_angle(i, j) for j in locs] for i in locs])
loc_port_angle = np.array([[central_angle(i, j) for j in ports] for i in locs])

# Evaluate costs and identify minimum
# rawcosts is a 1D array with a value for each location
# finishedcosts is a 2D array with a value for each location x port combination
# totalcosts is a 2D array with a value for each location x port combination
raw_costs = np.sum(loc_loc_angle * locs[:, 2], axis=1)
finished_costs = np.sum(locs[:, 2]) * loc_port_angle
total_costs = raw_costs[:, np.newaxis] + finished_costs

# Get index of the location-port combination corresponding to minimum cost
optimum = np.unravel_index(total_costs.argmin(), total_costs.shape)
print 'Optimum Locations:'
print 'Plant:\t%.2f° N, %.2f° W' % (locs[optimum[0]][0], locs[optimum[0]][1])
print 'Port:\t%.2f° N, %.2f° W' % (ports[optimum[1]][0], ports[optimum[1]][1])

# Test getCentralAngle function:
# Distance from London to New York should be approx 5570 km
#earth_mean_radius = 6371 # km
#london = np.array([51.5072, 0.1275])
#new_york = np.array([40.7127, 74.0059])
#test_dist = earth_mean_radius * central_angle(london, new_york)
#print test_dist

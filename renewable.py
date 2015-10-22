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

def central_angle(coords1, coords2):
    """Get central angle between two points on the surface of a sphere
    
    Keyword arguments:
    coords1 (numpy.array): two columns are lat, long in radians
    coords2 (numpy.array): two columns are lat, long in radians
           
    Returns:
    numpy.array: central angles in radians
    """
    dphi = coords2[:, 0] - coords1[:,0][:, np.newaxis]
    dtheta = coords2[:, 1] - coords1[:, 1][:, np.newaxis]
    a = (np.sin(dphi / 2)) ** 2 + \
        np.cos(coords1[:,0][:, np.newaxis]) * np.cos(coords2[:,0]) * \
        (np.sin(dtheta / 2)) ** 2
    return  2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

locs_r = locs[:, :2] * np.pi / 180.0
ports_r = ports * np.pi / 180.0
loc_loc_angle = central_angle(locs_r, locs_r)
loc_port_angle = central_angle(locs_r, ports_r)

# Evaluate costs
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

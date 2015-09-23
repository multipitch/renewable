# renewable
Finds the optimum location for a renewables plant and port based on raw material locations and quantities

####Goal:
The goal is to write a script in Python to work out the optimum locations for a processing plant and port.  
The processing plant must be at one of a number of raw materials locations.  
The tonnage of raw materials produced at each location is given, and latitude and longitude coordinates are given for all locations and ports.  
The optimum locations are those resulting in minimum transportation costs.

####Method:
1. Read data tables from the renewable.db file into numpy arrays.
2. Define a function that can return the central angle between two points on a sphere.  This is based on an equation from Sinnott (1984).
3. Create numpy arrays of all location-location angles and location-port angles.  Note that distances can be found by multiplying angle (in radians) x radius, but this is not necessary for a relative comparison, so no value need be assumed for the mean radius of the Earth.
4. Evaluate costs for transporting raw materials to each possible location.
   * Multiply the array of location-location angles by the tonnage column of the locations array.
   * For each candidate location, sum the costs of transporing from each location to the candidate.

5. Evaluate costs for transporting finished materials from each possible location to each possible port.
  a) Find the total tonnage produced at all locations by summing the tonnage column of the locations array.
  b) Multiply the array of location-port angles by the total tonnage.
6. Obtain an array of total costs for each combination of possible locations and ports, by adding array of raw material costs to the array of finished materials costs.
7. Find the minimum cost in the total costs array and find the coordinates of the corresponding location and port.
8. Print the optimum location and port in a human-readable format.

####Solution:
> Optimum Locations:
> Plant:	53.22° N, 6.68° W
> Port:	53.33° N, 6.25° W`

####Assumptions:
The database appears to have the headings on latitude and longitude mixed up.  
It is assumed that the first column in each table is latitude, in degrees North and the second column in each table is longitude, in degrees West.  
As a result, all coordinates refer to locations in Ireland.
The earth is assumed to be spherical.  
All routes are assumed to be geodesic i.e. "as the crow flies".
It is assumed that the tonnage of finished material is equal to the sum of the tonnage of raw materials.
It is assumed that the cost of transporting a given tonnage of any material is the same on any route and for any material.
Transportation costs from the port onwards are not considered as the locations of onward destinations are unknown.

####References:
Sinnott, R. W. (1984) _Virtues of the Haversine._ Sky and Telescope, 68(2), p. 159.

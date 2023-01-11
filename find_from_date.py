# and calculates position of satellite
# in the sky

import ephem
import datetime as dt
import numpy as np
from fastkml import kml
from shapely.geometry import Point, LineString, Polygon

positions = []

# load tle
tle = open('tle.txt', 'r')
tle_lines = tle.readlines()
tle.close()

# create satellite object
satellite = ephem.readtle(tle_lines[0], tle_lines[1], tle_lines[2])

t = dt.datetime(2023, 1, 4, 9, 48, 30)

satellite.compute(t)
positions.append((satellite.sublong / ephem.degree,
                  satellite.sublat / ephem.degree, satellite.elevation))
#print(satellite.elevation)

#print(positions)
"""
k = kml.KML()
ns = '{http://www.opengis.net/kml/2.2}'
p = kml.Placemark(ns, 'Sattrack', 'Test', '1000 Minute Track')
p.geometry = LineString(positions)  #, tesselate=1,altitudemode="absolute")
k.append(p)

with open("test.kml", 'w') as kmlfile:
  kmlfile.write(k.to_string())
""" #Only for testing and cool vis :)

satellite_obs = ephem.Observer()  #hacky
counter = 0
pass_now = False
for i in positions:
  #print(len(positions))
  satellite_obs.lon = i[0]
  satellite_obs.lat = i[1]
  satellite_obs.elevation = i[2]
  satellite_obs.date = t
  m = ephem.Moon()
  m.compute(satellite_obs)
  if m.alt > 0:
    print("Moon was above the horizon.")

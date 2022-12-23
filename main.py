# and calculates position of satellite
# in the sky

import ephem
import datetime as dt
import numpy as np
from fastkml import kml
from shapely.geometry import Point, LineString, Polygon

# load tle
tle = open('tle.txt', 'r')
tle_lines = tle.readlines()
tle.close()

# create satellite object
satellite = ephem.readtle(tle_lines[0], tle_lines[1], tle_lines[2])

start_dt = dt.datetime.today()
intervall = dt.timedelta(minutes=1)

timelist = []
for i in range(1000):
  timelist.append(start_dt + i * intervall)

positions = []
for t in timelist:
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
  satellite_obs.lon = i[0]
  satellite_obs.lat = i[1]
  satellite_obs.elevation = i[2]
  satellite_obs.date = timelist[counter]
  m = ephem.Moon()
  m.compute(satellite_obs)
  if m.alt > 0 and pass_now == False:
    print("NEW PASS:")
    print("START TIME: " + str(timelist[counter]))
    print("EL AT START" + str((m.alt / ephem.degree)))
    print("AZ AT START" + str((m.az / ephem.degree)))
    pass_now = True
  if m.alt < 0 and pass_now == True:
    print("END OF PASS:")
    print("END TIME: " + str(timelist[counter]))
    print("EL AT END" + str((m.alt / ephem.degree)))
    print("AZ AT END" + str((m.az / ephem.degree)))
    pass_now = False
  counter = counter + 1

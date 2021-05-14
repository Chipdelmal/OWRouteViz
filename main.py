

import numpy as np
import pytz as pytz
from os import path
import functions as fun
import xmltodict as xtd
import cartopy.crs as ccrs
from datetime import datetime
import matplotlib.pyplot as plt
from collections import OrderedDict
from cartopy.io.img_tiles import OSM
import cartopy.io.img_tiles as cimgt

# https://scitools.org.uk/cartopy/docs/latest/matplotlib/intro.html

###############################################################################
# Constants
###############################################################################

###############################################################################
# Inputs
###############################################################################
PATH = '/home/chipdelmal/Documents/OneWheel'
fName = '2021_05_13_02.tcx'

###############################################################################
# Read XML
###############################################################################
fPath = path.join(PATH, fName)
doc = fun.readTCX(fPath)
doc.keys()

###############################################################################
# Get Laps and segments
###############################################################################
lap = doc['TrainingCenterDatabase']['Activities']['Activity']['Lap']
track = lap['Track']['Trackpoint']
route = fun.getRoute(track)
meanRoute = fun.getRouteStat(route)

###############################################################################
# Iterate segments
#   Speed seems to be (m/s)
###############################################################################
pad = 0.01

# imagery = OSM()
imagery = cimgt.GoogleTiles()
fig = plt.figure(figsize=(12, 12))
ax = plt.axes(projection=ccrs.PlateCarree())
# ax.stock_img()
ax.add_image(imagery, 14)
ptsNum = len(track)
for tix in range(0, ptsNum-1):
    (sS, sE) = [route[i] for i in (tix, tix+1)]
    plt.plot(
        [sS['lon'], sE['lon']], 
        [sS['lat'], sE['lat']],
        color='#3a0ca3FF', linewidth=2,
        # marker='.', markersize=1,
        transform=ccrs.Geodetic()
    )
(cLat, cLon) = (meanRoute['lat'], meanRoute['lon'])
ax.set_extent(
    [cLon-pad, cLon+pad, cLat-pad, cLat+pad], 
    crs=ccrs.PlateCarree()
)


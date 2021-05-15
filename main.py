

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
import matplotlib.cm as cm
from matplotlib.colors import Normalize

# https://scitools.org.uk/cartopy/docs/latest/matplotlib/intro.html

###############################################################################
# Constants
###############################################################################
cmap = cm.Purples_r
norm = Normalize(vmin=0, vmax=8)
imagery = None # cimgt.GoogleTiles() imagery = OSM()

###############################################################################
# Inputs
###############################################################################
PATH = '/home/chipdelmal/Documents/OneWheel'
fName = '2021_05_15-01'

###############################################################################
# Read XML
###############################################################################
fPath = path.join(PATH, fName+'.tcx')
doc = fun.readTCX(fPath)
doc.keys()

###############################################################################
# Get Laps and segments
###############################################################################
lap = doc['TrainingCenterDatabase']['Activities']['Activity']['Lap']
track = lap['Track']['Trackpoint']
route = fun.getRoute(track)
meanRoute = fun.getRouteStat(route, fStat=np.median)
ptsNum = len(track)

###############################################################################
# Iterate segments
#   Speed seems to be (m/s)
###############################################################################
POINTS = False
pad = 0.0125
# (cLat, cLon) = (meanRoute['lat'], meanRoute['lon'])
(cLat, cLon) = (37.877928, -122.292065)



pth = path.join(PATH, 'img', "2021_05_13_01-final.png")
xy = fun.getRouteArray(route).T
# Generate figure -------------------------------------------------------------
(fig, ax) = (
    plt.figure(figsize=(6, 6)),
    plt.axes(projection=ccrs.PlateCarree())
)
ax.set_extent(
    [cLon-pad, cLon+pad, cLat-pad, cLat+pad], 
    crs=ccrs.PlateCarree()
)
# Add imagery if available ----------------------------------------------------
if imagery is not None:
    ax.add_image(imagery, 14)
else:
    ax.set_facecolor("black")
# Add previously generated map ------------------------------------------------
if preMap is not None:
    ax.imshow(
        plt.imread(pth), 
        extent=[cLon-pad, cLon+pad, cLat-pad, cLat+pad]
    )
# Loop over segments of the track ---------------------------------------------
for tix in range(0, ptsNum-1):
    (sS, sE) = [route[i] for i in (tix, tix+1)]
    plt.plot(
        [sS['lon'], sE['lon']], 
        [sS['lat'], sE['lat']],
        color=cmap(norm(sE['speed'])),
        alpha=.8,
        linewidth=1, solid_capstyle='round',
        # marker='o', markersize=1,
        transform=ccrs.Geodetic()
    )
    tixPad = str(tix).zfill(4)
    fimgName = path.join(PATH, 'img', '{}-{}.png'.format(fName, tixPad))
    fig.savefig(fimgName, dpi=250, bbox_inches='tight', pad_inches=0)
plt.cla() 
plt.clf() 
plt.close(fig)
plt.gcf()
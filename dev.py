import sys
import numpy as np
import pytz as pytz
from os import path
from glob import glob
import functions as fun
import constants as cst
import xmltodict as xtd
import cartopy.crs as ccrs
from datetime import datetime
import matplotlib.pyplot as plt
from collections import OrderedDict
from cartopy.io.img_tiles import OSM
import cartopy.io.img_tiles as cimgt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import matplotlib.patches as patches

###############################################################################
# Constants
###############################################################################
(CMAP, SPEED_NORM) = (
    cst.CMAP_W, Normalize(vmin=0, vmax=6.5)
)
(PAD, FIG_SIZE) = (0.005, (12, 12))
IMAGERY = cimgt.GoogleTiles() # None 
PRE_MAP = None
PROJ = ccrs.PlateCarree()
POINTS = False
WSIZE = 25
###############################################################################
# Inputs
###############################################################################
PATH = '/home/chipdelmal/Documents/OneWheel'
fPaths = sorted(glob(path.join(PATH, '*.tcx')))
fNames = [path.split(i)[-1].split('.')[0] for i in fPaths]
imgFgPth = path.join(PATH, 'img', "2021_05_13_01-final.png")
###############################################################################
# Get BBox
###############################################################################
bbox = fun.getBBoxFromFiles(fPaths)
extent = [
    bbox['lon'][0]-PAD, bbox['lon'][1]+PAD, 
    bbox['lat'][0]-PAD, bbox['lat'][1]+PAD
]
###############################################################################
# Generate Figure
###############################################################################
tFrames = 0
(fNum, fName) = (0, fNames[0])
###############################################################################
# Get Laps and segments
###############################################################################
routes = []
for fName in fNames:
    file = path.join(PATH, '{}.tcx'.format(fName))
    route = fun.getRouteFromFile(file)
    route = fun.movingAverageRoute(route, wSize=WSIZE)
    meanRoute = fun.getRouteStat(route, fStat=np.median)
    ptsNum = len(route)
    routes.append(route)
###############################################################################
# Iterate segments
###############################################################################
(fig, ax) = (plt.figure(figsize=FIG_SIZE), plt.axes(projection=PROJ))
ax.set_extent(extent, crs=PROJ)
# Add imagery if available ----------------------------------------------------
if IMAGERY is not None:
    ax.add_image(IMAGERY, 14)
ax.add_patch(
    patches.Rectangle(
        (extent[0], extent[2]), (extent[1]-extent[0]), (extent[3]-extent[2]),
        edgecolor=None, facecolor='#000000DD',
        fill=True
    )
)
for route in routes:
    plt.plot(
        [i['lon'] for i in route], 
        [i['lat'] for i in route],
        color='#1F75FE', # CMAP(SPEED_NORM(sE['speed'])),
        alpha=.2, # min(2*CMAP(SPEED_NORM(sE['speed']))[-1], 1),
        linewidth=2.5, 
        solid_capstyle='round',
        transform=ccrs.Geodetic()
    )
    # plt.plot(
    #     [i['lon'] for i in route], 
    #     [i['lat'] for i in route],
    #     color='#ffffff', # CMAP(SPEED_NORM(sE['speed'])),
    #     alpha=.75, # min(2*CMAP(SPEED_NORM(sE['speed']))[-1], 1),
    #     linewidth=.5, 
    #     solid_capstyle='round',
    #     transform=ccrs.Geodetic()
    # )
ax.set_extent(extent, crs=ccrs.PlateCarree())
fig.savefig(imgFgPth, dpi=500, bbox_inches='tight', pad_inches=0)
# Clearing and closing (fig, ax) ----------------------------------------------
# plt.clf()
# plt.cla() 
# plt.close(fig)
# plt.gcf()



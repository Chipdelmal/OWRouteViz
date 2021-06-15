import sys
import osmnx as ox
import numpy as np
import networkx as nx
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
ox.config(log_console=True, use_cache=True)


(AUTO_BOX, WSIZE) = (False, 50)
(OSMNX, IMAGERY) = (True, None) # cimgt.GoogleTiles() # None 
###############################################################################
# Constants
###############################################################################
(CMAP, SPEED_NORM) = (
    cst.CMAP_W, Normalize(vmin=0, vmax=6.5)
)
if AUTO_BOX:
    (PAD, FIG_SIZE) = (0.005, (12, 12))
else:
    (PAD, FIG_SIZE) = (0.04, (12, 12))
PROJ = ccrs.PlateCarree()
###############################################################################
# Inputs
###############################################################################
PATH = '/home/chipdelmal/Documents/OneWheel'
fPaths = sorted(glob(path.join(PATH, '*.tcx')))
fNames = [path.split(i)[-1].split('.')[0] for i in fPaths]
imgFgPth = path.join(PATH, 'img', "FullRoutes.png")
###############################################################################
# Get BBox
###############################################################################
bbox = fun.getBBoxFromFiles(fPaths)
extent = [
    bbox['lon'][0]-PAD, bbox['lon'][1]+PAD, 
    bbox['lat'][0]-PAD, bbox['lat'][1]+PAD
]
if not AUTO_BOX:
    centroid = [
        np.mean([bbox['lon'][1], bbox['lon'][0]]),
        np.mean([bbox['lat'][1], bbox['lat'][0]])
    ]
    extent = []
    extent.append(centroid[0]-PAD*1.275)
    extent.append(centroid[0]+PAD*1.275)
    extent.append(centroid[1]-PAD)
    extent.append(centroid[1]+PAD)
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
# Create figure
###############################################################################
(fig, ax) = (plt.figure(figsize=FIG_SIZE), plt.axes(projection=PROJ))
# Add imagery if available ----------------------------------------------------
if IMAGERY is not None:
    ax.add_image(IMAGERY, 14)
# Get graph object ------------------------------------------------------------
if OSMNX:
    G = ox.graph.graph_from_bbox(
        extent[2], extent[3],  extent[0], extent[1], 
        retain_all=True, simplify=False, network_type='drive',
        truncate_by_edge=False
    )
# Add black background --------------------------------------------------------
ax.add_patch(
    patches.Rectangle(
        (extent[0], extent[2]), (extent[1]-extent[0]), (extent[3]-extent[2]),
        edgecolor=None, facecolor='#000000',
        fill=True, zorder=-3
    )
)
# Plot routes -----------------------------------------------------------------
for route in routes:
    plt.plot(
        [i['lon'] for i in route], 
        [i['lat'] for i in route],
        color='#ffffff',
        alpha=.35, linewidth=.75,
        solid_capstyle='round',
        transform=ccrs.Geodetic()
    )
ox.plot_graph(
    G, ax=ax, show=True, close=False,
    edge_color='#1F75FE25', edge_linewidth=.75,
    node_size=0
)
ax.set_extent(extent, crs=PROJ)
fig.savefig(imgFgPth, dpi=500, bbox_inches='tight', pad_inches=0)
# Clearing and closing (fig, ax) ----------------------------------------------
plt.close(fig)

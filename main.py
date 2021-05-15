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

###############################################################################
# Constants
###############################################################################
(CMAP, SPEED_NORM) = (
    cm.Purples_r,
    Normalize(vmin=0, vmax=8)
)
PAD = 0.005
IMAGERY = None 
PRE_MAP = None
FIG_SIZE = (6, 6)
PROJ = ccrs.PlateCarree()

###############################################################################
# Inputs
###############################################################################
PATH = '/home/chipdelmal/Documents/OneWheel'
fNames = [
    '2021_05_13-01', '2021_05_13-02', 
    '2021_05_15-01', '2021_05_15-02'
]
imgFgPth = path.join(PATH, 'img', "2021_05_13_01-final.png")

###############################################################################
# Get BBox
###############################################################################
fPaths = [path.join(PATH, '{}.tcx'.format(fName)) for fName in fNames]
bbox = fun.getBBoxFromFiles(fPaths)

###############################################################################
# Get Laps and segments
###############################################################################
fName = fNames[1]
file = path.join(PATH, '{}.tcx'.format(fName))
route = fun.getRouteFromFile(file)
meanRoute = fun.getRouteStat(route, fStat=np.median)
ptsNum = len(route)


###############################################################################
# Iterate segments
#   Speed seems to be (m/s)
###############################################################################
(cLat, cLon) = (37.877928, -122.292065)
extent = [
    bbox['lon'][0]-PAD, bbox['lon'][1]+PAD, 
    bbox['lat'][0]-PAD, bbox['lat'][1]+PAD
]
# Generate figure -------------------------------------------------------------
(fig, ax) = (plt.figure(figsize=FIG_SIZE), plt.axes(projection=PROJ))
ax.set_extent(extent, crs=PROJ)
# Add imagery if available ----------------------------------------------------
if IMAGERY is not None:
    ax.add_image(imagery, 14)
else:
    ax.set_facecolor("black")
# Add previously generated map ------------------------------------------------
if PRE_MAP is not None:
    imgFg = plt.imread(imgFgPth)
    ax.imshow(imgFg, extent=extent)
# Loop over segments of the track ---------------------------------------------
for tix in range(0, ptsNum-1):
    (sS, sE) = [route[i] for i in (tix, tix+1)]
    plt.plot(
        [sS['lon'], sE['lon']], 
        [sS['lat'], sE['lat']],
        color=CMAP(SPEED_NORM(sE['speed'])),
        alpha=.75, linewidth=1, 
        solid_capstyle='round',
        transform=ccrs.Geodetic()
    )
    tixPad = str(tix).zfill(4)
    fimgName = path.join(PATH, 'img', '{}-{}.png'.format(fName, tixPad))
    fig.savefig(fimgName, dpi=250, bbox_inches='tight', pad_inches=0)
# Export final frame in transparent mode --------------------------------------
fimgName = path.join(PATH, 'img', '{}-{}.png'.format(fName, 'final'))
fig.savefig(
    fimgName, dpi=250, bbox_inches='tight', 
    pad_inches=0, transparent=True
)
# Clearing and closing (fig, ax) ----------------------------------------------
plt.cla() 
plt.clf() 
plt.close(fig)
plt.gcf()
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
    cm.OrRd_r, # cst.CMAP_W, # 
    Normalize(vmin=0, vmax=6.5)
)
(FRATE, PRATE) = (5, 1)
(PAD, FIG_SIZE) = (0.005, (8, 8))
IMAGERY = cimgt.GoogleTiles() # None 
PRE_MAP = None
PROJ = ccrs.PlateCarree()
(TRACE, POINTS) = (True, False)
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
(fig, ax) = (plt.figure(figsize=FIG_SIZE), plt.axes(projection=PROJ))
ax.set_extent(extent, crs=PROJ)
# Add previously generated map ------------------------------------------------
if PRE_MAP is not None:
    imgFg = plt.imread(fimgName)
    ax.imshow(imgFg, extent=extent)
# Add imagery if available ----------------------------------------------------
if IMAGERY is not None:
    ax.add_image(IMAGERY, 14)
    ax.add_patch(
        patches.Rectangle(
            (extent[0], extent[2]),
            (extent[1]-extent[0]), (extent[3]-extent[2]),
            edgecolor=None, facecolor='#000000E0',
            fill=True
        )
    )
else:
    ax.set_facecolor("#000000")
plt.gcf().set_facecolor('black')
# Iterate through frames ------------------------------------------------------
tFrames = 0
(fNum, fName) = (0, fNames[0])
for (fNum, fName) in enumerate(fNames):
    ###########################################################################
    # Get Laps and segments
    ###########################################################################
    file = path.join(PATH, '{}.tcx'.format(fName))
    route = fun.getRouteFromFile(file)
    route = fun.movingAverageRoute(route, wSize=WSIZE)
    meanRoute = fun.getRouteStat(route, fStat=np.median)
    ptsNum = len(route)
    ###########################################################################
    # Iterate segments
    #   Speed seems to be (m/s)
    ###########################################################################
    # Loop over segments of the track -----------------------------------------
    pString = '* Progress ({}/{}): {}/{}'
    for tix in range(0, ptsNum-1):
        print(pString.format(fNum+1, len(fNames), tix+1, ptsNum), end='\r')
        if (tix%FRATE==0) and (tix<ptsNum-FRATE):
            (sS, sE) = [route[i] for i in (tix, tix+FRATE)]
            # Render new elements ---------------------------------------------
            if TRACE:
                plt.plot(
                    [sS['lon'], sE['lon']], 
                    [sS['lat'], sE['lat']],
                    color='#1F75FE', # CMAP(SPEED_NORM(sE['speed'])),
                    alpha=.125, # min(2*CMAP(SPEED_NORM(sE['speed']))[-1], 1),
                    linewidth=2.5, 
                    solid_capstyle='round',
                    solid_joinstyle='round',
                    transform=ccrs.Geodetic()
                )
            # Plot markers ----------------------------------------------------
            if (POINTS) and (tix%PRATE==0) and (tix<ptsNum-PRATE):
                plt.plot(
                    sS['lon'], sS['lat'],
                    color='#1F75FE', # CMAP(SPEED_NORM(sE['speed'])), 
                    alpha=.25, # min(1.25*CMAP(SPEED_NORM(sE['speed']))[-1], 1),
                    marker='o', markersize=2.5,
                    markeredgewidth=.1, markeredgecolor='black',
                    linewidth=0,
                    transform=ccrs.Geodetic()
                )
            # Filename and export ---------------------------------------------
            ax.set_extent(extent, crs=ccrs.PlateCarree())
            tixPad = str(tFrames).zfill(8)
            fimgName = path.join(PATH, 'img', '{}.png'.format(tixPad))
            fig.savefig(fimgName, dpi=200, bbox_inches='tight', pad_inches=0)
            # Update frames counter -------------------------------------------
            tFrames = tFrames+1
    sys.stdout.write("\033[K")
# Clearing and closing (fig, ax) ----------------------------------------------
plt.clf()
plt.cla() 
plt.close(fig)
plt.gcf()



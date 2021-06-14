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
from collections import OrderedDict
import warnings
warnings.filterwarnings("ignore")
ox.config(log_console=True, use_cache=True)

###############################################################################
# Constants
###############################################################################
WSIZE = 25
(PAD, FIG_SIZE) = (0.005, (12, 12))
(CMAP, SPEED_NORM) = (cst.CMAP_W, Normalize(vmin=0, vmax=6.5))
###############################################################################
# Inputs
###############################################################################
PATH = '/home/chipdelmal/Documents/OneWheel'
fPaths = sorted(glob(path.join(PATH, '*.tcx')))
fNames = [path.split(i)[-1].split('.')[0] for i in fPaths]
imgFgPth = path.join(PATH, 'img', "FullRoutes.png")
###############################################################################
# Get BBox and Graph Object
###############################################################################
bbox = fun.getBBoxFromFiles(fPaths)
extent = [
    bbox['lon'][0]-PAD, bbox['lon'][1]+PAD, 
    bbox['lat'][0]-PAD, bbox['lat'][1]+PAD
]
# Get graph object ------------------------------------------------------------
G = ox.graph.graph_from_bbox(
    extent[2], extent[3],  extent[0], extent[1], 
    retain_all=True, simplify=True, network_type='all'
)
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
# Get Laps and segments
###############################################################################
steps = 10
route = routes[8]
# Segment the route in chunks -------------------------------------------------
segRun = [(i['lat'], i['lon']) for i in route[::int(len(route)/steps)]]
segRun = segRun + [(i['lat'], i['lon']) for i in [route[-1]]]
# Get shortest segments between chunks ----------------------------------------
path = []
for nix in range(len(segRun)-2):
    org = ox.get_nearest_node(G, segRun[nix])
    dst = ox.get_nearest_node(G, segRun[nix+1])
    path.extend(nx.shortest_path(G, org, dst, weight='length'))
path = list(OrderedDict.fromkeys(path))
# path = ox.distance.nearest_nodes(
#     G, [i[1] for i in segRun], [i[0] for i in segRun]
# )

fRoute = [path[:], path[:]]
cols = ['#4361ee50'] * len(fRoute)
ox.plot_graph_routes(
    G, fRoute, 
    route_colors=cols,
    bgcolor='#061529', 
    edge_color='#ffffff25', edge_linewidth=1,
    node_size=0, orig_dest_size=0
)

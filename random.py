
import functions as fun
import osmnx as ox
from os import path
import points as pts
import matplotlib.pyplot as plt
ox.config(log_console=True, use_cache=True)

#  Source: https://github.com/CarlosLannister/beautifulMaps
#   https://morioh.com/p/f30f0a215c2f

(point, label, fName, bldg, distance) = pts.TMP

PATH = '/home/chipdelmal/Documents/OneWheel'
DPI = 500
DST = distance

degs = [fun.decdeg2dms(i) for i in point]
degs = [[i for i in j] for j in degs]
(lat, lon) = ["{:.0f}° {:.0f}' {:.2f}".format(*i) for i in degs]
###############################################################################
# Colors
###############################################################################
bgColor = "#000000"
bdColor = '#ffffff11'
rdColor = '#000b82'
rdAlpha = .6
rdScale = 5
###############################################################################
# Get Network
###############################################################################
G = ox.graph_from_point(
    point, dist=DST, network_type='all',
    retain_all=True, simplify=True
)
if bldg:
    gdf = ox.geometries.geometries_from_point(
        point, tags={'building': True} , dist=DST
    )
###############################################################################
# Process Roads
###############################################################################
(u, v, key, data) = ([], [], [], [])
for uu, vv, kkey, ddata in G.edges(keys=True, data=True):
    u.append(uu)
    v.append(vv)
    key.append(kkey)
    data.append(ddata)    
(roadColors, roadWidths) = ([], [])
for item in data:
    if "length" in item.keys():
        if item["length"] <= 100:
            linewidth = 0.10*rdScale
            color = fun.lighten(rdColor, .5)
        elif item["length"] > 100 and item["length"] <= 200:
            linewidth = 0.15*rdScale
            color = fun.lighten(rdColor, .4)
        elif item["length"] > 200 and item["length"] <= 400:
            linewidth = 0.25*rdScale
            color = fun.lighten(rdColor, .3)
        elif item["length"] > 400 and item["length"] <= 800:
            linewidth = 0.35*rdScale
            color = fun.lighten(rdColor, .2)
        else:
            linewidth = 0.45*rdScale
            color = fun.lighten(rdColor, .1)
    else:
        color = rdColor
        linewidth = 0.10
    roadColors.append(color)
    roadWidths.append(linewidth)
###############################################################################
# Plot
###############################################################################
(fig, ax) = ox.plot_graph(
    G, node_size=0,figsize=(40, 40), 
    dpi=DPI, bgcolor=bgColor,
    save=False, edge_color=roadColors, edge_alpha=rdAlpha,
    edge_linewidth=roadWidths, show=False
)
if bldg:
    (fig, ax) = ox.plot_footprints(
        gdf, ax=ax,
        color=bdColor, dpi=DPI, save=False, show=False, close=False
    )
ax.scatter(
    point[1], point[0], marker="o",
    zorder=10, facecolors='#ffffffAA', 
    s=500, edgecolors='#ffffffAA', linewidth=5
)
ax.text(
    0.5, 0.85, '{}'.format(label), 
    horizontalalignment='center', verticalalignment='center', 
    transform=ax.transAxes, color='#ffffffDD', fontsize=250
)
ax.text(
    0.5, 0.1, 'N: {}\nW: {}'.format(lat, lon), 
    horizontalalignment='center', verticalalignment='center', 
    transform=ax.transAxes, color='#ffffffDD', fontsize=75
)
# ax.vlines([.5], 0, 1, transform=ax.transAxes, colors='#ffffffBB', ls='--', lw=1, zorder=5)
# ax.hlines([.5], 0, 1, transform=ax.transAxes, colors='#ffffffBB', ls='--', lw=1, zorder=5)
###############################################################################
# Export
###############################################################################
fig.tight_layout(pad=0)
fig.savefig(
    path.join(PATH, fName+'.png'), 
    dpi=DPI, bbox_inches='tight', format="png", 
    facecolor=fig.get_facecolor(), transparent=False
)
plt.close('all')

import subprocess
import osmnx as ox
from os import path
# import points as pts
import functions as fun
import matplotlib.pyplot as plt
ox.config(log_console=True, use_cache=True)

#  Source: https://github.com/CarlosLannister/beautifulMaps
#   https://morioh.com/p/f30f0a215c2f

(point, label, fName, bldg, distance) = pts.DNT

PATH = '/home/chipdelmal/Documents/OneWheel/maps/'
DPI = 300
DST = distance
###########################################################################
# Colors
###########################################################################
degs = [fun.decdeg2dms(i) for i in point]
degs = [[i for i in j] for j in degs]
(lat, lon) = ["{:.0f}° {:.0f}' {:.2f}".format(*i) for i in degs]
###########################################################################
# Colors
###########################################################################
bgColor = "#100F0F00"
bdColor = '#ffffff11'
rdColor = '#000000'# '#000FB8' # '#000b82'
(rdAlpha, rdScale) = (1, 5)
###########################################################################
# Get Network
###########################################################################
G = ox.graph_from_point(
    point, dist=DST, network_type='all',
    retain_all=True, simplify=True
)
if bldg:
    gdf = ox.geometries.geometries_from_point(
        point, tags={'building': True} , dist=DST
    )
###########################################################################
# Process Roads
###########################################################################
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
            linewidth = 0.1*rdScale
            color = fun.lighten(rdColor, .65)
        elif item["length"] > 100 and item["length"] <= 200:
            linewidth = 0.2*rdScale
            color = fun.lighten(rdColor, .75)
        elif item["length"] > 200 and item["length"] <= 400:
            linewidth = 0.3*rdScale
            color = fun.lighten(rdColor, .85)
        elif item["length"] > 400 and item["length"] <= 800:
            linewidth = 0.5*rdScale
            color = fun.lighten(rdColor, 0.95)
        else:
            linewidth = 0.6*rdScale
            color = fun.lighten(rdColor, 1.0)
    else:
        color = rdColor
        linewidth = 0.10
    roadColors.append(color)
    roadWidths.append(linewidth)
###########################################################################
# Plot
###########################################################################
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
    point[1], point[0], marker="x",
    zorder=10, color='#100F0FCC',
    # facecolors='#000000AA', edgecolors='#000000AA',
    s=7500, linewidth=5
)
ax.text(
    0.5, 0.8, '{}'.format(label), family='Latin Modern Roman Unslanted',
    horizontalalignment='center', verticalalignment='center', 
    transform=ax.transAxes, color='#100F0FDD', fontsize=300
)
ax.text(
    0.5, 0.15, 'N: {}\nW: {}'.format(lat, lon), family='Latin Modern Roman Unslanted',
    horizontalalignment='center', verticalalignment='center', 
    transform=ax.transAxes, color='#100F0FDD', fontsize=150
)
# ax.vlines([.5], 0, 1, transform=ax.transAxes, colors='#ffffffBB', ls='--', lw=1, zorder=5)
# ax.hlines([.5], 0, 1, transform=ax.transAxes, colors='#ffffffBB', ls='--', lw=1, zorder=5)
###########################################################################
# Export
###########################################################################
fig.tight_layout(pad=0)
fig.savefig(
    path.join(PATH, fName+'.png'), 
    dpi=DPI, bbox_inches='tight', format="png", 
    facecolor=fig.get_facecolor(), transparent=True
)
plt.clf()
plt.cla() 
plt.close(fig)
plt.gcf()
###########################################################################
# Inkscape
###########################################################################
fin = open(path.join(PATH, 'textured.svg'), "rt")
data = fin.read()
data = data.replace('MAP_IMG', fName)
fin.close()
fin = open(path.join(PATH, 'textured.svg'), "wt")
fin.write(data)
fin.close()
# Export composite image --------------------------------------------------
cmd = [
    'inkscape', 
    '--export-type=png', 
    '--export-dpi='+str(DPI), 
    path.join(PATH, 'textured.svg'), 
    '--export-filename='+path.join(PATH, 'MAP_'+fName+'.png')
]
subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
# Return svg to original state --------------------------------------------
fin = open(path.join(PATH, 'textured.svg'), "rt")
data = fin.read()
data = data.replace(fName,'MAP_IMG')
fin.close()
fin = open(path.join(PATH, 'textured.svg'), "wt")
fin.write(data)
fin.close()
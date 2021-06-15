import osmnx as ox
from os import path
ox.config(log_console=True, use_cache=True)

#  Source: https://github.com/CarlosLannister/beautifulMaps


point = (19.4928408, -99.2726895) # Mexico City
(point, label, fName) = ((19.492925759295318, -99.27052605182259), 'CDMX', 'Mirtos')
(point, label, fName) = ((37.8742145, -122.28609469999999), 'Berkeley, CA', 'Berkeley')


PATH = '/home/chipdelmal/Documents/OneWheel'
bgcolor = "#000000"
dist = 20000
###############################################################################
# Get Network
###############################################################################
G = ox.graph_from_point(
    point, dist=dist, network_type='all',
    retain_all=True, simplify=True
)
gdf = ox.footprints.footprints_from_point(point=point, distance=dist)
###############################################################################
# Process Roads
###############################################################################
u = []
v = []
key = []
data = []
for uu, vv, kkey, ddata in G.edges(keys=True, data=True):
    u.append(uu)
    v.append(vv)
    key.append(kkey)
    data.append(ddata)    
# List to store colors
roadColors = []
roadWidths = []
for item in data:
    if "length" in item.keys():
        if item["length"] <= 100:
            linewidth = 0.10
            color = "#5E7EBF"
        elif item["length"] > 100 and item["length"] <= 200:
            linewidth = 0.15
            color = "#5E7ECF"
        elif item["length"] > 200 and item["length"] <= 400:
            linewidth = 0.25
            color = "#5E7EDF"    
        elif item["length"] > 400 and item["length"] <= 800:
            color = "#5E7EEF"
            linewidth = 0.35
        else:
            color = "#5E7EFF"
            linewidth = 0.45
    else:
        color = "#5E7EFA"
        linewidth = 0.10
    roadColors.append(color)
    roadWidths.append(linewidth)
###############################################################################
# Plot
###############################################################################
(fig, ax) = ox.plot_graph(
    G, node_size=0,figsize=(27, 40), 
    dpi = 300, bgcolor = bgcolor,
    save = False, edge_color=roadColors,
    edge_linewidth=roadWidths, edge_alpha=1, show=False
)
ax.scatter(
    point[1], point[0], marker="x",
    c='#ff006e55', s=100, zorder=10
)
ax.annotate(
    label, xy=(0, .5), xytext=(.5, .5), 
    xycoords='figure fraction', textcoords='figure fraction',
    horizontalalignment='center', verticalalignment='center',
    color='#FFFFFFB5', fontsize=250
)
###############################################################################
# Export
###############################################################################
fig.tight_layout(pad=0)
fig.savefig(
    path.join(PATH, fName+'.png'), 
    dpi=500, bbox_inches='tight', format="png", 
    facecolor=fig.get_facecolor(), transparent=False
)
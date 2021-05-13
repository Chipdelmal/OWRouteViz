
from os import path
import xmltodict as xtd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

# https://scitools.org.uk/cartopy/docs/latest/matplotlib/intro.html

###############################################################################
# Constants
###############################################################################
KEYS = ('Time', 'Position', 'AltitudeMeters', 'DistanceMeters', 'Extensions')

###############################################################################
# Inputs
###############################################################################
PATH = '/home/chipdelmal/Documents/OneWheel'
fName = '2021_05_13_02.tcx'

###############################################################################
# Read XML
###############################################################################
fPath = path.join(PATH, fName)
with open(fPath) as fd:
    doc = xtd.parse(fd.read())
doc.keys()

###############################################################################
# Get Laps and segments
###############################################################################
lap = doc['TrainingCenterDatabase']['Activities']['Activity']['Lap']
track = lap['Track']['Trackpoint']

lap.keys()

###############################################################################
# Iterate segments
#   Speed seems to be (m/s)
###############################################################################
seg = track[0]
(time, pos, alt, dist, ext) = [seg[k] for k in KEYS]
(lat, lon) = [float(pos[k]) for k in ('LatitudeDegrees', 'LongitudeDegrees')]
speed = float(ext['TPX']['Speed'])

###############################################################################
# Map
###############################################################################
ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()

ny_lon, ny_lat = -75, 43
delhi_lon, delhi_lat = 77.23, 28.61

plt.plot([ny_lon, delhi_lon], [ny_lat, delhi_lat],
         color='blue', linewidth=2, marker='o',
         transform=ccrs.Geodetic(),
         )

plt.plot([ny_lon, delhi_lon], [ny_lat, delhi_lat],
         color='gray', linestyle='--',
         transform=ccrs.PlateCarree(),
         )

plt.text(ny_lon - 3, ny_lat - 12, 'New York',
         horizontalalignment='right',
         transform=ccrs.Geodetic())

plt.text(delhi_lon + 3, delhi_lat - 12, 'Delhi',
         horizontalalignment='left',
         transform=ccrs.Geodetic())

plt.show()
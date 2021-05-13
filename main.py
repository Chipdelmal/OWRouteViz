
from os import path
import xmltodict as xtd

###############################################################################
# Constants
###############################################################################
KEYS = ('Time', 'Position', 'AltitudeMeters', 'DistanceMeters')

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

lap = doc['TrainingCenterDatabase']['Activities']['Activity']['Lap']
lap.keys()

track = lap['Track']['Trackpoint']

seg = track[0]


(time, pos, alt, dist) = [seg[k] for k in KEYS]
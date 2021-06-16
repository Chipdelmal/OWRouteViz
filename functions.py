
import pandas as pd
import numpy as np
import pytz as pytz
import xmltodict as xtd
from datetime import datetime


KEYS = ('Time', 'Position', 'AltitudeMeters', 'DistanceMeters', 'Extensions')


###############################################################################
# File Operations
###############################################################################
def readTCX(fPath):
    with open(fPath) as fd:
        doc = xtd.parse(fd.read())
    return doc


def getTrackFromDoc(doc):
    lap = doc['TrainingCenterDatabase']['Activities']['Activity']['Lap']
    track = lap['Track']['Trackpoint']
    return track


def getRoute(track, segKeys=KEYS, timezone='US/Pacific'):
    ptsNum = len(track)
    route = [None] * ptsNum
    for tix in range(0, ptsNum):
        seg = getSegmentData(track[tix], segKeys=segKeys, timezone=timezone)
        route[tix] = seg
    return route


def getRouteFromFile(filePath):
    doc = readTCX(filePath)
    track = getTrackFromDoc(doc)
    route = getRoute(track)
    return route

###############################################################################
# Data Transform
###############################################################################
def getSegmentData(segment, segKeys=KEYS, timezone='US/Pacific'):
    (time, pos, alt, dist, ext) = [segment[k] for k in segKeys]
    (lat, lon) = [float(pos[k]) for k in ('LatitudeDegrees', 'LongitudeDegrees')]
    speed = float(ext['TPX']['Speed'])
    date = pytz.utc.localize(datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ'))
    date = date.astimezone(pytz.timezone(timezone))
    mvPt = {
        'date': date,
        'lat': lat, 'lon': lon, 'alt': alt,
        'dist': dist, 'speed': speed
    }
    return mvPt


def getRouteArray(route, mtr=('lon', 'lat', 'alt', 'speed')):
    ptsNum = len(route)
    coords = np.zeros((ptsNum, len(mtr)))
    for tix in range(0, ptsNum):
        seg = route[tix]
        coords[tix] = [seg[m] for m in mtr]
    return coords

###############################################################################
# Data Stats
###############################################################################
def getRouteStat(route, mtr=('lon', 'lat', 'alt', 'speed'), fStat=np.mean):
    coords = getRouteArray(route)
    center = fStat(coords, axis=0)
    return {m:v for (m, v) in zip(mtr, center)}

def getBBoxFromRoute(route):
    min = getRouteStat(route, fStat=np.min)
    max = getRouteStat(route, fStat=np.max)
    return [min, max]


def getBBoxFromFiles(filePaths):
    bboxPts = []
    for fName in filePaths:
        route = getRouteFromFile(fName)
        bboxRoute = getBBoxFromRoute(route)
        bboxPts.extend(bboxRoute)
    mtrs = ('lon', 'lat', 'alt', 'speed')
    boxUnravelled = [[i[k] for i in bboxPts] for k in (mtrs)]
    bbox = {k: (np.min(i), np.max(i)) for (k, i) in zip(mtrs, boxUnravelled)}
    return bbox


def movingAverage(numbersList, wSize=5):
    numbers_series = pd.Series(numbersList)
    windows = numbers_series.rolling(wSize, min_periods=1)
    moving_averages = windows.mean()
    return moving_averages.tolist()


def movingAverageRoute(
        route, wSize=10, 
        filtered=['lat', 'lon', 'alt', 'speed']
    ):
    numbers = [[i[j] for i in route] for j in filtered]
    zipped = list(zip(*[movingAverage(i, wSize=wSize) for i in numbers]))
    for (kix, fl) in enumerate(filtered):
        for (ix, r) in enumerate(route):
            route[ix][fl]=zipped[ix][kix]
    return route


def lighten(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])


def decdeg2dms(dd):
   is_positive = dd >= 0
   dd = abs(dd)
   minutes,seconds = divmod(dd*3600,60)
   degrees,minutes = divmod(minutes,60)
   degrees = degrees if is_positive else -degrees
   return (degrees,minutes,seconds)
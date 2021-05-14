
import numpy as np
import pytz as pytz
import xmltodict as xtd
from datetime import datetime


KEYS = ('Time', 'Position', 'AltitudeMeters', 'DistanceMeters', 'Extensions')


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



def readTCX(fPath):
    with open(fPath) as fd:
        doc = xtd.parse(fd.read())
    return doc


def getRoute(track, segKeys=KEYS, timezone='US/Pacific'):
    ptsNum = len(track)
    route = [None] * ptsNum
    for tix in range(0, ptsNum):
        seg = getSegmentData(track[tix], segKeys=segKeys, timezone=timezone)
        route[tix] = seg
    return route


def getRouteStat(route, mtr=('lon', 'lat', 'alt', 'speed'), fStat=np.mean):
    ptsNum = len(route)
    coords = np.zeros((ptsNum, len(mtr)))
    for tix in range(0, ptsNum):
        seg = route[tix]
        coords[tix] = [seg[m] for m in mtr]
    center = fStat(coords, axis=0)
    return {m:v for (m, v) in zip(mtr, center)}
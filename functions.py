
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


def getRouteArray(route, mtr=('lon', 'lat', 'alt', 'speed')):
    ptsNum = len(route)
    coords = np.zeros((ptsNum, len(mtr)))
    for tix in range(0, ptsNum):
        seg = route[tix]
        coords[tix] = [seg[m] for m in mtr]
    return coords


def getRouteStat(route, mtr=('lon', 'lat', 'alt', 'speed'), fStat=np.mean):
    coords = getRouteArray(route)
    center = fStat(coords, axis=0)
    return {m:v for (m, v) in zip(mtr, center)}


def generateColorSwatch(
    baseColor, levels,
    alphaOffset=(.1, .9), lumaOffset=(.1, 1),
):
    colorsList = [None] * levels
    for i in range(levels):
        c = Color(baseColor)
        baseLum = lumaOffset[1] - c.get_luminance()
        lumLevel = (baseLum - ((lumaOffset[1]-baseLum)/levels * i)) + (lumaOffset[0])
        c.set_luminance(lumLevel)
        rgb = c.get_rgb()
        alphaLevel = alphaOffset[0] + ((alphaOffset[1]-alphaOffset[0]) * i/levels)
        colorsList[i] = (rgb[0], rgb[1], rgb[2], alphaLevel)
    return colorsList
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Björn Edström <be@bjrn.se>
# See license for details.

import os
import sys
import time
import urllib2
import xml.etree.ElementTree as elementtree

CACHE_DIRECTORY = '/tmp'
CACHE_TIME = 3600


def download_and_cache(url):
    cache_name = str(hash(url)) + '.cache'
    cache_path = os.path.join(CACHE_DIRECTORY, cache_name)
    try:
        mtime = os.stat(cache_path).st_mtime
        if time.time() - mtime < CACHE_TIME:
            return file(cache_path).read()
    except OSError:
        pass
    data = urllib2.urlopen(url).read()
    with file(cache_path, 'w') as fileobj:
        fileobj.write(data)
    return data


def parse_yr_symbol(symbol):
    # http://om.yr.no/forklaring/symbol/
    # TODO (bjorn): What is this? "mf/03n.33"
    if symbol.startswith('mf/'):
        symbol = symbol[3:]
    if '.' in symbol:
        symbol = symbol.split('.')[0]
    symbol = symbol.strip('nd') # night/day
    snum = int(symbol)

    cloud_cover = 0
    snow = 0 # TODO

    if snum in (1,):
        # clear sky
        cloud_cover = 0
    elif snum in (2,):
        # fair
        cloud_cover = 1
    elif snum in (3, 17, 5, 18, 6, 7, 8, 19, 20, 21):
        # partly cloudy
        cloud_cover = 2
    else:
        # cloudy / overcast
        cloud_cover = 3

    return {'cloud-cover': cloud_cover}


def get_yr(url):
    # TODO (bjorn): Download etc.
    print >> sys.stderr, "Weather forecast from yr.no, delivered by the"
    print >> sys.stderr, "Norwegian Meteorological Institute and the NRK"
    print >> sys.stderr, url
    xml = download_and_cache(url)

    report = []

    tree = elementtree.fromstring(xml)
    for entry in tree.find('forecast').find('tabular'):

        wind_direction = float(entry.find('windDirection').attrib['deg'])
        wind_speed = float(entry.find('windSpeed').attrib['mps'])
        temp = int(entry.find('temperature').attrib['value'])
        pressure = float(entry.find('pressure').attrib['value'])
        rain = entry.find('precipitation').attrib
        symbol_var = entry.find('symbol').attrib['var']
        symbol = parse_yr_symbol(symbol_var)

        report.append({
                'wind-direction': wind_direction,
                'wind-speed': wind_speed,
                'temperature': temp,
                'pressure': pressure,

                # TODO (bjorn): We have min/max as well
                'rain': float(rain['value']),

                'cloud-cover': symbol['cloud-cover']})
    return report


def get_report(location, forecast_type='long'):
    if forecast_type == 'short':
        url = 'http://www.yr.no/place/%s/forecast_hour_by_hour.xml' % (location,)
    else:
        url = 'http://www.yr.no/place/%s/forecast.xml' % (location,)
    return get_yr(url)

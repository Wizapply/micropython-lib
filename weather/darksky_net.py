# Parse weather data from darksky.net

try:
    import ujson as ujson
except ImportError:
    import json as ujson

try:
    import ure as ure
except ImportError:
    import re as ure

import weather.weather_obs as wo

_cardinals = [
    'N',
    'NNE',
    'NE',
    'ENE',
    'E',
    'ESE',
    'SE',
    'SSE',
    'S',
    'SSW',
    'SW',
    'WSW',
    'W',
    'WNW',
    'NW',
    'NNW',
    'N',
]


_icon_map = {
    'clear-day'          : 'clear-day',
    'clear-night'        : 'clear-night',
    'partly-cloudy-day'  : 'cloudy-day',
    'partly-cloudy-night': 'cloudy-night',
    'cloudy'             : 'cloudy',
    'fog'                : 'fog',
    'rain'               : 'rain',
    'sleet'              : 'sleet',
    'snow'               : 'snow',
    'wind'               : 'wind',
    '_default_'          : '_unknown_',
}

def _icon_decode(icon):
    try:
        return _icon_map[icon]
    except KeyError:
        return _icon_map['_default_']

def _bearing_to_cardinal(bearing):
    point = int((bearing+11.25) / 22.5)
    return _cardinals[point]

_weather_obs_fields = [
    ( 'time_ts', ('time', ), None, ),
    ( 'summary', ('summary', ), None, ),
    ( 'code',    None, None, ),
    ( 'icon',    ('icon', ), _icon_decode, ),
    ( 'temperature_C', ('temperature', ), None, ),
    ( 'temperature_min_C', ('temperatureMin', ), None, ),
    ( 'temperature_max_C', ('temperatureMax', ), None, ),
    ( 'pressure_hPa', ('pressure', ), None, ),
    ( 'wind_speed_m_s', ('windSpeed', ), None, ),
    ( 'wind_direction_deg', ('windBearing', ), None, ),
    ( 'wind_direction_cardinal', ('windBearing', ), _bearing_to_cardinal, ),
    ( 'wind_gust_m_s', ('windGust', ), None, ),
    ( 'cloud_cover_ratio', ('cloudCover', ), None, ),
    ( 'relative_humidity_ratio', ('humidity', ), None, ),
    ( 'precipitation_mm', ('precipIntensity', ), None, ),
    ( 'precipitation_probability_ratio', ('precipProbability', ), None, ),
    ( 'sun_rise_ts', ('sunriseTime', ), None, ),
    ( 'sun_set_ts', ('sunsetTime', ), None, ),
    ( 'moon_rise_ts', None, None, ),
    ( 'moon_set_ts', None, None, ),
    ( 'moon_phase', None, None, ),
]


def process_data(wdata):
    wodata = {}
    for o in wdata:
        for f in _weather_obs_fields:
            field_name = f[0]
            path = f[1]
            convert = f[2]
            if path:
                v = o
                for p in path:
                    try:
                        v = v[p]
                    except KeyError:
                        v = None
                        break
            else:
                v = None
            if convert and v:
                v = convert(v)
            wodata[field_name] = v
        obs = wo.Weather_obs(**wodata)

    return obs


def process_json(file):
    obss = []

    data = file.read(500).decode('utf-8')
    m = None

    week = []
    daily = []
    currently = []
    
    r = {}

    m = ure.match('^{(.*?),"daily":{(.+?),"data":\[(.*?$)', data)
    if m:
        wdata = [ ujson.loads('{' + m.group(2) + '}') ]
        week = process_data(wdata)
        rest = m.group(3)
        data = rest + file.read(1000).decode('utf-8')
        m = ure.match('^({.+?})', data)
        wdata = [ ujson.loads(m.group(1)) ]
        daily = process_data(wdata)
        return { 'week': week, 'daily': daily, 'currently': None}
            
    m = ure.match('^{(.*?),"currently":{(.+?)}', data)
    if m:
        wdata = [ ujson.loads('{' + m.group(2) + '}') ]
        currently = process_data(wdata)
        return { 'currently': currently, 'week': None, 'daily': None }

    return None 

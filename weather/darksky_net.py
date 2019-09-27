# Parse weather data from darksky.net

try:
    import ujson as ujson
except ImportError:
    import json as ujson

import weather_obs as wo

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

def _bearing_to_cardinal(bearing):
    point = int((bearing+11.25) / 22.5)
    return _cardinals[point]

_weather_obs_fields = [
    ( 'time_ts', ('time', ), None, ),
    ( 'summary', ('summary', ), None, ),
    ( 'code',    None, None, ),
    ( 'icon',    ('icon', ), None, ),
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

def process_json(data_json):
    obss = []

    pdata = ujson.loads(data_json)
    for dtype in [ 'currently', 'hourly', 'daily' ]:
        try:
            wdata = pdata[dtype]
        except KeyError:
            wdata = None
        
        if not wdata:
            continue

        if dtype == 'currently':
            wdata = [ wdata ]
        if dtype == 'hourly' or dtype == 'daily':
            wdata = wdata['data']

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
            obss.append(obs)

    return obss


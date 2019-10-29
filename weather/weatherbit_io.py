# Parse weather data from weatherbit.io

try:
    import ujson as ujson
except ImportError:
    import json as ujson

import weather_obs as wo

_weather_obs_fields = [
    ( 'time_ts', ('ts', ), None, ),
    ( 'summary', ('weather', 'description', ), None, ),
    ( 'code',    ('weather', 'code', ), None, ),
    ( 'icon',    ('weather', 'icon', ), None, ),
    ( 'temperature_C', ('temp', ), None, ),
    ( 'temperature_min_C', ('min_temp', ), None, ),
    ( 'temperature_max_C', ('max_temp', ), None, ),
    ( 'pressure_hPa', ('pres', ), None, ),
    ( 'wind_speed_m_s', ('wind_spd', ), None, ),
    ( 'wind_direction_deg', ('wind_dir', ), None, ),
    ( 'wind_direction_cardinal', ('wind_cdir', ), None, ),
    ( 'wind_gust_m_s', ('wind_gust_spd', ), None, ),
    ( 'cloud_cover_ratio', ('clouds', ), None, ),
    ( 'relative_humidity_ratio', ('rh', ), lambda x: x/100, ),
    ( 'precipitation_mm', ('precip', ), None, ),
    ( 'precipitation_probability_ratio', ('pop', ), lambda x: x/100, ),
    ( 'sun_rise_ts', ('sunrise_ts', ), None, ),
    ( 'sun_set_ts', ('sunset_ts', ), None, ),
    ( 'moon_rise_ts', ('moonrise_ts', ), None, ),
    ( 'moon_set_ts', ('moonset_ts', ), None, ),
    ( 'moon_phase', ('moon_phase', ), None, ),
]

def process_json(file):
    obss = []

    pdata = ujson.loads(file.read())
    wdata = pdata['data']
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


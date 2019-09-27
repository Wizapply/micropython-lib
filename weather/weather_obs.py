# Weather observations and forecasts

try:
    import ucollections as uc
except ImportError:
    import collections as uc

Weather_obs = uc.namedtuple(
    'Weather_obs', (
        'time_ts',
        'summary',
        'code',
        'icon',
        'temperature_C',
        'temperature_min_C',
        'temperature_max_C',
        'pressure_hPa',
        'wind_speed_m_s',
        'wind_direction_deg',
        'wind_direction_cardinal',
        'wind_gust_m_s',
        'cloud_cover_ratio',
        'relative_humidity_ratio',
        'precipitation_mm',
        'precipitation_probability_ratio',
        'sun_rise_ts',
        'sun_set_ts',
        'moon_rise_ts',
        'moon_set_ts',
        'moon_phase',
    )
)


"""
Extract forecasts from weatherbit.io and darksky.net forecast data.

* Single function 

Data sources
============

weatherbit.io
-------------
* curl 'http://api.weatherbit.io/v2.0/current?key=d3fc630d26bb4a84b0392029a4c90ba0&lat=-43.49391&lon=172.57900' > test/weatherbit-currently.json
* curl 'http://api.weatherbit.io/v2.0/forecast/hourly?key=d3fc630d26bb4a84b0392029a4c90ba0&lat=-43.49391&lon=172.57900&hours=6' > test/weatherbit-hourly-6h.json
* curl 'http://api.weatherbit.io/v2.0/forecast/daily?key=d3fc630d26bb4a84b0392029a4c90ba0&lat=-43.49391&lon=172.57900&days=5' > test/weatherbit-daily-5d.json

darksky.net
-----------
* curl 'https://api.darksky.net/forecast/c795da7ea1fadbf5dccbf95d39ce7baa/-43.49391,172.57900?units=si&exclude=minutely,alerts,flags,daily,hourly' > test/darksky.net-currently.json
* curl 'https://api.darksky.net/forecast/c795da7ea1fadbf5dccbf95d39ce7baa/-43.49391,172.57900?units=si&exclude=minutely,alerts,flags,currently,daily' > test/darksky.net-hourly.json
* curl 'https://api.darksky.net/forecast/c795da7ea1fadbf5dccbf95d39ce7baa/-43.49391,172.57900?units=si&exclude=minutely,alerts,flags,currently,hourly' > test/darksky.net-daily.json

openweathermap.org
------------------
* curl 'http://api.openweathermap.org/data/2.5/weather?lat=-43.49391&lon=172.57900&APPID=bc805df06b9a715a84c3aa78ddbf4160' > test/openweathermap.org-currently.json
* curl 'http://api.openweathermap.org/data/2.5/forecast?lat=-43.49391&lon=172.57900&APPID=bc805df06b9a715a84c3aa78ddbf4160&cnt=24' > test/openweathermap.org-currently.json


TODO
----
* Conversion from bearing to cardinal only copes with 0--360 degrees.
* Does not extract darksky.io daily summary.
* Convert darksky.net and weatherbit.io icon codes into a common standard.
"""

try:
    import utime as utime
except ImportError:
    import time as utime


import weatherbit_io as weatherbit_io

weatherbit_io_files = [
    '../test/data/weatherbit.io-currently.json',
    '../test/data/weatherbit.io-hourly-6h.json',
    '../test/data/weatherbit.io-daily-5d.json',
]

for filename in weatherbit_io_files:
    with open(filename) as f:
        data_json = f
        obss = weatherbit_io.process_json(data_json)
#        for obs in obss:
#            print(obs)
#            print()

# Get the data
with open('../test/data/weatherbit.io-currently.json') as f:
    data_json = f
    current = weatherbit_io.process_json(data_json)[0]

with open('../test/data/weatherbit.io-hourly-6h.json') as f:
    data_json = f
    hourly = weatherbit_io.process_json(data_json)

with open('../test/data/weatherbit.io-daily-5d.json') as f:
    data_json = f
    daily = weatherbit_io.process_json(data_json)


c_fmt = '{hour:02d}:{minute:02d} {temperature:2.0f} {rain:2.0f} {summary}'
d_fmt = '{month:02d}-{day:02d} {temperature_min:2.0f}/{temperature_max:2.0f} {rain:2.0f} {summary}'


# Update screen
print('Christchurch - weatherbit.io')

o = current
tt = utime.localtime(o.time_ts)
print(tt)
print(c_fmt.format(hour=tt[3], minute=tt[4], temperature=o.temperature_C, rain=o.precipitation_mm, summary=o.summary))
print()

#for o in hourly[:6]:
#    tt = utime.localtime(o.time_ts)
#    print(c_fmt.format(hour=tt[3], minute=tt[4], temperature=o.temperature_C, rain=o.precipitation_mm, summary=o.summary))
#print()

for o in daily[:5]:
    tt = utime.localtime(o.time_ts)
    print(d_fmt.format(month=tt[1], day=tt[2], temperature_min=o.temperature_min_C, temperature_max=o.temperature_max_C, rain=o.precipitation_mm, summary=o.summary))
print()

print()


import darksky_net as darksky_net

darksky_net_files = [
    '../test/data/darksky.net-currently.json',
#    '../test/data/darksky.net-hourly.json',
    '../test/data/darksky.net-daily.json',
]

for filename in darksky_net_files:
    print(filename)
    with open(filename) as f:
        data_json = f
        obss = darksky_net.process_json(data_json)
        for obs in obss:
            print(obs)
            print()

# # Get the data
# with open('../test/data/darksky.net-currently.json') as f:
#     data_json = f
#     current = darksky_net.process_json(data_json)[0]
# 
# with open('../test/data/darksky.net-hourly.json') as f:
#     data_json = f
#     hourly = darksky_net.process_json(data_json)
# 
# with open('../test/data/darksky.net-daily.json') as f:
#     data_json = f
#     daily = darksky_net.process_json(data_json)

# Update screen
print('Christchurch - darksky.net')

c_fmt = '{hour:02d}:{minute:02d} {temperature:2.0f} {rain:2.0f} {summary}'

o = current
tt = utime.localtime(o.time_ts)
print(c_fmt.format(hour=tt[3], minute=tt[4], temperature=o.temperature_C, rain=o.precipitation_mm, summary=o.summary))
print()

#for o in hourly[:6]:
#    tt = utime.localtime(o.time_ts)
#    print(c_fmt.format(hour=tt[3], minute=tt[4], temperature=o.temperature_C, rain=o.precipitation_mm, summary=o.summary))
#print()

d_fmt = '{month:02d}-{day:02d} {temperature_min:2.0f}/{temperature_max:2.0f} {rain:2.0f} {summary}'

for o in daily[:5]:
    tt = utime.localtime(o.time_ts)
    print(d_fmt.format(month=tt[1], day=tt[2], temperature_min=o.temperature_min_C, temperature_max=o.temperature_max_C, rain=o.precipitation_mm, summary=o.summary))
print()

print()

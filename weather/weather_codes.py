
_codes = (
    ( 200, 'Thunderstorm', 'Thunderstorm with light rain', '11d' ),
    ( 201, 'Thunderstorm', 'Thunderstorm with rain', '11d' ),
    ( 202, 'Thunderstorm', 'Thunderstorm with heavy rain', '11d' ),
    ( 210, 'Thunderstorm', 'Tight thunderstorm', '11d' ),
    ( 211, 'Thunderstorm', 'Thunderstorm', '11d' ),
    ( 212, 'Thunderstorm', 'Heavy thunderstorm', '11d' ),
    ( 221, 'Thunderstorm', 'Ragged thunderstorm', '11d' ),
    ( 230, 'Thunderstorm', 'Thunderstorm with light drizzle', '11d' ),
    ( 231, 'Thunderstorm', 'Thunderstorm with drizzle', '11d' ),
    ( 232, 'Thunderstorm', 'Thunderstorm with heavy drizzle', '11d' ),
    ( 233, 'Thunderstorm', 'Thunderstorm with hail', None ),

    ( 300, 'Drizzle', 'Light intensity drizzle', '09d' ),
    ( 301, 'Drizzle', 'Drizzle', '09d' ),
    ( 302, 'Drizzle', 'Heavy intensity drizzle', '09d' ),
    ( 310, 'Drizzle', 'Light intensity drizzle rain', '09d' ),
    ( 311, 'Drizzle', 'Drizzle rain', '09d' ),
    ( 312, 'Drizzle', 'Heavy intensity drizzle rain', '09d' ),
    ( 313, 'Drizzle', 'Shower rain and drizzle', '09d' ),
    ( 314, 'Drizzle', 'Heavy shower rain and drizzle', '09d' ),
    ( 321, 'Drizzle', 'Shower drizzle', '09d' ),

    ( 500, 'Rain', 'Light rain', '10d' ),
    ( 501, 'Rain', 'Moderate rain', '10d' ),
    ( 502, 'Rain', 'Heavy intensity rain', '10d' ),
    ( 503, 'Rain', 'Very heavy rain', '10d' ),
    ( 504, 'Rain', 'Extreme rain', '10d' ),
    ( 511, 'Rain', 'Freezing rain', '13d' ),
    ( 520, 'Rain', 'Light intensity shower rain', '09d' ),
    ( 521, 'Rain', 'Shower rain', '09d' ),
    ( 522, 'Rain', 'Heavy intensity shower rain', '09d' ),
    ( 531, 'Rain', 'Ragged shower rain', '09d' ),

    ( 600, 'Snow', 'Light snow', '3d' ),
    ( 601, 'Snow', 'Snow', '13d' ),
    ( 602, 'Snow', 'Heavy snow', '13d' ),
    ( 610, 'Snow', 'Mix snow/rain', None ),
    ( 611, 'Snow', 'Sleet', '13d' ),
    ( 612, 'Snow', 'Light shower sleet', '13d' ),
#612     Heavy sleet     Weather API Day Sleets05d, Weather API Night Sleets05n
    ( 613, 'Snow', 'Shower sleet', '13d' ),
    ( 615, 'Snow', 'Light rain and snow', '13d' ),
    ( 616, 'Snow', 'Rain and snow', '13d' ),
    ( 620, 'Snow', 'Light shower snow', '13d' ),
    ( 621, 'Snow', 'Shower snow', '13d' ),
    ( 622, 'Snow', 'Heavy shower snow', '13d' ),
#623     Flurries     Weather API Day Flurriess06d, Weather API Night Flurriess06n

#700     Mist     Weather API Day Mista01d, Weather API Night Mista01n
    ( 701, 'Mist', 'Mist', '50d' ),
    ( 711, 'Smoke', 'Smoke', '50d' ),
    ( 721, 'Haze', 'Haze', '50d' ),
    ( 731, 'Dust', 'Sand/dust whirl', '50d' ),
    ( 741, 'Fog', 'Fog', '50d' ),
#751     Freezing Fog     Weather API Day Freezing foga06d, Weather API Night freezing foga06n
    ( 751, 'Sand', 'Sand', '50d' ),
    ( 761, 'Dust', 'Dust', '50d' ),
    ( 762, 'Ash', 'Volcanic ash', '50d' ),
    ( 771, 'Squall', 'Squalls', '50d' ),
    ( 781, 'Tornado', 'Tornado', '50d' ),

    ( 800, 'Clear', 'Clear sky', '01d 01n' ),

    ( 801, 'Clouds', 'Few clouds: 11-25%', '02d 02n' ),
    ( 802, 'Clouds', 'Scattered clouds: 25-50%', '03d 03n' ),
    ( 803, 'Clouds', 'Broken clouds: 51-84%', '04d 04n' ),
    ( 804, 'Clouds', 'Overcast clouds: 85-100%', '04d 04n' ),

#900     Unknown Precipitation     Weather API Day Unknown Precipitationu00d, Weather API Night Unknown Precipitationu00n
)


"""
Darksky icons


clear-day, clear-night, rain, snow, sleet, wind, fog, cloudy, partly-cloudy-day, or partly-cloudy-night
"""

import utime
import ulogging
import network
import unetmangler
import forecast

def time_unix_to_upy(unix_t):
    return unix_t - 946641600


def run(num=5, interval=120, debug=False):
    if debug:
        ulogging.getLogger('eng.sw.forecast').setLevel(ulogging.DEBUG)
        ulogging.getLogger('eng.sw.unetmangler').setLevel(ulogging.DEBUG)
        
    wlan_configs = [('wodexitose', 'mirodefamehe')]
    netif = network.WLAN(network.STA_IF)
    net = unetmangler.Net_Mangler('network', netif, wlan_configs)
    
    fc = forecast.Forecaster('9%20Liverton%20Crescent%20Christchurch%20NZ', 'c795da7ea1fadbf5dccbf95d39ce7baa', net, forecast_types=['currently'], forecast_interval_s=interval)  #pylint: disable=line-too-long,invalid-name
    fc_timestamp_ms = fc.forecast_timestamp_ms

    while True:
        net.step()
        fc.step()
        
        if fc.forecast_timestamp_ms != fc_timestamp_ms:
            fc_timestamp_ms = fc.forecast_timestamp_ms

            f = fc.forecast_data['currently']  #pylint: disable=invalid-name

            t_forecast_u = time_unix_to_upy(f['time'])
            t_forecast_s = utime.localtime(t_forecast_u)
            hour = t_forecast_s[3]
            minute = t_forecast_s[4]
            summary = f['summary']
            temperature_C = f['temperature']  #pylint: disable=invalid-name
            pressure_hPa = f['pressure']  #pylint: disable=invalid-name
            wind_m_s = f['windSpeed']
            wind_kn = wind_m_s * 1.94
            gust_m_s = f['windGust']
            gust_kn = gust_m_s * 1.94
            direction_d = f['windBearing']

            print('{}:{} {} {}'.format(hour, minute, temperature_C, summary))
            
            num -= 1

        if num == 0 and not net.is_connected():
            break

        utime.sleep_ms(100)

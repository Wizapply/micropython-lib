import utime
import network
import unetmangler
import utimemangler

import ulogging


wlan_configs = [
    ( 'wodexitose', 'mirodefamehe' ),
    ( 'Stephone', 'fcf91fef' ),
    ( 'Brush2', 'unicycleboys' ),
]

tzone_name = 'Pacific/Auckland'
timezonedb_apikey = 'K4MDCWIU6YM5'

def run(debug=False):
    if debug:
        ulogging.getLogger('eng.sw.utimemangler').setLevel(ulogging.DEBUG)
        ulogging.getLogger('eng.sw.netmangler').setLevel(ulogging.DEBUG)
    netif = network.WLAN(network.STA_IF)
    net = unetmangler.Net_Mangler('wlan', netif, wlan_configs)
    tm = utimemangler.Time_Mangler(net, tzone_name, timezonedb_apikey)
    while tm.state != tm.TIME_SET:
        net.step()
        tm.step()
        utime.sleep_ms(100)

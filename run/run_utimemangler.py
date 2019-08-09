import network
import unetmangler
import utimemangler
import utime

wlan_configs = [
    ( 'wodexitose', 'mirodefamehe' ),
    ( 'Stephone', 'fcf91fef' ),
    ( 'Brush2', 'unicycleboys' ),
]

tzone_name = 'Pacific/Auckland'
timezonedb_apikey = 'K4MDCWIU6YM5'

def run():
    netif = network.WLAN(network.STA_IF)
    net = unetmangler.Net_Mangler('wlan', netif, wlan_configs)
    tm = utimemangler.Time_Mangler(net, tzone_name, timezonedb_apikey)
    net.connect('run', 60000)
    while tm.confidence() < 0.8:
        net.step()
        tm.step()
        utime.sleep_ms(100)

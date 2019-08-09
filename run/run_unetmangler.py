import network
import unetmangler
import utime

wlan_configs = [
    ( 'wodexitose', 'mirodefamehe' ),
    ( 'Stephone', 'fcf91fef' ),
    ( 'Brush2', 'unicycleboys' ),
]

def run(duration_s=10):
    netif = network.WLAN(network.STA_IF)
    net = unetmangler.Net_Mangler('wlan', netif, wlan_configs)
    net.connect('run', duration_s * 1000)
    while True:
        net.step()
        utime.sleep_ms(100)

def connect():
    netif = network.WLAN(network.STA_IF)
    net = unetmangler.Net_Mangler('wlan', netif, wlan_configs)
    net.connect('run', 60000)
    while not net.is_connected():
        net.step()
        utime.sleep_ms(100)

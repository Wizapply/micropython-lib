
STA_IF = 1

STAT_IDLE = 0
STAT_CONNECTING = 1000
STAT_GOT_IP = 1010

class WLAN:
    def __init__(self, *args, **kwargs):
        self._status = STAT_IDLE
        self._rssi = -60

    def isconnected(self):
        return self._status == STAT_GOT_IP

    def status(self, item=None):
        if item is None:
            return self._status
        elif item == 'rssi':
            return self._rssi
        
    def active(self, active=None):
        return active

    def connect(self, *args, **kwargs):
        self._status = STAT_CONNECTING
    
    def config(self, item):
        if item == 'essid':
            return 'test_ssid'

    def disconnect(self):
        pass

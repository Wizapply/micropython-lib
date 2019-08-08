"""
Time mangler -- ensure that we have the time set

"""

import ulogging
import utime
import ntptime
try:
    import urequests as requests
except ImportError:
    import requests

_logger = ulogging.getLogger('eng.sw.utime')
_logger.setLevel(ulogging.INFO)


def get_tzone_data(apikey, tzone_name):
    params = []
    params.append('key={}'.format(apikey))
    params.append('format=json')
    params.append('by=zone')
    params.append('zone={}'.format(tzone_name))
    params_str = '&'.join(params)

    url_fmt = 'http://api.timezonedb.com/v2.1/get-time-zone?{params}'
    url = url_fmt.format(params=params_str)
    _logger.info('Requesting {}...'.format(url))
    headers = {}
#   headers['Accept-Encoding'] = 'gzip'

    try:
        req = requests.get(url, headers=headers, timeout=30)
    except (IndexError, OSError) as exc:  # IndexError is a strange exception to throw if there is no data...
        _logger.info('Requesting {}...failed'.format(url))
        _logger.info(exc)
        return None

    # Convert the forecast data from JSON to Python
    try:
        content = req.json()
    except ValueError:
        req.close()
        return None

    req.close()
    return content


class Time_Mangler:
    #pylint: disable=too-many-instance-attributes
    # Though I cannot seee that there are 10 of them?
    NOT_SET = 0
    CONNECTING = 1
    SETTING_TIME = 2
    WAITING_FOR_TIMEZONE = 3
    DISCONNECTING = 4
    TIME_SET = 5

    def __init__(self, net, tzone_name, tzone_apikey=None):
        self.net = net
        
        self.retry_interval_initial = 2
        self.retry_interval_not_set = 300  # 5 minutes
        self.retry_interval_set = 3600 # 1 hour
        self.timestamp = None
        self._confidence = 0.0

        self.time_set_timestamp = None
        self.next_set_timestamp = utime.time() + self.retry_interval_initial 
        self.network_timeout = 30 # Keep the network up for 30 s maximum

        self.tzone_name = tzone_name
        self.tzone_apikey = tzone_apikey
        self.tzone_data = None

        self.state = self.NOT_SET

    def confidence(self):
        return self._confidence

    def step(self):
        #pylint: disable=too-many-branches,too-many-statements
        time_now = utime.time()

        if self.state == self.NOT_SET:
            if time_now > self.next_set_timestamp:
                _logger.info('Time mangler...')
                _logger.debug('Connecting...')
                self.net.connect('timemangler', self.network_timeout)
                self.timestamp = time_now
                self.state = self.CONNECTING
            return

        if self.state == self.CONNECTING:
            if self.net.is_connected():
                _logger.debug('Connecting...done')
                _logger.debug('Setting time...')
                self.timestamp = time_now
                self.state = self.SETTING_TIME
            else:
                duration = time_now - self.timestamp
                if duration >= self.network_timeout:
                    _logger.debug('Connecting...timeout')
                    _logger.debug('Disconnecting...')
                    self.timestamp = time_now
                    self.state = self.DISCONNECTING
            return

        if self.state == self.SETTING_TIME:
            try:
                ntptime.settime()
                time_now = utime.time()   # Time has changed, so we must change our cached value
            except (OSError, IndexError):
                _logger.info('Setting time...failed ({})', utime.localtime())
                self.next_set_timestamp += self.retry_interval_set
                if self.next_set_timestamp < time_now:  # If we have missed a timestamp, jump ahead
                    self.next_set_timestamp = time_now + self.retry_interval_set
                self.timestamp = time_now
                self.state = self.DISCONNECTING
                return
                
            _logger.info('Setting time...done ({})', utime.localtime())
            self._confidence = 1.0
            self.time_set_timestamp = time_now
            self.next_set_timestamp += self.retry_interval_set
            if self.next_set_timestamp < time_now:  # If we have missed a timestamp, jump ahead
                self.next_set_timestamp = time_now + self.retry_interval_set
            _logger.debug('Getting timezone...')
            self.timestamp = time_now
            self.state = self.WAITING_FOR_TIMEZONE
            return

        if self.state == self.WAITING_FOR_TIMEZONE:
            if self.tzone_apikey:
                self.tzone_data = get_tzone_data(self.tzone_apikey, self.tzone_name)
            if self.tzone_data is None:
                _logger.debug('Getting timezone...failed')
                _logger.debug('Disconnecting...')
                self.timestamp = time_now
                self.state = self.DISCONNECTING
            else:
                _logger.debug('Getting timezone...done')
                _logger.info(self.tzone_data)
                _logger.debug('Disconnecting...')
                self.timestamp = time_now
                self.state = self.DISCONNECTING
            return

        if self.state == self.DISCONNECTING:
            self.net.disconnect('timemangler')
            _logger.debug('Disconnecting...done')
            _logger.info('Time mangler...done')
            self.timestamp = time_now
            self.state = self.TIME_SET
            return

        if self.state == self.TIME_SET:
            if time_now > self.next_set_timestamp:
                _logger.info('Time mangler...')
                _logger.debug('Connecting...')
                self.net.connect('timemangler', self.network_timeout)
                self.timestamp = time_now
                self.state = self.CONNECTING
            return

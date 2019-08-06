"""
Time mangler -- ensure that we have the time set

"""

import ulogging
import utime
import ntptime

_logger = ulogging.getLogger('eng.sw.utime')
_logger.setLevel(ulogging.INFO)


class Time_Mangler:
    #pylint: disable=too-many-instance-attributes
    # Though I cannot seee that there are 10 of them?
    NOT_SET = 0
    CONNECTING = 1
    SETTING_TIME = 2
    DISCONNECTING = 3
    TIME_SET = 4

    def __init__(self, net):
        self.net = net
        
        self.retry_interval_initial = 2
        self.retry_interval_not_set = 300  # 5 minutes
        self.retry_interval_set = 3600 # 1 hour
        self.timestamp = None

        self.time_set_timestamp = None
        self.next_set_timestamp = utime.time() + self.retry_interval_initial 
        self.network_timeout = 30 # Keep the network up for 30 s maximum

        self.state = self.NOT_SET

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
                self.timestamp = time_now
            return

        if self.state == self.CONNECTING:
            if self.net.is_connected():
                _logger.debug('Connecting...done')
                _logger.debug('Setting time...')
                self.state = self.SETTING_TIME
            else:
                duration = time_now - self.timestamp
                if duration >= self.network_timeout:
                    _logger.debug('Connecting...timeout')
                    _logger.debug('Disconnecting...')
                    self.state = self.DISCONNECTING
                    self.timestamp = time_now
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
                self.state = self.DISCONNECTING
                return
                
            _logger.info('Setting time...done ({})', utime.localtime())
            self.time_set_timestamp = time_now
            self.next_set_timestamp += self.retry_interval_set
            if self.next_set_timestamp < time_now:  # If we have missed a timestamp, jump ahead
                self.next_set_timestamp = time_now + self.retry_interval_set
            self.state = self.DISCONNECTING
            return

        if self.state == self.DISCONNECTING:
            self.net.disconnect('timemangler')
            _logger.debug('Disconnecting...done')
            _logger.info('Time mangler...done')
            self.state = self.TIME_SET
            return

        if self.state == self.TIME_SET:
            if time_now > self.next_set_timestamp:
                _logger.info('Time mangler...')
                _logger.debug('Connecting...')
                self.net.connect('timemangler', self.network_timeout)
                self.timestamp = time_now
                self.state = self.CONNECTING
                self.timestamp = time_now
            return

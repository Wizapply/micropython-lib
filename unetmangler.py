"""
Network Mangler -- Connect to a network from a set of configurations

Given a list of network connection details, connect to one of them
* try the most recent one* do a scan and connect to the strongest
* connect to them in sequence
"""

import utime
import network
import sleepy

import ulogging
_logger = ulogging.getLogger('eng.sw.unetmangler')
_logger.setLevel(ulogging.INFO)


class Net_User:
    #pylint: disable=too-few-public-methods
    def __init__(self, user_id, duration, connect_time):
        self.user_id = user_id
        self.duration = duration
        self.connect_time = connect_time


class Net_Mangler:
    #pylint: disable=too-many-instance-attributes
    # Though I cannot seee that there are 10 of them?
    IDLE = 0
    CONNECTING = 1
    CONNECTED = 2
    DISCONNECTING = 3

    def __init__(self, name, netif, configs):
        self.name = name
        self.netif = netif
        self.configs = configs

        self.connect_timeout_ms = 10000
        self.disconnect_timeout_ms = 2000
        self.previous_connection_config = 0
        self.connection_attempt_config = 0
        self.wlan_ssid = None
        self.maximum_duration = 120000

        self.state_timestamp = utime.ticks_ms()

        self.users = {}
        self.state = self.IDLE

    def connect(self, user_id, duration):
        _logger.debug('{}: User {} connect ({} s)', self.name, user_id, duration)
        time_now = utime.ticks_ms()
        if duration > 0:
            self.users[user_id] = Net_User(user_id, duration, time_now)
        else:
            self._remove_user(user_id)

    def disconnect(self, user_id):
        _logger.debug('{}: User {} disconnect', self.name, user_id)
        self._remove_user(user_id)

    def expire_user(self, user_id):
        _logger.debug('{}: User {} timeout', self.name, user_id)
        self._remove_user(user_id)

    def _remove_user(self, user_id):
        try:
            del self.users[user_id]
        except KeyError:
            pass

    def is_connected(self):
        return self.state == self.CONNECTED



    def step(self):
        #pylint: disable=too-many-branches,too-many-statements
        time_now = utime.ticks_ms()
        state_duration_ms = utime.ticks_diff(time_now, self.state_timestamp)

        # Remove expired users from the list
        for uid in list(self.users.keys()):
            user = self.users[uid]
            connected_duration = utime.ticks_diff(time_now, user.connect_time)
            if connected_duration >= user.duration:
                self.expire_user(uid)

        status = self.netif.status()

        if self.state == self.IDLE:
            if self.users:
                sleepy.keep_awake(self.name, self.maximum_duration)
                self.netif.active(True)
                self.netif.disconnect()

                self.connection_attempt_config = self.previous_connection_config

                self.wlan_ssid = self.configs[self.connection_attempt_config][0]
                wlan_key = self.configs[self.connection_attempt_config][1]

                _logger.info('{}: Connecting {}...', self.name, self.wlan_ssid)
                self.netif.connect(self.wlan_ssid, wlan_key)

                self.state_timestamp = time_now
                self.state = self.CONNECTING
            return

        if self.state == self.CONNECTING:
            #if status in [ network.STAT_GOT_IP ]:  #pylint: disable=bad-whitespace
            if self.netif.isconnected():
                self.previous_connection_config = self.connection_attempt_config
                self.wlan_ssid = self.netif.config('essid')
                rssi = self.netif.status('rssi')
                _logger.info('{}: Connecting {}...connected ({})', self.name, self.wlan_ssid, rssi)
                self.state_timestamp = time_now
                self.state = self.CONNECTED
                return

            if state_duration_ms >= self.connect_timeout_ms:
                _logger.debug('{}: Connecting {}...timeout', self.name, self.wlan_ssid)
                self.connection_attempt_config += 1
                if self.connection_attempt_config >= len(self.configs):
                    self.connection_attempt_config = 0

                self.netif.disconnect()
                if self.users:
                    self.wlan_ssid = self.configs[self.connection_attempt_config][0]
                    wlan_key = self.configs[self.connection_attempt_config][1]

                    _logger.debug('{}: Connecting {}...', self.name, self.wlan_ssid)
                    self.netif.connect(self.wlan_ssid, wlan_key)

                    self.state_timestamp = time_now
                    self.state = self.CONNECTING
                else:
                    _logger.debug('{}: Disconnecting {}...', self.name, self.wlan_ssid)

                    self.state_timestamp = time_now
                    self.state = self.DISCONNECTING
            return

        if self.state == self.CONNECTED:
            if not self.users:
                _logger.debug('{}: Disconnecting {}...', self.name, self.wlan_ssid)
                self.netif.disconnect()

                self.state_timestamp = time_now
                self.state = self.DISCONNECTING
            return

        if self.state == self.DISCONNECTING:
            if status not in [ network.STAT_CONNECTING, network.STAT_GOT_IP ] or state_duration_ms >= self.disconnect_timeout_ms:  #pylint: disable=line-too-long,bad-whitespace
                self.netif.active(False)
                sleepy.keep_awake(self.name, 0)
                _logger.info('{}: Disconnecting {}...done', self.name, self.wlan_ssid)
                self.state_timestamp = time_now
                self.state = self.IDLE
            return

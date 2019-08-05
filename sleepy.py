"""
Go to sleep unless something is keeping us awake
"""

import ulogging
import utime

_logger = ulogging.getLogger('eng.sw.sleepy')
_logger.setLevel(ulogging.INFO)


_users = {}
_indicator = None

def init(indicator):
    global _indicator  #pylint: disable=global-statement
    _indicator = indicator
    if _indicator: _indicator.on()

def keep_awake(user_id, duration_ms):
    ticks_now = utime.ticks_ms()
    if duration_ms != 0:
        _logger.debug('Keep awake: {}', user_id)
        _users[user_id] = ticks_now + duration_ms
    else:
        _logger.debug('Allow sleep: {}', user_id)
        try:
            del _users[user_id]
        except KeyError:
            pass


def sleep(duration_ms):
    ticks_now = utime.ticks_ms()
    for user_id in list(_users.keys()):
        expiry_time = _users[user_id]
        ticks_left = utime.ticks_diff(expiry_time, ticks_now)
        if ticks_left <= 0:
            _logger.info('Expired: {}', user_id)
            keep_awake(user_id, 0)

    if not _users:
        if _indicator: _indicator.off()
        utime.sleep_ms(duration_ms)
#        machine.lightsleep(duration_ms)
        if _indicator: _indicator.on()

"""
Watchdog monitor

Various services must report in periodically. If all of them have reported in, the watchdog
monitor feeds the hardware watchdog. Otherwise, the monitor does not feed the hardware watchdog
and eventually the system restarts.
"""

import ulogging
import utime
import machine

_logger = ulogging.getLogger('eng.sw.wdog')
_logger.setLevel(ulogging.INFO)


class TaskWatchdog:
    #pylint: disable=too-few-public-methods
    def __init__(self, name, timeout):
        self.name = name
        self.timeout = timeout

        self.feed_time = utime.time()

    def feed(self):
        _logger.debug('{}: feed')
        time_now = utime.time()
        self.feed_time = time_now


_twdogs = {}
_wdt = None

def init(timeout):
    global _wdt  #pylint: disable=global-statement
    if _wdt is None:
        _wdt = machine.WDT(timeout=timeout)

def get(name, timeout):
    try:
        twdog = _twdogs[name]
    except KeyError:
        twdog = TaskWatchdog(name, timeout)
        _twdogs[name] = twdog
    return twdog

def step():
    time_now = utime.time()

    task_is_late = False
    for name, twdog in _twdogs.items():  #pylint: disable=unused-variable
        feed_delay = time_now - twdog.feed_time
        if feed_delay >= twdog.timeout:
            _logger.warning('{}: is late', wdog.name)
            task_is_late = True

    if not task_is_late:
        if _wdt: _wdt.feed()

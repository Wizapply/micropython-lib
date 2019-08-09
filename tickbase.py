
import ulogging
import utime

_logger = ulogging.getLogger('eng.sw.tickbase')
_logger.setLevel(ulogging.INFO)


class Tickbase:
    #pylint: disable=too-few-public-methods
    def __init__(self, get_ticks, ticks_per_s, overflow):
        self.get_ticks = get_ticks
        self.ticks_per_s = ticks_per_s
        self.overflow = overflow

tickbase_ms = Tickbase(utime.ticks_ms, 1000, None)
tickbase_us = Tickbase(utime.ticks_us, 1000000, None)

class Ticked_action:
    #pylint: disable=too-few-public-methods
    def __init__(self, name, action, interval, initial_delay=0, tickbase=tickbase_ms, drifter=False):  #pylint: disable=line-too-long,too-many-arguments
        self.name = name
        self.action = action
        self.interval = interval
        self.tickbase = tickbase
        self.drifter = drifter
        self.ticks_next = self.tickbase.get_ticks() + initial_delay

    def step(self):
        ticks_now = self.tickbase.get_ticks()
        ticks_left = utime.ticks_diff(self.ticks_next, ticks_now)
        if ticks_left <= 0:
            _logger.debug('{}: Running...', self.name)
            self.action(ticks_now)
            _logger.debug('{}: Running...done', self.name)
            if self.drifter:
                self.ticks_next = ticks_now + self.interval
            else:
                self.ticks_next = self.ticks_next + self.interval

def Ticked_action_ms(name, action, interval, initial_delay, drifter=False):  #pylint: disable=invalid-name
    ticker = Ticked_action(name, action, interval, initial_delay, tickbase_ms, drifter)
    return ticker

def Ticked_action_us(name, action, interval, initial_delay, drifter=False):  #pylint: disable=invalid-name
    ticker = Ticked_action(name, action, interval, initial_delay, tickbase_us, drifter)
    return ticker

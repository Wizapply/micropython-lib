

_ticks_us = 0

def time():
    return _ticks_us / 1000000

def ticks_ms():
    return _ticks_us / 1000

def ticks_us():
    return _ticks_us

def ticks_diff(t1, t2):
    return t1 - t2

def sleep_ms(duration_ms):
    global _ticks_us
    _ticks_us += duration_ms * 1000

def sleep_us(duration_us):
    global _ticks_us
    _ticks_us += duration_us


def localtime(t):
    return (0, 0, t)


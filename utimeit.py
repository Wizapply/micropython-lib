"""
timeit - A simple function-timing function

Use it as a decorator

@timeit_ms
def slow_function(n)
    pass

or alias the function to time

slow_function = timeit_ms(slow_function)
"""

import utime

def timeit(f):
    def timed(*args, **kw):
        ts = utime.ticks_ms()
        result = f(*args, **kw)
        te = utime.ticks_ms()
        duration = utime.ticks_diff(te, ts)
        print('{}: {}'.format(f.__name__, duration))
#        print 'func:%r args:[%r, %r] took: %2.4f sec' % (f.__name__, args, kw, te-ts)
        return result
    return timed

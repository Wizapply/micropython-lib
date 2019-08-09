
import sleepy
import utime

def test_it():
    class Indicator:
        def on(self):
            pass
        def off(self):
            pass

    utime._ticks_us = 0

    ind = Indicator()
    sleepy.init(ind)
    
    assert(utime.ticks_ms() == 0)
    sleepy.sleep(100)
    assert(utime.ticks_ms() == 100)

    sleepy.keep_awake('me', 1000)
    sleepy.sleep(100)
    assert(utime.ticks_ms() == 100)
    
    sleepy.keep_awake('me', 0)
    sleepy.sleep(100)
    assert(utime.ticks_ms() == 200)
    
    sleepy.keep_awake('me', 1000)
    sleepy.keep_awake('you', 500)
    sleepy.sleep(100)
    assert(utime.ticks_ms() == 200)
    
    utime.sleep_ms(499)
    sleepy.sleep(100)
    assert(utime.ticks_ms() == 699)

    utime.sleep_ms(1)
    sleepy.sleep(100)
    assert(utime.ticks_ms() == 700)

    utime.sleep_ms(499)
    sleepy.sleep(100)
    assert(utime.ticks_ms() == 1199)

    utime.sleep_ms(1)
    sleepy.sleep(100)
    assert(utime.ticks_ms() == 1300)



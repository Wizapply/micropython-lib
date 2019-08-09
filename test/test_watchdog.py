
import watchdog

def test_it():
    watchdog.init(10000)
    wdog = watchdog.get('test', 1000)
    wdog.feed()
    watchdog.step()
    

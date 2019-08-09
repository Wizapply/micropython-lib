import tickbase
import utime


def test_tickbase_zero_delay():
    _action_count = 0
    def action(ticks_now):
        nonlocal _action_count
        _action_count += 1

    ticker = tickbase.Ticked_action_ms('test', action, 1000, 0)
    
    assert(_action_count == 0)

    ticker.step()
    assert(_action_count == 1)

    utime.sleep_ms(999)
    ticker.step()
    assert(_action_count == 1)

    utime.sleep_ms(1)
    ticker.step()
    assert(_action_count == 2)


def test_tickbase_with_delay():
    _action_count = 0
    def action(ticks_now):
        nonlocal _action_count
        _action_count += 1

    ticker = tickbase.Ticked_action_ms('test', action, 1000, 500, drifter=False)
    
    assert(_action_count == 0)

    ticker.step()
    assert(_action_count == 0)

    utime.sleep_ms(499)
    ticker.step()
    assert(_action_count == 0)

    utime.sleep_ms(1)
    ticker.step()
    assert(_action_count == 1)
    
    utime.sleep_ms(999)
    ticker.step()
    assert(_action_count == 1)

    utime.sleep_ms(1)
    ticker.step()
    assert(_action_count == 2)


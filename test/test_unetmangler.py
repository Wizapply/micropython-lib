
import unetmangler
import network


def test_cycle():
    mnet = network.WLAN()
    nm = unetmangler.Net_Mangler('test', mnet, [('test_ssid', 'test_wpa_key')])
    assert(nm.state == nm.IDLE)
    
    nm.step()
    assert(nm.state == nm.IDLE)
    
    nm.connect('test_user', 10000)
    nm.step()
    assert(nm.state == nm.CONNECTING)

    nm.step()
    assert(nm.state == nm.CONNECTING)

    mnet._status = network.STAT_GOT_IP
    nm.step()
    nm.step()
    assert(nm.state == nm.CONNECTED)

    nm.step()
    assert(nm.state == nm.CONNECTED)

    nm.disconnect('test_user')
    nm.step()
    assert(nm.state == nm.DISCONNECTING)

    nm.step()
    assert(nm.state == nm.DISCONNECTING)

    mnet._status = network.STAT_IDLE
    nm.step()
    assert(nm.state == nm.IDLE)
    
    nm.step()
    assert(nm.state == nm.IDLE)


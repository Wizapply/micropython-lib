

class I2C:
    def __init__(self, *args, **kwargs):
        pass

class Pin:
    OUT = 0x01
    PULL_UP = 0x10
    def __init__(self, *args, **kwargs):
        pass

    def on(self):
        pass
        
    def off(self):
        pass

    def value(self, value=None):
        pass

class WDT:
    def __init__(self, timeout):
        pass

    def feed(self):
        pass


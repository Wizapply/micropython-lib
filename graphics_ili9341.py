class Context:
    def __init__(self, dev):
        self.dev = dev
        
    def draw_window(self, x, y, width, height):
        self.xabs = x
        self.yabs = y
        self.width = width
        self.height = height
        
    def rect(self, x, y, width, height, color):
        x += self.xabs
        y += self.yabs
#        print('rect', x, y, width, height, color)
        self.dev.fill_rect(x, y, width, height, color)

    def text(self, x, y, width, height, text, font, fg, bg):
        x += self.xabs
        y += self.yabs
#        print('text', x, y, width, height, "'"+text+"'", str(font), fg, bg)
        self.dev.text(text, x, y, font.ff, fg, bg)


class Font:
    def __init__(self, name, ff):
        self.name = name
        self.ff = ff

    def text_width(self, text):
        return self.ff.get_width(text)
    
    def text_height(self, text):
        return self.ff.height()
    
    def __str__(self):
        return '{}'.format(self.name)

_fonts = {}

try:
    import fonts.DejaVuSans_12
    _fonts['small'] = Font('DejaVuSans_12', fonts.DejaVuSans_12)
except ImportError:
    pass

try:
    import fonts.DejaVuSans_16
    _fonts['medium'] = Font('DejaVuSans_16', fonts.DejaVuSans_16)
except ImportError:
    pass

try:
    import fonts.DejaVuSans_Bold_16
    _fonts['medium-bold'] = Font('DejaVuSans_Bold_16', fonts.DejaVuSans_Bold_16)
except ImportError:
    pass

try:
    import fonts.DejaVuSans_20
    _fonts['large'] = Font('DejaVuSans_20', fonts.DejaVuSans_20)
except ImportError:
    pass

try:
    import fonts.DejaVuSans_Bold_20
    _fonts['large-bold'] = Font('DejaVuSans_Bold_20', fonts.DejaVuSans_Bold_20)
except ImportError:
    pass

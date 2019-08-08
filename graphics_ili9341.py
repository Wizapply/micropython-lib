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
        #print('rect', x, y, width, height, color)
        self.dev.fill_rect(x, y, width, height, color)

    def text(self, x, y, width, height, text, font, fg, bg):
        x += self.xabs
        y += self.yabs
        #print('text', x, y, width, height, text, str(font), fg, bg)
        self.dev.text(text, x, y, fg, font.ff)


class Font:
    def __init__(self, name, ff):
        self.name = name
        self.ff = ff

    def text_size(self, text):
        width = len(text) * self.ff.max_width()
        height = self.ff.height()
        return width, height
    
    def __str__(self):
        return '{}'.format(self.name)

fonts = {}

try:
    import glcdfont
    fonts['small'] = Font('glcd', glcdfont)
except ImportError:
    pass

try:
    import tt14
    fonts['normal'] = Font('tt14', tt14)
except ImportError:
    pass

try:
    import tt24
    fonts['large'] = Font('tt24', tt24)
except ImportError:
    pass

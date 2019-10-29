class Context:
    def __init__(self, dev):
        self.dev = dev
        
    def draw_window(self, x, y, width, height):
        self.xabs = x
        self.yabs = y
        self.width = width
        self.height = height
        
    def pixel(self, x, y, color):
        x += self.xabs
        y += self.yabs
#        print('pixel', x, y, color)
        self.dev.pixel(x, y, color)

    def line(self, x0, y0, x1, y1, color):
        x0 += self.xabs
        y0 += self.yabs
        x1 += self.xabs
        y1 += self.yabs
        #print('line', x0, y0, x1, y1, color)
        self.dev.line(x0, y0, x1, y1, color)

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
        width = 0
        for ch in text:
            _, _, w =self.ff.get_ch(ch)
            width += w
        return width

        return self.ff.get_width(text)
    
    def text_height(self, text):
        return self.ff.height()
    
    def __str__(self):
        return '{}'.format(self.name)

_font_map = {
    'small' : 'DejaVuSans_12',
    'medium' : 'DejaVuSans_16',
    'medium-bold': 'DejaVuSans_Bold_16',
    'large'      : 'DejaVuSans_20',
    'large-bold' : 'DejaVuSans_Bold_20',
    'weather-small' : 'PE_Icon_Set_Weather_24',
}

_fonts = {}

for alias, font_name in _font_map.items():
    try:
        font_module = __import__('fonts.' + font_name, None, None, [ font_name ])
        _fonts[alias] = Font('DejaVuSans_12', font_module)
    except ImportError:
        pass

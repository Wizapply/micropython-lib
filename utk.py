import utimeit

class Color:
    BLACK   = 0x000000
    NAVY    = 0x000080
    BLUE    = 0x0000FF
    GREEN   = 0x008000
    TEAL    = 0x008080
    LIME    = 0x00FF00
    AQUA    = 0x00FFFF
    MAROON  = 0x800000
    PURPLE  = 0x800080
    OLIVE   = 0x808000
    GRAY    = 0x808080
    SILVER  = 0xC0C0C0
    RED     = 0xFF0000
    FUSCHIA = 0xFF00FF
    YELLOW  = 0xFFFF00
    WHITE   = 0xFFFFFF

    CYAN    = 0x00FFFF
    MAGENTA = 0xFF00FF


    @staticmethod
    def from_rgb(r, g, b):
        return Color.from_rgb_hex(r, g, b)

    @staticmethod
    def from_rgb_hex(r, g, b):
        return ((r & 0xFF) << 16) + ((g & 0xFF) << 8) + (b & 0xFF)

    @staticmethod
    def from_rgb_fraction(r, g, b):
        return Color.from_rgb(int(round(r*255)), int(round(g*255)), int(round(b*255)))

    @staticmethod
    def from_hsl(h, s, l):
        """
        Convert (hue, saturation, lightness) triplet to RGB

        References
            https://www.w3.org/TR/css-color-3/
            http://www.niwa.nu/2013/05/math-behind-colorspace-conversions-rgb-hsl/
            https://serennu.com/colour/rgbtohsl.php
        """
        if l <= 0.5:
            m2 = l*(s + 1.)
        else:
            m2 = l + s - l*s
        m1 = l * 2. - m2
        r = Color._hue_to_rgb(m1, m2, h+1./3.)
        g = Color._hue_to_rgb(m1, m2, h)
        b = Color._hue_to_rgb(m1, m2, h-1./3.)
        return Color.rgb_fraction(r, g, b)

    @staticmethod
    def _hue_to_rgb(m1, m2, h):
        if h < 0.:
            h = h + 1.
        if h > 1.:
            h = h - 1.
        if h*6. < 1.:
            return m1 + (m2-m1)*h*6.
        elif h*2. < 1.:
            return m2
        elif h*3. < 2.:
            return m1 + (m2-m1)*(2./3.-h)*6.
        else:
            return m1

    @staticmethod
    def hsl_from_color(color):
        r, g, b = Color.to_rgb_fraction(color)
        rgb_min = min(r, g, b)
        rgb_max = max(r, g, b)
        l = (rgb_min + rgb_max) / 2.
        if l <= 0.5:
            s = (rgb_max - rgb_min) / (rgb_max + rgb_min)
        else:
            s = (rgb_max - rgb_min) / (2. - rgb_max - rgb_min)
        if r > g and r > b:   # Red is the biggest component
            h = (g - b) / (rgb_max - rgb_min)
        elif g > r and g > b:   # Green is the biggest component
            h = 2. + (b - r) / (rgb_max - rgb_min)
        else:  # Assume that Blue is the biggest component
            h = 4. + (r - g) / (rgb_max - rgb_min)

        return h, s, l

    @staticmethod
    def to_rgb_hex(color):
        r = ((color >> 16) & 0xFF)
        g = ((color >> 8) & 0xFF)
        b = ((color) & 0xFF)
        return r, g, b
        
    @staticmethod
    def to_rgb_fraction(color):
        r, g, b = Color.to_rgb_hex(color)
        return r / 255., g / 255., b / 255.        


class _Base:
    CONFIG_ATTRS = {
        'x': 0,
        'y': 0,
        'width': None,
        'height': None,
    }
    
    PLACE_ATTRS = [
        'x',
        'y',
        'width',
        'height',
    ]

    def __init__(self, parent=None):
        self.config(**self.CONFIG_ATTRS)

        self.parent = parent
        self.children = []
        if self.parent:
            self.parent.children.append(self)
            self.parent._is_dirty = True
        
        self._is_dirty = True

        self._x = 0
        self._y = 0
        self._width = 0
        self._height = 0

        self._in_grid = None

        self._rows = {}
        self._columns = {}

    def config(self, **kwargs):
        self._config(self.CONFIG_ATTRS, kwargs)
        return self

    def _config(self, attrs, kwargs):
        for k, v in kwargs.items():
            if k in attrs:
                self._is_dirty = True
                setattr(self, k, v)
            else:
                raise(AttributeError, '{}.{}: unknown attribute'.format(self.__class__.__name__, k))

    # place geometry manager
    def place(self, **kwargs):
        self._config(self.PLACE_ATTRS, kwargs)
        if self.parent:
            self.parent._is_dirty = True
        return self

    # grid geometry manager
    def grid(self, row, column=1, rowspan=1, columnspan=1):
        if self.parent is None:
            return
        self._in_grid = self.parent
        self._is_dirty = True
        self.parent._is_dirty = True

        try:
            rowa = self._in_grid._rows[row]
        except KeyError:
            rowa = {}
            self._in_grid._rows[row] = rowa
        rowa[column] = self

        try:
            cola = self._in_grid._columns[column]
        except KeyError:
            cola = {}
            self._in_grid._columns[column] = cola
        cola[row] = self

        return self

    # update operations
    def draw(self, context, force=False):
        self._calculate()
        self._draw(context, force)

    def _draw(self, context, force=False):
        self._xabs = self._x
        self._yabs = self._y
        if self.parent:
            self._xabs += self.parent._xabs
            self._yabs += self.parent._yabs

        if force or self._is_dirty:
            context.draw_window(self._xabs, self._yabs, self._width, self._height)
            self._paint(context)
            self._is_dirty = False
        
        for child in self.children:
            child._draw(context)

    def _calculate(self):
        self._x = 0
        if self.x:
            self._x = self.x
        self._y = 0
        if self.y:
            self._y = self.y

        for child in self.children:
            child._calculate()

        self._width = 0
        if self.children:
            self._width = max(child._x + child._width for child in self.children)
        if self.width is not None:
            self._width = self.width

        self._height = 0
        if self.children:
            self._height = max(child._y + child._height for child in self.children)
        if self.height is not None:
            self._height = self.height

        # Calculate the height of each row, and set the height of all items in the row
        if self._rows:
            for r, rowa in self._rows.items():
                row_height = max(item._height for c, item in rowa.items())
                for c, item in rowa.items():
                    item._height = row_height        

        # Calculate the width of each column, and set the width of all items the the column
        if self._columns:
            for c, cola in self._columns.items():
                column_width = max(item._width for r, item in cola.items())
                for r, item in cola.items():
                    item._width = column_width

        # Calculate the x-offset of each item in each row
        # Adjust our width
        if self._rows:
            for r, rowa in self._rows.items():
                x_offset = 0
                for c, item in rowa.items():
                    item._x = x_offset
                    x_offset += item._width
            if self.width is None:
                self._width = max(self._width, x_offset)

        # Calculate the y-offset of each item in each column
        # Adjust our height
        if self._columns:
            for c, cola in self._columns.items():
                y_offset = 0
                for r, item in cola.items():
                    item._y = y_offset
                    y_offset += item._height
            if self.height is None:
                self._height = max(self._height, y_offset)


class Empty (_Base):
    def _paint(self, context):
        pass


class Tk (_Base):
    CONFIG_ATTRS = {
        'x': 0,
        'y': 0,
        'width': None,
        'height': None,
        'fg': Color.WHITE,
        'bg': Color.BLACK,
    }

    def _paint(self, context):
        context.rect(0, 0, self._width, self._height, self.bg)


class Label (_Base):
    CONFIG_ATTRS = {
        'x': 0,
        'y': 0,
        'width': None,
        'height': None,
        'fg': Color.WHITE,
        'bg': Color.BLACK,
        'pad_left': 4,
        'pad_right': 4,
        'pad_top': 4,
        'pad_bottom': 4,
        'anchor': 'w',
        'font': None,
    }

    def __init__(self, parent=None, text=''):
        super().__init__(parent)
        self.text = text

    def _calculate(self):
        super()._calculate()
        if self.font:
            text_width = self.font.text_width(self.text)
            text_height = self.font.text_height(self.text)
            if self.width is None:
                self._width = max(self._width, text_width + self.pad_left + self.pad_right)
            if self.height is None:
                self._height = max(self._height, text_height + self.pad_top + self.pad_bottom)

    #@utimeit.timeit
    def _paint(self, context):
        if self.anchor == 'n':
            top_offset = 0
            left_offset = int(((self._width - self.pad_left - self.pad_right) - self.font.text_width(self.text)) / 2)
        elif self.anchor == 'ne':
            top_offset = 0
            left_offset = ((self._width - self.pad_left - self.pad_right) - self.font.text_width(self.text))
        elif self.anchor == 'e':
            top_offset = int(((self._height - self.pad_top - self.pad_bottom) - self.font.text_height(self.text)) / 2)
            left_offset = ((self._width - self.pad_left - self.pad_right) - self.font.text_width(self.text))
        elif self.anchor == 'se':
            top_offset = ((self._height - self.pad_top - self.pad_bottom) - self.font.text_height(self.text))
            left_offset = int(((self._width - self.pad_left - self.pad_right) - self.font.text_width(self.text)) / 2)
        elif self.anchor == 's':
            top_offset = ((self._height - self.pad_top - self.pad_bottom) - self.font.text_height(self.text))
            left_offset = int(((self._width - self.pad_left - self.pad_right) - self.font.text_width(self.text)) / 2)
        elif self.anchor == 'sw':
            top_offset = ((self._height - self.pad_top - self.pad_bottom) - self.font.text_height(self.text))
            left_offset = 0
        elif self.anchor == 'w':
            top_offset = int(((self._height - self.pad_top - self.pad_bottom) - self.font.text_height(self.text)) / 2)
            left_offset = 0
        elif self.anchor == 'nw':
            top_offset = 0
            left_offset = 0
        else:
            top_offset = int(((self._height - self.pad_top - self.pad_bottom) - self.font.text_height(self.text)) / 2)
            left_offset = int(((self._width - self.pad_left - self.pad_right) - self.font.text_width(self.text)) / 2)

#         print(self._width, self._height, self.pad_left, self.pad_right, self.pad_top, self.pad_bottom, "'"+self.text+"'", self.font, self.fg, self.bg)
#         print(left_offset, top_offset, self.font.text_width(self.text))
        context.rect(0, 0, self._width, self._height, self.bg)
        context.text(left_offset + self.pad_left, top_offset + self.pad_top, self._width, self._height, self.text, self.font, self.fg, self.bg)

    def value(self, text=None):
        if text:
            if self.text != text:
                self.text = text
                self._is_dirty = True
        return self.text


class Sparkline (_Base):
    CONFIG_ATTRS = {
        'x': 0,
        'y': 0,
        'width': None,
        'height': None,
        'fg': Color.WHITE,
        'bg': Color.BLACK,
        'pad_left': 4,
        'pad_right': 4,
        'pad_top': 4,
        'pad_bottom': 4,
        'max_values': 64,
        'vrange_min': 10,
        'highlight': Color.RED,
    }

    def __init__(self, parent):  #pylint: disable=super-init-not-called
        super().__init__(parent)
        if self.highlight is None:
            self.highlight = self.style.fg

        if self.max_values is None and self.width is not None:
            self.max_values = (self.width - (self.pad_left + self.pad_right))  #pylint: disable=no-member
        self.value = [ None for i in range(self.max_values) ]

    @utimeit.timeit
    def _paint(self, context):
        values = [ v for v in self.value if v is not None ]  #pylint: disable=bad-whitespace
        if not values:
            return

        vmin = min(values)
        vmax = max(values)
        vrange = vmax - vmin
        if vrange < self.vrange_min:
            vofs = round((self.vrange_min - vrange) / 2)
            vmin = vmin - vofs
            vrange = self.vrange_min

        yrange = self._height - (self.pad_top + self.pad_bottom)
        scale = yrange / vrange

        context.rect(0, 0, self._width, self._height, self.bg)

        #pylint: disable=invalid-name
        x0 = self.pad_left
        y0 = None
        for v in self.value:
            x1 = x0 + 1
            if v is None:
                y1 = None
            else:
                y1 = -round((v - vmin) * scale) + self._height - self.pad_bottom

            if y0 is None:
                if y1 is None: # Both are none
                    pass
                else:  # y1 not none
                    context.pixel(x1, y1, self.fg)
            else:  # y0 not none
                if y1 is None:
                    context.pixel(x0, y0, self.fg)
                else:  # Both not none
                    context.line(x0, y0, x1, y1, self.fg)

            x0 = x1
            y0 = y1

        # Draw a slightly larger 'dot' at the RH end of the line
        if y0 is not None:
            context.pixel(x0, y0, self.highlight)
            context.pixel(x0-1, y0, self.highlight)
            context.pixel(x0+1, y0, self.highlight)
            context.pixel(x0, y0-1, self.highlight)
            context.pixel(x0, y0+1, self.highlight)

    
    def append_value(self, value):
        if type(value) is list:
            self.value.extend(value)
        else:
            self.value.append(value)
        while len(self.value) > self.max_values:
            self.value.pop(0)
        self._is_dirty = True



# TODO: Styles (standard collections of fonts, colour, borders, etc)
# TODO: Graphics context drivers for each display controller
# TODO: Graphics context driver for BMP, PNG etc
# TODO: Make grid geometry manager 'optional' to reduce memory footprint if it is not used

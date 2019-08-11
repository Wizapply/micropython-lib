class Color:
    BLACK = 0x000000
    RED   = 0xFF0000
    GREEN = 0x008000
    WHITE = 0xFFFFFF


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

#        print(self._width, self._height, self.pad_left, self.pad_right, self.pad_top, self.pad_bottom, "'"+self.text+"'", self.font, self.fg, self.bg)
#        print(left_offset, top_offset)
        context.rect(0, 0, self._width + self.pad_left + self.pad_right, self._height + self.pad_top + self.pad_bottom, self.bg)
        context.text(left_offset + self.pad_left, top_offset + self.pad_top, self._width, self._height, self.text, self.font, self.fg, self.bg)

    def value(self, text=None):
        if text:
            if self.text != text:
                self.text = text
                self._is_dirty = True
        return self.text


# TODO: Colours
# TODO: Sparkline widget
# TODO: Borders and margins around widgets
# TODO: Styles (standard collections of fonts, colour, borders, etc)
# TODO: Graphics context drivers for each display controller
# TODO: Graphics context driver for BMP, PNG etc
# TODO: Calculate sizes and positions when items are added or moved rather than every time they are drawn
# TODO: Dirty flag to prevent unnecessary recalculations and/or redraws
# TODO: Make grid geometry manager 'optional' to reduce memory footprint if it is not used

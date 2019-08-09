import utk as tk

class Context_Test:
    def __init__(self):
        self._rects = []
        self._texts = []
        
    def draw_window(self, x, y, width, height):
        self.xabs = x
        self.yabs = y
        self.width = width
        self.height = height
        
    def rect(self, x, y, width, height, color):
        x += self.xabs
        y += self.yabs
        print('rect', x, y, width, height, color)
        self._rects.append((x, y, width, height, color))

    def text(self, x, y, width, height, text, font, fg, bg):
        x += self.xabs
        y += self.yabs
        print('text', x, y, width, height, text, str(font), fg, bg)
        self._texts.append((x, y, width, height, text, str(font), fg, bg))


class Font:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def text_size(self, text):
        width = len(text) * self.size
        height = self.size
        return width, height
    
    def __str__(self):
        return '{}-{}'.format(self.name, self.size)

sans10 = Font(name='sans', size=10)
sans20 = Font(name='sans', size=20)
serif10 = Font(name='serif', size=10)
serif20 = Font(name='serif', size=20)

def test_Tk():
    root = tk.Tk()
    root.config(fg=tk.Color.WHITE, bg=tk.Color.BLACK)
    root.place(x=0, y=0, width=320, height=240)

    ctx = Context_Test()
    root.draw(ctx)
    assert(len(ctx._rects) == 1)
    assert(ctx._rects[0] == (0, 0, 320, 240, tk.Color.BLACK))


def test_Label():
    root = tk.Tk()
    root.config(x=0, y=0, width=320, height=240)
    
    l1 = tk.Label(root, text='Text in Label l1')
    l1.place(x=100, y=50, width=70, height= 20)
    l1.config(font=sans20, fg=tk.Color.RED, bg=tk.Color.GREEN)

    ctx = Context_Test()
    root.draw(ctx)
    
    assert(len(ctx._rects) == 2)
    assert(ctx._rects[0] == (0, 0, 320, 240, tk.Color.BLACK))
    assert(ctx._rects[1] == (100, 50, 70, 20, tk.Color.GREEN))
    assert(len(ctx._texts) == 1)
    assert(ctx._texts[0] == (100, 50, 70, 20, 'Text in Label l1', 'sans-20', tk.Color.RED, tk.Color.GREEN))


def test_nested():
    root = tk.Tk()
    root.config(x=0, y=0, width=320, height=240)
    
    l1 = tk.Label(root, text='Text in Label l1')
    l1.place(x=100, y=50, width=70, height= 20)
    l1.config(font=sans20, fg=tk.Color.RED, bg=tk.Color.GREEN)

    l2 = tk.Label(l1, text='Text in Label l2')
    l2.place(x=200, y=150, width=80, height= 30)
    l2.config(font=serif10, fg=tk.Color.GREEN, bg=tk.Color.RED)

    ctx = Context_Test()
    root.draw(ctx)
    
    l1.place(x=1000)
    l2.place(y=2000)
    root.draw(ctx)

    assert(len(ctx._rects) == 6)
    assert(ctx._rects[0] == (0, 0, 320, 240, tk.Color.BLACK))
    assert(ctx._rects[1] == (100, 50, 70, 20, tk.Color.GREEN))
    assert(ctx._rects[2] == (300, 200, 80, 30, tk.Color.RED))
    assert(ctx._rects[3] == (0, 0, 320, 240, tk.Color.BLACK))
    assert(ctx._rects[4] == (1000, 50, 70, 20, tk.Color.GREEN))
    assert(ctx._rects[5] == (1200, 2050, 80, 30, tk.Color.RED))

    assert(len(ctx._texts) == 4)
    assert(ctx._texts[0] == (100, 50, 70, 20, 'Text in Label l1', 'sans-20', tk.Color.RED, tk.Color.GREEN))
    assert(ctx._texts[1] == (300, 200, 80, 30, 'Text in Label l2', 'serif-10', tk.Color.GREEN, tk.Color.RED))
    assert(ctx._texts[2] == (1000, 50, 70, 20, 'Text in Label l1', 'sans-20', tk.Color.RED, tk.Color.GREEN))
    assert(ctx._texts[3] == (1200, 2050, 80, 30, 'Text in Label l2', 'serif-10', tk.Color.GREEN, tk.Color.RED))


def test_parent_resize():
    root = tk.Tk()
    
    l1 = tk.Label(root, text='Text in Label l1')
    l1.config(font=sans10)
    l1.place(x=100, y=50, width=80, height= 20)

    ctx = Context_Test()
    root.draw(ctx)

    assert(len(ctx._rects) == 2)
    assert(ctx._rects[0] == (0, 0, 100+80, 50+20, tk.Color.BLACK))
    assert(ctx._rects[1] == (100, 50, 80, 20, tk.Color.BLACK))

    assert(len(ctx._texts) == 1)
    assert(ctx._texts[0] == (100, 50, 80, 20, 'Text in Label l1', 'sans-10', tk.Color.WHITE, tk.Color.BLACK))


def test_label_autosize():
    root = tk.Tk()
    
    l1 = tk.Label(root, text='Text in Label l1')
    l1.config(font=sans10)

    ctx = Context_Test()
    root.draw(ctx)

    assert(len(ctx._rects) == 2)
    assert(ctx._rects[0] == (0, 0, 160, 10, tk.Color.BLACK))
    assert(ctx._rects[1] == (0, 0, 160, 10, tk.Color.BLACK))

    assert(len(ctx._texts) == 1)
    assert(ctx._texts[0] == (0, 0, 160, 10, 'Text in Label l1', 'sans-10', tk.Color.WHITE, tk.Color.BLACK))


def test_grid():
    root = tk.Tk()
    root.config(x=0, y=0, width=320, height=240)
    
    l1 = tk.Label(root, text='Text in Label l1').config(width=100, height=20).grid(row=0, column=0)
    l2 = tk.Label(root, text='Text in Label l2').config(width=200, height=30).grid(row=0, column=1)
    l3 = tk.Label(root, text='Text in Label l3').config(width=150, height=40).grid(row=1, column=0)
    l4 = tk.Label(root, text='Text in Label l4').config(width=180, height=10).grid(row=1, column=1)

    print('----------------------')
    ctx = Context_Test()
    root.draw(ctx)
    
    assert(len(ctx._rects) == 5)
    assert(ctx._rects[0] == (  0,  0, 320, 240, tk.Color.BLACK))
    assert(ctx._rects[1] == (  0,  0, 150, 30, tk.Color.BLACK))
    assert(ctx._rects[2] == (150,  0, 200, 30, tk.Color.BLACK))
    assert(ctx._rects[3] == (  0, 30, 150, 40, tk.Color.BLACK))
    assert(ctx._rects[4] == (150, 30, 200, 40, tk.Color.BLACK))

def test_grid_nested():
    root = tk.Tk()
    root.config(x=0, y=0, width=320, height=240)
    
    l0 = tk.Label(root, text='No text').place(x=1000, y=2000)

    l1 = tk.Label(l0, text='Text in Label l1').config(width=100, height=20).grid(row=0, column=0)
    l2 = tk.Label(l0, text='Text in Label l2').config(width=200, height=30).grid(row=0, column=1)
    l3 = tk.Label(l0, text='Text in Label l3').config(width=150, height=40).grid(row=1, column=0)
    l4 = tk.Label(l0, text='Text in Label l4').config(width=180, height=10).grid(row=1, column=1)

    ctx = Context_Test()
    root.draw(ctx)
    
    assert(len(ctx._rects) == 6)
    assert(ctx._rects[0] == (  0,  0, 320, 240, tk.Color.BLACK))
    assert(ctx._rects[1] == (1000, 2000, 350, 70, tk.Color.BLACK))
    assert(ctx._rects[2] == (1000, 2000, 150, 30, tk.Color.BLACK))
    assert(ctx._rects[3] == (1150, 2000, 200, 30, tk.Color.BLACK))
    assert(ctx._rects[4] == (1000, 2030, 150, 40, tk.Color.BLACK))
    assert(ctx._rects[5] == (1150, 2030, 200, 40, tk.Color.BLACK))

def test_weather_ui():
    fonts = [
        sans20,
        sans10,
    ]
    
    u_root = tk.Tk().place(x=0, y=0, width=320, height=240)
    
    b_title = tk.Empty(u_root).grid(row=0, column=0)
    l_title = tk.Label(b_title, text='Christchurch').grid(row=0, column=0).config(width=256, height=32, font=fonts[0])
    l_ltime = tk.Label(b_title, text='00:00')       .grid(row=0, column=1).config(width=64, font=fonts[1])
   
    b_summary = tk.Empty(u_root).grid(row=1, column=0) 
    l_summary = tk.Label(b_summary, text='A very long description').config(width=320, font=fonts[0])
    
    b_data = tk.Empty(u_root).grid(row=2, column=0)
    l_tspark  = tk.Label(b_data, text='...')         .grid(row=0, column=0).config(width=192, font=fonts[1])
    l_tvalue  = tk.Label(b_data, text='--')          .grid(row=0, column=1).config(width=64, font=fonts[1])
    l_tunit   = tk.Label(b_data, text='~C')          .grid(row=0, column=2).config(width=64, font=fonts[1])
    
    l_pspark  = tk.Label(b_data, text='...')         .grid(row=1, column=0).config(width=192, font=fonts[1])
    l_pvalue  = tk.Label(b_data, text='--')          .grid(row=1, column=1).config(width=64, font=fonts[1])
    l_punit   = tk.Label(b_data, text='hPa')         .grid(row=1, column=2).config(width=64, font=fonts[1])
    
    l_wspark  = tk.Label(b_data, text='...')         .grid(row=2, column=0).config(width=192, font=fonts[1])
    l_wvalue  = tk.Label(b_data, text='--')          .grid(row=2, column=1).config(width=64, font=fonts[1])
    l_wunit   = tk.Label(b_data, text='kn')          .grid(row=2, column=2).config(width=64, font=fonts[1])
    
    b_status  = tk.Empty(u_root).grid(row=3, column=0)
    l_ftime   = tk.Label(b_status, text='...')         .grid(row=0, column=0).config(width=64, font=fonts[1])
    l_f2      = tk.Label(b_status, text='...')         .grid(row=0, column=1).config(width=64, font=fonts[1])
    l_f3      = tk.Label(b_status, text='...')         .grid(row=0, column=2).config(width=64, font=fonts[1])
    l_f4      = tk.Label(b_status, text='...')         .grid(row=0, column=3).config(width=64, font=fonts[1])
    l_f5      = tk.Label(b_status, text='...')         .grid(row=0, column=4).config(width=64, font=fonts[1])

    ctx = Context_Test()
    u_root.draw(ctx)

from PIL import Image, ImageDraw, ImageTk
from Tkconstants import W, E, S, N
from Tkinter import Tk, Canvas, Frame, BOTH, NW, Label, Text, Button
from ttk import Style
from utils.tools import generate_random_color, convert_rgb_to_hex

DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600
DEFAULT_COLOR = '#1A735F'


class MiniPaint(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.drawing_line = False

    def initUI(self):
        self.setup_window()
        self.setup_canvas()
        self.setup_buttons()

    def setup_window(self):
        self.parent.title("Mini Paint")
        self.pack(fill=BOTH, expand=1)
        self.setup_grid_padding()

        lbl = Label(self, text="Draw whatever you want!")
        lbl.grid(sticky=W, pady=4, padx=5)

    def setup_grid_padding(self):
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

    def setup_canvas_size(self):
        self.canvas_width = self.canvas_image.width() + 20
        self.canvas_height = self.canvas_image.height() + 20

    def setup_canvas_image(self):
        self.image = Image.new("RGB", (DEFAULT_WIDTH, DEFAULT_HEIGHT), '%s' % DEFAULT_COLOR)
        self.canvas_image = ImageTk.PhotoImage(self.image)
        self.setup_canvas_size()

    def setup_canvas(self):
        self.setup_canvas_image()
        self.canvas = Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.canvas.create_image(10, 10, anchor=NW, image=self.canvas_image)
        self.canvas.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=E + W + S + N)
        self.canvas.bind("<ButtonPress-1>", self.draw_point)

    def draw_point(self, event):
        self.canvas.create_rectangle((event.x - 2, event.y - 2, event.x + 2, event.y + 2), fill='#000000')

    def setup_buttons(self):
        point_button = Button(self, text="Point", command=self.)
        point_button.grid(row=1, column=3)

        line_button = Button(self, text="Line", command=self.draw_line)
        line_button.grid(row=2, column=3)

        clear_button = Button(self, text="Clear", command=self.clear_canvas)
        clear_button.grid(row=5, column=0, padx=5)

    def clear_canvas(self):
        self.setup_canvas()


def main():
    root = Tk()
    root.resizable(width=False, height=False)
    app = MiniPaint(root)
    root.mainloop()


if __name__ == '__main__':
    main()

from PIL import Image, ImageDraw, ImageTk
from Tkconstants import W, E, S, N
from Tkinter import Tk, Canvas, Frame, BOTH, NW, Label, Text, Button
from ttk import Style
from utils.tools import generate_random_color, convert_rgb_to_hex


class MiniPaint(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.initUI()

    def get_pixel(self, event):
        self.draw_point(event.x, event.y)

    def draw_point(self, x, y):
        print x, y
        point = convert_rgb_to_hex(generate_random_color())
        self.canvas.create_rectangle((x - 2, y - 2, x + 2, y + 2), fill='#000000')

        # minipaint.rectangle(, fill=point)

    def initUI(self):
        self.parent.title("Windows")
        self.style = Style()
        self.style.theme_use("classic")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        lbl = Label(self, text="Draw whatever you want!")
        lbl.grid(sticky=W, pady=4, padx=5)

        self.img = Image.new("RGB", (800, 600), '#1A735F')
        self.tatras = ImageTk.PhotoImage(self.img)

        self.canvas = Canvas(self, width=self.img.size[0] + 20, height=self.img.size[1] + 20, cursor="cross")
        self.canvas.create_image(10, 10, anchor=NW, image=self.tatras)
        self.canvas.grid(row=1, column=0, columnspan=2, rowspan=4,
                         padx=5, sticky=E + W + S + N)

        self.canvas.bind("<ButtonPress-1>", self.get_pixel)

        abtn = Button(self, text="Point")
        abtn.grid(row=1, column=3)

        cbtn = Button(self, text="Close")
        cbtn.grid(row=1, column=4, pady=5, padx=5)

        hbtn = Button(self, text="Clear")
        hbtn.grid(row=5, column=0, padx=5)

        # obtn = Button(self, text="OK")
        # obtn.grid(row=5, column=3)


def main():
    root = Tk()
    root.resizable(width=False, height=False)
    app = MiniPaint(root)
    root.mainloop()


if __name__ == '__main__':
    main()

from Tkinter import Tk, Canvas, Frame, BOTH, NW
import Image 
import ImageTk

class ImageDrawer(Frame):

    def __init__(self, window, image_path):
        Frame.__init__(self, window)
        self.window = window
        self.image = Image.open(image_path)
        self.image_width, self.image_height = self.image.size

    def draw(self):
        photo_image = ImageTk.PhotoImage(self.image)

        self.window.title("High Tatras")
        self.pack(fill=BOTH, expand=1)

        canvas = self.create_canvas()
        canvas.create_image(10, 10, anchor=NW, image=photo_image)

        canvas.pack(fill=BOTH, expand=1)
        self.window.mainloop()

    def create_canvas(self):
        PADDING = 20
        canvas_width = self.image_width + PADDING
        canvas_height = self.image_height + PADDING

        return Canvas(self, width=canvas_width, height=canvas_height)


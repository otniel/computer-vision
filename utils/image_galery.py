__author__ = 'otniel'

import Image
import ImageTk
import Tkinter

image_list = ['mason.jpg', 'pitufo.png']
text_list = ['apple', 'bird']
current = 0

def move(delta):
    global current, image_list
    if not (0 <= current + delta < len(image_list)):
        tkMessageBox.showinfo('End', 'No more image.')
        return
    current += delta
    image = Image.open(image_list[current])
    image = image.resize((350, 350), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    label['text'] = text_list[current]
    label['image'] = photo
    label.photo = photo

root = Tkinter.Tk()

label = Tkinter.Label(root, compound=Tkinter.TOP)
label.pack()

frame = Tkinter.Frame(root)
frame.pack()

Tkinter.Button(frame, text='Previous picture', command=lambda: move(-1)).pack(side=Tkinter.LEFT)
Tkinter.Button(frame, text='Next picture', command=lambda: move(+1)).pack(side=Tkinter.LEFT)
Tkinter.Button(frame, text='Quit', command=root.quit).pack(side=Tkinter.LEFT)

move(0)

root.mainloop()
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import Plotter
from RpnCalc import *

root = Tk()
canvas = Frame(root)

mode = StringVar(root)
mode.set('Select a color mode')
OptionMenu_mode = OptionMenu(root, mode, "RGB", "HSV", "CMYK", "YCbCr")
OptionMenu_mode.grid(row=0, columnspan=2, column=0, padx=5, sticky=EW)

function1 = StringVar(root)
Label(root, text="Function 1 (R/H/C/Y): ").grid(row=1,column=0,sticky=W,padx=5)
Entry_function1 = Entry(root, textvariable=function1, width=20)
Entry_function1.grid(row=2, column=0, sticky=EW)

function2 = StringVar(root)
Label(root, text="Function 2 (G/S/M/Cb): ").grid(row=3,column=0,sticky=W,padx=5)
Entry_function2 = Entry(root, textvariable=function2)
Entry_function2.grid(row=4, column=0, sticky=EW)

function3 = StringVar(root)
Label(root, text="Function 3 (B/V/Y/Cr): ").grid(row=5,column=0,sticky=W,padx=5)
Entry_function3 = Entry(root, textvariable=function3)
Entry_function3.grid(row=6, column=0, sticky=EW)

function4 = StringVar(root)
function4.set('0')
Label(root, text="Function 4 (CMYK Only): ").grid(row=7,column=0,sticky=W,padx=5)
Entry_function4 = Entry(root, textvariable=function4)
Entry_function4.grid(row=8, column=0, sticky=EW)


def randomize_entry(event):
    expr = random_rpn_expr(.90)
    event.widget.variable.set(expr)

Button_random_function_1 = Button(root, text="Randomize Function 1")
Button_random_function_1.grid(row=1, column=1, padx=5, sticky=EW)
Button_random_function_1.variable=function1
Button_random_function_1.bind("<Button-1>", randomize_entry)

Button_random_function_2 = Button(root, text="Randomize Function 2")
Button_random_function_2.grid(row=3, column=1, padx=5, sticky=EW)
Button_random_function_2.variable=function2
Button_random_function_2.bind("<Button-1>", randomize_entry)

Button_random_function_3 = Button(root, text="Randomize Function 3")
Button_random_function_3.grid(row=5, column=1, padx=5, sticky=EW)
Button_random_function_3.variable=function3
Button_random_function_3.bind("<Button-1>", randomize_entry)

Button_random_function_4 = Button(root, text="Randomize Function 4")
Button_random_function_4.grid(row=7, column=1, padx=5, sticky=EW)
Button_random_function_4.variable=function4
Button_random_function_4.bind("<Button-1>", randomize_entry)


Button_make_img = Button(root, text="Create image")
Button_make_img.grid(row=4, column=5, padx=10, sticky=EW)
def generate_and_push_img(event):
    Label_pic.config(width = width.get())
    Label_pic.config(height = height.get())
    exprs = [function1.get(), function2.get(), function3.get()]
    if mode.get() == 'CMYK':
        exprs.append(function4.get())
    layers = [Plotter.make_plot_rpn(expr, width.get(), height.get()) for expr in exprs]
    img = Image.merge(mode.get(), layers)
    if mode.get() == 'RGB':
        img.save('render.bmp')
    else:
        img.convert('RGB').save('render.jpg')
    img = ImageTk.PhotoImage(img)
    Label_pic.image = img
    Label_pic.config(image = Label_pic.image)
Button_make_img.bind("<Button-1>", generate_and_push_img)

Label(root, text="Width:").grid(row=0,column=3,sticky=W,padx=5)
width = IntVar()
width.set(192)
Scale_width = Scale(root, from_=1920, to=1, orient=VERTICAL, variable=width, showvalue=0)
Scale_width.grid(row=1, rowspan=6, column=3, sticky=NS)
Entry_width = Entry(root, textvariable=width).grid(row=7, column=3, sticky=E)

Label(root, text="Height:").grid(row=0,column=4,sticky=W,padx=5)
height = IntVar()
height.set(108)
Scale_height = Scale(root, from_=1080, to=1, orient=VERTICAL, variable=height, showvalue=0)
Scale_height.grid(row=1, rowspan=6, column=4, sticky=NS)
Entry_height = Entry(root, textvariable=height).grid(row=7, column=4, sticky=E)


img_placeholder = ImageTk.PhotoImage(Image.new('RGB', (400, 400), 'white'))
display_img = img_placeholder
Label_pic = Label(root, image=display_img)
Label_pic.grid(row=0, rowspan=9, column=6, padx=10, pady=10, sticky=W)


root.mainloop()

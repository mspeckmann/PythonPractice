'''Melinda Speckmann
Assignment 4
Due 11/13/17'''


# Build GUI with tkinter (Tkinter in 2.X) with buttons that change color and grow

from tkinter import *
import tkinter.font as tkFont
import random

class MyGui:
    """
    A GUI with buttons that change color and make the label grow
    """
    colors = ['blue', 'green', 'orange', 'red', 'brown', 'yellow', 'pink']

    def __init__(self, parent, wintitle='popup', growing = True):
        #Implement per step 1
        self.parent = parent
        self.wintitle = wintitle
        self.parent.title(wintitle)
        self.growing = growing
        mainframe = Frame(parent)
        Button(mainframe, text = 'Spam', command=self.reply).pack(side = LEFT)
        Button(mainframe, text = 'Grow', command=self.grower).pack(side = LEFT)
        Button(mainframe, text = 'Stop', command=self.stop).pack(side = LEFT)
        self.customFont = tkFont.Font(family="Athelas", size =30)
        self.l = Label(parent, text="Hello", font = self.customFont)
        self.l.pack()
        mainframe.pack()

    def reply(self):
        #Implement per step 2
        self.start()
        self.grow()

    def grow(self):
        #Implement per step 3
        if self.growing:
            self.grower()
        self.l.after(500,self.grow)

    def grower(self):
        #Implement per step 4
        size = self.customFont['size']
        self.customFont.configure(size = size + 5)
        random.shuffle(self.colors)
        self.l.config(bg = self.colors[0])

    def stop(self):
        #Implement per step 5
        global growing
        self.growing = False

    def start(self):
        #Implement per step 5
        global growing
        self.growing = True

class MySubGui(MyGui):
    #Implement per step 6
    colors = ['grey', 'pink', 'purple', 'white','magenta']



#USE TO TEST CODE
MyGui(Tk(), 'main')
MyGui(Toplevel())
MySubGui(Toplevel())


mainloop()

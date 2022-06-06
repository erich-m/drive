#python version 3.7.2
#import packages from graphics
from doctest import master
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

#import packages for file and data management
import configparser
import json
from collections import OrderedDict#for reading from the json maintaining order of the dictionary

#import os and subprocess for path configurations and external program openings
import os
import subprocess

import copy



class Window(Tk):
    def __init__(self,name,w,h):
        super().__init__()
        self.title(name)
        self.minsize(w,h)
        self.resizable(False,False)

        self.frame = Frame(self)
        self.label = Label(self.frame,text="Hello World")
        self.label.pack()
        self.frame.pack()

class GeneralFrame(ttk.Frame):
    def __init__(self,parent,child):
        super().__init__()
        


window = Window("Export Configuration Manager",200,400)
window.mainloop()





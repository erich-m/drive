#python version 3.7.2
#import packages from graphics
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


#create the window class
class Window:
    def __init__(self,master):
        self.master = master

        #create the header frame
        self.header = Frame(self.master,highlightthickness=3,highlightbackground="black")
        
        self.title = Label(self.header,text="Description",font=config.get('guidata','headerfont'))
        self.description = Label(self.header,text="Use this application to configure the data exporting from SCANeR Studio.\nAny changes will affect data collected in future simulations",font=config.get('guidata','bodyfont'))
        self.instructions = Label(self.header,text="Add items to the list of current fields by selecting from the avaiable fields and pressing \"ADD\".\nRemove any fields from the current list by selecting a field and pressing \"REMOVE\".\nOrder the list by pressing \"MOVE UP\" and \"MOVE DOWN\".\nEdit any field properties in the properties section",font=config.get('guidata','smallerfont'))
        self.title.pack()
        self.description.pack()
        self.instructions.pack()

        self.header.pack(expand=True,fill='x')
        #create the header frame

        #list frames
        self.listframe = Frame(self.master,highlightthickness=3,highlightbackground="black")
        self.leftframe = Frame
        self.listframe.pack(expand=True,fill='x')
        #list frames

def initpath():#initialize the path to the directory that SCANeR Studio uses
    if str(os.getcwd()) != 'C:\\OKTAL\\SCANeRstudio_1.6\\data\GUELPH_DATA_1.6\\script\\python':
            os.chdir('C:\\OKTAL\\SCANeRstudio_1.6\\data\GUELPH_DATA_1.6\\script\\python')#this is the path that the python directory should be working from

initpath()#initializes the working directory
#set up the configuration file parser
config = configparser.ConfigParser()
config.read("settings.cfg")

#defaults are read into a list of function dictionary definitions
defaults = (json.load((open(config.get('guipaths','defaults'),encoding="utf8")),object_pairs_hook=OrderedDict)).values()
fields = [h["name"] for h in defaults if "name" in h]#fields are the function names accessed by the field name

included = list((json.load((open(config.get('guipaths','included'),encoding="utf8")),object_pairs_hook=OrderedDict)).values())

root = Tk()
window = Window(root)
#set title, size and disable resize
root.resizable(False,False)
root.title(config.get('guidata','main'))
root.iconbitmap("export.ico")
root.minsize(config.get('guidata','width'),config.get('guidata','height'))
root.mainloop()
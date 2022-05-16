#python version 3.7.2
from tkinter import *
from tkinter import ttk

import configparser
import json
from collections import OrderedDict#for reading from the json maintaining order of the dictionary

import os
import subprocess

class Window:
    def __init__(self,master):
        self.master = master

        self.header = Label(self.master,text="Description:",font=config.get('guidata','headerfont'))
        self.header.grid(row=0,column=0,columnspan=6)

        self.description = Label(self.master,text="Use this application to configure the data exporting from SCANeR Studio.\nSelect the data fields to edit and collect below.\nAny changes will affect data colelcted in future simulations",font=config.get('guidata','bodyfont'))
        self.description.grid(row=1,column=0,columnspan=6)

        self.separator1 = ttk.Separator(self.master,orient="horizontal")
        self.separator1.grid(row=2,column=0,columnspan=6,sticky="ew",pady=5)

        self.location = Label(self.master,text="File Location:" + config.get('guipaths','data'),font=config.get('guidata','smallfont'))
        self.location.grid(row=3,column=0,columnspan=6)

        self.opendata = Button(self.master,text="Open File Location",font=config.get('guidata','smallfont'),command=self.__openfilelocation)
        self.opendata.grid(row=4,column=0,columnspan=6)

        self.separator2 = ttk.Separator(self.master,orient="horizontal")
        self.separator2.grid(row=5,column=0,columnspan=6,sticky="ew",pady=5)

        self.filename = Label(self.master, text = "File Name: ",font=config.get('guidata','smallfont'),anchor="e")
        self.filename.grid(row=6,column=0,columnspan=2,sticky="e")

        self.nameentry = Entry(self.master,font=config.get('guidata','smallfont'))
        self.nameentry.insert("1",config.get('general','name'))
        self.nameentry.grid(row=6,column=2,columnspan=2,sticky="ew")

        self.suffix = Label(self.master,text=config.get('fixed','suffix'),font=config.get('guidata','smallfont'),anchor="w")
        self.suffix.grid(row=6,column=4,columnspan=2,sticky="w")

        self.filenamedesc = Label(self.master,text="The date and time of the simulation will be added to the file name during setup",font=config.get('guidata','smallfont'))
        self.filenamedesc.grid(row=7,column=0,columnspan=6)
       
        self.separator3 = ttk.Separator(self.master,orient="horizontal")
        self.separator3.grid(row=8,column=0,columnspan=6,sticky="ew",pady=5)

        self.currentlabel = Label(self.master,text="Current Fields:",font=config.get('guidata','bodyfont'))
        self.currentlabel.grid(row=9,column=0,columnspan=3)

        self.selectlabel = Label(self.master,text="Available Fields:",font=config.get('guidata','bodyfont'))
        self.selectlabel.grid(row=9,column=3,columnspan=3)

        self.selectlist = Listbox(self.master,selectmode=SINGLE)
        
        for f in range(len(fields)):
            self.selectlist.insert(f+1,fields[f])

        self.selectlist.grid(row=10,column=3,columnspan=3,sticky="ew",padx=5)

    def __openfilelocation(self):
        subprocess.Popen(config.get('guipaths','opendata'))


def initpath():
    if str(os.getcwd()) != 'C:\\OKTAL\\SCANeRstudio_1.6\\data\GUELPH_DATA_1.6\\script\\python':
            os.chdir('C:\\OKTAL\\SCANeRstudio_1.6\\data\GUELPH_DATA_1.6\\script\\python')#this is the path that the python directory should be working from

initpath()

config = configparser.ConfigParser()
config.read("settings.cfg")

included = (json.load((open(config.get('guipaths','included'))),object_pairs_hook=OrderedDict)).values()
fields = [h["name"] for h in included if "name" in h]

root = Tk()
window = Window(root)
#set title and minimum size
root.title(config.get('guidata','main'))
root.minsize(config.get('guidata','width'),config.get('guidata','height'))
root.mainloop()

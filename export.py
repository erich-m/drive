#python version 3.7.2
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

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

        self.opendata = Button(self.master,text="Open File Location",font=config.get('guidata','smallfont'),bg='cyan',command=self.__openfilelocation)
        self.opendata.grid(row=4,column=0,columnspan=6)

        self.separator2 = ttk.Separator(self.master,orient="horizontal")
        self.separator2.grid(row=5,column=0,columnspan=6,sticky="ew",pady=5)

        self.filename = Label(self.master, text = "Save as: ",font=config.get('guidata','smallfont'),anchor="e")
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

        self.rightframe = Frame(self.master)
        self.selectlist = Listbox(self.rightframe,selectmode=SINGLE,font=config.get('guidata','smallfont'),activestyle='none')
        
        self.selectlist.pack(side="left",fill=BOTH)

        self.scrollbarright = Scrollbar(self.rightframe)
        self.scrollbarright.pack(side="right",fill=BOTH)

        for f in range(len(fields)):
            self.selectlist.insert(f+1,fields[f])

        self.selectlist.config(yscrollcommand=self.scrollbarright.set)
        self.scrollbarright.config(command=self.selectlist.yview)

        self.rightframe.grid(row=10,column=3,columnspan=3,padx=5)

        self.leftframe = Frame(self.master)
        self.includelist = Listbox(self.leftframe,selectmode=SINGLE,font=config.get('guidata','smallfont'),activestyle='none')

        self.includelist.pack(side="left",fill=BOTH)

        self.scrollbarleft = Scrollbar(self.leftframe)
        self.scrollbarleft.pack(side="right",fill=BOTH)

        self.includelist.config(yscrollcommand=self.scrollbarleft.set)
        self.scrollbarleft.config(command=self.includelist.yview)

        self.leftframe.grid(row=10,column=0,columnspan=3,padx=5)

        self.separator4 = ttk.Separator(self.master,orient="horizontal")
        self.separator4.grid(row=11,column=0,columnspan=6,sticky="ew",pady=5)

        self.separator5 = ttk.Separator(self.master,orient="horizontal")
        self.separator5.grid(row=13,column=0,columnspan=6,sticky="ew",pady=5)

        self.save = Button(self.master,text="Save Configuration",font=config.get('guidata','bodyfont'),bg='green',command=self.__saveconfig)
        self.save.grid(row=14,column=0,columnspan=3,pady=5)

        self.save = Button(self.master,text="Cancel Configuration",font=config.get('guidata','bodyfont'),bg='red',command=self.__openmessagebox)
        self.save.grid(row=14,column=3,columnspan=3,pady=5)

        self.addremove = Frame(self.master)
        self.add = Button(self.addremove,text="Add Field",font=config.get('guidata','smallfont'),command=self.__addinclude)
        self.add.pack(side="top",fill=BOTH,pady=5)
        self.remove = Button(self.addremove,text="Remove Field",font=config.get('guidata','smallfont'))
        self.remove.pack(side="bottom",fill=BOTH,pady=5)
        self.addremove.grid(row=12,column=0,columnspan=3)

    def __openfilelocation(self):
        subprocess.Popen(config.get('guipaths','opendata'))

    def __openmessagebox(self):
        self.cancel = messagebox.askquestion('Cancel?','Cancelling will not save any configurations. Do you wish to cancel?')
        if self.cancel == 'yes':
            self.master.destroy()

    def __addinclude(self):
        try:
            print(self.selectlist.get(self.selectlist.curselection()))
        except Exception:
            pass


#file names cannot have \/:*?"<>|
#warn that settings are unverified (for vehicles that dont exist)
    def __saveconfig(self):

        print("saving configurations")
        self.master.destroy()


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

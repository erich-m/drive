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

        self.recent = ""
        #header label
        self.header = Label(self.master,text="Description:",font=config.get('guidata','headerfont'))
        self.header.grid(row=0,column=0,columnspan=6)
        #configurator description
        self.description = Label(self.master,text="Use this application to configure the data exporting from SCANeR Studio.\nAny changes will affect data collected in future simulations",font=config.get('guidata','bodyfont'))
        self.description.grid(row=1,column=0,columnspan=6)

        #instructions
        self.instructions = Label(self.master,text="Add items to the list of current fields by selecting from the avaiable fields and pressing \"ADD\".\nRemove any fields from the current list by selecting a field and pressing \"REMOVE\".\nOrder the list by pressing \"MOVE UP\" and \"MOVE DOWN\".\nEdit any field properties in the properties section",font=config.get('guidata','smallerfont'))
        self.instructions.grid(row=2,column=0,columnspan=6)
        #separator for visuals
        self.separator1 = ttk.Separator(self.master,orient="horizontal")
        self.separator1.grid(row=3,column=0,columnspan=6,sticky="ew",pady=5)

        #headers for the selection lists
        self.listheaders = Frame(self.master)
        currentlabel = Label(self.listheaders,text="Current Fields:",font=config.get('guidata','headerfont'))
        currentlabel.pack(side="left",fill=BOTH,padx=75)

        self.selectlabel = Label(self.listheaders,text="Available Fields:",font=config.get('guidata','headerfont'))
        self.selectlabel.pack(side="right",fill=BOTH,padx=75)
        self.listheaders.grid(row=4,column=0,columnspan=6)

        #field boxes
        self.centerframe = Frame(self.master)
        self.rightframe = Frame(self.centerframe)
        self.selectlist = Listbox(self.rightframe,selectmode=SINGLE,font=config.get('guidata','smallfont'),activestyle='none',width=25,bd=3)
        self.selectlist.bind("<<ListboxSelect>>",lambda event,directed="right":self.__update(directed))
        
        self.selectlist.pack(side="left",fill=BOTH)

        self.scrollbarright = Scrollbar(self.rightframe)
        self.scrollbarright.pack(side="right",fill=BOTH,expand=True)

        for f in range(len(fields)):
            self.selectlist.insert(f+1,fields[f])

        self.selectlist.config(yscrollcommand=self.scrollbarright.set)
        self.scrollbarright.config(command=self.selectlist.yview)

        self.rightframe.pack(side="right",fill=BOTH,padx=30)

        self.leftframe = Frame(self.centerframe)
        self.includelist = Listbox(self.leftframe,selectmode=SINGLE,font=config.get('guidata','smallfont'),activestyle='none',width=25,bd=3)
        self.includelist.bind("<<ListboxSelect>>",lambda event,directed="left":self.__update(directed))

        self.includelist.pack(side="left",fill=BOTH)

        self.scrollbarleft = Scrollbar(self.leftframe)
        self.scrollbarleft.pack(side="right",fill=BOTH)

        self.includelist.config(yscrollcommand=self.scrollbarleft.set)
        self.scrollbarleft.config(command=self.includelist.yview)

        self.leftframe.pack(side="left",fill=BOTH,padx=30)
        self.centerframe.grid(row=5,column=0,columnspan=6)

    #separator
        self.separator2 = ttk.Separator(self.master,orient="horizontal")
        self.separator2.grid(row=6,column=0,columnspan=6,sticky="ew",pady=5)

        #list manager buttons
        self.listmanagerbuttons = Frame(self.master)
        self.remove = Button(self.listmanagerbuttons,text="REMOVE -->",font=config.get('guidata','bodyfont'),command=self.__removeinclude,width=15)
        self.remove.grid(row=0,column=0,columnspan=1,padx=2)
        self.up = Button(self.listmanagerbuttons,text="MOVE UP",font=config.get('guidata','bodyfont'),command=self.__moveup,width=15)
        self.up.grid(row=0,column=1,columnspan=1,padx=2)
        self.down = Button(self.listmanagerbuttons,text="MOVE DOWN",font=config.get('guidata','bodyfont'),command=self.__movedown,width=15)
        self.down.grid(row=0,column=2,columnspan=1,padx=2)
        self.add = Button(self.listmanagerbuttons,text="<-- ADD",font=config.get('guidata','bodyfont'),command=self.__addinclude,width=15)
        self.add.grid(row=0,column=3,columnspan=1,padx=2)
        self.listmanagerbuttons.grid(row=7,column=0,columnspan=6)

        #separator
        self.separator3 = ttk.Separator(self.master,orient="horizontal")
        self.separator3.grid(row=8,column=0,columnspan=6,sticky="ew",pady=5)

        self.propheader = Label(self.master,text="Field Properties",font=config.get('guidata','headerfont'),anchor="w")
        self.propheader.grid(row=9,column=0,columnspan=6,sticky="ew",padx=5,pady=5)

        #property frame
        self.propframe = Frame(self.master)
        self.descriptionframe = Frame(self.propframe)

        self.descriptionscroll = Scrollbar(self.descriptionframe,orient='vertical')
        self.descriptionscroll.pack(side="right",fill="y")

        self.fielddescription = Text(self.descriptionframe,wrap="word",width=39,height=6,bd=3,font=config.get('guidata','smallfont'),yscrollcommand=self.descriptionscroll.set)
        self.fielddescription.insert(END,"Class: \nDescription: ")
        self.fielddescription.config(state=DISABLED)

        self.descriptionscroll.config(command=self.fielddescription.yview)
        self.fielddescription.pack(side="left",fill=BOTH,expand=False)

        self.descriptionframe.pack(side="left",fill=BOTH,expand=False)

        self.editframe = Frame(self.propframe)
        self.editframe.pack(side="right",fill=BOTH,expand=True)

        self.field = Frame(self.editframe)
        self.noentry = Label(self.field,text="No Properties to Edit",font=config.get('guidata','bodyfont'))
        self.noentry.pack()
        self.field.pack()

        self.finallist = []

        self.propframe.grid(row=10,column=0,columnspan=6,sticky="ew")

        #separator
        self.separator4 = ttk.Separator(self.master,orient="horizontal")
        self.separator4.grid(row=11,column=0,columnspan=6,sticky="ew",pady=5)

        self.filename = Label(self.master, text = "Save as: ",font=config.get('guidata','smallfont'),anchor="e")
        self.filename.grid(row=12,column=1,columnspan=1,sticky="e")

        self.nameentry = Entry(self.master,font=config.get('guidata','smallfont'))
        self.nameentry.insert("1",config.get('general','name'))
        self.nameentry.grid(row=12,column=2,columnspan=2,sticky="ew")

        self.suffix = Label(self.master,text=config.get('fixed','suffix'),font=config.get('guidata','smallfont'),anchor="w")
        self.suffix.grid(row=12,column=4,columnspan=1,sticky="w")

        self.filenamedesc = Label(self.master,text="The date and time of the simulation will be added to the file name during setup",font=config.get('guidata','smallfont'))
        self.filenamedesc.grid(row=13,column=0,columnspan=6)

        #separator
        self.separator5 = ttk.Separator(self.master,orient="horizontal")
        self.separator5.grid(row=14,column=0,columnspan=6,sticky="ew",pady=5)

        #save and cancel buttons
        self.exitframe = Frame(self.master)
        self.save = Button(self.exitframe,text="Save Configuration",font=config.get('guidata','bodyfont'),bg='green',command=self.__savebox)
        self.save.pack(side="left",fill=BOTH,padx=50,pady=5)

        self.save = Button(self.exitframe,text="Cancel Configuration",font=config.get('guidata','bodyfont'),bg='red',command=self.__cancelbox)
        self.save.pack(side="right",fill=BOTH,padx=50,pady=5)
        self.exitframe.grid(row=15,column=0,columnspan=6)

        #separator
        self.separator6 = ttk.Separator(self.master,orient="horizontal")
        self.separator6.grid(row=16,column=0,columnspan=6,sticky="ew",pady=5)
        
        #file location
        self.location = Label(self.master,text="Data files are created and stored in the folder below during the simulation.\nFile Location:" + config.get('guipaths','data'),font=config.get('guidata','smallfont'))
        self.location.grid(row=17,column=0,columnspan=6)

        self.opendata = Button(self.master,text="Open File Location",font=config.get('guidata','smallfont'),command=self.__openfilelocation)
        self.opendata.grid(row=18,column=0,columnspan=6)

        #separator
        self.separator7 = ttk.Separator(self.master,orient="horizontal")
        self.separator7.grid(row=19,column=0,columnspan=6,sticky="ew",pady=5)

    def __update(self,directed):
        leftselect = self.includelist.curselection()
        rightselect = self.selectlist.curselection()
        
        if len(leftselect) > len(rightselect) and directed == "left":#selected item from left list
            # print("selected item from left")
            self.__fieldupdates("left")
        elif len(leftselect) < len(rightselect) and directed == "right":#selected item from right list
            # print("item selected from right")
            self.__fieldupdates("right")
        else:#no item selected
            pass

    def __fieldupdates(self,directed):
        fromlist = ""
        name = ""
        if directed == "left":
            name = self.includelist.get(self.includelist.curselection())
            fromlist = "left"
        elif directed == "right":
            name = self.selectlist.get(self.selectlist.curselection())
            fromlist = "right"
        else:
            return
        
        self.recent = name
        #Update the function description
        func = (next(f for f in defaults if f["name"] == name))
        description = "Class: " + func["class"] + "\nDescription: " + func["description"]
        self.fielddescription.config(state=NORMAL)
        self.fielddescription.delete("1.0",END)
        self.fielddescription.insert(END,description)
        self.fielddescription.config(state=DISABLED)

        self.propheader.config(text="Field Properties: " + func["name"])

        for child in self.editframe.winfo_children():
            child.destroy()

        argc = func["argc"]
        argvkeys = list(func["argv"].keys())
        argvvalues = list(func["argv"].values())
        # print("values",argvvalues)
        if argc == 0:
            self.field = Frame(self.editframe)
            self.noentry = Label(self.field,text="No Properties to Edit",font=config.get('guidata','bodyfont'))
            self.noentry.pack()
            self.field.pack()
        else:
            for a in range(argc):
                self.field = Frame(self.editframe)
                self.entrylabel = Label(self.field,text=argvkeys[a] + ":",font=config.get('guidata','bodyfont'))
                self.entrylabel.pack(side="left")
                if fromlist == "left":#if left list, show properties of what is in the current list
                    # print("show properties from the current list")
                    current = self.finallist[self.includelist.curselection()[0]]
                    self.displayfield = Label(self.field,text=list(current["argv"].values())[a],font=config.get('guidata','bodyfont'))
                    self.displayfield.pack(side="right")
                else:
                    validation = self.editframe.register(self.__numvalidate)
                    self.entryfield = Entry(self.field,validate="key",validatecommand=(validation,'%P'),font=config.get('guidata','bodyfont'))
                    self.entryfield.insert(END,argvvalues[a])
                    self.entryfield.pack(side="right")
                self.field.pack()

    def __openfilelocation(self):
        subprocess.Popen(config.get('guipaths','opendata'))

    def __cancelbox(self):
        cancel = messagebox.askquestion('Cancelling...','Cancelling will not save any configurations. Do you wish to cancel?',icon='warning')
        if cancel == 'yes':
            self.master.destroy()

    def __numvalidate(self,p):#validate the entry widget for the field by checking what the value of the entry will be if the character is accepted
        return len(p) <= 5 and p.isdigit() or len(p) == 0

    def __addinclude(self):#adding moves from right to left
        try:
            name = self.recent
            self.includelist.insert(END,name)#add to the include list display

            func = (next(f for f in defaults if f["name"] == name))
            fielddata = []
            for primary in self.editframe.winfo_children():
                for secondary in primary.winfo_children():
                    if isinstance(secondary,Entry):
                        data = secondary.get()
                        fielddata.append(data)
            func["argv"] = dict(zip(list(func["argv"].keys()),fielddata))
            self.finallist.append(func)
            # print(self.finallist)
        except Exception:
            pass

    def __removeinclude(self):
        try:
            selection = self.includelist.curselection()
            self.includelist.delete(self.includelist.curselection())
            # print("remove from list",selection[0])
            del self.finallist[selection[0]]
            # print(self.finallist)
        except Exception:
            pass

    def __moveup(self):
        try:
            current = self.includelist.curselection()[0]
            if not current:
                return
            text = self.includelist.get(current)
            self.includelist.delete(current)
            self.includelist.insert(current-1,text)
        except Exception:
            pass
            
    def __movedown(self):
        try:
            current = self.includelist.curselection()[0]
            text=self.includelist.get(current)
            self.includelist.delete(current)
            self.includelist.insert(current+1, text)
        except Exception:
            pass

#file names cannot have \/:*?"<>|
#warn that settings are unverified (for vehicles that dont exist)
    def __savebox(self):
        functionnames = list(range(len(self.finallist)))
        finalwrite = dict(zip(functionnames,self.finallist))
        # print(finalwrite)
        with open(config.get('guipaths','included'),"w") as included:
            json.dump(finalwrite,included)

        messagebox.showwarning('Saving...','All settings are unverfied and may not operate as intended. Errors may arise during simulation process',icon='info')
        self.master.destroy()

def initpath():
    if str(os.getcwd()) != 'C:\\OKTAL\\SCANeRstudio_1.6\\data\GUELPH_DATA_1.6\\script\\python':
            os.chdir('C:\\OKTAL\\SCANeRstudio_1.6\\data\GUELPH_DATA_1.6\\script\\python')#this is the path that the python directory should be working from

initpath()

config = configparser.ConfigParser()
config.read("settings.cfg")

defaults = (json.load((open(config.get('guipaths','defaults'),encoding="utf8")),object_pairs_hook=OrderedDict)).values()
fields = [h["name"] for h in defaults if "name" in h]


includefields = []

root = Tk()
window = Window(root)
#set title and minimum size
root.resizable(False,False)
root.title(config.get('guidata','main'))
root.minsize(config.get('guidata','width'),config.get('guidata','height'))
root.mainloop()

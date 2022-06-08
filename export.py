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
    def __init__(self,master,currentconfig):
        self.master = master

        self.recent = ""
        self.finallist = currentconfig

        for s  in range(1,15,2):
            self.separator = ttk.Separator(self.master,orient="horizontal")
            self.separator.grid(row=s,column=0,columnspan=6,sticky="ew",pady=5)

        self.headerframe = Frame(self.master)
        #header label
        self.header = Label(self.headerframe,text="Description:",font=config.get('guidata','headerfont'))
        self.header.pack()
        #configurator description
        self.description = Label(self.headerframe,text="Use this application to configure the data exporting from SCANeR Studio.\nAny changes will affect data collected in future simulations",font=config.get('guidata','bodyfont'))
        self.description.pack()

        #instructions
        self.instructions = Label(self.headerframe,text="Add items to the list of current fields by selecting from the avaiable fields and pressing \"ADD\".\nRemove any fields from the current list by selecting a field and pressing \"REMOVE\".\nOrder the list by pressing \"MOVE UP\" and \"MOVE DOWN\".\nEdit any field properties in the properties section",font=config.get('guidata','smallerfont'))
        self.instructions.pack()
        self.headerframe.grid(row=0,column=0,columnspan=6)

        self.centerframe = Frame(self.master)
        #headers for the selection lists
        self.listheaders = Frame(self.centerframe)
        currentlabel = Label(self.listheaders,text="Current Fields:",font=config.get('guidata','headerfont'))
        currentlabel.pack(side="left",fill=BOTH,padx=75)

        self.selectlabel = Label(self.listheaders,text="Available Fields:",font=config.get('guidata','headerfont'))
        self.selectlabel.pack(side="right",fill=BOTH,padx=75)
        self.listheaders.pack(side="top")

        #field boxes
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
        for d in range(len(self.finallist)):
            self.includelist.insert(d,self.finallist[d]["name"])

        self.includelist.pack(side="left",fill=BOTH)

        self.scrollbarleft = Scrollbar(self.leftframe)
        self.scrollbarleft.pack(side="right",fill=BOTH)

        self.includelist.config(yscrollcommand=self.scrollbarleft.set)
        self.scrollbarleft.config(command=self.includelist.yview)

        self.leftframe.pack(side="left",fill=BOTH,padx=30)
        self.centerframe.grid(row=2,column=0,columnspan=6)

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
        self.listmanagerbuttons.grid(row=4,column=0,columnspan=6)

        self.propframe = Frame(self.master)
        self.propheader = Label(self.propframe,text="Field Properties",font=config.get('guidata','headerfont'),anchor="w")
        self.propheader.pack(side="top",fill=BOTH)

        #property frame
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

        self.propframe.grid(row=6,column=0,columnspan=6,sticky="ew")

        self.filenameframe = Frame(self.master)

        self.filenamedesc = Label(self.filenameframe,text="The date and time of the simulation will be added to the file name during setup",font=config.get('guidata','smallfont'))
        self.filenamedesc.pack(side="bottom",fill=BOTH)

        self.filename = Label(self.filenameframe, text = "Save as: ",font=config.get('guidata','smallfont'),anchor="e")
        self.filename.pack(side="left",fill=BOTH,expand=True)

        self.nameentry = Entry(self.filenameframe,font=config.get('guidata','smallfont'))
        self.nameentry.insert("1",config.get('general','name'))
        self.nameentry.pack(side="left",fill=BOTH,expand=True)

        self.suffix = Label(self.filenameframe,text=config.get('fixed','suffix'),font=config.get('guidata','smallfont'),anchor="w")
        self.suffix.pack(side="left",fill=BOTH,expand=True)
        
        self.filenameframe.grid(row=8,column=0,columnspan=6,sticky="ew")

        #save and cancel buttons
        self.exitframe = Frame(self.master)
        self.save = Button(self.exitframe,text="Save Configuration",font=config.get('guidata','bodyfont'),bg='green',command=self.__savebox)
        self.save.pack(side="left",fill=BOTH,padx=50,pady=5)

        self.save = Button(self.exitframe,text="Cancel Configuration",font=config.get('guidata','bodyfont'),bg='red',command=self.__cancelbox)
        self.save.pack(side="right",fill=BOTH,padx=50,pady=5)
        self.exitframe.grid(row=10,column=0,columnspan=6)

        #separator
        self.separator6 = ttk.Separator(self.master,orient="horizontal")
        self.separator6.grid(row=11,column=0,columnspan=6,sticky="ew",pady=5)
        
        self.filelocationframe = Frame(self.master)
        #file location
        self.location = Label(self.filelocationframe,text="Data files are created and stored in the folder below during the simulation.\nFile Location:" + config.get('guipaths','data'),font=config.get('guidata','smallfont'))
        self.location.pack(side="top")

        self.opendata = Button(self.filelocationframe,text="Open File Location",font=config.get('guidata','smallfont'),command=self.__openfilelocation)
        self.opendata.pack(side="bottom")
        self.filelocationframe.grid(row=12,column=0,columnspan=6,sticky="ew")

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
            # print(func)
            self.finallist.append(func.copy())
            print(self.finallist)
            # print(self.finallist)
        except Exception:
            pass

    def __removeinclude(self):#removes item from list
        try:
            selection = self.includelist.curselection()
            self.includelist.delete(self.includelist.curselection())
            # print("remove from list",selection[0])
            del self.finallist[selection[0]]
            # print(self.finallist)
        except Exception:
            pass

    def __moveup(self):#moves item up in the left list
        try:
            current = self.includelist.curselection()[0]
            if not current:
                return
            text = self.includelist.get(current)
            self.includelist.delete(current)
            self.includelist.insert(current-1,text)

            self.finallist[current-1],self.finallist[current] = self.finallist[current],self.finallist[current-1]
        except Exception:
            pass
            
    def __movedown(self):#moves item down in the left list
        try:
            current = self.includelist.curselection()[0]
            text=self.includelist.get(current)
            self.includelist.delete(current)
            self.includelist.insert(current+1, text)

            self.finallist[current+1],self.finallist[current] = self.finallist[current],self.finallist[current+1]
        except Exception:
            pass

#file names cannot have \/:*?"<>|
    def __savebox(self):
        functionnames = list(range(len(self.finallist)))
        finalwrite = dict(zip(functionnames,self.finallist))

        nameoffile = self.nameentry.get()


        #TODO: Check and update the file name
        badchars = "\/:*?<>|"
        if not any(c in nameoffile for c in badchars):
            config.set('general','name',nameoffile)
            with open("settings.cfg","w") as configfile:
                config.write(configfile)

            # print(finalwrite)
            with open(config.get('guipaths','included'),"w") as included:
                json.dump(finalwrite,included)

            messagebox.showwarning('Saving...','All settings are unverfied and may not operate as intended. Errors may arise during simulation process',icon='info')
            self.master.destroy()
        else:
            messagebox.showerror('Save Failed','File names cannot contain any of the following characters: \/:*?<>|')

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
window = Window(root,included)
#set title, size and disable resize
root.resizable(False,False)
root.title(config.get('guidata','main'))
root.iconbitmap("export.ico")
root.minsize(config.get('guidata','width'),config.get('guidata','height'))
root.mainloop()
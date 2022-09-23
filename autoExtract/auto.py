from tkinter import *

class Window:
    def __init__(self,master):
        self.master = master

        self.headerframe = Frame(self.master)

        self.header = Label(self.headerframe,text="Description",font="Tahoma 15 bold")
        self.header.pack()

        self.description = Label(self.headerframe,text="Use this application to configure the automatic exporting of data from SCANeR Studio.",font="Tahoma 13")
        self.description.pack()

        self.instructions = Label(self.headerframe,text="Instructions:",font="Tahoma 13")
        self.instructions.pack()

        self.headerframe.grid(row=0,column=0,columnspan=6)
        

root = Tk()
window = Window(root)

root.resizable(False,False)
root.title("Automatic Extracter")
root.minsize(550,700)
root.mainloop()

#coding: UTF-8
import mice#for scaner studio functions
import os #use for path navigation

# import customcsv as csvw
#path: C:\OKTAL\SCANeRstudio_1.6\bin\x64

class customcsv:#custom csv writer to write to csv without extra newline characters
    def __init__(self,filename,delim,headers):#constructor to get the file name, headers, and deliminator for the file
        self.filename = filename#csv file name
        self.delim = delim#csv deliminator (separator)
        self.headers = headers#headers for the csv file

        self.state = False#keeps track of the state of the file for the writer object

        self.mode = "a"#if the file does not exist, the file is created to append to

        self.__writercreate()#create the writer by opening the file

    def __initpath(self):#ensure the path is set to the correct location
        if str(os.getcwd()) != 'M:\\SCANeRstudio_1.6\\data\\GUELPH_DATA_1.6\\script\\python':#this is the path that
            os.chdir('M:\\SCANeRstudio_1.6\\data\\GUELPH_DATA_1.6\\script\\python')

    def __writercreate(self):
        try:#attempt to open the designated file and then set the open state to True for the instance
            self.__initpath()
            self.file = open(self.filename,self.mode)

            self.state = True
            return 1
        except Exception as e:#if there are file errors, they will be caught here
            self.state = False
            return 0

    def writerclose(self):#close the file
        if self.state:
            self.file.close()
            self.state = False

    def writeheaders(self):#write the headers to the csv file
        if self.state:
            string = ""
            for h in self.headers:#loop through the array of headers and print them out to the file with the deliminator
                string += h
                string += self.delim
            string += "\n"

            self.file.write(string)

    def writedata(self,data):#write the data to the csv file
        if self.state:
            string = ""
            for h in self.headers:
                current = str(data.get(h))
                if current != None:
                    string += current
                string += self.delim
            string += "\n"

            self.file.write(string)

def gettimecode():#retrieves the values fromt he variables to get the right code for the file
    #fail if any of the date variables are not set
    if int(mice.variables["year"]) == -1 or int(mice.variables["month"]) == -1 or int(mice.variables["day"]) == -1 or int(mice.variables["hour"]) == -1 or int(mice.variables["minute"]) == -1 or int(mice.variables["second"]) == -1:
        return -1
    year = str(int(mice.variables["year"]))
    month = str(int(mice.variables["month"])).zfill(2)
    day = str(int(mice.variables["day"])).zfill(2)
    hour = str(int(mice.variables["hour"])).zfill(2)
    minute = str(int(mice.variables["minute"])).zfill(2)
    second = str(int(mice.variables["second"])).zfill(2)

    code = year + month + day + hour + minute + second
    return code

def main():
    headers = ["Timestamp","Position X","Position Y"]

    folder = "data/"
    name = "test"
    code = gettimecode()

    if code == -1:
        return code

    suffix = ".csv"
    file = folder + name + "-" + code + suffix

    writer = customcsv(file,";",headers)
    timestamp = mice.getScenarioClock()
    posx = mice.vehicles.values()[0].pos[0]
    posy = mice.vehicles.values()[0].pos[1]
    
    writer.writedata({"Timestamp":timestamp,"Position X":posx,"Position Y":posy})

    writer.writerclose()
    return 1#return 1 on success

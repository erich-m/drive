#python version 2.7.11
#coding: UTF-8
import mice#for scaner studio functions
import os #use for path navigation

from datetime import datetime as dt

import sys

import ConfigParser

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
                current = data.get(h)
                if current != None:
                    string += current
                string += self.delim
            string += "\n"

            self.file.write(string)

def settimecode():#time code is used for saving the files with different names and not overwriting already existing data
    #get the time data for the file code
        current = dt.now()
        year = current.year
        month = current.month
        day = current.day
        hour = current.strftime("%H")#get 24 hour value
        minute = current.minute
        second = current.second
        code = str(year) + str(month).zfill(2) + str(day).zfill(2) + str(hour).zfill(2) + str(minute).zfill(2) +str(second).zfill(2)
        
        #save into the correct variables scaner variables have to be less than ~32000
        mice.variables["year"] = float(year)
        mice.variables["month"] = float(month)
        mice.variables["day"] = float(day)
        mice.variables["hour"] = float(hour)
        mice.variables["minute"] = float(minute)
        mice.variables["second"] = float(second)

        return code
        
def main():
    print("info: ",sys.version_info)
    print("path: ",sys.executable)

    config = ConfigParser.ConfigParser()
    config.read("M:/SCANeRstudio_1.6/data/GUELPH_DATA_1.6/script/python/settings.cfg")

    headers = ["Timestamp","Position X","Position Y"]

    folder = config.get('general','folder')
    name = config.get('name')
    code = settimecode()
    
    suffix = config.get('suffix')
    file = folder + name + "-" + code + suffix
    
    writer = customcsv(file,config.get('general','delim'),headers)#create the new csv file

    writer.writeheaders()#write the headers

    writer.writerclose()#close the file
    return 1#return 1 on success
#python version 2.7.11
#coding: UTF-8
import mice#for scaner studio functions
import os #use for path navigation

from datetime import datetime as dt

import sys

import ConfigParser#for reading paths, settings and csv configurations

import json#for reading function definitions
from collections import OrderedDict#for reading from the json maintaining order of the dictionary

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
        if str(os.getcwd()) != 'M:\\SCANeRstudio_1.6\\data\\GUELPH_DATA_1.6\\script\\python':
            os.chdir('M:\\SCANeRstudio_1.6\\data\\GUELPH_DATA_1.6\\script\\python')#this is the path that the python directory should be working from

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

        return code

def main():
    #debug print python details
    print("python version: ",sys.version_info)
    print("python path: ",sys.executable)

    #create configparser to read the settings and standards from the configuration file
    config = ConfigParser.ConfigParser()
    config.read("M:/SCANeRstudio_1.6/data/GUELPH_DATA_1.6/script/python/settings.cfg")
    
    #*Headers are the function names that are in the include.json
    """ 1. open the json file "include.json", which contains the functions and the set parameters for the data collection
        2. load the file as a python dictionary with the json.loads function which contains keys (scaner function names) 
        and values (name, function call, class, argument count and arguments to format into string)
        3. convert the dictionary of function key/value pairs into a list of function definitions
        4. iterate through the list of function definitions. for each definition, get the value by 
        the key "name" and create a list of all the names, only if the key exists (which it should unless it is changed in the future
        The dictionary then applies OrderedDict to maintain the order than they appear in the json file originally"""
    included = (json.load((open(config.get('paths','included'))),object_pairs_hook=OrderedDict)).values()
    headers = [h["name"] for h in included if "name" in h]

    folder = config.get('fixed','folder')#get folder name from config
    name = config.get('general','name')#get file name from config
    code = settimecode()#get timestamp for file name
    
    suffix = config.get('fixed','suffix')#get file type from config
    file = folder + name + "-" + code + suffix

    writer = customcsv(file,config.get('fixed','delim'),headers)#create the new csv file
    writer.writeheaders()#write the headers
    writer.writerclose()#close the file

    filepath = config.get('paths','recent') + file#get full path for the csv file
    config.set('paths','datafile',filepath)#set to the datapth field in the cfg file
    with open(config.get('paths','configuration'),'w') as settings:
        config.write(settings)#write the new file name to the settings file

    return 1#return 1 on success
#python version 2.7.11
#coding: UTF-8
import mice#for scaner studio functions
import os #use for path navigation

from datetime import datetime as dt#import datetime for the timestamps on the csv file names

import sys#import sys for the system information

import ConfigParser#import configparser to be able to read/write tot he configuration file (the file contains paths, settings etc)

import json#import json to be able to read from the list of functions for the data to collect
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
        if not self.state:#if the writer is not currently activated yet
            try:#attempt to open the designated file and then set the open state to True for the instance
                self.__initpath()#initialize the path if needed to operate in the correct directory
                self.file = open(self.filename,self.mode)

                self.state = True#set the state to true
                return 1
            except Exception:#if there are file errors, they will be caught here
                self.state = False
                return -1

    def writerclose(self):#close the file
        if self.state:#if the file is open, close it and set the open state to false
            self.file.close()
            self.state = False

    def writeheaders(self):#write the headers to the csv file
        if self.state:
            string = ""
            for h in self.headers:#loop through the array of headers and print them out to the file with the deliminator
                string += h + self.delim
            string += "\n"

            self.file.write(string)

    def writedata(self,data):#write the data to the csv file
        if self.state:#if the writer is active, create a string, and loop through the list of defined headers
            string = ""
            for h in self.headers:
                current = str(data.get(h))#for each header, get the corresponding value associated with it as a string
                if current != None:#if the value is not empty, write the value
                    string += current
                string += self.delim#always write a deliminator to separate columns
            string += "\n"#write a single newline

            self.file.write(string)#write to the file

def main():
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

    if mice.isScenarioBeginning():#run setup on first loop through the script
        #debug print python details
        print("python version: ",sys.version_info)
        print("python path: ",sys.executable)

        #set up the file name from the configuration settings file
        folder = config.get('fixed','folder')#get folder name from config
        name = config.get('general','name')#get file name from config
        code = dt.now().strftime("%Y%j%H%M%S")#get timestamp for the csv file formatted as: year, day of year, time
        suffix = config.get('fixed','suffix')#get file type from config
        prepfile = folder + name + "-" + code + suffix#get the csv file that is set up

        writer = customcsv(prepfile,config.get('fixed','delim'),headers)#create the new csv file
        writer.writeheaders()#write the headers

        filepath = config.get('paths','recent') + prepfile#get full path for the csv file
        config.set('paths','datafile',filepath)#set to the datapth field in the cfg file
        with open(config.get('paths','configuration'),'w') as settings:
            config.write(settings)#write the new file name to the settings file
    #run export procedures to get the data from the simulation and then write it to the csv file
    file = config.get('paths','datafile')#read from the config file for the csv code

    writer = customcsv(file,config.get('fixed','delim'),headers)

    """ Similar to above...instead of getting the values at the key "name", the values from "function" key
    are retrieved and then formatted using % tuple(list) method to replace %s indicators in the function. The list
    comes from the value at key "argv"...only if both fields are in the dictionary (which they should be unless the code is changed
    map then applies the python function "eval" to each of the function calls in the "calls" array """
    calls = [(f["function"] % tuple(f["argv"].values())) for f in included if ("function" in f and "argv" in f)]#call
    results = map(eval,calls)
    #take the header and the results and join the arrays into a key value pair 
    data = dict(zip(headers,results))

    writer.writedata(data)#write the data to the csv using class method

    writer.writerclose()#close the file
    return 1#return 1 on success

    #*Complete By Wednesday
    #TODO: Create GUI to edit the JSON file of includes...pull the function defs from the defaults.json
    #TODO: Do testing of the entire list of functions so far
    #TODO: Add to Barbs study for pilot test
    #TODO: Add the rest of the applicable "Get" methods to the defaults.json file such as getClosestVehicleToPoint
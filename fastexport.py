#python version 2.7.11
#coding: UTF-8
import mice#for scaner studio functions
import os #use for path navigation

import ConfigParser
import json

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

def main():
    config = ConfigParser.ConfigParser()
    config.read("M:/SCANeRstudio_1.6/data/GUELPH_DATA_1.6/script/python/settings.cfg")
    
    #*Headers are the function names that are in the include.json
    """ 1. open the json file "include.json", which contains the functions and the set parameters for the data collection
        2. load the file as a python dictionary with the json.loads function which contains keys (scaner function names) 
        and values (name, function call, class, argument count and arguments to format into string)
        3. convert the dictionary of function key/value pairs into a list of function definitions
        4. iterate through the list of function definitions. for each definition, get the value by 
        the key "name" and create a list of all the names, only if the key exists (which it should unless it is changed in the future"""
    included = (json.load(open(config.get('paths','included')))).values()
    headers = [h["name"] for h in included if "name" in h]

    file = config.get('paths','datafile')#read from the config file for the csv code

    writer = customcsv(file,config.get('fixed','delim'),headers)

    """ Similar to above...instead of getting the values at the key "name", the values from "function" key
    are retrieved and then formatted using % tuple(list) method to replace %s indicators in the function. The list
    comes from the value at key "argv"...only if both fields are in the dictionary (which they should be unless the code is changed
    map then applies the python function "eval" to each of the function calls in the "calls" array """
    calls = [(f["function"] % tuple(f["argv"])) for f in included if ("function" in f and "argv" in f)]#call
    results = map(eval,calls)
    #take the header and the results and join the arrays into a key value pair 
    data = dict(zip(headers,results))

    writer.writedata(data)#write the data to the csv using class method
    writer.writerclose()

    return 1#return 1 on success

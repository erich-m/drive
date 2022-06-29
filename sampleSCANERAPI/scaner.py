#!/usr/bin/python
from ctypes import *
import sys
import os
from optparse import OptionParser

if (os.name == 'nt'):
    print("working directory: " + os.getcwd())
    scaner_api = CDLL(r"C:\OKTAL\SCANeRstudio_1.6\APIs\samples\ScanerAPI\python\SCANeR_API_C.1.6.dll")
else:
    scaner_api = CDLL('libScanerAPI.so')

#structures first
class DataInterface(Structure):
    pass

class FieldInfo(Structure):
    _fields_ = [("name", c_char * 256),
                ("type_name", c_char * 256)]

class Position(Structure):
    _fields_ = [("x", c_double),
                ("y", c_double),
                ("z", c_double)]
    def __str__(self):
        return "(" + str(self.x) + " " + str(self.y) + " " + str(self.z) + ")"
                
class Vehicle(Structure):
    _fields_ = [("id", c_int),
                ("vehicleName", c_char * 256),
                ("type", c_int),
                ("behaviour", c_int),
                ("state", c_int),
                ("initPosition", Position),
                ("heading", c_double)]
                
    def __str__(self):
        return "id: {0}\nname: {1}\ntype: {2}\nbehaviour: {3}\nstate: {4}\n"\
                "initPosition: {5}\n"\
                "heading: {6}".format(self.id, self.vehicleName, Vehicle.get_type_str(self.type), Vehicle.get_behaviour_str(self.behaviour), Vehicle.get_state_str(self.state), self.initPosition, self.heading)
    
    @staticmethod
    def get_type_str(type):
        if type == CAR:
            return "CAR"
        if type == TRACTOR:
            return "TRACTOR"
        if type == SEMI_TRAILER:
            return "SEMI_TRAILER"
        if type == TRAILER:
            return "TRAILER"
        if type == CAR:
            return "CAR"
        if type == BUS:
            return "BUS"
        if type == MOTORBIKE:
            return "MOTORBIKE"
        if type == BICYCLE:
            return "BICYCLE"
        if type == PEDESTRIAN:
            return "PEDESTRIAN"
        if type == STATIC_OBJECT:
            return "STATIC_OBJECT"
        if type == TRAM:
            return "TRAM"
        if type == TRAIN:
            return "TRAIN"
        if type == UNKNOWN_TYPE:
            return "UNKNOWN_TYPE"
        if type == ALIVEBEING:
            return "ALIVEBEING"
            
    @staticmethod
    def get_behaviour_str(behaviour):
        if behaviour == EXTERNAL:
            return "EXTERNAL"
        if behaviour == AUTONOMOUS:
            return "AUTONOMOUS"
        if behaviour == INTERACTIVE:
            return "INTERACTIVE"
        if behaviour == ANIMATED:
            return "ANIMATED"
        if behaviour == VB_UNKNONW:
            return "VB_UNKNONW"
    
    @staticmethod
    def get_state_str(state):
        if state == V_GHOST:
            return "V_GHOST"
        if state == V_VISIBLE:
            return "V_VISIBLE"
        if state == V_ALIVE:
            return "V_ALIVE"
        if state == V_UNKNOWN:
            return "V_UNKNOWN"

class Vehicle(Structure):
    _fields_ = [("id", c_int),
                ("name", c_char * 256),
                ("mass", c_double),
                ("static_object", c_char),
                ("state", c_int),
                ("init_position", Position),
                ("heading", c_double),
                ("name", c_byte * 256),
                ("has_heighmap", c_char),
                ("scale", Position),
                ("friction", c_double),
                ("rolling_frition", c_double),
                ]
                
MAX_VEHICLES_NUMBER = 512
MAX_OBJECTS_NUMBER = 512

class  InitialConditions(Structure):
    _fields_ = [("scenario_name", c_char * 256), 
            ("terrain_name", c_char * 256),
            ("vehicles_count", c_int),
            ("vehicles", Vehicle * MAX_VEHICLES_NUMBER),
            ("objects_count", c_int),
            ("objects", Vehicle * MAX_VEHICLES_NUMBER)]

            
    def __str__(self):
        static_str = "scenario: {0}\n"\
                "terrain: {1}\n"\
                "vehicle count: {2}\n"\
                "objects_count: {3}".format(self.scenario_name, self.terrain_name, self.vehicles_count, self.objects_count);
                
        vehicles_str = "";
        for vehicle_index in range(0, self.vehicles_count):
            print (vehicle_index)
            vehicles_str += str(self.vehicles[vehicle_index])
            vehicles_str += "\n"
            
        return static_str + vehicles_str

class APIProcessInfo(Structure):
    MAX_PROCNAME_SIZE=255
    MAX_HOSTNAME_SIZE=255
    _fields_ = [("state", c_int),
                ("name", c_char*MAX_PROCNAME_SIZE),
                ("frequency", c_float),
                ("desiredFrequency", c_float),
                ("hostname", c_char*MAX_HOSTNAME_SIZE)]
#functions
scaner_api.Process_InitParams.argtypes = [c_char_p, c_char_p, c_float]
scaner_api.Process_GetId.restype = c_int
scaner_api.Process_GetTime.restype = c_double
scaner_api.Process_GetRecordDir.restype = c_char_p

scaner_api.Com_declareInputData.restype = c_void_p
scaner_api.Com_releaseInterface.argtypes = [c_void_p]
scaner_api.Com_validateStateEvent.argtypes = [c_void_p]
scaner_api.Com_getShortData.restype = c_short
scaner_api.Com_getCharData.restype = c_byte
scaner_api.Com_getFloatData.restype = c_float
scaner_api.Com_getDoubleData.restype = c_double
scaner_api.Com_getStringData.argtypes = [c_void_p, c_char_p]
scaner_api.Com_getStringData.restype = c_char_p
scaner_api.Com_getNextEvent.restype = c_void_p
scaner_api.Com_getMessageEventDataStringId.restype = c_char_p
scaner_api.Com_getInitConditions.restype = POINTER(InitialConditions)
scaner_api.Com_getInitConditions.argtypes = [c_void_p]

scaner_api.Com_getTypeEvent.argtypes = [c_void_p]
scaner_api.Com_getStateEventType.argtypes = [c_void_p]

scaner_api.Com_setShortData.argtypes = [c_void_p, c_char_p, c_short]
scaner_api.Com_setLongData.argtypes = [c_void_p, c_char_p, c_long]
scaner_api.Com_setCharData.argtypes = [c_void_p, c_char_p, c_byte]
scaner_api.Com_setFloatData.argtypes =  [c_void_p, c_char_p, c_float]
scaner_api.Com_setDoubleData.argtypes =  [c_void_p, c_char_p, c_double]
scaner_api.Com_setStringData.argtypes = [c_void_p, c_char_p, c_char_p]

scaner_api.Utils_getPath.argtypes = [c_char_p]
scaner_api.Utils_getPath.restype = c_char_p

scaner_api.Utils_getMultiplePath.argtypes = [c_char_p]
scaner_api.Utils_getMultiplePath.restype = POINTER(c_char_p)

scaner_api.Simulation_InitParams.argtypes = [c_char_p, c_float]
scaner_api.Simulation_Launch.restype = c_byte
scaner_api.Simulation_LoadScenario.restype = c_byte
scaner_api.Simulation_Play.restype = c_byte
scaner_api.Simulation_Pause.restype = c_byte
scaner_api.Simulation_UnLoad.restype = c_byte
scaner_api.Simulation_Stop.restype = c_byte
scaner_api.Simulation_KillAllProcesses.restype = c_byte
scaner_api.Simulation_AllProcessesOk.restype = c_byte
scaner_api.Simulation_WaitForState.restype = c_byte
scaner_api.Simulation_StartProcess.restype = c_byte
scaner_api.Simulation_GetProcessInfo.restype = c_byte
scaner_api.Simulation_IsProcessAutoLaunched.restype = c_byte
scaner_api.Simulation_Shutdown.restype = c_byte
scaner_api.Simulation_setVarEnv.restype = c_byte

Process_InitParams = scaner_api.Process_InitParams
Process_Run = scaner_api.Process_Run
Process_Wait = scaner_api.Process_Wait
Process_GetState = scaner_api.Process_GetState
Process_Close = scaner_api.Process_Close
Process_GetId = scaner_api.Process_GetId
Process_GetTime = scaner_api.Process_GetTime
Process_OutputLevel = scaner_api.Process_OutputLevel
Process_GetRecordDir = scaner_api.Process_GetRecordDir

Com_registerEvent = scaner_api.Com_registerEvent
Com_getTypeEvent = scaner_api.Com_getTypeEvent
Com_getStateEventType = scaner_api.Com_getStateEventType
Com_validateStateEvent = scaner_api.Com_validateStateEvent
Com_getNextEvent = scaner_api.Com_getNextEvent

Com_getMessageEventDataInterface = scaner_api.Com_getMessageEventDataInterface
Com_getMessageEventDataStringId = scaner_api.Com_getMessageEventDataStringId
Com_declareInputData = scaner_api.Com_declareInputData
Com_declareOutputData = scaner_api.Com_declareOutputData
Com_releaseInterface = scaner_api.Com_releaseInterface
Com_updateInputs = scaner_api.Com_updateInputs
Com_updateOutputs = scaner_api.Com_updateOutputs
Com_getShortData = scaner_api.Com_getShortData
Com_getCharData = scaner_api.Com_getCharData
Com_getFloatData = scaner_api.Com_getFloatData
Com_getDoubleData = scaner_api.Com_getDoubleData
Com_getLongData = scaner_api.Com_getLongData
Com_getStringData = scaner_api.Com_getStringData
Com_setShortData = scaner_api.Com_setShortData
Com_setCharData = scaner_api.Com_setCharData
Com_setFloatData = scaner_api.Com_setFloatData
Com_setDoubleData = scaner_api.Com_setDoubleData
Com_setStringData = scaner_api.Com_setStringData
Com_setLongData = scaner_api.Com_setLongData
Com_getFieldInfoArray = scaner_api.Com_getFieldInfoArray
Com_getFieldNumber = scaner_api.Com_getFieldNumber
Com_getInitConditions = scaner_api.Com_getInitConditions

Utils_getPath = scaner_api.Utils_getPath
Utils_getMultiplePath = scaner_api.Utils_getMultiplePath
Utils_releaseChar = scaner_api.Utils_releaseChar

Simulation_InitParams = scaner_api.Simulation_InitParams
#Simulation_Close = scaner_api.Simulation_Close

Simulation_Launch = scaner_api.Simulation_Launch
Simulation_LoadScenario = scaner_api.Simulation_LoadScenario
Simulation_Play = scaner_api.Simulation_Play
Simulation_Pause = scaner_api.Simulation_Pause
Simulation_UnLoad = scaner_api.Simulation_UnLoad
Simulation_Stop = scaner_api.Simulation_Stop

Simulation_KillAllProcesses = scaner_api.Simulation_KillAllProcesses
Simulation_AllProcessesOk = scaner_api.Simulation_AllProcessesOk
Simulation_WaitForState = scaner_api.Simulation_WaitForState
Simulation_StartProcess = scaner_api.Simulation_StartProcess
Simulation_KillProcess = scaner_api.Simulation_KillProcess
Simulation_KillProcesses = scaner_api.Simulation_KillProcesses
Simulation_UpdateProcessInfo = scaner_api.Simulation_UpdateProcessInfo
Simulation_getProcessNumber = scaner_api.Simulation_getProcessNumber
Simulation_getAllProcessInfo = scaner_api.Simulation_getAllProcessInfo
Simulation_GetProcessInfo = scaner_api.Simulation_GetProcessInfo
Simulation_GetIdFromName = scaner_api.Simulation_GetIdFromName
Simulation_IsProcessAutoLaunched = scaner_api.Simulation_IsProcessAutoLaunched
Simulation_Shutdown = scaner_api.Simulation_Shutdown
Simulation_ChangeConfig = scaner_api.Simulation_ChangeConfig
Simulation_setVarEnv = scaner_api.Simulation_setVarEnv

#enum
(PS_DEAD,
PS_DAEMON,
PS_LOADED,
PS_PAUSED,
PS_READY,
PS_RUNNING) = map(int, range(6))

def state_string(state):
    """return the input state as it's string representation"""
    if state == PS_DEAD:
        return "DEAD"
    if state == PS_DAEMON:
        return "DAEMON"
    if state == PS_LOADED:
        return "LOADED"
    if state == PS_PAUSED:
        return "PAUSED"
    if state == PS_READY:
        return "READY"
    if state == PS_RUNNING:
        return "RUNNING"

OL_Notify = 1
OL_Debug = 2
OL_Warning = 3
OL_Err = 4

(UT_Unknown, UT_AllData, UT_NetworkData, UT_ShmData) = map(int, range(4))

(ET_message, ET_state, ET_unknown) = map(int, range(3))

(ST_Unknown, ST_Load, ST_Start, ST_Init, ST_Go, ST_Pause, ST_Stop, ST_Unload, ST_Kill) = map(int, range(9))

(V_GHOST, V_VISIBLE, V_ALIVE, V_UNKNOWN) = map(int, range(4))

UNKNOWN_TYPE=0
RIGID=1
TRACTOR=2
SEMI_TRAILER=3
TRAILER=4
CAR=5
BUS=6
MOTORBIKE=7
BICYCLE=8
PEDESTRIAN=9
STATIC_OBJECT=10
TRAM=11
TRAIN=12
ALIVEBEING=13
CNT_VEHICLETYPE = 14

EXTERNAL=0
AUTONOMOUS=1
INTERACTIVE=2
ANIMATED=3
VB_UNKNONW=4

#APIShutdownType
ST_POWEROFF  = 0 
ST_REBOOT	  = 1
ST_SHUTDOWN  = 2
ST_STANDBY	  = 3

#OState
O_GHOST = 0;
O_VISIBLE = 1;
O_ALIVE = 2;
O_UNKNOWN = 3;

# event more pythonic test
class Events:
    """
    python iterable on scaner api events
    """
    def __iter__(self):
        return EventsIterator()
        
class Event:
    def __init__(self):
        self.c_event = Com_getNextEvent()
        if self.c_event:
            self.type = Com_getTypeEvent(self.c_event)
        
    def __nonzero__(self):
        return self.c_event != None
        
    def state(self):
        if self.type == ET_state:
            return Com_getStateEventType(self.c_event)
        else:
            return None
        
    def validate(self):
        if self.type == ET_state:
            Com_validateStateEvent(self.c_event)
        
    def data_interface(self):
        return Com_getMessageEventDataInterface(self.c_event)
        
    def message_name(self):
        return Com_getMessageEventDataStringId(self.c_event)
        
    def get_initial_conditions(self):
        return Com_getInitConditions(self.c_event)
    
class EventsIterator:
    """
    Iterator on scaner api events
    """
    def next(self):
        event = Event()
        if not event:
            raise StopIteration
        return event

class ScanerApiOption(OptionParser):
    def __init__(self, default_name = 'PYTHON', default_config = 'NL_1.1', default_frequency = 20, default_config_file="", usage=""):
        OptionParser.__init__(self, usage)
        self.add_option("-p", "--process_name", 
                          dest="process_name",
                          type="string", default=default_name,
                          help="Process name")
        self.add_option("-c", "--configuration",
                          dest="configuration", default=default_config,
                          help="Scaner Configuration")
        self.add_option("-f", "--frequency",
                          dest="frequency",
                          type = 'int', default=default_frequency,
                          help="Module frequency")
        self.add_option("--cfg", "--config_file",
                        dest="config_file",
                        type = "string", default=default_config_file,
                        help="Configuration file name")
    def parse_args(self, args=None, values=None):
        if not args:
            args = sys.argv
        try:
            args[args.index('-cfg')] = '--cfg'
            print ('-cfg detected')
        except ValueError:
            pass
        return OptionParser.parse_args(self, args, values)
            
                          
def get_main_arg():
    argv = (c_char_p * len(sys.argv))()
    for i in range(len(sys.argv)):
        argv[i] = sys.argv[i]
    return argv
    
def print_info_message(data_interface):
    print (get_message_description(data_interface))
    
def get_message_description(data_interface):
    nb_field = scaner_api.Com_getFieldNumber(data_interface);
    if nb_field == 0:
        return ""

    description_string = ""
    field_info_array = (FieldInfo * nb_field)();
    if scaner_api.Com_getFieldInfoArray(data_interface, field_info_array) != 0:
        for i in range(nb_field):
            description_string = description_string + '\t' + field_info_array[i].name + " type of " + field_info_array[i].type_name + '\n'
            
    return description_string

def print_set_itinerary(data_interface):
    id = scaner_api.Com_getShortData(data_interface, 'vhlId')
    print ('id ', id)
    add = scaner_api.Com_getCharData(data_interface, 'add')
    print ('add ', ord(add))
    directions = scaner_api.Com_getShortData(data_interface, 'directionsCount')
    print ('directionsCount ', directions)
    
    for direction in range(directions):
        dir = scaner_api.Com_getCharData(data_interface, 'directions['+str(direction)+']')
        print ('directions['+str(direction)+'] ', ord(dir))

def print_path(data_interface):
    id = scaner_api.Com_getShortData(data_interface, 'vhlId')
    print ('id ', id)
    directions = scaner_api.Com_getShortData(data_interface, 'directionsCount')
    print ('directionsCount ', directions)
    
    for direction in range(directions):
        dir = scaner_api.Com_getCharData(data_interface, 'directions['+str(direction)+']/direction')
        print ('directions['+str(direction)+']/direction ', ord(dir))
        intersection = scaner_api.Com_getLongData(data_interface, 'directions['+str(direction)+']/intersection')
        print ('directions['+str(direction)+']/intersection ', intersection)
        
def print_infra_position(data_interface):
    id = scaner_api.Com_getShortData(data_interface, 'id')
    print ('id ', id)
    x = Com_getFloatData(data_interface, 'x')
    y = Com_getFloatData(data_interface, 'y')
    z = Com_getFloatData(data_interface, 'z')
    print ('(', x, ' ', y, ' ', z, ')')
    h = Com_getFloatData(data_interface, 'h')
    p = Com_getFloatData(data_interface, 'p')
    r = Com_getFloatData(data_interface, 'r')
    print ('(', h, ' ', p, ' ', r, ')')
    
def print_collision(data_interface):
    type = scaner_api.Com_getShortData(data_interface, 'collisionType')
    print ('type ', type)
    id1 = scaner_api.Com_getShortData(data_interface, 'id1')
    print ('id1 ', id1)
    id2 = scaner_api.Com_getShortData(data_interface, 'id2')
    print ('id2 ', id2)
    
    x = Com_getFloatData(data_interface, 'point1_X')
    y = Com_getFloatData(data_interface, 'point1_Y')
    z = Com_getFloatData(data_interface, 'point1_Z')
    print ('(', x, ' ', y, ' ', z, ')')
    x = Com_getFloatData(data_interface, 'point2_X')
    y = Com_getFloatData(data_interface, 'point2_Y')
    z = Com_getFloatData(data_interface, 'point2_Z')
    print ('(', x, ' ', y, ' ', z, ')')
    x = Com_getFloatData(data_interface, 'force1_X')
    y = Com_getFloatData(data_interface, 'force1_Y')
    z = Com_getFloatData(data_interface, 'force1_Z')
    print ('force (', x, ' ', y, ' ', z, ')')
    x = Com_getFloatData(data_interface, 'force2_X')
    y = Com_getFloatData(data_interface, 'force2_Y')
    z = Com_getFloatData(data_interface, 'force2_Z')
    print ('force (', x, ' ', y, ' ', z, ')')

def print_trafic_light_update(data_interface):
    id = Com_getShortData(data_interface, 'id')
    stateCount = Com_getCharData(data_interface, 'stateCount')
    print ('Road Sign ', str(id))
    for stateIndex in range(ord(stateCount)):
        state = Com_getCharData(data_interface, 'state[' + str(stateIndex) + ']')
        print ('Light ', stateIndex, ' state ', ord(state))

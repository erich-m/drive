import ctypes
import sys
import os
from optparse import OptionParser

is_64bit = platform.architecture()[0]
if is_64bit == "64bit":
	os.environ['PATH'] += ';'+os.environ['STUDIO_PATH']+'/SCANeRstudio_1.6/APIs/bin/x64/vs2013/'
else
	os.environ['PATH'] += ';'+os.environ['STUDIO_PATH']+'/SCANeRstudio_1.6/APIs/bin/win32/vs2013/'

scenario_api = ctypes.CDLL('ScenarioAPI.dll')

#functions
scenario_api.Scenario_Init.argtypes = [ctypes.c_char_p]
scenario_api.Scenario_Init.restype = ctypes.c_int

scenario_api.Scenario_Load.argtypes = [ctypes.c_char_p]
scenario_api.Scenario_Load.restype = ctypes.c_int

scenario_api.Scenario_Save.argtypes = [ctypes.c_char_p]
scenario_api.Scenario_Save.restype = ctypes.c_int

scenario_api.Scenario_ModifyNodeValue.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
scenario_api.Scenario_ModifyNodeValue.restype = ctypes.c_int

Scenario_Init = scenario_api.Scenario_Init
Scenario_Load = scenario_api.Scenario_Load
Scenario_Save = scenario_api.Scenario_Save
Scenario_ModifyNodeValue = scenario_api.Scenario_ModifyNodeValue
Scenario_Close = scenario_api.Scenario_Close

class ScenarioApiOption(OptionParser):
    def __init__(self, default_config = 'DEFAULT_1.6', default_config_file="", usage=""):
        OptionParser.__init__(self, usage)
        self.add_option("-c", "--configuration",
                          dest="configuration", default=default_config,
                          help="Scaner Configuration")


import os
import inspect
this_file = inspect.currentframe().f_code.co_filename
this_dir = os.path.dirname(this_file)
# to find scenario_api dll

is_64bit = platform.architecture()[0]
if is_64bit == "64bit":
	os.chdir(os.path.abspath(this_dir+'./../../../bin/x64/vs2013'))
else
	os.chdir(os.path.abspath(this_dir+'./../../../bin/win32/vs2013'))

from scenario import *

parser = ScenarioApiOption()
(options, args) = parser.parse_args()
print "Config:" + options.configuration

# initialise using configuration name
Scenario_Init(options.configuration)

request_res = 0
initial_speed = 10
# load scenario from the given configuration
Scenario_Load("Studio_trafficStopSign")
for i in range(5):
    request_res = Scenario_ModifyNodeValue("/sce/Scenario/Vehicle[id=3]/initialSpeed", str(initial_speed))
    print "Request Initial Speed set to " + str(initial_speed) + " : " + str(request_res)
    scenario_name = "Studio_trafficStopSign_InitialSpeed" + str(initial_speed)
    # save the modified scenario to current configuration
    Scenario_Save(scenario_name)
    initial_speed += 5

# exit Scenario API
Scenario_Close()

#!/usr/bin/python
import os
import inspect
this_file = inspect.currentframe().f_code.co_filename
this_dir = os.path.dirname(this_file)
# to find scaner_api dll
if (os.name == 'nt'):
    os.chdir(os.path.abspath(this_dir+'./../bin/win32/vs2013'))

from scaner import *

parser = ScanerApiOption()
(options, args) = parser.parse_args()
Process_InitParams(options.process_name, options.configuration, ctypes.c_float(options.frequency))

data_interface_path = Com_declareInputData('Network/IVehicle/VehiclePath', 0)
print_info_message(data_interface_path)

status = PS_DAEMON
counter = 0
try:
    while status != PS_DEAD:
        # Process manager Run 
        Process_Run()
        Process_Wait()

        #Process manager State
        oldStatus = status
        status = Process_GetState()

        # Scaner API is now running 
        if status == PS_RUNNING:
            counter += 1
            #get a copy of the structure of exchange data 
            Com_updateInputs(UT_NetworkData)
            
            if counter % 10 == 0:
                print_path(data_interface_path)
        Process_Wait()
except KeyboardInterrupt:
    print 'Bye bye'
    Process_Close()



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

Com_registerEvent('Network/IVehicle/VehiclePath', 0)

status = PS_DAEMON
try:
    while status != PS_DEAD:
        # Process manager Run 
        Process_Run()
        Process_Wait()
        
        #Process manager State
        old_status = status
        status = Process_GetState()
        if status != old_status:
            print status

        # Event dequeing 
        event = Com_getNextEvent()

        while event:
            evtType = Com_getTypeEvent(event)
            if evtType == ET_message:
                data_interface_path = Com_getMessageEventDataInterface(event)
                msg_name = Com_getMessageEventDataStringId(event)
                if 'Network/IVehicle/VehiclePath' in msg_name:
                    print_path(data_interface_path)
            event = Com_getNextEvent()
        
        
except KeyboardInterrupt:
    print 'Bye bye'
    Process_Close()

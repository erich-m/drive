import os
# to find scaner_api dll
if (os.name == 'nt'):
    os.chdir(os.path.abspath('../bin/win32/vs2013'))

import math
import ctypes

from scaner import *

parser = ScanerApiOption()

(options, args) = parser.parse_args()
Process_InitParams(options.process_name, options.configuration, options.frequency)

status = PS_DAEMON
Com_registerEvent("LOAD", -1)

try:
    while status != PS_DEAD:
        # Process manager Run 
        Process_Run()
        Process_Wait()

        #Process manager State
        oldStatus = status
        status = Process_GetState()
        
        for event in Events():
            if event.type() == ET_state and event.state() == ST_Load:
                print ("inital state")
                init = Com_getInitConditions(event.c_event)
                print (init)
                event.validate()
                Com_updateOutputs(UT_NetworkData)

            

except KeyboardInterrupt:
    print ('Bye bye')
    Process_Close()
except:
    Process_Close()
    raise

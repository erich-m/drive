#!/usr/bin/python
import os
import inspect
this_file = inspect.currentframe().f_code.co_filename
this_dir = os.path.dirname(this_file)
# to find scaner_api dll
if (os.name == 'nt'):
    os.chdir(os.path.abspath(this_dir+'./../bin/win32/vs2013'))

from scaner import *

def print_laser(data_interface):
    print ('globalId ', scaner_api.Com_getLongData(data_interface, 'globalId'))
    print ('vhlId ', scaner_api.Com_getShortData(data_interface, 'vhlId'))
    print ('sensorId ', scaner_api.Com_getShortData(data_interface, 'sensorId'))
    print ('frameCount ', scaner_api.Com_getShortData(data_interface, 'frameCount'))
    near_id = scaner_api.Com_getShortData(data_interface, 'nearestPoint'))
    print ('nearestPoint ', near_id)
    result_array_count = scaner_api.Com_getShortData(data_interface, 'resultArrayCount')
    print ('resultArrayCount ', result_array_count)
    for i in range(result_array_count):
        print ('hit ', scaner_api.Com_getCharData(data_interface, 'resultArray['+str(i)+']/hit'))
        print ('Hangle ', scaner_api.Com_getFloatData(data_interface, 'resultArray['+str(i)+']/Hangle'))
        print ('Vangle ', scaner_api.Com_getFloatData(data_interface, 'resultArray['+str(i)+']/Vangle'))
        print ('absposx ', scaner_api.Com_getFloatData(data_interface, 'resultArray['+str(i)+']/absposx'))
        print ('absposy ', scaner_api.Com_getFloatData(data_interface, 'resultArray['+str(i)+']/absposy'))
        print ('absposz ', scaner_api.Com_getFloatData(data_interface, 'resultArray['+str(i)+']/absposz'))
        print ('relposx ', scaner_api.Com_getFloatData(data_interface, 'resultArray['+str(i)+']/relposx'))
        print ('relposy ', scaner_api.Com_getFloatData(data_interface, 'resultArray['+str(i)+']/relposy'))
        print ('relposz ', scaner_api.Com_getFloatData(data_interface, 'resultArray['+str(i)+']/relposz'))
        print ('distance ', scaner_api.Com_getFloatData(data_interface, 'resultArray['+str(i)+']/distance'))
        

parser = ScanerApiOption()
(options, args) = parser.parse_args()
Process_InitParams(options.process_name, options.configuration, ctypes.c_float(options.frequency))
laser_message_name = 'Network/ISensor/LaserMeter'
Com_registerEvent(laser_message_name, -1)

status = PS_DAEMON
try:
    while status != PS_DEAD:
        # Process manager Run 
        Process_Wait()
        Process_Run()
        
        #Process manager State
        old_status = status
        status = Process_GetState()
        if status != old_status:
            print (status)

        # Event dequeing 
        event = Com_getNextEvent()

        while event:
            evtType = Com_getTypeEvent(event)
            if evtType == ET_message:
                data_interface_path = Com_getMessageEventDataInterface(event)
                msg_name = Com_getMessageEventDataStringId(event)
                print (msg_name)
                if laser_message_name in msg_name:
                    print_laser(data_interface_path)
            event = Com_getNextEvent()
        
        
except KeyboardInterrupt:
    print ('Bye bye')
    Process_Close()

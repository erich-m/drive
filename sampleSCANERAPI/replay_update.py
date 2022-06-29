#!/usr/bin/python
import os
# to find scaner_api dll
if (os.name == 'nt'):
    os.chdir(os.path.abspath('../bin/win32/vs2013'))

import math
import ctypes
from euclid import *
from scaner import *

class Tec:
    def __init__(self, length, width, rear_overbang):
        self.length = length
        self.width = width
        self.rear_overbang = rear_overbang

parser = ScanerApiOption()

(options, args) = parser.parse_args()
Process_InitParams(options.process_name, options.configuration, 20)

status = PS_DAEMON
Com_registerEvent("LOAD", -1)

try:
    vehicle_info = {}
    update = {}
    update[4] = Com_declareOutputData('Network/IVehicle/VehicleUpdate', 4)
    update[64] = Com_declareOutputData('Network/IVehicle/VehicleUpdate', 64)
    techs = {}
    techs[64] = Tec(12.4, 2.65, 0)
    techs[4] = Tec(11.990, 2.500, 3.160)
    segment = {}
    segment[4] = []
    segment[4].append(Com_declareOutputData('Network/ICarto/CartoDrawSegment', 1004))
    segment[4].append(Com_declareOutputData('Network/ICarto/CartoDrawSegment', 1005))
    segment[4].append(Com_declareOutputData('Network/ICarto/CartoDrawSegment', 1006))
    segment[4].append(Com_declareOutputData('Network/ICarto/CartoDrawSegment', 1007))
    segment[64] = []
    segment[64].append(Com_declareOutputData('Network/ICarto/CartoDrawSegment', 1064))
    segment[64].append(Com_declareOutputData('Network/ICarto/CartoDrawSegment', 1065))
    segment[64].append(Com_declareOutputData('Network/ICarto/CartoDrawSegment', 1066))
    segment[64].append(Com_declareOutputData('Network/ICarto/CartoDrawSegment', 1067))

    record_line_replayed = 0;
    while status != PS_DEAD:
        # Process manager Run 
        Process_Run()
        Process_Wait()

        #Process manager State
        oldStatus = status
        status = Process_GetState()
        
        for event in Events():
            if event.type == ET_state \
            and event.state() == ST_Load:
                print "inital state"
                
                init = Com_getInitConditions(event.c_event)
                print init.scenario_name
                scenario_name = init.scenario_name
                record_path = Utils_getPath('data/record')
                files = [] 
                files.append((4, record_path + '/' + scenario_name + '-4.txt'))
                files.append((64, record_path + '/' + scenario_name + '-64.txt'))
                
                for file in files:
                    record_file = open (file[1], 'r')
                    datas = []
                    first = True
                    for line in record_file:
                        if first:
                            first = False
                            continue
                        try:
                            line = line.strip()
                            data_set = line.split('\t')
                            data_line = []
                            for data in data_set:
                                data_line.append(float(data))
                            datas.append(data_line)
                        except:
                            #print line
                            raise
                            
                    #print file[0], datas
                    vehicle_info[file[0]] = datas
                event.validate()
        
        if status == PS_RUNNING:
            for id in [4, 64]:
                #print id, vehicle_info[id]
                data = vehicle_info[id][record_line_replayed]
                data_interface = update[id];
                Com_setShortData(data_interface, 'vhlId', id)
                print 'id', id
                Com_setCharData(data_interface, 'state', 2)
                for i in range(6):
                    Com_setFloatData(data_interface, 'pos[%s]'%i, data[i+1])
                    print 'pos[%s]'%i, data[i+1]
                m = Matrix4.new_translate(data[1], data[2], data[3])
                m *= Matrix4.new_rotate_axis(data[6], Vector3(1.0, 0.0, 0.0))
                m *= Matrix4.new_rotate_axis(data[5], Vector3(0.0, 1.0, 0.0))
                m *= Matrix4.new_rotate_axis(data[4], Vector3(0.0, 0.0, 0.1))
                
                print "m=", m
                tech = techs[id]
                f_right = Point3(tech.length - tech.rear_overbang, -tech.width / 2.0, data[3]);
                f_left = Point3(tech.length - tech.rear_overbang, tech.width / 2.0, data[3]);
                r_right = Point3(- tech.rear_overbang, -tech.width / 2.0, data[3]);
                r_left = Point3(- tech.rear_overbang, tech.width / 2.0, data[3]);
                f_right = m*f_right
                f_left = m*f_left
                r_right = m*r_right
                r_left = m*r_left
                
                print 'f_right: %s'%f_right
                print 'f_left: %s'%f_left
                print 'r_right: %s'%r_right
                print 'r_left: %s'%r_left
                
                Com_setShortData(segment[id][0], 'name', 1000+id)
                for i in range(3):
                    Com_setFloatData(segment[id][0], 'pos1[%s]'%i, f_right[i])
                for i in range(3):
                    Com_setFloatData(segment[id][0], 'pos2[%s]'%i, r_right[i])
                Com_setCharData(segment[id][0], 'r', 255)
                Com_setCharData(segment[id][0], 'g', 255)
                Com_setCharData(segment[id][0], 'b', 255)
                
                Com_setShortData(segment[id][1], 'name', 1001+id)
                for i in range(3):
                    Com_setFloatData(segment[id][1], 'pos1[%s]'%i, r_right[i])
                for i in range(3):
                    Com_setFloatData(segment[id][1], 'pos2[%s]'%i, r_left[i])
                Com_setCharData(segment[id][1], 'r', 255)
                Com_setCharData(segment[id][1], 'g', 255)
                Com_setCharData(segment[id][1], 'b', 255)
                
                Com_setShortData(segment[id][2], 'name', 1002+id)
                for i in range(3):
                    Com_setFloatData(segment[id][2], 'pos1[%s]'%i, r_left[i])
                for i in range(3):
                    Com_setFloatData(segment[id][2], 'pos2[%s]'%i, f_left[i])
                Com_setCharData(segment[id][2], 'r', 255)
                Com_setCharData(segment[id][2], 'g', 255)
                Com_setCharData(segment[id][2], 'b', 255)

                Com_setShortData(segment[id][3], 'name', 1003+id)
                for i in range(3):
                    Com_setFloatData(segment[id][3], 'pos1[%s]'%i, f_left[i])
                for i in range(3):
                    Com_setFloatData(segment[id][3], 'pos2[%s]'%i, f_right[i])
                Com_setCharData(segment[id][3], 'r', 255)
                Com_setCharData(segment[id][3], 'g', 255)
                Com_setCharData(segment[id][3], 'b', 255)
                
            record_line_replayed = record_line_replayed + 1

        Com_updateOutputs(UT_NetworkData)
            

except KeyboardInterrupt:
    print 'Bye bye'
    Process_Close()
except:
    Process_Close()
    raise

import mice
def main():
    ''' set maximum of the first vehicle if any'''
    if mice.vehicles.values():
        veh = mice.vehicles.values()[0]
        print "set maximum speed of vehicle %s" % veh.name
    	mice.setMaximumSpeed(veh.id, 20)
	return 0
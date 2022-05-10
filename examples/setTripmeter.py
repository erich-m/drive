import mice
def main():
    ''' init trip meter of the second vehicle if any'''
    if len(mice.vehicles.values()) >= 2:
        veh = mice.vehicles.values()[1]
        print "init tripmeter of vehicle %s" % veh.name
        mice.setTripMeter(veh.id, 0)
    return 0
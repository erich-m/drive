import mice
def main():
    ''' set vehicle tech of the first vehicle if any'''
    if mice.vehicles.values():
        veh = mice.vehicles.values()[0]
        mice.setVehicleTech(veh.id, 16, 1)
    return 0
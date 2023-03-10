import mice

def main():
    dyn_tgt = 'dyn-tgt'
    dyn_rpl = 'dyn-rpl'
    stc_tgt = 'stc-tgt'
    ''' set maximum of the first vehicle if any'''
    #loop through the vehicles in the simulation
    for v in range(len(mice.vehicles.values())):
        veh = mice.vehicles.values()[v-1]
        name = veh.name
        tid = veh.id#target id

        #this will switch visibility states of a vehicle labeled with stc-tgt
        if name.__contains__(stc_tgt):
            mice.setVisibility(tid,not(mice.isVisible(tid)))
        #this will match any dynamic-target labeled vehicle
        elif name.__contains__(dyn_tgt):

            key = name[7:]
            veh_match = dyn_rpl + (key)
            print(veh_match)

            match_found = False
            for c in range(len(mice.vehicles.values())):
                car = mice.vehicles.values()[c-1]
                car_name = car.name
                rid = car.id#replacer id

                if car_name == veh_match:
                    match_found = True
                    break
            if not(match_found):
                #no match found, switch visibility to toggle (moving vehicle that is to have visibility swapped)
                mice.setVisibility(tid,0)
            else:
                #match found, perform dynamic vehicle replacement
                mice.setVisibility(rid,1)
                mice.setActivation(rid,1)
                mice.setPosition(rid,mice.getPositionVector(tid,0),mice.getPositionVector(tid,1),mice.getAngularPositionVector(tid,0))
                # mice.setSpeedObligatory(rid,mice.getSpeed(tid),1,0)
                # mice.setAccelerationObligatory(rid,mice.getAcceleration(tid),1)
                mice.setVehicleAutonomousMode(rid,-1,1)
                print(mice.getVehicleAutonomousMode(rid,-1))
                mice.setVisibility(tid,0)
        else:
            print("Vehicle not specified for change detection protocols")


    return 0
import mice
import collections

def recursivePrint(obj, prefix):
    for name in dir(obj):
        if not name.startswith('__'):
            attr = getattr(obj, name)
            if isinstance(attr, collections.Iterable):
                i=0
                for elem in attr:
                    recursivePrint(elem, "%(prefix)s.%(name)s[%(i)d]"%locals())
                    i += 1
            else:
                print '%(prefix)s.%(name)s: %(attr)s'%locals()

def printTec(tec):
    print ">>> IN printTec"
    recursivePrint(tec, 'tec')
    print "<<< OUT printTec"

def main():
    print ">> IN printVehicleTech"
    print "vehicles in scenario:", len(mice.vehicles)
    for veh in mice.vehicles:
        print "Id = ", veh.id
        print "NickName = ", veh.name
        print "Pos = ", veh.pos
        print "Angles = ", veh.angles
        printTec(veh.tec)
    print "<< OUT printVehicleTech"
    return 0.0
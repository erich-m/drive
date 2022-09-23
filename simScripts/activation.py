#coding: UTF-8
import mice

def main():
    currentdistance = mice.getCartesianDistance(0,mice.variables["measureID"]) #current distance in meters
    currentspeed = mice.getSpeed(0) / 3.6 #current speed in m/s
    
    estimatedtime = currentdistance/currentspeed - mice.variables["activation"]
    return estimatedtime#return the estimated time on success
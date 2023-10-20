#!/usr/bin/python3

from brping import Ping360
import numpy as np
from timeit import default_timer as timer


def calculate_sample_period():
    return 2*sonarRange/(numPoints*speedSound*samplePeriodSickDuration)

def sample_period():
    return samplePeriod*samplePeriodSickDuration

def transmit_duration_max():
    return min(firmwareMaxTransmitDuration, sample_period() * 64e6)

def adjust_transmit_duration():
    duration=8000*(sonarRange/speedSound)
    transmit_duration=max(2.5*sample_period()/1000, duration)
    return max(firmwareMinTransmitDuration, min(transmit_duration_max(), transmit_duration))


# initialize and connect to ping360
myPing=Ping360()
myPing.connect_serial("/dev/ttyUSB0", 115200)

if myPing.initialize() is False:
    print("Failed to initialize Ping!")
    exit(1)

#parameters defined by the documentation
firmwareMinTransmitDuration=5
firmwareMaxTransmitDuration=500 
samplePeriodSickDuration=25e-9

#parameters defined by user
speedSound=1500       # m/s
numPoints=int(1200)   #200~1200
gain=0                # low gain
startAngle=0          # 0 degres
endAngle=int(200)     # 180 degrees
point=0
sonarRange=10         # 10 meters range
samplePeriod=calculate_sample_period()
transmitDuration=adjust_transmit_duration()
sonarImageRaw=np.zeros((endAngle,numPoints), dtype=np.uint8)

# set the parameters to the ping360
myPing.set_mode(1)                  #Ping360 mode
myPing.set_gain_setting(gain)
myPing.set_angle(startAngle)
myPing.set_transmit_duration(int(transmitDuration))        
myPing.set_sample_period(int(samplePeriod))
myPing.set_transmit_frequency(740)
myPing.set_number_of_samples(numPoints)

start = timer()

for angle in range(startAngle,endAngle,2):
    myPing.set_angle(angle)
    sonarData=myPing.transmit()
    if sonarData:
        sonarImageRaw[angle]=sonarData.msg_data[24:]
    else:
        print("Failed to get distance data")

end = timer()

print(end-start)
#!/usr/bin/python3

import serial
from brping import Ping360
import numpy as np

def calculate_sample_period():
    return 2*range/(numPoints*speedSound*samplePeriodSickDuration)

def sample_period():
    return samplePeriod*samplePeriodSickDuration

def transmit_duration_max():
    return min(firmwareMaxTransmitDuration, sample_period() * 64e6)

def adjust_transmit_duration():
    duration=8000*(range/speedSound)
    transmit_duration=max(2.5*sample_period()/1000, duration)
    return max(firmwareMinTransmitDuration, min(transmit_duration_max(), transmit_duration))

def radioRead():
    messageEnd=False
    while not messageEnd:
        bufferDecoded=[]
        buf=s.read(1)
        if buf:
            if buf.decode(encoding='ascii', errors='replace') == '*':
                bufferDecoded.append(buf.decode(encoding='ascii', errors='replace'))
                if len(bufferDecoded)>50:
                    bufferDecoded.clear()
                    break
                while buf.decode(encoding='ascii', errors='replace') != '|':
                    buf=s.read(1)
                    bufferDecoded.append(buf.decode(encoding='ascii', errors='replace'))
                messageStr=''
                messageStr=messageStr.join(bufferDecoded[1:-1])
                bufferDecoded.clear()
                messageEnd=True
    return messageStr

def radioWrite(message):
    startbyte='*'
    endByte='|'
    message=str(message)
    message=startbyte+message+endByte
    s.write(bytes(message,'ascii'))

# initialize the radio
s=serial.Serial('/dev/ttyUSB1')
s.baudrate=9600
s.bytesize=serial.EIGHTBITS #number of bits per bytes
s.parity=serial.PARITY_NONE #set parity check: no parity
s.stopbits=serial.STOPBITS_ONE #number of stop bits
s.timeout=0 #non-block read
s.xonxoff=False #disable software flow control
s.rtscts=False #disable hardware (RTS/CTS) flow control
s.dsrdtr=False #disable hardware (DSR/DTR) flow control
s.setRTS(0) # <---- THIS SOLVED THE PROBLEM READING SERIAL DATA WITH APC220

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
speedSound=1500 # m/s
numPoints=600 
gain=0          # low gain
startAngle=0    # 0 degres
endAngle=200    # 180 degres
angle=startAngle
point=0
range=10        # 10 meters range
samplePeriod=calculate_sample_period()
transmitDuration=adjust_transmit_duration()

numberOfMatrixSamples=input('Distancia')*50
#numberOfMatrixSamples=int(radioRead())*50
dataMatrixCartesian=np.zeros((numberOfMatrixSamples,endAngle,numPoints), dtype=np.uint8)
aux=0
myPing.transmit()

# set the parameters to the ping360
myPing.set_mode(1)                  #Ping360 mode
myPing.set_gain_setting(gain)
myPing.set_angle(startAngle)
myPing.set_transmit_duration(int(transmitDuration))        
myPing.set_sample_period(int(samplePeriod))
myPing.set_transmit_frequency(740)
myPing.set_number_of_samples(numPoints)

while aux<numberOfMatrixSamples:
    print(aux+1)
    radioWrite(aux+1)
    while angle<endAngle:
        data=myPing.transmit() # read data
        # if data found
        if data:
            dataMatrixCartesian[aux][angle][point:numPoints]=data.msg_data[24:]
            np.save(str(aux),dataMatrixCartesian[aux])
        else:
            print("Failed to get distance data")
        angle+=1
        myPing.set_angle(angle)
    
    angle=0
    aux+=1

np.save('matrixSample',dataMatrixCartesian)
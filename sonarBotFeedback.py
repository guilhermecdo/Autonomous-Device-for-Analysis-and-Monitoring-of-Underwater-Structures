#!/usr/bin/python3

import serial

s=serial.Serial('/dev/ttyUSB0')
s.baudrate=9600
s.bytesize=serial.EIGHTBITS #number of bits per bytes
s.parity=serial.PARITY_NONE #set parity check: no parity
s.stopbits=serial.STOPBITS_ONE #number of stop bits
s.timeout=0 #non-block read
s.xonxoff=False #disable software flow control
s.rtscts=False #disable hardware (RTS/CTS) flow control
s.dsrdtr=False #disable hardware (DSR/DTR) flow control
s.setRTS(0) # <---- THIS SOLVED THE PROBLEM READING SERIAL DATA WITH APC220

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

distance=int(input('Digite a Distancia'))

radioWrite(distance)

for i in range (int(distance)*50) :    
    print(radioRead())
s.close()
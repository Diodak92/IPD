import random
import time

import pymodbus
import serial
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient #initialize a serial RTU client instance
from pymodbus.transaction import ModbusRtuFramer

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

#count= the number of registers to read
#unit= the slave unit this request is targeting
#address= the starting address to read from

# specify com port and transmission parameters
com = "/dev/ttyUSB0"
client = ModbusClient(method='rtu', port=com, stwopbits = 1, bytesize = 8, parity = 'N', baudrate = 38400)

#Connect to the serial modbus server
#connection = client.connect()
#print(connection)

print("Software for automatic testing of IPD phase switching module: ")
switchingCyckles = int(input("Please enter number of switching cyckles: "))
cyckleTime = int(input("Please enter time beetwen switching cyckles  [s]: "))

# function for decoding and printing device status
def statusDecode(status):
    state = ''
    standby = False
    error =[False, '']
    #if(~status & 0b00001111 | status & 0b00001000):
    #    state = "Device is switched off"
    if(status & 0b00000001 | status & 0b00001000 == 9):
        state = "The first phase is on"
    if(status & 0b00000010 | status & 0b00001000 == 10):
        state = "The second phase is on"
    if(status & 0b00000100 | status & 0b00001000 == 12):
        state = "The third phase is on"
    if(status & 0b00010000):
        # set standby marker
        standby = True
    if(status & 0b00100000):
        error[0] = True
        error[1] = "Error! Relay short circuit detected"
    if(status & 0b01000000):
        error[0] = True
        error[1] = "Error! Unknown control register value"
    if(status & 0b10000000):
        error[0] = True
        error[1] = "Device fault!"
    elif(state == ''):
        state = "Uknown status"
    decodedStatus = [state, standby, error]
    return decodedStatus


previousState = 0
newState = 0

for cyckle in range(switchingCyckles + 1):
    statusReg = 0   
    # chceck if device is ready for next switching cyckle
    while(statusDecode(statusReg)[1] != True):
        statusReg = int(input("Please enter value for device status register:"))
        deviceStatus = statusDecode(statusReg)
        print(deviceStatus[0])
        if(deviceStatus[2][0] == True):
            print(deviceStatus[2][1])
            newState = random.randint(0,3)
            if(newState != previousState):
                previousState = newState
                print("Switching cyckle number:", cyckle, "new state" , newState)
            time.sleep(cyckleTime)
            break
    else:
        continue
    break
print("Done! Working fine!")

#Closes the underlying socket connection
#client.close()
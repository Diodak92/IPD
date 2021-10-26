from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from time import sleep 
import logging

SM4_MODBUS_ADDR = 1
EMSCX3_MODBUS_ADDR = 10

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.ERROR)

# initialize a serial RTU client instance
# CHECK CORRECT COM PORT! (On Windows in Device Mennager) 
client = ModbusClient(method="rtu", port="COM8", stopbits=1, bytesize=8, parity='N', baudrate=38400)
# Connect to the serial modbus server
connection = client.connect()
print("got connection : ", connection)

### FUNCTIONS DEFINITION ###
def read_casd_state():
    result = client.read_discrete_inputs(0x4000, 3, unit=10)
    #print(result)
    return(result.bits[0:3])    

def read_sm4_state():
    result = client.read_holding_registers(4211, 2, unit=SM4_MODBUS_ADDR)
    if result: 
        status1 = result.registers[0]
        status2 = result.registers[1]
        print("SSR state: ", status1, "remote motor state: ", status2)
        return([status1, status2])

def set_SSR(state):
    resp = client.write_register(4211, state, unit=SM4_MODBUS_ADDR)
    return(resp)

def  countdown(seconds):
    print("CIRCUIT BRAKER OVERLOADED!!! RESET IN: ")
    for i in range (seconds, 0, -1):
        sleep(1)
        print(i, " s")

def reset_MDM(seconds):
    countdown(seconds)
    resp1 = client.write_register(4212, 0x01, unit=SM4_MODBUS_ADDR)
    sleep(1)
    resp2 = client.write_register(4212, 0x00, unit=SM4_MODBUS_ADDR)
    return(resp1, resp2)

### MAIN PROGRAM ###
cycles = int(input("Enter number of overload cycles: "))
wait_time = int(input("Enter time to reset overloaded circuit braker [s]: "))

on = 1
off = 0
i = 1

print("STARTING AUTOMATIC CIRCUIT BRAKER OVERLOAD TEST\n")
print("TEST: ", i)
while(cycles>=i):
    set_SSR(on)
    sleep(1)
    cb_state = read_casd_state()
    if(cb_state[2] == 1):#(cb_state[0] == 1 or cb_state[2] == 1):
        print("CB-open: ", cb_state[0]," CB-closed: ", cb_state[1], " CB-tripped: ", cb_state[2])
        reset_MDM(wait_time)
        print("\n")
        i = i+1
        print("TEST: ", i)
set_SSR(off)
print("Test done, outlet disconnected")
client.close()

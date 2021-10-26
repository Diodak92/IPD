
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from time import sleep 
import logging

SM4_MODBUS_ADDR = 1
EMSCX3_MODBUS_ADDR = 10

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.ERROR)

# initialize a serial RTU client instance
client = ModbusClient(method="rtu", port="COM8", stopbits=1, bytesize=8, parity='N', baudrate=38400)
# Connect to the serial modbus server
connection = client.connect()
print("got connection : ", connection)

### FUNCTIONS DEFINITION ###
def read_casd_state():
    result = client.read_discrete_inputs(0x4000, 3, uint=EMSCX3_MODBUS_ADDR)
    if result: 
        status1 = result.bits[0]
        status2 = result.bits[1]
        status3 = result.bits[2]
        print("CB-open: ",status1, "CB-closed: ", status2, " CB-tripped: ", status3)
        return([status1, status2, status3])

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

def set_MDM(state):
    resp = client.write_register(4212, state, unit=SM4_MODBUS_ADDR)
    return(resp)

### MAIN PROGRAM ###
cycles = int(input("Enter number of overload cycles: "))
wait_time = float(input("Enter test loop cycle time min 30 [s]: "))
if wait_time <= 30:
    wait_time = 30

read_sm4_state()
read_casd_state()
sec = 1
on = 1
off = 0

for i in range(1, cycles+1):
    print("TEST: ", i)
    set_SSR(on)
    sleep(sec)
    set_SSR(off)
    cb_state = read_casd_state()
    if (cb_state[0] == 1 or cb_state[2] == 1):
        sleep(sec)
        set_MDM(on)
        sleep(sec)
        set_MDM(off)
        print("\n")
        sleep(wait_time-3*sleep)

print("Test done, outlet disconnected")
client.close()

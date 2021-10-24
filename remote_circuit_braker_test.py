
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
        status1 = result.registers[0]
        status2 = result.registers[1]
        status3 = result.registers[2]
        print("CB-open: ",status1, "CB-closed: ", status2, " CB-tripped: ", status3)

def read_SM4_state():
    result = client.read_holding_registers(0xFA1, 1, unit=SM4_MODBUS_ADDR)
    if result: tt = result.registers
    print(tt)

def set_SM4_outputs(state):
    resp = client.write_register(4220, state, unit=SM4_MODBUS_ADDR)

### MAIN PROGRAM ###

cycles = int(input("Enter number of overload cycles: "))
wait_time = float(input("Enter test loop cycle time min 30 [s]: "))

read_casd_state()
state = 0 

for i in range(1, cycles+1):
    print("TEST: ", i)
    set_SM4_outputs(state)
    state !=state
    print("\n")
    sleep(wait_time)

print("Test done, outlet disconnected")
client.close()

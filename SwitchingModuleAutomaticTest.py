### REGISTER MAP ###

# 40001 = control_reg
# 40002 = soft_start_time_reg
# 40003 = status_reg
# 40004 = rms_rurrent_reg
# 40005 = cycle_reg[0]
# 40006 = cycle_reg[1]
# 40007 = cycle_reg[2]

### STATUS REGISTER ###
# 0b10000000 = PHASE1_BIT
# 0b01000000 = PHASE2_BIT 
# 0b00100000 = PHASE3_BIT
# 0b00010000 = BUSSY_BIT
# 0b00001000 = VOLTAGE_ON_OUTPUT_BIT
# 0b00000100 = SHORT_CIRCUIT_BIT
# 0b00000010 = INVALID_CMD_REG_BIT
# 0b00000001 = INTERNAL_ERROR_BIT

from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from time import sleep
import logging
import random

MODBUS_ADDR = 100

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.ERROR)

# initialize a serial RTU client instance
client = ModbusClient(method="rtu", port="COM8", stopbits=1, bytesize=8, parity='N', baudrate=38400)

# Connect to the serial modbus server
connection = client.connect()
print("got connection : ", connection)

### FUNCTIONS DEFINITION ###
def read_reg():
    result = client.read_holding_registers(0x00, 7, unit=MODBUS_ADDR)
    if result:
        print('[{}]'.format(', '.join(hex(x) for x in result.registers)))
        tt = bin(result.registers[2])
        #while len(tt) < 8:
        #    tt += '0'
        #print(tt)
        #print('phase: {}{}{}  bussy: {}  v_on_out: {} short: {} inv_cmd: {} err: {}'.format(tt[0], tt[1],
        #                                                                                    tt[2], tt[3],
        #                                                                                    tt[4], tt[5],
        #                                                                                    tt[6], tt[7]))
def read_status_reg():
    result = client.read_holding_registers(0x02, 1, unit=MODBUS_ADDR)
    if result:
        tt = bin(result.registers[0])
        print(tt)

def read_current():
    result = client.read_holding_registers(0x03, 1, unit=MODBUS_ADDR)
    if result:
        #print('[{}]'.format(', '.join(hex(x) for x in result.registers)))
        tt = result.registers[0]
        tt = round((tt/1000.0), 2)
        if tt <= 0.05:
            tt = 0
        print("Measured current: ",tt," [A]")

def read_switching_cycles():
    result = client.read_holding_registers(0x04, 3, unit=MODBUS_ADDR)
    if result:
        #print('[{}]'.format(', '.join(x for x in result.registers)))
        tt = result.registers
        print("Number of cycles: \n", "R1: ", tt[0], "\n R2: ", tt[1], "\n R3: ", tt[2])

def set_phase(phase):
    resp = client.write_register(0x00, phase, unit=MODBUS_ADDR)

def set_soft_start(time):
    resp = client.write_register(0x01, time, unit=MODBUS_ADDR)

### MAIN PROGRAM ###
current_measure_cycles = 5
set_soft_start(int(input("Enter soft start time 500:5000 [ms]: ")))
cycles = int(input("Enter number of switching cycles: "))
wait_time = float(input("Enter test loop cycle time [s]: "))
until_measure_time = wait_time/(current_measure_cycles+1)

for i in range(1, cycles+1):
    selected_phase = random.randint(0,3)
    set_phase(selected_phase)
    print("TEST: ", i, " Selected phase: ", selected_phase)
    for j in range(0,current_measure_cycles):
        sleep(until_measure_time)
        read_current()
    read_switching_cycles()
    read_reg()
    print("\n")
    sleep(wait_time-current_measure_cycles*until_measure_time)

set_phase(0)
print("Test done, outlet disconnected")

client.close()

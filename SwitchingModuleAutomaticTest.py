from pymodbus.client.sync import ModbusSerialClient as ModbusClient  # initialize a serial RTU client instance
from time import sleep
import logging


MODBUS_ADDR = 100

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.ERROR)

client = ModbusClient(method="rtu", port="COM8", stopbits=1, bytesize=8, parity='N', baudrate=38400)

# Connect to the serial modbus server
connection = client.connect()
print("got connection : ", connection)

# client.write_register(0x00, 0, unit=MODBUS_ADDR)


def read_reg():
    result = client.read_holding_registers(0x00, 7, unit=MODBUS_ADDR)
    if result:
        print('[{}]'.format(', '.join(hex(x) for x in result.registers)))
        tt = bin(result.registers[1])
        tt = tt[2:]
        while len(tt) < 8:
            tt += '0'
        print(tt)
        print('phase: {}{}{}  bussy: {}  v_on_out: {} short: {} inv_cmd: {} err: {}'.format(tt[0], tt[1],
                                                                                            tt[2], tt[3],
                                                                                            tt[4], tt[5],
                                                                                            tt[6], tt[7]))


def read_current():
    result = client.read_holding_registers(0x04, 1, unit=MODBUS_ADDR)
    if result:
        print('[{}]'.format(', '.join(hex(x) for x in result.registers)))
        tt = result.registers[0]
        print(tt)


def set_phase(phase):
    resp = client.write_register(0x00, phase, unit=MODBUS_ADDR)


def set_soft_start(time):
    resp = client.write_register(0x01, time, unit=MODBUS_ADDR)


# for i in range(0, 3):
#     result = client.read_holding_registers(0x00, 5, unit=MODBUS_ADDR)
#     if result:
#         print('[{}]'.format(', '.join(hex(x) for x in result.registers)))
#         tt = bin(result.registers[1])
#         tt = tt[2:]
#         while len(tt) < 8:
#             tt += '0'
#         print('phase: {}{}{}  bussy: {}  v_on_out: {} short: {} inv_cmd: {} err: {}'.format(tt[0], tt[1],
#                                                                                             tt[2], tt[3],
#                                                                                             tt[4], tt[5],
#                                                                                             tt[6], tt[7]))
#     client.write_register(0x00, i % 4, unit=MODBUS_ADDR)
#     sleep(2)

# print("elo")
# for i in range(0, 3):
#     # set_phase(0)
#     # sleep(0.5)
#     read_reg()
#     sleep(0.5)



# read_reg()
# sleep(10)



wait_time = 3.0

# for i in range(0, 100):
#     sleep(0.1)
#     read_reg()

set_soft_start(1500)


# for i in range(0, 50):
#     set_phase(0)
#     sleep(wait_time)
#     read_reg()
#     set_phase(3)
#     sleep(wait_time)
#
#
# set_phase(0)
# sleep(wait_time)
# set_phase(1)
# sleep(wait_time)
# set_phase(2)
# sleep(wait_time)
# set_phase(3)
# sleep(wait_time)
# set_phase(0)
# #
for i in range(0, 50):
    set_phase(0)
    sleep(wait_time)
    read_reg()
    set_phase(1)
    sleep(wait_time)
    read_reg()
    set_phase(2)
    sleep(wait_time)
    read_reg()
    set_phase(3)
    sleep(wait_time)
    read_reg()

set_phase(0)


client.close()

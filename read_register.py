#!/usr/bin/python3
from pymodbus.client import ModbusSerialClient as ModbusClient
import pymodbus.utilities
from pymodbus.utilities import computeCRC
import logging
import time
import collections
import binascii
import struct
import datetime
now = str(datetime.datetime.utcnow())
logging.basicConfig(filename='mat3.log',level=logging.DEBUG)
log = logging.getLogger()
SERIAL = '/dev/ttyUSB1'
BAUD = 9600
SLAVE = 1
client = ModbusClient(method='rtu', port=SERIAL, startbits=1, stopbits=1, timeout=2, baudrate=BAUD, parity='N',errorcheck="crc16")
client.strict = False
address = 8190
while (address < 8273):
  address = address+2
  if address == 8234:
    address = 16424
  result = client.read_holding_registers(address, 2, SLAVE)
  print(result)
  if result:
    if result.isError():
        log.warning('warning '+str(address) + '  Global error is: %s', result)
    else:
        #decoder = BinaryPayloadDecoder.fromRegisters(result.registers, endian=Endian.Big)
        v1 = hex(result.registers[0]).replace('0x','')
        v2 = hex(result.registers[1]).replace('0x','')
        if v2 == '0':
           v2 = '0000'
        if len(v2) == 3:
           v2='0'+v2
        if len(v2) == 2:
           v2='00'+v2
        print(v1)
        print(v2)
        (myfloat,) = struct.unpack('>f',binascii.unhexlify(v1+v2))
        myfloat = float(myfloat)/10
        #if(mbreg==54):
        print ( now +";"+ str(address) +";"+ str(myfloat))

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.compat import iteritems
from pymodbus.client.sync import ModbusTcpClient

import datetime
import socket

# O endereço do servidor Modbus TCP
SERVER_HOST = '192.168.10.232'
SERVER_PORT = 502

# O endereço do dispositivo Modbus que estamos lendo
DEVICE_ADDRESS = 1

# O endereço do registrador Modbus que contém os valores de data/hora
DATETIME_REGISTER = 32500

# O número de valores de 16 bits que contêm a data/hora
DATETIME_LENGTH = 10

print("01")

# Cria um socket TCP/IP e se conecta ao servidor Modbus
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_HOST, SERVER_PORT))


print("02")

# Le os valores Modbus da data/hora do dispositivo
client = ModbusTcpClient(SERVER_HOST)
result = client.read_holding_registers(DATETIME_REGISTER, DATETIME_LENGTH, unit=1)

""" 
response = sock.recv(1024)
print("response: ", response)
decoder = BinaryPayloadDecoder.fromRegisters(response, byteorder=Endian.Big, wordorder=Endian.Little)
print('decoder', decoder)
modbus_values = [decoder.decode_16bit_int() for i in range(DATETIME_LENGTH)]

# Converte os valores Modbus em um objeto de data/hora
dt_values = modbus_values[:6] + [0] * 2
date_time = datetime.datetime(*dt_values)

# Exibe o objeto de data/hora como uma string formatada
print(date_time.strftime("%d/%m/%Y %H:%M:%S"))
"""
print("result ", result)
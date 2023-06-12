import modbus_tk
import ctypes
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
from struct import unpack
import struct



master = modbus_tcp.TcpMaster("192.168.10.232", 502)
master.set_timeout(5.0)


def leDword(dword_address):
    # Leitura de um registrador DWORD 
    dword_data = master.execute(1, cst.READ_HOLDING_REGISTERS, dword_address, 2)
    dword_value = (dword_data[1] << 16) + dword_data[0]
    return dword_value

def leReal(real_address):
    real_data = master.execute(1, cst.READ_HOLDING_REGISTERS, real_address, 2)
    real_bytes = bytearray([real_data[0] & 0xFF, real_data[0] >> 8, real_data[1] & 0xFF, real_data[1] >> 8])
    real_value = ctypes.c_float.from_buffer(real_bytes).value
    return  real_value

def leString(start_address):
    string_data = []
    for i in range(start_address, start_address + 9):
        register_data = master.execute(1, cst.READ_HOLDING_REGISTERS, i, 1)
        string_data.extend(register_data)
    # Converter os valores dos registradores em uma string
    string_value = ''.join([chr(byte & 0xFF) + chr((byte & 0xFF00) >> 8) for byte in string_data])
    # Remover caracteres adicionais além dos 15 primeiros caracteres
    string_value = string_value[:15]
    # Remover caracteres nulos ('\x00') adicionais, se existirem
    string_value = string_value.replace('\x00', '')
    return string_value

#print("Valor da String:", leString(10014))

#print("Valor do REAL:", leReal(10044))

#print("Valor do DWORD:", leDword(10042))






#resultado = (master.execute(1, cst.READ_HOLDING_REGISTERS, 10000, 65))
#print(resultado)
#resultado = (master.execute(1, cst.READ_HOLDING_REGISTERS, 35000, 15))
#print(resultado)
#resultado = (master.execute(1, cst.READ_HOLDING_REGISTERS, 10014, 15))
#print(resultado)
master.close()



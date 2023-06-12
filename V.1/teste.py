import modbus_tk.defines as cst
from modbus_tk import modbus_tcp

master = modbus_tcp.TcpMaster("192.168.10.232", 502)
master.set_timeout(5.0)

resposta = master.execute(1, cst.READ_HOLDING_REGISTERS, 10000, 15)#10014

print(resposta)
caracteres_ascii = ""

for numero in resposta:
    caractere = chr(numero)
    caracteres_ascii += caractere

print(caracteres_ascii)











master.close()

import ctypes
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp


class maquina:
    def __init__(self, host, nome):
        self.host = host
        self.nome = nome
  
    def conecta(self):
        try:
            self.master = modbus_tcp.TcpMaster(self.host, 502)
            self.master.set_timeout(5.0)        
            print("conexão aberta com: ", self.host)
        except modbus_tcp.ModbusError as e:
            print("Erro ao conectar:", str(e))
        except Exception as e:
            print("Erro desconhecido ao conectar:", str(e))

    def desconecta(self):
        try:
            self.master.close()
        except modbus_tcp.ModbusError as e:
            print("Erro ao desconectar:", str(e))
        except Exception as e:
            print("Erro desconhecido ao desconectar:", str(e))

        

    def leDword(self, dword_address):
        try:
            dword_data = self.master.execute(1, cst.READ_HOLDING_REGISTERS, dword_address, 2)
            dword_value = (dword_data[1] << 16) + dword_data[0]
            return dword_value
        except modbus_tcp.ModbusError as e:
            print("Erro:", str(e))
        except Exception as e:
            print("Erro desconhecido:", str(e))

    def leReal(self, real_address):
        try:
            real_data = self.master.execute(1, cst.READ_HOLDING_REGISTERS, real_address, 2)
            real_bytes = bytearray([real_data[0] & 0xFF, real_data[0] >> 8, real_data[1] & 0xFF, real_data[1] >> 8])
            real_value = ctypes.c_float.from_buffer(real_bytes).value
            return  real_value
        except modbus_tcp.ModbusError as e:
            print("Erro:", str(e))
        except Exception as e:
            print("Erro desconhecido:", str(e))
    
    def leString(self, start_address):
        try:
            resposta = self.master.execute(1, cst.READ_HOLDING_REGISTERS, start_address, 15)
            caracteres_ascii = ""

            for numero in resposta:
                if 32 <= numero <= 126:  # Intervalo dos caracteres imprimíveis na tabela ASCII
                    caractere = chr(numero)
                    caracteres_ascii += caractere

            return caracteres_ascii
        except modbus_tcp.ModbusError as e:
            print("Erro:", str(e))
        except Exception as e:
            print("Erro desconhecido:", str(e))
        

    def leWord(self,word_address):
        try:
            resultado = (self.master.execute(1, cst.READ_HOLDING_REGISTERS, word_address, 1))
            return resultado[0]
        except modbus_tcp.ModbusError as e:
            print("Erro:", str(e))
        except Exception as e:
            print("Erro desconhecido:", str(e))
    
    def LeDataHora(self, start_address):
        try:
            data = (self.master.execute(1, cst.READ_HOLDING_REGISTERS, start_address, 6))
            resultado = "{:02d}-{:02d}-{:04d} {:02d}:{:02d}:{:02d}".format(
                data[2], data[1], data[0], data[3], data[4], data[5])
            return resultado
        except modbus_tcp.ModbusError as e:
            print("Erro:", str(e))
        except Exception as e:
            print("Erro desconhecido:", str(e))
        
    
    def escreveLinha(self, address):
        resposta = False
        try:
            # Conectar-se ao dispositivo PLC
            self.master.execute(1, cst.WRITE_SINGLE_REGISTER, 36000, output_value=address)
            #print("status da escrita da linha: ")
            resposta = True
        except:           
            print('erro fatal na escrita da linha')
            resposta = False
        
        return resposta
        
    def carregaLinhaRelatorio(self):
        estado = False
        try:
            # Escrever o valor True na bobina
            self.master.execute(1, cst.WRITE_SINGLE_COIL, 42000, output_value=True)
            #self.master.execute(1, cst.WRITE_SINGLE_COIL, 42000, output_value=False)
            estado = True
            #print("status da escrita da linha: ")
        except:  
            estado = False
            print('erro fatal no carregamento da linha do relatorio no TRUE')
            
        
        return estado
            

    def leBool(self, address):
        try:
            resultado = (self.master.execute(1, cst.READ_COILS, address, 1))
            return resultado[0]
        except modbus_tcp.ModbusError as e:
            print("Erro:", str(e))
        except Exception as e:
            print("Erro desconhecido:", str(e))

            
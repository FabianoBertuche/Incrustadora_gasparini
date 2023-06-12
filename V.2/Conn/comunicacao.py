
import ctypes
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp


class maquina:
    def __init__(self, host):
        self.host = host
  
    def conecta(self):
        self.master = modbus_tcp.TcpMaster(self.host, 502)
        self.master.set_timeout(5.0)
        
        print("conexão aberta com: ", self.host)

    def desconecta(self):
        self.master.close()
        #print("conexão fechada")

    def leDword(self, dword_address):
        # Leitura de um registrador DWORD
        print('tentando ler: ', dword_address) 
        dword_data = self.master.execute(1, cst.READ_HOLDING_REGISTERS, dword_address, 2)
        dword_value = (dword_data[1] << 16) + dword_data[0]
        return dword_value

    def leReal(self, real_address):
        real_data = self.master.execute(1, cst.READ_HOLDING_REGISTERS, real_address, 2)
        real_bytes = bytearray([real_data[0] & 0xFF, real_data[0] >> 8, real_data[1] & 0xFF, real_data[1] >> 8])
        real_value = ctypes.c_float.from_buffer(real_bytes).value
        return  real_value
    
    def leString(self, start_address):
        resposta = self.master.execute(1, cst.READ_HOLDING_REGISTERS, start_address, 15)
        caracteres_ascii = ""

        for numero in resposta:
            if 32 <= numero <= 126:  # Intervalo dos caracteres imprimíveis na tabela ASCII
                caractere = chr(numero)
                caracteres_ascii += caractere

        return caracteres_ascii
   

    

    def leWord(self,word_address):
        resultado = (self.master.execute(1, cst.READ_HOLDING_REGISTERS, word_address, 1))
        return resultado[0]
    
    def LeDataHora(self, start_address):
        data = (self.master.execute(1, cst.READ_HOLDING_REGISTERS, start_address, 6))
        resultado = "{}/{}/{} {}:{}:{}".format(data[2], data[1] , data[0], data[3] , data[4] , data[5]  )
        return resultado
    
    def escreveLinha(self, address):
        resposta = False
        try:
            # Conectar-se ao dispositivo PLC
            self.master.execute(1, cst.WRITE_SINGLE_REGISTER, 15000, output_value=address)
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
        resultado = (self.master.execute(1, cst.READ_COILS, address, 1))
        return resultado[0]

            
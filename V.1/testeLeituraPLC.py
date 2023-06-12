
from Conn.comunicacao import maquina
from Data.dados import BancoDados

db1 = BancoDados()
db1.criaTabelas()

maq01 = "192.168.10.232"
#maq02 = "192.168.10.235"

plc1 = maquina(maq01)
plc1.conecta()

#cria o vetor que ira receber os valores a serem escritos no banco
dados = [] 
dados.append( plc1.host) #end_maquina
dados.append(plc1.leDword(10012)) # ID_REGISTRO
dados.append( plc1.leString(10014)) # NR_DOCUMENTO
dados.append(plc1.leDword(10042) ) #NR_BATELADA
dados.append( plc1.leWord(10061) ) #TIPO_BATELADA
dados.append( plc1.LeDataHora(10000)) #H_INICIO
dados.append( plc1.LeDataHora(10006) ) # H_FIM
dados.append( plc1.leReal(10044) ) #Q_SEMENTE
dados.append( plc1.leReal(10046)) # Q_COLA
dados.append( plc1.leReal(10048))#Q_CORANTE
dados.append( plc1.leReal(10050) )#Q_PO1
dados.append(plc1.leReal(10052) )#Q_PO2
dados.append( plc1.leWord(10054))#T_ALIMENTA_SEMENTE
dados.append( plc1.leWord(10055) )#T_DOSA_COLA
dados.append( plc1.leWord(10056) )#T_DOSA_CORANTE
dados.append(plc1.leWord(10057) ) #T_DOSA_PO1
dados.append(plc1.leWord(10058) )#T_DOSA_PO2
dados.append( plc1.leWord(10059))#T_CICLO_PANELA
dados.append( plc1.leWord(10060))#T_PAUSA

print(dados)

db1.gravaRelatorio(dados)

plc1.desconecta()
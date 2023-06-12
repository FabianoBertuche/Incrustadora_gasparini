import time
from Conn.comunicacao import maquina
from Data.dados import BancoDados

db1 = BancoDados()
db1.criaTabelas()

maq01 = "192.168.10.232"
#maq02 = "192.168.10.235"

plc1 = maquina(maq01)
plc1.conecta()

tagStart = True
espera = True

#função sincronismo

while tagStart:
    linhaLida = 0
    idRegistro = 0

    # testa se deve sencronizar
    #busca no banco de dados ULTIMA_LINHA_LIDA, ULTIMO_ID_LIDO do ultimo sincronismo
    posicao_anterior = db1.buscaUltimaSinc()
    print("Ultima posição salva no banco",posicao_anterior)
    
    #busca no plc a proxima linha    
    if posicao_anterior[0] + 1 < 1501 :
        plc1.escreveLinha(posicao_anterior[0] + 1)
        linhaLida = posicao_anterior[0] + 1 
    else:
        plc1.escreveLinha(4)
        linhaLida = 4 

    plc1.carregaLinhaRelatorio()

    #faz pausa
    time.sleep(0.15)

    #le id do registro
    idRegistro = plc1.leDword(10000)
    print("linha lida: ",linhaLida, ", id do registro: ",idRegistro )

    # verifica se id lido é > que ultimo id salvo
    if (idRegistro > posicao_anterior[1] ):
        dados = [] 

        #print("esta lendo isso")
        print(plc1.leString(10002))
        #print(plc1.leDword(10028))
        dados.append( plc1.host) #end_maquina
        dados.append(plc1.leDword(10000)) # ID_REGISTRO
        dados.append( plc1.leString(10002)) # NR_DOCUMENTO
        dados.append(plc1.leDword(10050) ) #NR_BATELADA
        dados.append( plc1.leWord(10069) ) #TIPO_BATELADA
        dados.append( plc1.LeDataHora(10017)) #H_INICIO
        dados.append( plc1.LeDataHora(10023) ) # H_FIM
        dados.append( plc1.leReal(10052) ) #Q_SEMENTE
        dados.append( plc1.leReal(10054)) # Q_COLA
        dados.append( plc1.leReal(10056))#Q_CORANTE
        dados.append( plc1.leReal(10058) )#Q_PO1
        dados.append(plc1.leReal(10060) )#Q_PO2
        dados.append( plc1.leWord(10062))#T_ALIMENTA_SEMENTE
        dados.append( plc1.leWord(10063) )#T_DOSA_COLA
        dados.append( plc1.leWord(10064) )#T_DOSA_CORANTE
        dados.append(plc1.leWord(10065) ) #T_DOSA_PO1
        dados.append(plc1.leWord(10066) )#T_DOSA_PO2
        dados.append( plc1.leWord(10067))#T_CICLO_PANELA
        dados.append( plc1.leWord(10068))#T_PAUSA 
        db1.gravaRelatorio(dados)
       
        #tagStart = False
        print(dados)

        atualizaDB = [linhaLida, idRegistro]
        db1.salvaUltimaSinc(atualizaDB)
    else:
        #sai do loop
        tagStart = False
        print ("sem novos Registros")

    #faz pausa
    time.sleep(0.1)





plc1.desconecta()
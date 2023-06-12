#importações
import platform
import sys, os
from variaveis import servidores
#configurações
sys.path.insert(0, "..")


def check():
    from variaveis import servidores
    # Variaveis Globais
    lista = []
    listaFinal = []
    servidor = []
    resposta=[]
    
    # abrir arquivo com endereços dos servers OPC-UA
    with open("data/conect.bin","r") as arquivo:
        lista = arquivo.readlines()
  
    #limpa lista
    for l in lista:
        tira="\n,[]'"
        char_rep={k: '' for k in tira}
        string1=str(l).translate(str.maketrans(char_rep))
        listaFinal.append(string1)
     
    resposta= []

    for l in listaFinal:
        #print("checando: ",l)
        if platform.system().lower() == "windows":
            response = os.system("ping -n 1 -w 500 " + l + " > nul")
            if response == 0:
                #print("alive")
                resposta.append(l)
            
    servidores = []
    return resposta
    
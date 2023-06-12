
import locServer



#region declara variaveis

lista = []
listaEnderecos= []

#endregion


#region cria objeto  Maquinas
#busca servidores possiveis
# abrir arquivo com endereços
if True:
    with open("data/conect.bin","r") as arquivo:
        lista = arquivo.readlines()
    
    #limpa lista
    for l in lista:
        tira="\n,[]'"
        char_rep={k: '' for k in tira}
        string1=str(l).translate(str.maketrans(char_rep))
        listaEnderecos.append(string1)

    print(listaEnderecos)
#endregion

leitor = locServer.check()

print(leitor)
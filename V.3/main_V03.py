#region Descrição da versão
###############################################################################
#!/usr/bin/env python3                                                        #
# -*- coding: utf-8 -*-                                                       #
#---------------------------------------------------------------------------- #
# Created By  : Fabiano Bertuche                                              #
# Created Date: 01/05/2023                                                    #
# version ='0.01'                                                              #
# --------------------------------------------------------------------------- #
# Descrição:                                                                  #
###############################################################################
#endregion

#region importações
import sys
from tkinter.filedialog import asksaveasfile
import tkinter as tk
from tkinter import   ttk ,Label, LabelFrame, PhotoImage, Frame, Text, Scrollbar
from pystray import MenuItem as item
import pystray
from PIL import ImageTk, Image
import threading
import time
from Conn.comunicacao import maquina
from Data.dados import BancoDados
#from acessaPlc import plc

import locServer
#endregion

#region declara variaveis
lista = []
listaEnderecos= []
listaMaquinas ={}
ordem_atual = {}

# Variável de controle para sinalizar o fechamento do programa
fechando_programa = False

db1 = BancoDados()
db1.criaTabelas()

janela = tk.Tk() 
janela.title('Pinhalense Interface Log')
janela.iconbitmap("img/logo.ico")

imagem1 = PhotoImage(file="img/off.png")
imagem2 = PhotoImage(file="img/off.png")
imagem3 = PhotoImage(file="img/off.png")
imagem4 = PhotoImage(file="img/off.png")

tagStart = True
tempoEntreLEituras = 10
#endregion

#region log
"""
def redirecionar_saida(widget):
    class RedirecionadorSaida:
        def __init__(self, widget):
            self.widget = widget

        def write(self, texto):
            self.widget.insert('end', texto)
            self.widget.see('end')  # Rolagem automática para o final

    sys.stdout = RedirecionadorSaida(widget)
"""
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
        listaMaquinas.update({string1 : 0})

    print(listaEnderecos)#lista para exibir 
    print(listaMaquinas)#dicionario para status
#endregion

#region cria instancias com os IP

plc1 = maquina(listaEnderecos[0], "Maquina01")
plc2 = maquina(listaEnderecos[1], "Maquina02")
plc3 = maquina(listaEnderecos[2], "Maquina03")
plc4 = maquina(listaEnderecos[3], "Maquina04")

#endregion

#region função do botão escolhe local para salvar
def save():  
    #chama interface do sistema para escolher local a salvar   
    files = [('CSV UTF-8(Delimitado por virgulas)', '*.csv')] 
    file = asksaveasfile(filetypes = files, defaultextension = files) 
    local =file.name 
    print(local)
    #atualiza label com novo local de salvamento
    #labela2.config(text= local)
    # atualiza arquivo config com local de salvamento
    arquivo = open("data/config.bin", 'w')
    arquivo.write(local)
    arquivo.close()
    #testa função salvar 
    #gravaLog()

#endregion

#region  cria interface

#region funcoes de try
# função para sair da janela
def quit_window(icon, item):
   global fechando_programa
   fechando_programa = True

   icon.stop()
   janela.destroy()   
# função para mostrar a janela novamente
def show_window(icon, item):
   icon.stop()
   janela.after(0,janela.deiconify())

# Ocultar a janela e mostrar na barra de tarefas do sistema
def hide_window():
   janela.withdraw()
   image=Image.open("img/logo.ico")
   menu=(item('Fechar', quit_window), item('Mostrar', show_window))
   icon=pystray.Icon("Pinhalense", image, "Pinhalense Interface Log", menu)
   icon.run()

janela.protocol('WM_DELETE_WINDOW', hide_window)

#endregion 

# region Inserir Logo Pinhalense
frame0 = Frame(janela,  padx=5, pady=5)
frame0.grid(row=0, column=0)

imagem = PhotoImage(file="img/logo-pinhalense.png")
w = Label(frame0, image=imagem)
w.imagem = imagem
w.grid(row=0, column=0)
#endregion


#region exibe DB



def abrir_nova_tela():
    # Criar uma nova janela
    global ordem_atual

    janelaDB = tk.Toplevel()
    janelaDB.title('Registors no Banco de Dados')

    

    dados = db1.exibeRelatorio()
    # Criar o Treeview para exibir os dados em uma tabela
    treeview = ttk.Treeview(janelaDB, show="headings")
    treeview["columns"] = ("End_Maquina", "ID_Registro", "NR_DOCUMENTO", "NR_BATELADA", "TIPO_BATELADA", "H_INICIO",
                           "H_FIM", "Q_SEMENTE", "Q_COLA", "Q_CORANTE", "Q_PO1", "Q_PO2", "T_ALIMENTA_SEMENTE",
                           "T_DOSA_COLA", "T_DOSA_CORANTE", "T_DOSA_PO1", "T_DOSA_PO2", "T_CICLO_PANELA", "T_PAUSA")
    # Remover caracteres especiais dos nomes das colunas
    colunas = treeview["columns"]
    colunas_formatadas = [col.replace("_", " ") for col in colunas]
    # Definir os cabeçalhos das colunas
    for col, col_formatada in zip(colunas, colunas_formatadas):
        col_encoded = col.encode("utf-8")
        treeview.heading(col_encoded, text=col_formatada, command=lambda c=col_encoded: sort_column(treeview, c))
    # Definir estilos das linhas alternadas
    treeview.tag_configure("linha_clara", background="#FFFFFF")
    treeview.tag_configure("linha_escura", background="#EAEAEA")
    # Inicializar a ordem atual das colunas
    for col in colunas:
        col_encoded = col.encode("utf-8")
        ordem_atual[col_encoded] = "asc"

    # inserir scroll
    vsb = ttk.Scrollbar(janelaDB, orient="vertical", command=treeview.yview)
    vsb.pack(side='right', fill='y')
    treeview.configure(yscrollcommand=vsb.set)

    
    # Inserir os dados na tabela
    for i, row in enumerate(dados):
        estilo_linha = "linha_clara" if i % 2 == 0 else "linha_escura"
        treeview.insert("", tk.END, text=row[0], values=row[1:], tags=(estilo_linha,))
    # Adicionar o Treeview à nova janela
    treeview.pack(fill=tk.BOTH, expand=True)
    

       
    # Adicionar widgets à nova janela
    # ...

#region organiza colunas
def sort_column(treeview, col):
    global ordem_atual
    # Obter todos os itens da tabela
    items = treeview.get_children("")
    # Verificar a ordem atual da coluna
    ordem = ordem_atual[col]
    if ordem == "asc":
        ordem_atual[col] = "desc"
    else:
        ordem_atual[col] = "asc"
    # Ordenar os itens com base no valor da coluna
    items = sorted(items, key=lambda item: treeview.set(item, col), reverse=(ordem == "desc"))
    # Reordenar os itens na tabela
    for index, item in enumerate(items):
        treeview.move(item, "", index)
#endregion

#endregion

#region cria a frame Status Maquinas:
frame1 = LabelFrame(janela, text="Maquinas:", padx=5, pady=5 )
frame1.grid(row=1, column=0, sticky='we')


###### exibe os endereços e os estatus
frameip = LabelFrame(frame1, text="Status:", padx=5, pady=5 )
frameip.grid( row=0 ,column=0, sticky='we')
#1

imagem_label1 = Label(frameip, image=imagem1)
imagem_label1.imagem = imagem1
imagem_label1.grid(row=0, column=0)

labela21 = Label(frameip, text= listaEnderecos[0])
labela21.grid(row=0, column=1)

#2

imagem_label2 = Label(frameip, image=imagem2)
imagem_label2.imagem = imagem2
imagem_label2.grid(row=1, column=0)

labela22 = Label(frameip, text= listaEnderecos[1])
labela22.grid(row=1, column=1)

#3

imagem_label3 = Label(frameip, image=imagem3)
imagem_label3.imagem = imagem3
imagem_label3.grid(row=2, column=0)

labela23 = Label(frameip, text= listaEnderecos[2])
labela23.grid(row=2, column=1)

#4

imagem_label4 = Label(frameip, image=imagem4)
imagem_label4.imagem = imagem4
imagem_label4.grid(row=3, column=0)

labela24 = Label(frameip, text= listaEnderecos[3])
labela24.grid(row=3, column=1)


# botão abrir relatorios
framedb = LabelFrame(frame1, text="Status Maquinas:", padx=5, pady=5 )
framedb.grid(row=0, column=2, sticky='we')

botaoDB = ttk.Button(framedb, text="Registos Salvos", command= abrir_nova_tela)
botaoDB.grid(row=2, column=3)


#endregion

#region cria a frame de Processo:
frame2 = LabelFrame(janela, text="Processo:", padx=5, pady=5 )
frame2.grid(row=2, column=0, sticky='we')

# Criar Text widget para exibir a saída
text_widget = Text(frame2, height=10, width=40)
text_widget.pack(side='left', fill='both', expand=True)

# Adicionar uma barra de rolagem
scrollbar = Scrollbar(frame2)
scrollbar.pack(side='right', fill='y')

# Associar a barra de rolagem com o Text widget
text_widget.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_widget.yview)

# Redirecionar a saída padrão para o Text widget
"""

redirecionar_saida(text_widget)

"""
#endregion

#region cria a frame de salvar em:
frame3 = LabelFrame(janela, text="Salvar em:", padx=5, pady=5 )
frame3.grid(row=3, column=0, sticky='we')

#LAbel exibe o caminho de onde esa sendo salvo
labela4 = Label(frame3, text= 'teste teste')
labela4.grid(row=3, column=1)

#btn seleciona onde salvar o arquivo
btn = ttk.Button(frame3, text = 'Salvar como', command = lambda : save()) 
btn.grid(row=3, column=0)

#endregion

#region Minha_funcao
def minha_funcao():

    if not fechando_programa:
    
        leitor = locServer.check()
        #print(leitor)

        #zera o dicionario
        for chave in listaMaquinas:
            listaMaquinas[chave] = 0

        #seta dispositivo online
        for e in leitor:
            listaMaquinas[e] = 1

       # print(listaMaquinas)#dicionario atualizado  
        mudaImagnes()  
        funcaoPrincipal() 

        # Coloque o código da sua função aqui
        #print("Executando minha_funcao()")

       
    threading.Timer(tempoEntreLEituras, minha_funcao).start()

#endregion

#region consultaPlcGravaBanco
def consultaPlcGravaBanco(PLC, posicaoBanco):

    #print("##################################", endereco)
    plc = PLC
    plc.conecta()
    tagStart = True

         #função sincronismo
    while tagStart:
        linhaLida = 0
        idRegistro = 0

            # testa se deve sencronizar
            #busca no banco de dados ULTIMA_LINHA_LIDA, ULTIMO_ID_LIDO do ultimo sincronismo
        posicao_anterior = db1.buscaUltimaSinc(posicaoBanco)
        print("Ultima posição salva no banco",posicao_anterior)
            
            #busca no plc a proxima linha    
        if posicao_anterior[0] + 1 < 1501 :
            plc.escreveLinha(posicao_anterior[0] + 1)
            linhaLida = posicao_anterior[0] + 1 
        else:
            plc.escreveLinha(4)
            linhaLida = 4 

        plc.carregaLinhaRelatorio()

            #faz pausa
        time.sleep(0.2)

            #le id do registro
        idRegistro = plc.leDword(10000)
        print("linha lida: ",linhaLida, ", id do registro: ",idRegistro )

            # verifica se id lido é > que ultimo id salvo
        if ((idRegistro) == posicao_anterior[1]+1 ):
            dados = [] 

                #print("esta lendo isso")
                #print(plc4.leString(10002))
                #print(plc1.leDword(10028))
            dados.append( plc.nome) #end_maquina
            dados.append(plc.leDword(10000)) # ID_REGISTRO
            dados.append( plc.leString(10002)) # NR_DOCUMENTO
            dados.append(plc.leDword(10050) ) #NR_BATELADA
            dados.append( plc.leWord(10069) ) #TIPO_BATELADA
            dados.append( plc.LeDataHora(10017)) #H_INICIO
            dados.append( plc.LeDataHora(10023) ) # H_FIM
            dados.append( plc.leReal(10052) ) #Q_SEMENTE
            dados.append( plc.leReal(10054)) # Q_COLA
            dados.append( plc.leReal(10056))#Q_CORANTE
            dados.append( plc.leReal(10058) )#Q_PO1
            dados.append(plc.leReal(10060) )#Q_PO2
            dados.append( plc.leWord(10062))#T_ALIMENTA_SEMENTE
            dados.append( plc.leWord(10063) )#T_DOSA_COLA
            dados.append( plc.leWord(10064) )#T_DOSA_CORANTE
            dados.append(plc.leWord(10065) ) #T_DOSA_PO1
            dados.append(plc.leWord(10066) )#T_DOSA_PO2
            dados.append( plc.leWord(10067))#T_CICLO_PANELA
            dados.append( plc.leWord(10068))#T_PAUSA 
                
            
                #tagStart = False
            print(dados)

            db1.gravaRelatorio(dados)
            atualizaDB = [linhaLida, idRegistro]
            db1.salvaUltimaSinc(atualizaDB, posicaoBanco)
        else:
                #sai do loop
            tagStart = False
            print ("sem novos Registros")

    plc.desconecta()

    # Removendo a referência ao objeto
    del plc

#endregion

#region funcaoPrincipal

def funcaoPrincipal():
    tagStart = True

    #1
    if listaMaquinas[listaEnderecos[0]] == 1 :
        consultaPlcGravaBanco(plc1,1)
       

    #2
    if listaMaquinas[listaEnderecos[1]] == 1 :        
        consultaPlcGravaBanco(plc2,2)

    #3
    if listaMaquinas[listaEnderecos[2]] == 1 :
        consultaPlcGravaBanco(plc3,3)

    #4
    if listaMaquinas[listaEnderecos[3]] == 1 :
       consultaPlcGravaBanco(plc4,4)

#endregion

#region muda imagens
def mudaImagnes():
    global imagem_label4, imagem_label3, imagem_label2, imagem_label1

     #1
    if listaMaquinas[listaEnderecos[0]] == 1 :
        nova_imagem1 = PhotoImage(file="img/on.png")       
    else:
        nova_imagem1 = PhotoImage(file="img/off.png") 
    # Atualizar a imagem exibida
    imagem_label1.configure(image=nova_imagem1)
    imagem_label1.image = nova_imagem1  # Atualizar a referência da imagem

     #2
    if listaMaquinas[listaEnderecos[1]] == 1 :
        nova_imagem2 = PhotoImage(file="img/on.png")       
    else:
        nova_imagem2 = PhotoImage(file="img/off.png") 
    # Atualizar a imagem exibida
    imagem_label2.configure(image=nova_imagem2)
    imagem_label2.image = nova_imagem2  # Atualizar a referência da imagem

     #3
    if listaMaquinas[listaEnderecos[2]] == 1 :
        nova_imagem3 = PhotoImage(file="img/on.png")       
    else:
        nova_imagem3 = PhotoImage(file="img/off.png") 
    # Atualizar a imagem exibida
    imagem_label3.configure(image=nova_imagem3)
    imagem_label3.image = nova_imagem3  # Atualizar a referência da imagem

    #4
    if listaMaquinas[listaEnderecos[3]] == 1 :
        nova_imagem4 = PhotoImage(file="img/on.png")       
    else:
        nova_imagem4 = PhotoImage(file="img/off.png") 
    # Atualizar a imagem exibida
    imagem_label4.configure(image=nova_imagem4)
    imagem_label4.image = nova_imagem4  # Atualizar a referência da imagem

 #  

#endregion

#region inicializa
minha_funcao()

# Iniciar a função repetidamente após 10 segundos
threading.Timer(tempoEntreLEituras, minha_funcao).start()

# Iniciar o loop principal do Tkinter
janela.mainloop()

#endregion

#endregion
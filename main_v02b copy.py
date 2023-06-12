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
from tkinter import Tk, ttk ,Label, LabelFrame, PhotoImage, Frame, Text, Scrollbar
from pystray import MenuItem as item
import pystray
from PIL import ImageTk, Image
import threading
import time

import locServer
#endregion

#region declara variaveis
lista = []
listaEnderecos= []
listaMaquinas ={}
# Variável de controle para sinalizar o fechamento do programa
fechando_programa = False



#endregion

janela = Tk() 
janela.title('Pinhalense Interface Log')
janela.iconbitmap("img/logo.ico")

imagem1 = PhotoImage(file="img/off.png")
imagem2 = PhotoImage(file="img/off.png")
imagem3 = PhotoImage(file="img/off.png")
imagem4 = PhotoImage(file="img/off.png")



#region log
def redirecionar_saida(widget):
    class RedirecionadorSaida:
        def __init__(self, widget):
            self.widget = widget

        def write(self, texto):
            self.widget.insert('end', texto)
            self.widget.see('end')  # Rolagem automática para o final

    sys.stdout = RedirecionadorSaida(widget)

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


# region Inserir Logo Pinhalense
frame0 = Frame(janela,  padx=5, pady=5)
frame0.grid(row=0, column=0)

imagem = PhotoImage(file="img/logo-pinhalense.png")
w = Label(frame0, image=imagem)
w.imagem = imagem
w.grid(row=0, column=0)
#endregion

#region cria a frame Status Maquinas:
frame1 = LabelFrame(janela, text="Status Maquinas:", padx=5, pady=5 )
frame1.grid(row=1, column=0, sticky='we')


###### exibe os endereços e os estatus
#1

imagem_label1 = Label(frame1, image=imagem1)
imagem_label1.imagem = imagem1
imagem_label1.grid(row=0, column=0)

labela21 = Label(frame1, text= listaEnderecos[0])
labela21.grid(row=0, column=1)



#2

imagem_label2 = Label(frame1, image=imagem2)
imagem_label2.imagem = imagem2
imagem_label2.grid(row=1, column=0)

labela22 = Label(frame1, text= listaEnderecos[1])
labela22.grid(row=1, column=1)

#3

imagem_label3 = Label(frame1, image=imagem3)
imagem_label3.imagem = imagem3
imagem_label3.grid(row=2, column=0)

labela23 = Label(frame1, text= listaEnderecos[2])
labela23.grid(row=2, column=1)

#4

imagem_label4 = Label(frame1, image=imagem4)
imagem_label4.imagem = imagem4
imagem_label4.grid(row=3, column=0)

labela24 = Label(frame1, text= listaEnderecos[3])
labela24.grid(row=3, column=1)
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
redirecionar_saida(text_widget)

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


def minha_funcao():

    if not fechando_programa:
    
        leitor = locServer.check()
        print(leitor)

        #zera o dicionario
        for chave in listaMaquinas:
            listaMaquinas[chave] = 0

        #seta dispositivo online
        for e in leitor:
            listaMaquinas[e] = 1

        print(listaMaquinas)#dicionario atualizado  
        mudaImagnes()  

        # Coloque o código da sua função aqui
        print("Executando minha_funcao()")

       
    threading.Timer(5, minha_funcao).start()

    

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
   
minha_funcao()



# Iniciar a função repetidamente após 10 segundos
threading.Timer(5, minha_funcao).start()

# Iniciar o loop principal do Tkinter
janela.mainloop()


#endregion
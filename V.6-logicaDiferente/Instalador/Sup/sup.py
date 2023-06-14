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
import xlwt
from tkinter.filedialog import asksaveasfile
import tkinter as tk
from tkinter import   messagebox, ttk ,Label, LabelFrame, PhotoImage, Frame, Text, Scrollbar, filedialog
from pystray import MenuItem as item
import csv
from PIL import ImageTk, Image
import threading
import time
from Conn.comunicacao import maquina
from Data.dados import BancoDados
from tkcalendar import DateEntry
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


dados2 = []

janela = tk.Tk() 
janela.title('Pinhalense Interface Log')
janela.iconbitmap("img/logo.ico")

imagem1 = PhotoImage(file="img/off.png")
imagem2 = PhotoImage(file="img/off.png")
imagem3 = PhotoImage(file="img/off.png")
imagem4 = PhotoImage(file="img/off.png")

tagStart = True
tempoEntreLEituras = 3
auxLinha=0

#endregion

# Função que será chamada quando o botão "Fechar" da janela for clicado
def on_close():
    messagebox.showinfo("Aviso", "Não é possível fechar a janela!")

    print("Não é possível fechar a janela!")
    pass  # Aqui você pode colocar o código que deseja executar antes de impedir o fechamento da janela



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

    #print(listaEnderecos)#lista para exibir 
    #print(listaMaquinas)#dicionario para status
#endregion

#region cria instancias com os IP

plc1 = maquina(listaEnderecos[0], "Maquina01")
plc2 = maquina(listaEnderecos[1], "Maquina02")
plc3 = maquina(listaEnderecos[2], "Maquina03")
plc4 = maquina(listaEnderecos[3], "Maquina04")

#endregion


#region  cria interface

#region funcoes de try

#endregion 



def fechaJanela():
    resposta = messagebox.askyesno("Confirmação", "Deseja realmente parar os registros e fechar a janela?")
    if resposta:
        janela.destroy()  # Fecha a janela Tkinter

#region exibe tela DB

def abrirTelaRelatorioBatelada():

    global ordem_atual, dados2
    nomeMaquinas = db1.recebeNomeMAquinas()
    nomeMaquinas.insert(0, 'Todos')
    dados2 = ()

    # atualiza treeview
    def atualizar_treeview (event):
        global dados2
        # Limpar dados existentes no treeview
        treeview.delete(*treeview.get_children())

        # Obter a opção selecionada no combobox
        opcao_selecionada = combobox.get()

        dados2 = db1.filtraRelatorio(opcao_selecionada)

        #print(dados2)

        # Preencher o treeview com os dados retornados
        for dado in dados2:
            treeview.insert('', 'end', values=dado)

    def exportarXLS():
         # Obter o local e o nome do arquivo usando o filedialog
        arquivo = filedialog.asksaveasfilename(defaultextension='.xls',
                                            filetypes=[('Arquivos Excel', '*.xls')],
                                            title='Salvar como')

        if arquivo:
            # Criar um objeto Workbook
            workbook = xlwt.Workbook()
            # Adicionar uma nova planilha ao workbook
            worksheet = workbook.add_sheet('Dados')

            cabecario = ['n°','end_maquina', 'ID_REGISTRO', 'NR_DOCUMENTO', 'NR_BATELADA', \
                         'TIPO_BATELADA', 'H_INICIO', 'H_FIM', 'Q_SEMENTE', 'Q_COLA', \
                        'Q_CORANTE', 'Q_PO1', 'Q_PO2', 'T_ALIMENTA_SEMENTE', 'T_DOSA_COLA',\
                         'T_DOSA_CORANTE', 'T_DOSA_PO1', 'T_DOSA_PO2', 'T_CICLO_PANELA', 'T_PAUSA']
            
            for coluna, dado in enumerate(cabecario):
                worksheet.write(0, coluna, dado)  # O primeiro argumento é o número da linha (0 nesse caso)

            # Escrever os dados no arquivo Excel
            for linha, valores in enumerate(dados2):
                for coluna, valor in enumerate(valores):
                    worksheet.write(linha + 1, coluna, valor)

            # Salvar o arquivo Excel
            workbook.save(arquivo)

            # Exibir uma mensagem de sucesso
            tk.messagebox.showinfo('Sucesso', 'Arquivo Excel salvo com sucesso!')

    def exportarCSV():
         # Obter o local e o nome do arquivo usando o filedialog
        arquivo = filedialog.asksaveasfilename(defaultextension='.csv',
                                            filetypes=[('Arquivos CSV', '*.csv')],
                                            title='Salvar como')

        if arquivo:
            # Abrir o arquivo CSV para escrita
            with open(arquivo, 'w', newline='') as f:
                # Criar o objeto writer para escrever no arquivo CSV
                writer = csv.writer(f, delimiter=',')

                # Escrever os dados no arquivo CSV
                for linha in dados2:
                    writer.writerow(linha)

            # Exibir uma mensagem de sucesso
            tk.messagebox.showinfo('Sucesso', 'Arquivo CSV salvo com sucesso!')

    def filtra():
        global dados2
        opcao_selecionada = combobox.get()
        data_InicialSelecionada = date_inicio.get()
        data_finalSelecionada = date_fim.get()
        hora_selecionada = "00"
        minutos_selecionados = "00"
        segundos_selecionados = "00"
        data_hora_inicio = f"{data_InicialSelecionada} {hora_selecionada}:{minutos_selecionados}:{segundos_selecionados}"
        data_hora_fim = f"{data_finalSelecionada} {hora_selecionada}:{minutos_selecionados}:{segundos_selecionados}"
            
         # Limpar dados existentes no treeview
        treeview.delete(*treeview.get_children())
   
        if opcao_selecionada == 'Todos':
            dados2 = db1.buscarPorPeriodo(data_hora_inicio, data_hora_fim)
            #print(dados2)
            # Preencher o treeview com os dados retornados
            for dado in dados2:
                treeview.insert('', 'end', values=dado)

        else:
            dados2 = db1.buscarPorPeriodoMaquina(data_hora_inicio, data_hora_fim, opcao_selecionada)
            #print(dados2)
            # Preencher o treeview com os dados retornados
            for dado in dados2:
                treeview.insert('', 'end', values=dado)
            
        

    

    # Criar uma nova janela

    

    janelaDB = tk.Toplevel()
    janelaDB.title('Registros Relatorio Batelada')

    frameDB1 = tk.LabelFrame(janelaDB, text="Comandos", padx=5, pady=5)
    frameDB1.grid(row=0, column=0, sticky='we')

    framecombo = tk.LabelFrame(frameDB1, text="Maquinas:", padx=5, pady=5)
    framecombo.grid(row=0, column=0, sticky='ns')


    combobox = ttk.Combobox(framecombo, width=32, values=nomeMaquinas)
    combobox.current(0)
    combobox.bind("<<ComboboxSelected>>", atualizar_treeview)
    combobox.grid(row=1, column=0)

    labelespaco0 = tk.Label(framecombo, text="  ", padx=5, pady=5)
    labelespaco0.grid(row=1, column=1)


    framedata = tk.LabelFrame(frameDB1, text="Datas:", padx=5, pady=5)
    framedata.grid(row=0, column=1, sticky='ns')

    labelde = tk.Label(framedata, text="De: ", padx=5, pady=5)
    labelde.grid(row=0, column=0, sticky='we')

    # Criar um DateEntry para seleção da data
    date_inicio = DateEntry(framedata, width=22, date_pattern='dd-mm-yyyy', padx=5, pady=5)
    date_inicio.grid(row=0, column=1, sticky='we')

    labelate = tk.Label(framedata, text="ate: ", padx=5, pady=5)
    labelate.grid(row=0, column=2, sticky='we')

    date_fim = DateEntry(framedata, width=22, date_pattern='dd-mm-yyyy', padx=5, pady=5)
    date_fim.grid(row=0, column=3, sticky='we')

    labelespaco = tk.Label(framedata, text="  ", padx=5, pady=5)
    labelespaco.grid(row=0, column=4, sticky='we')

    botao_filtrar = tk.Button(framedata, width=23, text='filtrar por data', command=filtra)
    botao_filtrar.grid(row=0, column=5, sticky='ns')




    frameExport = tk.LabelFrame(frameDB1, text="Exportar:", padx=5, pady=5)
    frameExport.grid(row=0, column=2, sticky='ns')

    botao_voltar = tk.Button(frameExport, text='Exportar .CSV', width=23, command=exportarCSV, padx=5, pady=5)
    botao_voltar.grid(row=1, column=1)

    botao_voltar = tk.Button(frameExport, text='Exportar .xls', width=23, command=exportarXLS, padx=5, pady=5)
    botao_voltar.grid(row=1, column=2)

    





    frameDB2 = tk.LabelFrame(janelaDB, text="Dados:", padx=5, pady=5)
    frameDB2.grid(row=2, column=0, sticky='we')   

    janelaDB.resizable(False, False)

    dados = db1.exibeRelatorio()
    dados2 = dados

    treeview = ttk.Treeview(frameDB2, show="headings")
    treeview["columns"] = ("End_Maquina", "ID_Registro", "NR_DOCUMENTO", "NR_BATELADA", "TIPO_BATELADA", "H_INICIO",
                           "H_FIM", "Q_SEMENTE", "Q_COLA", "Q_CORANTE", "Q_PO1", "Q_PO2")
    colunas = treeview["columns"]

    treeview.column("End_Maquina", width=120)
    treeview.column("ID_Registro", width=30)
    treeview.column("NR_DOCUMENTO", width=80)
    treeview.column("NR_BATELADA", width=80)
    treeview.column("TIPO_BATELADA", width=80)
    treeview.column("H_INICIO", width=230)
    treeview.column("H_FIM", width=230)
    treeview.column("Q_SEMENTE", width=80)
    treeview.column("Q_COLA", width=80)
    treeview.column("Q_CORANTE", width=80)
    treeview.column("Q_PO1", width=50)
    treeview.column("Q_PO2", width=50)

    treeview.heading("End_Maquina", text="Maquina")
    treeview.heading("ID_Registro", text="Id")
    treeview.heading("NR_DOCUMENTO", text="Nr Doc")
    treeview.heading("NR_BATELADA", text="Nr Bat")
    treeview.heading("TIPO_BATELADA", text="Tipo")
    treeview.heading("H_INICIO", text="Inicio")
    treeview.heading("H_FIM", text="Fim")
    treeview.heading("Q_SEMENTE", text="Semente")
    treeview.heading("Q_COLA", text="Cola")
    treeview.heading("Q_CORANTE", text="Corante")
    treeview.heading("Q_PO1", text="Po 1")
    treeview.heading("Q_PO2", text="Po 2")

    treeview.configure(height=30)

    def center_data():

        treeview.update()
        width = treeview.winfo_width()
        for col in treeview["columns"]:
            treeview.column(col, anchor=tk.CENTER, width=int(width / len(treeview["columns"])) - 1)
        treeview.update_idletasks()

    frameDB2.bind("<Configure>", center_data)

    treeview.tag_configure("linha_clara", background="#FFFFFF")
    treeview.tag_configure("linha_escura", background="#EAEAEA")

    for col in colunas:
        col_encoded = col.encode("utf-8")
        ordem_atual[col_encoded] = "asc"

    vsb = ttk.Scrollbar(frameDB2, orient="vertical", command=treeview.yview)
    vsb.grid(row=0, column=1, sticky='ns')
    treeview.configure(yscrollcommand=vsb.set)
    treeview.grid(row=0, column=0, sticky='ns')
    janelaDB.grid_rowconfigure(2, weight=1)
    janelaDB.grid_columnconfigure(1, weight=1)

    for i, row in enumerate(dados):
        estilo_linha = "linha_clara" if i % 2 == 0 else "linha_escura"
        treeview.insert("", tk.END, text=row[0], values=row[1:], tags=(estilo_linha,))

    center_data()

    janelaDB.mainloop()


   
def abrirTelaRelatorioGeral():

    global ordem_atual, dados2
    nomeMaquinas = db1.recebeNomeMAquinasGeral()
    #print(nomeMaquinas)
    nomeMaquinas.insert(0, 'Todos')
    dados2 = ()

    # atualiza treeview
    def atualizar_treeview (event):
        global dados2
        # Limpar dados existentes no treeview
        treeview.delete(*treeview.get_children())

        # Obter a opção selecionada no combobox
        opcao_selecionada = combobox.get()

        dados2 = db1.filtraRelatorioGeral(opcao_selecionada)

        #print(dados2)

        # Preencher o treeview com os dados retornados
        for dado in dados2:
            treeview.insert('', 'end', values=dado)

    def exportarXLS():
         # Obter o local e o nome do arquivo usando o filedialog
        arquivo = filedialog.asksaveasfilename(defaultextension='.xls',
                                            filetypes=[('Arquivos Excel', '*.xls')],
                                            title='Salvar como')

        if arquivo:
            # Criar um objeto Workbook
            workbook = xlwt.Workbook()
            # Adicionar uma nova planilha ao workbook
            worksheet = workbook.add_sheet('Dados')

            cabecario = ["ID", "End_Maquina","ID_REGISTRO", "H_INICIO", "H_FIM", "Q_BATELADA",\
                          "C_SEMENTE", "C_COLA", "C_COREANTE", "Q_PO1", "Q_PO2"]
            
            for coluna, dado in enumerate(cabecario):
                worksheet.write(0, coluna, dado)  # O primeiro argumento é o número da linha (0 nesse caso)

            # Escrever os dados no arquivo Excel
            for linha, valores in enumerate(dados2):
                for coluna, valor in enumerate(valores):
                    worksheet.write(linha + 1, coluna, valor)

            # Salvar o arquivo Excel
            workbook.save(arquivo)

            # Exibir uma mensagem de sucesso
            tk.messagebox.showinfo('Sucesso', 'Arquivo Excel salvo com sucesso!')

    def exportarCSV():
         # Obter o local e o nome do arquivo usando o filedialog
        arquivo = filedialog.asksaveasfilename(defaultextension='.csv',
                                            filetypes=[('Arquivos CSV', '*.csv')],
                                            title='Salvar como')

        if arquivo:
            # Abrir o arquivo CSV para escrita
            with open(arquivo, 'w', newline='') as f:
                # Criar o objeto writer para escrever no arquivo CSV
                writer = csv.writer(f, delimiter=',')

                # Escrever os dados no arquivo CSV
                for linha in dados2:
                    writer.writerow(linha)

            # Exibir uma mensagem de sucesso
            tk.messagebox.showinfo('Sucesso', 'Arquivo CSV salvo com sucesso!')

    def filtra():
        global dados2
        opcao_selecionada = combobox.get()
        data_InicialSelecionada = date_inicio.get()
        data_finalSelecionada = date_fim.get()
        hora_selecionada = "00"
        minutos_selecionados = "00"
        segundos_selecionados = "00"
        data_hora_inicio = f"{data_InicialSelecionada} {hora_selecionada}:{minutos_selecionados}:{segundos_selecionados}"
        data_hora_fim = f"{data_finalSelecionada} {hora_selecionada}:{minutos_selecionados}:{segundos_selecionados}"
            
         # Limpar dados existentes no treeview
        treeview.delete(*treeview.get_children())
   
        if opcao_selecionada == 'Todos':
            dados2 = db1.buscarPorPeriodoGeral(data_hora_inicio, data_hora_fim)
            #print(dados2)
            # Preencher o treeview com os dados retornados
            for dado in dados2:
                treeview.insert('', 'end', values=dado)

        else:
            dados2 = db1.buscarPorPeriodoMaquinaGeral(data_hora_inicio, data_hora_fim, opcao_selecionada)
            #print(dados2)
            # Preencher o treeview com os dados retornados
            for dado in dados2:
                treeview.insert('', 'end', values=dado)
            
        

    

    # Criar uma nova janela

    

    janelaDB = tk.Toplevel()
    janelaDB.title('Registros Relatorio Geral')

    frameDB1 = tk.LabelFrame(janelaDB, text="Comandos", padx=5, pady=5)
    frameDB1.grid(row=0, column=0, sticky='we')

    framecombo = tk.LabelFrame(frameDB1, text="Maquinas:", padx=5, pady=5)
    framecombo.grid(row=0, column=0, sticky='ns')


    combobox = ttk.Combobox(framecombo, width=32, values=nomeMaquinas)
    combobox.current(0)
    combobox.bind("<<ComboboxSelected>>", atualizar_treeview)
    combobox.grid(row=1, column=0)

    labelespaco0 = tk.Label(framecombo, text="  ", padx=5, pady=5)
    labelespaco0.grid(row=1, column=1)


    framedata = tk.LabelFrame(frameDB1, text="Datas:", padx=5, pady=5)
    framedata.grid(row=0, column=1, sticky='ns')

    labelde = tk.Label(framedata, text="De: ", padx=5, pady=5)
    labelde.grid(row=0, column=0, sticky='we')

    # Criar um DateEntry para seleção da data
    date_inicio = DateEntry(framedata, width=22, date_pattern='dd-mm-yyyy', padx=5, pady=5)
    date_inicio.grid(row=0, column=1, sticky='we')

    labelate = tk.Label(framedata, text="ate: ", padx=5, pady=5)
    labelate.grid(row=0, column=2, sticky='we')

    date_fim = DateEntry(framedata, width=22, date_pattern='dd-mm-yyyy', padx=5, pady=5)
    date_fim.grid(row=0, column=3, sticky='we')

    labelespaco = tk.Label(framedata, text="  ", padx=5, pady=5)
    labelespaco.grid(row=0, column=4, sticky='we')

    botao_filtrar = tk.Button(framedata, width=23, text='filtrar por data', command=filtra)
    botao_filtrar.grid(row=0, column=5, sticky='ns')




    frameExport = tk.LabelFrame(frameDB1, text="Exportar:", padx=5, pady=5)
    frameExport.grid(row=0, column=2, sticky='ns')

    botao_voltar = tk.Button(frameExport, text='Exportar .CSV', width=23, command=exportarCSV, padx=5, pady=5)
    botao_voltar.grid(row=1, column=1)

    botao_voltar = tk.Button(frameExport, text='Exportar .xls', width=23, command=exportarXLS, padx=5, pady=5)
    botao_voltar.grid(row=1, column=2)

    





    frameDB2 = tk.LabelFrame(janelaDB, text="Dados:", padx=5, pady=5)
    frameDB2.grid(row=2, column=0, sticky='we')   

    janelaDB.resizable(False, False)

    dados = db1.exibeRelatorioGeral()
    dados2 = dados

    #print(dados)

    treeview = ttk.Treeview(frameDB2, show="headings")
    treeview["columns"] = ("End_Maquina","ID_REGISTRO", "H_INICIO", "H_FIM", "Q_BATELADA", "C_SEMENTE", "C_COLA", "C_COREANTE", "Q_PO1", "Q_PO2")
    colunas = treeview["columns"]

    
    treeview.column("End_Maquina", width=100)    
    treeview.column("ID_REGISTRO", width=50)
    treeview.column("H_INICIO", width=220)
    treeview.column("H_FIM", width=220)
    treeview.column("Q_BATELADA", width=100)
    treeview.column("C_SEMENTE", width=100)
    treeview.column("C_COLA", width=100)
    treeview.column("C_COREANTE", width=100)
    treeview.column("Q_PO1", width=100)
    treeview.column("Q_PO2", width=100)

    
    treeview.heading("End_Maquina", text="Maquina")
    treeview.heading("ID_REGISTRO", text="Id Registro")
    treeview.heading("H_INICIO", text="Inicio")
    treeview.heading("H_FIM", text="Fim")
    treeview.heading("Q_BATELADA", text="Qt. Bateladas")
    treeview.heading("C_SEMENTE", text="Qt. Sementes")
    treeview.heading("C_COLA", text="Qt. Cola")
    treeview.heading("C_COREANTE", text="Qt. Corante")
    treeview.heading("Q_PO1", text="Qt. Pó 1")
    treeview.heading("Q_PO2", text="Qt. Pó 2")

    treeview.configure(height=30)

    def center_data():

        treeview.update()
        width = treeview.winfo_width()
        for col in treeview["columns"]:
            treeview.column(col, anchor=tk.CENTER, width=int(width / len(treeview["columns"])) - 1)
        treeview.update_idletasks()

    frameDB2.bind("<Configure>", center_data)

    treeview.tag_configure("linha_clara", background="#FFFFFF")
    treeview.tag_configure("linha_escura", background="#EAEAEA")

    for col in colunas:
        col_encoded = col.encode("utf-8")
        ordem_atual[col_encoded] = "asc"

    vsb = ttk.Scrollbar(frameDB2, orient="vertical", command=treeview.yview)
    vsb.grid(row=0, column=1, sticky='ns')
    treeview.configure(yscrollcommand=vsb.set)
    treeview.grid(row=0, column=0, sticky='ns')
    janelaDB.grid_rowconfigure(2, weight=1)
    janelaDB.grid_columnconfigure(1, weight=1)

    for i, row in enumerate(dados):
        estilo_linha = "linha_clara" if i % 2 == 0 else "linha_escura"
        treeview.insert("", tk.END, text=row[0], values=row[1:], tags=(estilo_linha,))

    center_data()

    janelaDB.mainloop()



  

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

 # region Inserir Logo Pinhalense



#endregion

frame = LabelFrame(janela, text="", padx=5, pady=5 )
frame.grid(row=0, column=0, sticky='w')
imagem = PhotoImage(file="img/logo-pinhalense.png")
w = Label(frame, image=imagem, anchor='w')
w.imagem = imagem
w.grid(row=0, column=0)


#region cria a frame Status Maquinas:

frame1 = LabelFrame(frame, text="Maquinas:", padx=5, pady=5 )
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

labeles1 = tk.Label(frameip, text=">>", padx=5, pady=5)
labeles1.grid(row=0, column=2, sticky='we')

labelplc1 = tk.Label(frameip, text=plc1.nome, padx=5, pady=5)
labelplc1.grid(row=0, column=3, sticky='we')

#2

imagem_label2 = Label(frameip, image=imagem2)
imagem_label2.imagem = imagem2
imagem_label2.grid(row=1, column=0)

labela22 = Label(frameip, text= listaEnderecos[1])
labela22.grid(row=1, column=1)

labeles2 = tk.Label(frameip, text=">>", padx=5, pady=5)
labeles2.grid(row=1, column=2, sticky='we')

labelplc2 = tk.Label(frameip, text=plc2.nome, padx=5, pady=5)
labelplc2.grid(row=1, column=3, sticky='we')

#3

imagem_label3 = Label(frameip, image=imagem3)
imagem_label3.imagem = imagem3
imagem_label3.grid(row=2, column=0)

labela23 = Label(frameip, text= listaEnderecos[2])
labela23.grid(row=2, column=1)

labeles3 = tk.Label(frameip, text=">>", padx=5, pady=5)
labeles3.grid(row=2, column=2, sticky='we')

labelplc3 = tk.Label(frameip, text=plc3.nome, padx=5, pady=5)
labelplc3.grid(row=2, column=3, sticky='we')

#4

imagem_label4 = Label(frameip, image=imagem4)
imagem_label4.imagem = imagem4
imagem_label4.grid(row=3, column=0)

labela24 = Label(frameip, text= listaEnderecos[3])
labela24.grid(row=3, column=1)

labeles4 = tk.Label(frameip, text=">>", padx=5, pady=5)
labeles4.grid(row=3, column=2, sticky='we')

labelplc4 = tk.Label(frameip, text=plc4.nome, padx=5, pady=5)
labelplc4.grid(row=3, column=3, sticky='we')


# botão abrir relatorios
framedb = LabelFrame(frame1, text="Opções:", padx=5, pady=5 )
framedb.grid(row=0, column=2, sticky="nsew")

botaoDB1 = ttk.Button(framedb, text="Relatorio Batelada", command= abrirTelaRelatorioBatelada)
botaoDB1.grid(row=1, column=3, sticky='we')

botaoDB1 = ttk.Button(framedb, text="Relatorio Geral", command= abrirTelaRelatorioGeral)
botaoDB1.grid(row=2, column=3, sticky='we')




botaofecha = ttk.Button(framedb, text="Parar Log", command= fechaJanela)
botaofecha.grid(row=4, column=3, sticky='we')


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


#endregion

#region Minha_funcao
def minha_funcao():

    while True:
    
        leitor = locServer.check()
        
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
        time.sleep(tempoEntreLEituras)  # Espera 

        if listaMaquinas[listaEnderecos[0]] == 1 or listaMaquinas[listaEnderecos[1]] == 1 or\
                listaMaquinas[listaEnderecos[2]] == 1 or listaMaquinas[listaEnderecos[3]] == 1:
            print(" ")
        else:
            print( "Nenhum Equipamento Encontrado")
            print(" ")

       
   

#endregion

#region consultaPlcGravaBancoRelatorio Batelada
def consultaPlcGravaBancoRelatorioBatelada(PLC):

    #print("##################################", endereco)
    plc = PLC
    #plc = plc4
    plc.conecta()
    tagStart = True
    posicaoUltimaLinha = 0

         #função sincronismo
    while tagStart:
        linhaLida = 0
        idRegistro = 0
       
        #le posicao da ultima linha salva
        posicaoUltimaLinha = plc.leWord(36000)
        #print(posicaoUltimaLinha)
        ultimoIDPlc = plc.leDword(36002) - 1
        ultimaLinhaDB = db1.buscaUltimoRegistro()

        # reinicia as linhas
        if posicaoUltimaLinha > 699:
            posicaoUltimaLinha = 1
        # verifica se o registro da linha no plc é maior que o do banco
        print(ultimoIDPlc, '>',ultimaLinhaDB )
        if ultimoIDPlc > ultimaLinhaDB:
            plc.escreveLinhaBatelada(posicaoUltimaLinha)
            plc.carregaLinhaBatelada()

            #faz pausa
            time.sleep(0.2) #le id do registro
            
            dados = [] 
                
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
            #print(dados)

            if plc.leDword(10000) > 0:
                db1.gravaRelatorio(dados)
                #atualizaDB = [linhaLida, idRegistro]
                # db1.salvaUltimaSinc(atualizaDB, posicaoBanco)
                auxLinha = posicaoUltimaLinha
                plc.escreveLinhaBatelada(posicaoUltimaLinha + 1)
            else:
                #print("id_Registro = 0")
                tagStart = False
        else:
                #sai do loop
            tagStart = False
            print ("sem novos Registros")
            plc.escreveLinhaBatelada(posicaoUltimaLinha)

    plc.desconecta()

    # Removendo a referência ao objeto
    del plc


def consultaPlcGravaBancoRelatorioGeral(PLC):

    #print("##################################", endereco)
    plc = PLC
    #plc = plc4
    plc.conecta()
    tagStart = True
    posicaoUltimaLinha = 0

         #função sincronismo
    while tagStart:
        
        #print("relatorio geral")
       
        #le posicao da ultima linha salva
        posicaoUltimaLinha = plc.leWord(36004)
        #print(posicaoUltimaLinha)
        ultimoIDPlc = plc.leDword(36006) - 1
        ultimaLinhaDB = db1.buscaUltimoRegistroGeral()

        # reinicia as linhas
        if posicaoUltimaLinha > 19:
            posicaoUltimaLinha = 1
        # verifica se o registro da linha no plc é maior que o do banco
        print(ultimoIDPlc, '>',ultimaLinhaDB )
        if ultimoIDPlc > ultimaLinhaDB:
            #print("entro")
            plc.escreveLinhaGeral(posicaoUltimaLinha)
            plc.carregaLinhaGeral()

            #faz pausa
            time.sleep(0.2) #le id do registro
            
            dados = [] 
                
            dados.append( plc.nome) #end_maquina
            dados.append(plc.leDword(11000)) # ID_REGISTRO            
            dados.append( plc.LeDataHora(11002)) #H_INICIO
            dados.append( plc.LeDataHora(11008) ) # H_FIM
            dados.append(plc.leDword(11034)) # QT_BATELADAS  
            dados.append( plc.leReal(11036) ) #CONSUMO_SEMENTES
            dados.append( plc.leReal(11038) ) #CONSUMO_COLA
            dados.append( plc.leReal(11040) ) #CONSUMO_CORANTE
            dados.append( plc.leReal(11042) ) #CONSUMO_PO_01
            dados.append( plc.leReal(11044) ) #CONSUMO_PO_02
              
                #tagStart = False
            #print(dados)

            if plc.leDword(11000) > 0:
                db1.gravaRelatorioGeral(dados)
                #atualizaDB = [linhaLida, idRegistro]
                # db1.salvaUltimaSinc(atualizaDB, posicaoBanco)
                plc.escreveLinhaGeral(posicaoUltimaLinha + 1)
            else:
                #print("id_Registro = 0")
                tagStart = False
        else:
                #sai do loop
            tagStart = False
            print ("sem novos Registros")
            plc.escreveLinhaGeral(posicaoUltimaLinha)

    plc.desconecta()

    # Removendo a referência ao objeto
    del plc






#endregion

#region funcaoPrincipal

def funcaoPrincipal():
    tagStart = True

    #1
    if listaMaquinas[listaEnderecos[0]] == 1 :
        consultaPlcGravaBancoRelatorioBatelada(plc1)       
        consultaPlcGravaBancoRelatorioGeral(plc1)   

    #2
    if listaMaquinas[listaEnderecos[1]] == 1 :        
        consultaPlcGravaBancoRelatorioBatelada(plc2)
        consultaPlcGravaBancoRelatorioGeral(plc2)  

    #3
    if listaMaquinas[listaEnderecos[2]] == 1 :
        consultaPlcGravaBancoRelatorioBatelada(plc3)
        consultaPlcGravaBancoRelatorioGeral(plc3)  

    #4
    if listaMaquinas[listaEnderecos[3]] == 1 :
       consultaPlcGravaBancoRelatorioBatelada(plc4)
       consultaPlcGravaBancoRelatorioGeral(plc4)  

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
#minha_funcao()

# Cria uma thread para executar a função ciclica
thread = threading.Thread(target=minha_funcao)
thread.daemon = True  # Define a thread como um daemon para que seja encerrada quando o programa principal for encerrado

# Inicia a execução da função ciclica
thread.start()

# Impede o fechamento da janela ao pressionar o botão "Fechar"
janela.protocol("WM_DELETE_WINDOW", on_close)

janela.resizable(width=False, height=False) 




# Iniciar o loop principal do Tkinter
janela.mainloop()

#endregion


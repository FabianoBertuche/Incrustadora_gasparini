import sqlite3
import tkinter as tk
from tkinter import ttk

janela = tk.Tk()
janela.title("Exibição da Tabela")

con = sqlite3.connect('dbRBatelada.db')
cursor = con.cursor()


consulta = "SELECT * FROM  Dados"
cursor.execute(consulta)

dados = cursor.fetchall()

treeview = ttk.Treeview(janela)
treeview["columns"] = tuple(cursor.description)

# Configurar os cabeçalhos das colunas
for coluna, descricao in enumerate(cursor.description):
    treeview.heading(coluna, text=descricao[0])

# Inserir os dados na tabela
for linha in dados:
    treeview.insert("", "end", values=linha)

treeview.pack(fill="both", expand=True)
cursor.close()
con.close()

janela.mainloop()

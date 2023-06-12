import tkinter as tk
from tkcalendar import DateEntry
from tkinter import messagebox
from datetime import datetime

def obter_data_hora():
    data_selecionada = date_entry.get()
    hora_selecionada = spinbox_hora.get()
    minutos_selecionados = spinbox_minutos.get()
    segundos_selecionados = spinbox_segundos.get()
    data_hora = f"{data_selecionada} {hora_selecionada}:{minutos_selecionados}:{segundos_selecionados}"
    messagebox.showinfo('Data e Hora Selecionadas', data_hora)

# Criar a janela principal
janela = tk.Tk()

# Criar um objeto StringVar para armazenar os valores selecionados
valor_hora = tk.StringVar()
valor_minutos = tk.StringVar()
valor_segundos = tk.StringVar()

# Obter a data e hora atual
data_hora_atual = datetime.now()

# Criar um Combobox para seleção da hora
spinbox_hora = tk.Spinbox(janela, from_=0, to=23, textvariable=valor_hora, width=2, wrap=True)
spinbox_hora.delete(0, tk.END)
spinbox_hora.insert(0, data_hora_atual.hour)
spinbox_hora.pack(side=tk.LEFT)

# Criar um Combobox para seleção dos minutos
spinbox_minutos = tk.Spinbox(janela, from_=0, to=59, textvariable=valor_minutos, width=2, wrap=True)
spinbox_minutos.delete(0, tk.END)
spinbox_minutos.insert(0, data_hora_atual.minute)
spinbox_minutos.pack(side=tk.LEFT)

# Criar um Combobox para seleção dos segundos
spinbox_segundos = tk.Spinbox(janela, from_=0, to=59, textvariable=valor_segundos, width=2, wrap=True)
spinbox_segundos.delete(0, tk.END)
spinbox_segundos.insert(0, data_hora_atual.second)
spinbox_segundos.pack(side=tk.LEFT)

# Criar um DateEntry para seleção da data
date_entry = DateEntry(janela, width=12, date_pattern='yyyy-mm-dd')
date_entry.pack()

# Criar um botão para obter os valores selecionados
botao_obter = tk.Button(janela, text='Obter Data e Hora', command=obter_data_hora)
botao_obter.pack()

# Executar o loop principal da janela
janela.mainloop()

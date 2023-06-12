import csv
from tkinter.filedialog import asksaveasfile
from tkinter import Tk, ttk ,Label, LabelFrame, PhotoImage, Frame
from pystray import MenuItem as item
import pystray
from PIL import Image
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

#declara variaveis



#abre arquivo com o local onde sera salvo os log
with open("data/config.bin","r") as arquivo:
        local = arquivo.read()        
        print("Salvando em: " + local)
arquivo.close()

#função converte word para binario
def wordBinario(dividendo):
   quociente = 1
   lista = []
   while quociente >= 1:
      resto = dividendo % 2
      lista.insert(0,resto)
      quociente = dividendo // 2
      dividendo = quociente
   #binario = ''.join([str(item) for item in lista])
   #return binario
   return lista

#função converte word para binario
def int_to_bin(num):
    """
    Converte um número inteiro de 16 bits em binário.
    """
    bin=[]
    # Converte o número para binário com 16 bits
    binario = format(num, '016b')
    #converte em vetor
    for i in binario:
          bin.append(i)
    #retorna
    return bin



# função que ira gravar os logs
def gravaLog():  
      with open(local, 'w') as csvfile: 
        csv.writer(csvfile, delimiter=',').writerow(['João', '30' ])
        csv.writer(csvfile, delimiter=',').writerow(['José', '27'])
        csv.writer(csvfile, delimiter=',').writerow(['Pedro', '20'])

#função do botão escolhe local para salvar
def save():  
    #chama interface do sistema para escolher local a salvar   
    files = [('CSV UTF-8(Delimitado por virgulas)', '*.csv')] 
    file = asksaveasfile(filetypes = files, defaultextension = files) 
    local =file.name 
    print(local)
    #atualiza label com novo local de salvamento
    labela2.config(text= local)
    # atualiza arquivo config com local de salvamento
    arquivo = open("data/config.bin", 'w')
    arquivo.write(local)
    arquivo.close()
    #testa função salvar 
    gravaLog()


   

# interface
janela = Tk() 
janela.title('Pinhalense Interface Log')
janela.iconbitmap("img/logo.ico")


# função para sair da janela
def quit_window(icon, item):
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


# Inserir Logo Pinhalense
frame0 = Frame(janela,  padx=5, pady=5)
frame0.grid(row=0, column=0)
imagem = PhotoImage(file="img/logo-pinhalense.png")
w = Label(frame0, image=imagem)
w.imagem = imagem
w.grid(row=0, column=0)

# cria a frame de salvar em:
frame1 = LabelFrame(janela, text="Salvar em:", padx=5, pady=5 )
frame1.grid(row=1, column=0, sticky='we')

#LAbel exibe o caminho de onde esa sendo salvo
labela2 = Label(frame1, text= local)
labela2.grid(row=1, column=1)

#btn seleciona onde salvar o arquivo
btn = ttk.Button(frame1, text = 'Salvar como', command = lambda : save()) 
btn.grid(row=1, column=0)




janela.mainloop()
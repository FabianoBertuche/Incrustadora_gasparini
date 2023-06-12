import csv

from tkinter import * 
from tkinter import ttk 
from tkinter.filedialog import asksaveasfile 
  
root = Tk() 
root.geometry('200x150') 
global files, file
local = ''

def save(): 
    global files, file, local
    files = [('CSV UTF-8(Delimitado por virgulas)', '*.csv')] 
    file = asksaveasfile(filetypes = files, defaultextension = files) 
    local =file.name 
    print(local)

    with open(local, 'w') as csvfile: #with open('./teste.csv', 'w') as csvfile:
        csv.writer(csvfile, delimiter=',').writerow(['João', '30' ])
        csv.writer(csvfile, delimiter=',').writerow(['José', '27'])
        csv.writer(csvfile, delimiter=',').writerow(['Pedro', '20'])
    

  
btn = ttk.Button(root, text = 'Save', command = lambda : save()) 
btn.pack(side = TOP, pady = 20) 
  
save()




mainloop() 


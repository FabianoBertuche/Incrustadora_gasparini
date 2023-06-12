import xlwt



workbook = xlwt.Workbook()
sheet = workbook.add_sheet('Planilha1')


linha = ['Dado1', 'Dado2', 'Dado3', 'Dado4']
for coluna, dado in enumerate(linha):
    sheet.write(0, coluna, dado)  # O primeiro argumento é o número da linha (0 nesse caso)

workbook.save('nome_do_arquivo.xls')

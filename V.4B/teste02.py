from tkcalendar import DateEntry

# Criação do DateEntry com o padrão desejado
date_entry = DateEntry(janela, width=12, date_pattern='yyyy-mm-dd')

# Obtém a data no formato padrão
data_padrao = date_entry.get()

# Converte a data para o formato desejado (dd-mm-aaaa)
dia, mes, ano = data_padrao.split('-')
data_formatada = f"{dia}-{mes}-{ano}"

print(data_formatada)  # Saída: dd-mm-aaaa


linha lida:  26 , id do regist
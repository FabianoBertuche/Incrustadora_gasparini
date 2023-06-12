import sqlite3

class BancoDados():

    def __init__(self):
        print("")

    def criaTabelas(self):
        cnnOpcoes = sqlite3.connect('dbSupervisorio.db')
        consultaOpcoes = cnnOpcoes.cursor()
        
        consultaOpcoes.execute('CREATE TABLE IF NOT EXISTS relatorioBatelada( ID INTEGER PRIMARY KEY AUTOINCREMENT , end_maquina TEXT, ID_REGISTRO INTEGER,\
                               NR_DOCUMENTO TEXT, NR_BATELADA INTEGER, TIPO_BATELADA INTEGER, H_INICIO TEXT, H_FIM TEXT, Q_SEMENTE REAL, Q_COLA REAL, \
                               Q_CORANTE REAL, Q_PO1 REAL, Q_PO2 REAL, T_ALIMENTA_SEMENTE INTEGER, T_DOSA_COLA INTEGER, \
                               T_DOSA_CORANTE INTEGER, T_DOSA_PO1 INTEGER,  T_DOSA_PO2 INTEGER,T_CICLO_PANELA INTEGER,T_PAUSA INTEGER )')
        
        # Criar tabela
        consultaOpcoes.execute('CREATE TABLE IF NOT EXISTS ctrlSincronismo( \
            ID INTEGER PRIMARY KEY AUTOINCREMENT, \
            ULTIMA_LINHA_LIDA INTEGER DEFAULT 0, \
            ULTIMO_ID_LIDO INTEGER DEFAULT 0, \
            TEMPO_ESPERA_LEITURA REAL DEFAULT 0.1)')
        
        # Verificar se a tabela está vazia
        consultaOpcoes.execute('SELECT COUNT(*) FROM ctrlSincronismo')
        result = consultaOpcoes.fetchone()
        if result[0] == 0:

            valores = [(0, 0), (0, 0), (0, 0), (0, 0)]
            # Inserir a primeira linha com valores iniciais
            consultaOpcoes.executemany('INSERT INTO ctrlSincronismo (ULTIMA_LINHA_LIDA, ULTIMO_ID_LIDO) VALUES (?, ?)', valores)        
                  
            cnnOpcoes.commit()

        cnnOpcoes.close()
        #print("Banco de Dados Localizado")

    def gravaRelatorio(self, dados):
        cnnConexao = sqlite3.connect('dbSupervisorio.db')
        consultaConexao = cnnConexao.cursor()
        consultaConexao.execute("INSERT INTO relatorioBatelada (end_maquina, ID_REGISTRO, NR_DOCUMENTO, NR_BATELADA, TIPO_BATELADA, H_INICIO, H_FIM, Q_SEMENTE, Q_COLA, \
            Q_CORANTE, Q_PO1, Q_PO2, T_ALIMENTA_SEMENTE, T_DOSA_COLA, T_DOSA_CORANTE, T_DOSA_PO1, T_DOSA_PO2, T_CICLO_PANELA, T_PAUSA) \
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (dados[0], dados[1], dados[2], dados[3], dados[4], dados[5], dados[6], dados[7], dados[8], dados[9], dados[10], dados[11], dados[12], dados[13],
            dados[14], dados[15], dados[16], dados[17], dados[18]))
                                
        cnnConexao.commit()
        cnnConexao.close()
        #print("Dados gravados com sucesso")


    def buscaUltimaSinc(self, posicao):
        # Estabelecer conexão com o banco de dados
        cnnOpcoes = sqlite3.connect('dbSupervisorio.db')
        consultaOpcoes = cnnOpcoes.cursor()
        
        # Consulta para obter os valores das colunas da primeira linha
        consultaOpcoes.execute('SELECT ULTIMA_LINHA_LIDA, ULTIMO_ID_LIDO FROM ctrlSincronismo WHERE ID = ?', (posicao,))
        resultado = consultaOpcoes.fetchone()

        # Fechar conexão
        cnnOpcoes.close()

        # Retorna a consulta
        return resultado
    
    def salvaUltimaSinc(self, dados, posicao):
        cnnConexao = sqlite3.connect('dbSupervisorio.db')
        consultaConexao = cnnConexao.cursor()
        consultaConexao.execute('UPDATE ctrlSincronismo SET ULTIMA_LINHA_LIDA = ?, ULTIMO_ID_LIDO = ? WHERE ID = ?', (dados[0], dados[1], posicao))

        cnnConexao.commit()
        cnnConexao.close()


    def exibeRelatorio(self):
        cnnConexao = sqlite3.connect("dbSupervisorio.db")
        cursor = cnnConexao.cursor()
        cursor.execute("SELECT * FROM relatorioBatelada")
        dados = cursor.fetchall()
        cursor.close()
        cnnConexao.close()

        return dados


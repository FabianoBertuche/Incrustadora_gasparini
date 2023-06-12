import sqlite3
from datetime import datetime

class BancoDados():

    def __init__(self):
        print("")

    def criaTabelas(self):
        try:
            cnnOpcoes = sqlite3.connect('dbSupervisorio.db')
            consultaOpcoes = cnnOpcoes.cursor()
            # tabela relatorio
            consultaOpcoes.execute('CREATE TABLE IF NOT EXISTS relatorioBatelada( ID INTEGER PRIMARY KEY AUTOINCREMENT , end_maquina TEXT, ID_REGISTRO INTEGER DEFAULT 0,\
                                NR_DOCUMENTO TEXT, NR_BATELADA INTEGER, TIPO_BATELADA INTEGER, H_INICIO DATETIME, H_FIM DATETIME, Q_SEMENTE REAL, Q_COLA REAL, \
                                Q_CORANTE REAL, Q_PO1 REAL, Q_PO2 REAL, T_ALIMENTA_SEMENTE INTEGER, T_DOSA_COLA INTEGER, \
                                T_DOSA_CORANTE INTEGER, T_DOSA_PO1 INTEGER,  T_DOSA_PO2 INTEGER,T_CICLO_PANELA INTEGER,T_PAUSA INTEGER )')
            
            
            
            # Verificar se a tabela está vazia
            consultaOpcoes.execute('SELECT COUNT(*) FROM relatorioBatelada')
            result = consultaOpcoes.fetchone()
            if result[0] == 0:

                ss = ['TEXT',  0, 'TEXT',  0,  0,  '00-00-0000 00:00:00',  '00-00-0000 00:00:00', 0,  0,  0,  0,  0,  0,  0, 0, 0, 0, 0, 0]
                self.gravaRelatorio(ss)   


            

             # tabela relatorio geral
            consultaOpcoes.execute('CREATE TABLE IF NOT EXISTS relatorioGeral( ID INTEGER PRIMARY KEY AUTOINCREMENT , end_maquina TEXT, ID_REGISTRO INTEGER DEFAULT 0,\
                                 H_INICIO DATETIME, H_FIM DATETIME,  Q_BATELADAS INTEGER, C_SEMENTE REAL, C_COLA REAL,\
                                C_CORANTE REAL, C_PO1 REAL, C_PO2 REAL )')
                     
            
            # Verificar se a tabela está vazia
            consultaOpcoes.execute('SELECT COUNT(*) FROM relatorioGeral')
            result = consultaOpcoes.fetchone()

            if result[0] == 0:
                print("grava prineiro registro relatorio geral")
                ss2 = ['TEXT',  0, '00-00-0000 00:00:00',  '00-00-0000 00:00:00', 0,  0,  0,  0,  0,  0]
                self.gravaRelatorioGeral(ss2)   
                
            
            
            




            # Criar tabela sincronismo
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
            
        except sqlite3.Error as e:
            print("Erro:", str(e))
            return None
        except Exception as e:
            print("Erro desconhecidos:", str(e))
            return None

    def gravaRelatorio(self, dados):
        try:
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

        except sqlite3.Error as e:
            print("Erro:", str(e))
            return None
        except Exception as e:
            print("Erro desconhecidos:", str(e))
            return None


    def gravaRelatorioGeral(self, dados):

        print("tentando gravar relatorio geral")
        try:
            cnnConexao = sqlite3.connect('dbSupervisorio.db')
            consultaConexao = cnnConexao.cursor()
            consultaConexao.execute("INSERT INTO relatorioGeral (end_maquina, ID_REGISTRO ,H_INICIO, H_FIM ,  Q_BATELADAS , C_SEMENTE , C_COLA ,\
                                C_CORANTE , C_PO1 , C_PO2)  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (dados[0], dados[1], dados[2], dados[3], dados[4], dados[5], dados[6], dados[7], dados[8], dados[9]))
                                    
            cnnConexao.commit()
            cnnConexao.close()
            #print("Dados gravados com sucesso")

        except sqlite3.Error as e:
            print("Erro:", str(e))
            return None
        except Exception as e:
            print("Erro desconhecidos:", str(e))
            return None

    def buscaUltimaSinc(self, posicao):
        # Estabelecer conexão com o banco de dados
        try:
            cnnOpcoes = sqlite3.connect('dbSupervisorio.db')
            consultaOpcoes = cnnOpcoes.cursor()
            
            # Consulta para obter os valores das colunas da primeira linha
            consultaOpcoes.execute('SELECT ULTIMA_LINHA_LIDA, ULTIMO_ID_LIDO FROM ctrlSincronismo WHERE ID = ?', (posicao,))
            resultado = consultaOpcoes.fetchone()

            # Fechar conexão
            cnnOpcoes.close()

            # Retorna a consulta
            return resultado
        
        except sqlite3.Error as e:
            print("Erro:", str(e))
            return None
        except Exception as e:
            print("Erro desconhecidos:", str(e))
            return None
    
    def salvaUltimaSinc(self, dados, posicao):
        try:
            cnnConexao = sqlite3.connect('dbSupervisorio.db')
            consultaConexao = cnnConexao.cursor()
            consultaConexao.execute('UPDATE ctrlSincronismo SET ULTIMA_LINHA_LIDA = ?, ULTIMO_ID_LIDO = ? WHERE ID = ?', (dados[0], dados[1], posicao))
            cnnConexao.commit()
            cnnConexao.close()

        except sqlite3.Error as e:
            print("Erro:", str(e))
            return None
        except Exception as e:
            print("Erro desconhecidos:", str(e))
            return None


    def exibeRelatorio(self):
        try:
            cnnConexao = sqlite3.connect("dbSupervisorio.db")
            cursor = cnnConexao.cursor()
            cursor.execute("SELECT * FROM relatorioBatelada")
            dados = cursor.fetchall()
            cursor.close()
            cnnConexao.close()   
            return dados
        
        except sqlite3.Error as e:
            print("Erro:", str(e))
            return None
        except Exception as e:
            print("Erro desconhecidos:", str(e))
            return None
    
    def recebeNomeMAquinas(self):
        try:
            cnnConexao = sqlite3.connect("dbSupervisorio.db")
            cursor = cnnConexao.cursor()
            cursor.execute("SELECT DISTINCT end_maquina FROM relatorioBatelada")
            dados = cursor.fetchall()
            dados_unicos = [item[0] for item in dados]
            cursor.close()
            cnnConexao.close()
            return dados_unicos
        
        except sqlite3.Error as e:
            print("Erro:", str(e))
            return None
        except Exception as e:
            print("Erro desconhecidos:", str(e))
            return None
        

    def recebeNomeMAquinasGeral(self):
        try:
            cnnConexao = sqlite3.connect("dbSupervisorio.db")
            cursor = cnnConexao.cursor()
            cursor.execute("SELECT DISTINCT end_maquina FROM relatorioGeral")
            dados = cursor.fetchall()
            dados_unicos = [item[0] for item in dados]
            cursor.close()
            cnnConexao.close()
            return dados_unicos
        
        except sqlite3.Error as e:
            print("Erro:", str(e))
            return None
        except Exception as e:
            print("Erro desconhecidos:", str(e))
            return None

    

    def filtraRelatorio(self, valor):
        try:
            if valor == 'Todos':
                cnnConexao = sqlite3.connect("dbSupervisorio.db")
                cursor = cnnConexao.cursor()
                cursor.execute("SELECT * FROM relatorioBatelada")
                dados = cursor.fetchall()
                cursor.close()
                cnnConexao.close()                
                return dados            
            else:
                cnnConexao = sqlite3.connect("dbSupervisorio.db")
                cursor = cnnConexao.cursor()
                cursor.execute("SELECT * FROM relatorioBatelada WHERE end_maquina = ?", (valor,))
                dados = cursor.fetchall()
                cursor.close()
                cnnConexao.close()
                return dados
            
        except sqlite3.Error as e:
            print("Erro:", str(e))
            return None
        except Exception as e:
            print("Erro desconhecidos:", str(e))
            return None
        

    def buscarPorPeriodo(self, tempo_inicial, tempo_final):
        try:
            cnnConexao = sqlite3.connect("dbSupervisorio.db")
            cursor = cnnConexao.cursor()
            cursor.execute("SELECT * FROM relatorioGeral WHERE H_INICIO >= ? AND H_FIM <= ?", (tempo_inicial, tempo_final))
            dados = cursor.fetchall()
            cursor.close()
            cnnConexao.close()
            return dados
        
        except sqlite3.Error as e:
            print("Erro:", str(e))
            return None
        except Exception as e:
            print("Erro desconhecidos:", str(e))
            return None
        

    def buscarPorPeriodoGeral (self, tempo_inicial, tempo_final):
        try:
            cnnConexao = sqlite3.connect("dbSupervisorio.db")
            cursor = cnnConexao.cursor()
            cursor.execute("SELECT * FROM relatorioBatelada WHERE H_INICIO >= ? AND H_FIM <= ?", (tempo_inicial, tempo_final))
            dados = cursor.fetchall()
            cursor.close()
            cnnConexao.close()
            return dados
        
        except sqlite3.Error as e:
            print("Erro:", str(e))
            return None
        except Exception as e:
            print("Erro desconhecidos:", str(e))
            return None
    
    def buscarPorPeriodoMaquina(self, tempo_inicial, tempo_final, end_maquina):
        try:
            cnnConexao = sqlite3.connect("dbSupervisorio.db")
            cursor = cnnConexao.cursor()
            cursor.execute("SELECT * FROM relatorioBatelada WHERE H_INICIO >= ? AND H_FIM <= ? AND end_maquina = ?", (tempo_inicial, tempo_final, end_maquina))
            dados = cursor.fetchall()
            cursor.close()
            cnnConexao.close()
            return dados
        
        except sqlite3.Error as e:
            print("Erro:", str(e))
            return None
        except Exception as e:
            print("Erro desconhecidos:", str(e))
            return None

    

    def buscaUltimoRegistro(self):
        try:
            cnnConexao = sqlite3.connect("dbSupervisorio.db")
            cursor = cnnConexao.cursor()
            cursor.execute("SELECT ID_REGISTRO FROM relatorioBatelada ORDER BY ID_REGISTRO DESC LIMIT 1")
            ultimo_id = cursor.fetchone()[0]
            cursor.close()
            cnnConexao.close()
            return ultimo_id
        except sqlite3.Error as e:
            print("Erro:", str(e))
            return None
        except Exception as e:
            print("Erro desconhecidos:", str(e))
            return None
        

    def buscaUltimoRegistroGeral(self):
        try:
            cnnConexao = sqlite3.connect("dbSupervisorio.db")
            cursor = cnnConexao.cursor()
            cursor.execute("SELECT ID_REGISTRO FROM relatorioGeral ORDER BY ID_REGISTRO DESC LIMIT 1")
            ultimo_id = cursor.fetchone()[0]
            cursor.close()
            cnnConexao.close()
            return ultimo_id
        except sqlite3.Error as e:
            print("Erro:", str(e))
            return None
        except Exception as e:
            print("Erro desconhecidos:", str(e))
            return None
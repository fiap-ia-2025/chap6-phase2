# Importação dos módulos
import oracledb

#Usando o conteúdo do cap 06
class DatabaseConnection:

    def __init__(self):
        # Try para tentativa de Conexão com o Banco de Dados
        try:
            # Efetua a conexão com o Usuário no servidor
            self.connection = oracledb.connect(user='user', password="pass", dsn='url')
            self.connection_register = self.connection.cursor()
            self.connection_list = self.connection.cursor()
            self.is_connected = True
        except Exception as e:
            # Informa o erro
            print("Erro ao conectar na base de dados: ", e)
            self.is_connected = False
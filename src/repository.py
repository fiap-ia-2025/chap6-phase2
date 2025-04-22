from farm import Farm
from database_connection import DatabaseConnection
import pandas as pd


class Repository:

    #Salva os dados da fazenda na base de dados, e consulta pelo id do dado salvo
    def save_farm(self, farm=Farm):
        database_connection = DatabaseConnection()
        if database_connection.is_connected:
            #Tratamento de exceção para evitar que o sistema seja interrompido
            try:
                query = f""" INSERT INTO fazenda (nome, estado, cidade) VALUES ('{farm.get_name()}', '{farm.get_state()}', '{farm.get_city()}') """

                database_connection.connection_register.execute(query)
                database_connection.connection.commit()

                database_connection.connection_list.execute(
                    'select * from fazenda order by id desc fetch first 1 rows only')
                data = database_connection.connection_list.fetchall()
                list_farm = []
                for dt in data:
                    list_farm.append(dt)

                list_farm_df = pd.DataFrame.from_records(list_farm,
                                                         columns=['id', 'nome', 'estado', 'cidade', 'dt_inclusao'])

                return int(list_farm_df['id'][0])

            except Exception as e:
                print(f"Erro ao inserir fazenda na base de dados, erro: {e}!")

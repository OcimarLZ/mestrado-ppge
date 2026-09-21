import pandas as pd
from bdados.tratar_bdados_app import criar_conexao

def carregar_dataframe(sql, params=None):
    # Conectar ao banco de dados SQLite
    modulo = "BD_INEP"
    conexao_result = criar_conexao(modulo)
    db_bi_cnx = conexao_result[0]
    # Executar a query e carregar os resultados em um DataFrame
    df = pd.read_sql_query(sql, db_bi_cnx, params=params)
    # Fechar a conexão com o banco de dados
    db_bi_cnx.close()
    return df



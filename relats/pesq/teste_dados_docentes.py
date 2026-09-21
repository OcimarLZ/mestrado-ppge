"""
Script de teste para verificar os dados de docentes.
Verifica se os dados estão sendo carregados corretamente do banco.
"""

import sys
import os
import pandas as pd

# Adiciona o path das dependências ao sistema
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from bdados.ler_bdados_to_df import carregar_dataframe
from sql_queries import *

def testar_dados_docentes():
    """Testa o carregamento de dados de docentes"""
    
    print("🔍 Testando dados de docentes...")
    print("=" * 60)
    
    # Teste 1: Dados globais de docentes
    print("1. Testando dados globais de docentes:")
    sql_global = get_sql_docentes_global()
    print(f"SQL: {sql_global}")
    
    try:
        df_global = carregar_dataframe(sql_global)
        print(f"✅ Dados carregados: {len(df_global)} linhas")
        print("Primeiras linhas:")
        print(df_global.head())
        print()
    except Exception as e:
        print(f"❌ Erro: {e}")
        print()
    
    # Teste 2: Dados de docentes por titulação
    print("2. Testando dados de docentes doutores:")
    sql_doutores = get_sql_docentes_por_titulacao('dout')
    print(f"SQL: {sql_doutores}")
    
    try:
        df_doutores = carregar_dataframe(sql_doutores)
        print(f"✅ Dados carregados: {len(df_doutores)} linhas")
        print("Primeiras linhas:")
        print(df_doutores.head())
        print()
    except Exception as e:
        print(f"❌ Erro: {e}")
        print()
    
    # Teste 3: Verificar anos disponíveis
    print("3. Verificando anos disponíveis na tabela ies_censo:")
    sql_anos = """
    SELECT DISTINCT ano_censo 
    FROM ies_censo 
    WHERE ano_censo >= 2005 
    ORDER BY ano_censo
    """
    
    try:
        df_anos = carregar_dataframe(sql_anos)
        print("Anos disponíveis:")
        print(df_anos)
        print()
    except Exception as e:
        print(f"❌ Erro: {e}")
        print()
    
    # Teste 4: Verificar dados de docentes por ano
    print("4. Verificando dados de docentes por ano:")
    sql_docentes_ano = """
    SELECT 
        ano_censo,
        COUNT(*) as total_ies,
        SUM(qt_doc_total) as total_docentes,
        SUM(qt_doc_ex_dout) as total_doutores,
        SUM(qt_doc_ex_mest) as total_mestres
    FROM ies_censo 
    WHERE ano_censo >= 2005 
    GROUP BY ano_censo 
    ORDER BY ano_censo
    """
    
    try:
        df_docentes_ano = carregar_dataframe(sql_docentes_ano)
        print("Dados de docentes por ano:")
        print(df_docentes_ano)
        print()
    except Exception as e:
        print(f"❌ Erro: {e}")
        print()
    
    # Teste 5: Verificar se há dados para 2006
    print("5. Verificando dados específicos para 2006:")
    sql_2006 = """
    SELECT 
        ano_censo,
        COUNT(*) as total_ies,
        SUM(qt_doc_total) as total_docentes
    FROM ies_censo 
    WHERE ano_censo = 2006
    GROUP BY ano_censo
    """
    
    try:
        df_2006 = carregar_dataframe(sql_2006)
        print("Dados para 2006:")
        print(df_2006)
        print()
    except Exception as e:
        print(f"❌ Erro: {e}")
        print()

def testar_processamento():
    """Testa o processamento de dados"""
    
    print("🔍 Testando processamento de dados...")
    print("=" * 60)
    
    from data_processors import carregar_dados_por_ano, carregar_dados_agrupados
    
    # Teste 1: Carregar dados globais
    print("1. Testando carregamento de dados globais:")
    dados_globais = carregar_dados_por_ano(get_sql_docentes_global(), "Docentes", 2006, 2025)
    print(f"Dados carregados: {dados_globais}")
    print()
    
    # Teste 2: Carregar dados por titulação
    print("2. Testando carregamento de dados por titulação:")
    dados_doutores = carregar_dados_por_ano(get_sql_docentes_por_titulacao('dout'), "Docentes", 2006, 2025)
    print(f"Dados doutores: {dados_doutores}")
    print()
    
    # Teste 3: Carregar dados agrupados
    print("3. Testando carregamento de dados agrupados:")
    dados_por_categoria = carregar_dados_agrupados(get_sql_docentes_por_categoria(), "categoria", "Docentes", 2006, 2025)
    print(f"Dados por categoria: {dados_por_categoria}")
    print()

if __name__ == "__main__":
    print("🚀 Iniciando testes de dados de docentes...")
    print()
    
    testar_dados_docentes()
    testar_processamento()
    
    print("✅ Testes concluídos!") 
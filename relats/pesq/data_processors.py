"""
Módulo para processar dados e gerar linhas da planilha.
Contém funções para carregar dados e formatar linhas.
"""

import pandas as pd
from bdados.ler_bdados_to_df import carregar_dataframe

# Importa as consultas SQL - usando imports absolutos para compatibilidade
try:
    # Tenta import relativo (quando executado como módulo)
    from .sql_queries import *
except ImportError:
    # Se falhar, usa import absoluto (quando executado diretamente)
    from sql_queries import *


def carregar_dados_por_ano(sql_query, coluna_valor, ano_inicio=2005, ano_fim=2025):
    """
    Carrega dados de uma consulta SQL e retorna um dicionário com valores por ano.
    
    Args:
        sql_query (str): Consulta SQL
        coluna_valor (str): Nome da coluna que contém o valor
        ano_inicio (int): Ano inicial (padrão: 2005)
        ano_fim (int): Ano final (padrão: 2025)
    
    Returns:
        dict: Dicionário com valores por ano
    """
    try:
        df = carregar_dataframe(sql_query)
        dados_por_ano = df.set_index("ano")[coluna_valor].to_dict()
        
        # Preenche anos sem dados com 0
        for ano in range(ano_inicio, ano_fim):
            if ano not in dados_por_ano:
                dados_por_ano[ano] = 0
                
        return dados_por_ano
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return {}


def carregar_dados_agrupados(sql_query, coluna_agrupamento, coluna_valor, ano_inicio=2005, ano_fim=2025):
    """
    Carrega dados agrupados de uma consulta SQL.
    
    Args:
        sql_query (str): Consulta SQL
        coluna_agrupamento (str): Nome da coluna de agrupamento
        coluna_valor (str): Nome da coluna que contém o valor
        ano_inicio (int): Ano inicial (padrão: 2005)
        ano_fim (int): Ano final (padrão: 2025)
    
    Returns:
        dict: Dicionário com dados agrupados por categoria
    """
    try:
        df = carregar_dataframe(sql_query)
        categorias_unicas = df[coluna_agrupamento].unique()
        
        dados_agrupados = {}
        for categoria in sorted(categorias_unicas):
            dados_categoria = df[df[coluna_agrupamento] == categoria]
            dados_por_ano = dados_categoria.set_index("ano")[coluna_valor].to_dict()
            
            # Preenche anos sem dados com 0
            for ano in range(ano_inicio, ano_fim):
                if ano not in dados_por_ano:
                    dados_por_ano[ano] = 0
                    
            dados_agrupados[categoria] = dados_por_ano
            
        return dados_agrupados
    except Exception as e:
        print(f"Erro ao carregar dados agrupados: {e}")
        return {}


def carregar_dados_multi_agrupados(sql_query, coluna_agrupamento1, coluna_agrupamento2, coluna_valor, ano_inicio=2005, ano_fim=2025):
    """
    Carrega dados com múltiplos agrupamentos de uma consulta SQL.
    
    Args:
        sql_query (str): Consulta SQL
        coluna_agrupamento1 (str): Nome da primeira coluna de agrupamento
        coluna_agrupamento2 (str): Nome da segunda coluna de agrupamento
        coluna_valor (str): Nome da coluna que contém o valor
        ano_inicio (int): Ano inicial (padrão: 2005)
        ano_fim (int): Ano final (padrão: 2025)
    
    Returns:
        dict: Dicionário com dados agrupados por categoria e subcategoria
    """
    try:
        df = carregar_dataframe(sql_query)
        categorias_unicas = df[coluna_agrupamento1].unique()
        
        dados_agrupados = {}
        for categoria in sorted(categorias_unicas):
            dados_categoria = df[df[coluna_agrupamento1] == categoria]
            subcategorias_unicas = dados_categoria[coluna_agrupamento2].unique()
            
            dados_agrupados[categoria] = {}
            for subcategoria in sorted(subcategorias_unicas):
                dados_subcategoria = dados_categoria[dados_categoria[coluna_agrupamento2] == subcategoria]
                dados_por_ano = dados_subcategoria.set_index("ano")[coluna_valor].to_dict()
                
                # Preenche anos sem dados com 0
                for ano in range(ano_inicio, ano_fim):
                    if ano not in dados_por_ano:
                        dados_por_ano[ano] = 0
                        
                dados_agrupados[categoria][subcategoria] = dados_por_ano
            
        return dados_agrupados
    except Exception as e:
        print(f"Erro ao carregar dados multi-agrupados: {e}")
        return {}


def criar_linha_dados(tipo_dado, agrupamento, categoria, sub_categoria, dados_por_ano, ano_inicio=2005, ano_fim=2025):
    """
    Cria uma linha de dados para a planilha.
    
    Args:
        tipo_dado (str): Tipo de dado (ex: "Nro de IES")
        agrupamento (str): Agrupamento (ex: "Nenhum", "Grande Cat.Adm")
        categoria (str): Categoria (ex: "Global", "Públicas")
        sub_categoria (str): Sub-categoria (ex: "Global", "Licenciaturas")
        dados_por_ano (dict): Dicionário com valores por ano
        ano_inicio (int): Ano inicial (padrão: 2005)
        ano_fim (int): Ano final (padrão: 2025)
    
    Returns:
        list: Lista com os dados da linha
    """
    linha = [tipo_dado, agrupamento, categoria, sub_categoria]
    
    for ano in range(ano_inicio, ano_fim):
        valor = dados_por_ano.get(ano, 0)
        linha.append(valor)
    
    return linha


def processar_dados_ies(todas_linhas, sub_categoria_global):
    """Processa dados de IES e adiciona às linhas da planilha"""
    
    # 1. Dados globais de IES
    dados_globais = carregar_dados_por_ano(get_sql_ies_global(), "QtdeIes")
    linha_global = criar_linha_dados("Nro de IES", "Nenhum", "Global", sub_categoria_global, dados_globais)
    todas_linhas.append({"dados": linha_global, "secao": "global"})
    
    # 2. Dados de IES por rede
    dados_por_rede = carregar_dados_agrupados(get_sql_ies_por_rede(), "rede", "QtdeIes")
    for rede in sorted(dados_por_rede.keys()):
        linha_rede = criar_linha_dados("Nro de IES", "Grande Cat.Adm", rede, sub_categoria_global, dados_por_rede[rede])
        todas_linhas.append({"dados": linha_rede, "secao": "rede"})
    
    # 3. Dados de IES por categoria administrativa
    dados_por_categoria = carregar_dados_agrupados(get_sql_ies_por_categoria(), "categoria", "QtdeIes")
    for categoria in sorted(dados_por_categoria.keys()):
        linha_categoria = criar_linha_dados("Nro de IES", "Cat.Adm", categoria, sub_categoria_global, dados_por_categoria[categoria])
        todas_linhas.append({"dados": linha_categoria, "secao": "categoria"})


def processar_dados_municipios(todas_linhas, sub_categoria_global):
    """Processa dados de municípios e adiciona às linhas da planilha"""
    
    # 4. Dados de Municípios com IES
    dados_municipios = carregar_dados_por_ano(get_sql_municipios_com_ies(), "QtdeMunicipios")
    linha_municipios = criar_linha_dados("Nro de Municipios", "Nenhum", "IES", sub_categoria_global, dados_municipios)
    todas_linhas.append({"dados": linha_municipios, "secao": "municipios"})
    
    # 5. Dados de Municípios com Cursos
    dados_municipios_cursos = carregar_dados_por_ano(get_sql_municipios_com_cursos(), "QtdeMunicipios")
    linha_municipios_cursos = criar_linha_dados("Nro de Municipios", "Nenhum", "IES + Polos", sub_categoria_global, dados_municipios_cursos)
    todas_linhas.append({"dados": linha_municipios_cursos, "secao": "municipios_cursos"})
    
    # 5a. Dados de Municípios com Cursos de Licenciatura
    dados_municipios_licenciatura = carregar_dados_por_ano(get_sql_municipios_com_cursos_licenciatura(), "QtdeMunicipios")
    linha_municipios_licenciatura = criar_linha_dados("Nro de Municipios", "Nenhum", "IES + Polos", "Licenciaturas", dados_municipios_licenciatura)
    todas_linhas.append({"dados": linha_municipios_licenciatura, "secao": "municipios_licenciatura"})
    
    # 5b. Dados de Municípios com Cursos de Licenciatura por Modalidade de Ensino
    dados_municipios_licenciatura_modalidade = carregar_dados_agrupados(get_sql_municipios_com_cursos_licenciatura_por_modalidade(), "modalidade", "QtdeMunicipios")
    for modalidade in sorted(dados_municipios_licenciatura_modalidade.keys()):
        dados_modalidade = dados_municipios_licenciatura_modalidade[modalidade]
        linha_modalidade = criar_linha_dados("Nro de Municipios", "Licenciaturas", "IES ou Polos", modalidade, dados_modalidade)
        todas_linhas.append({"dados": linha_modalidade, "secao": "municipios_licenciatura_modalidade"})
    
    # 5c. Dados de Municípios com Cursos de Licenciatura por Categoria e Modalidade
    dados_municipios_licenciatura_categoria_modalidade = carregar_dados_multi_agrupados(
        get_sql_municipios_com_cursos_licenciatura_por_categoria_modalidade(), 
        "categoria", "modalidade", "QtdeMunicipios"
    )
    for categoria in sorted(dados_municipios_licenciatura_categoria_modalidade.keys()):
        dados_categoria = dados_municipios_licenciatura_categoria_modalidade[categoria]
        for modalidade in sorted(dados_categoria.keys()):
            dados_modalidade = dados_categoria[modalidade]
            linha_categoria_modalidade = criar_linha_dados("Nro de Municipios", "Licenciaturas", categoria, modalidade, dados_modalidade)
            todas_linhas.append({"dados": linha_categoria_modalidade, "secao": "municipios_licenciatura_categoria_modalidade"})


def processar_dados_docentes(todas_linhas, sub_categoria_global):
    """Processa dados de docentes e adiciona às linhas da planilha"""
    
    # 6. Dados de Docentes Total (TODAS AS CATEGORIAS)
    dados_docentes = carregar_dados_por_ano(get_sql_docentes_global(), "Docentes", 2005, 2025)
    linha_docentes = criar_linha_dados("Nro de Docentes", "Nenhum", "Global", sub_categoria_global, dados_docentes, 2005, 2025)
    todas_linhas.append({"dados": linha_docentes, "secao": "docentes"})
    
    # 7. Dados de Docentes por Titulação (TODAS AS CATEGORIAS)
    titulacoes = [
        ("dout", "Doutores(as)"),
        ("mest", "Mestres(as)"),
        ("esp", "Especialistas"),
        ("grad", "Graduados(as)")
    ]
    
    for tipo_tit, nome_tit in titulacoes:
        dados_titulacao = carregar_dados_por_ano(get_sql_docentes_por_titulacao(tipo_tit), "Docentes", 2005, 2025)
        linha_titulacao = criar_linha_dados("Nro de Docentes", "Nenhum", nome_tit, sub_categoria_global, dados_titulacao, 2005, 2025)
        todas_linhas.append({"dados": linha_titulacao, "secao": "docentes_titulacao"})
    
    # 8. Dados de Docentes Total FILTRADOS (CATEGORIAS 1,2,3,5,7,8,9)
    dados_docentes_filtrados = carregar_dados_por_ano(get_sql_docentes_filtrados(), "Docentes", 2005, 2025)
    linha_docentes_filtrados = criar_linha_dados("Nro de Docentes", "Cat.Adm Pesq", "Global", sub_categoria_global, dados_docentes_filtrados, 2005, 2025)
    todas_linhas.append({"dados": linha_docentes_filtrados, "secao": "docentes_filtrados"})
    
    # 9. Dados de Docentes por Titulação FILTRADOS
    for tipo_tit, nome_tit in titulacoes:
        dados_titulacao_filtrados = carregar_dados_por_ano(get_sql_docentes_por_titulacao_filtrados(tipo_tit), "Docentes", 2005, 2025)
        linha_titulacao_filtrados = criar_linha_dados("Nro de Docentes", "Cat.Adm Pesq", nome_tit, sub_categoria_global, dados_titulacao_filtrados, 2005, 2025)
        todas_linhas.append({"dados": linha_titulacao_filtrados, "secao": "docentes_titulacao_filtrados"})
    
    # 10. Dados de Docentes Total POR CATEGORIA
    dados_docentes_por_categoria = carregar_dados_agrupados(get_sql_docentes_por_categoria(), "categoria", "Docentes", 2005, 2025)
    for categoria in sorted(dados_docentes_por_categoria.keys()):
        dados_categoria_docentes = dados_docentes_por_categoria[categoria]
        linha_categoria_docentes = criar_linha_dados("Nro de Docentes", categoria, "Global", sub_categoria_global, dados_categoria_docentes, 2005, 2025)
        todas_linhas.append({"dados": linha_categoria_docentes, "secao": "docentes_por_categoria"})
    
    # 11. Dados de Docentes por Titulação POR CATEGORIA
    for tipo_tit, nome_tit in titulacoes:
        dados_titulacao_por_categoria = carregar_dados_agrupados(get_sql_docentes_por_titulacao_por_categoria(tipo_tit), "categoria", "Docentes", 2005, 2025)
        for categoria in sorted(dados_titulacao_por_categoria.keys()):
            dados_categoria_titulacao = dados_titulacao_por_categoria[categoria]
            linha_categoria_titulacao = criar_linha_dados("Nro de Docentes", categoria, nome_tit, sub_categoria_global, dados_categoria_titulacao, 2005, 2025)
            todas_linhas.append({"dados": linha_categoria_titulacao, "secao": "docentes_titulacao_por_categoria"})


def processar_dados_cursos(todas_linhas, sub_categoria_global):
    """Processa dados de cursos e adiciona às linhas da planilha"""
    
    # 12. Dados de Cursos Global
    dados_cursos_global = carregar_dados_por_ano(get_sql_cursos_global(), "QtdeCursos")
    linha_cursos_global = criar_linha_dados("Nro de Cursos", "Nenhum", "Global", sub_categoria_global, dados_cursos_global)
    todas_linhas.append({"dados": linha_cursos_global, "secao": "cursos_global"})
    
    # 13. Dados de Cursos por Rede
    dados_cursos_por_rede = carregar_dados_agrupados(get_sql_cursos_por_rede(), "rede", "QtdeCursos")
    for rede in sorted(dados_cursos_por_rede.keys()):
        linha_rede_cursos = criar_linha_dados("Nro de Cursos", "Grande Cat.Adm", rede, sub_categoria_global, dados_cursos_por_rede[rede])
        todas_linhas.append({"dados": linha_rede_cursos, "secao": "cursos_rede"})
    
    # 14. Dados de Cursos por Categoria Administrativa
    dados_cursos_por_categoria = carregar_dados_agrupados(get_sql_cursos_por_categoria(), "categoria", "QtdeCursos")
    for categoria in sorted(dados_cursos_por_categoria.keys()):
        linha_categoria_cursos = criar_linha_dados("Nro de Cursos", "Cat.Adm", categoria, sub_categoria_global, dados_cursos_por_categoria[categoria])
        todas_linhas.append({"dados": linha_categoria_cursos, "secao": "cursos_categoria"})


def processar_dados_licenciaturas(todas_linhas, sub_categoria_licenciaturas):
    """Processa dados de licenciaturas e adiciona às linhas da planilha"""
    
    # 15. Dados de Licenciaturas Global
    dados_licenciaturas_global = carregar_dados_por_ano(get_sql_licenciaturas_global(), "QtdeCursos")
    linha_licenciaturas_global = criar_linha_dados("Nro de Cursos", "Nenhum", "Global", sub_categoria_licenciaturas, dados_licenciaturas_global)
    todas_linhas.append({"dados": linha_licenciaturas_global, "secao": "licenciaturas_global"})
    
    # 16. Dados de Licenciaturas por Rede
    dados_licenciaturas_por_rede = carregar_dados_agrupados(get_sql_licenciaturas_por_rede(), "rede", "QtdeCursos")
    for rede in sorted(dados_licenciaturas_por_rede.keys()):
        linha_rede_licenciaturas = criar_linha_dados("Nro de Cursos", "Grande Cat.Adm", rede, sub_categoria_licenciaturas, dados_licenciaturas_por_rede[rede])
        todas_linhas.append({"dados": linha_rede_licenciaturas, "secao": "licenciaturas_rede"})
    
    # 17. Dados de Licenciaturas por Categoria Administrativa
    dados_licenciaturas_por_categoria = carregar_dados_agrupados(get_sql_licenciaturas_por_categoria(), "categoria", "QtdeCursos")
    for categoria in sorted(dados_licenciaturas_por_categoria.keys()):
        linha_categoria_licenciaturas = criar_linha_dados("Nro de Cursos", "Cat.Adm", categoria, sub_categoria_licenciaturas, dados_licenciaturas_por_categoria[categoria])
        todas_linhas.append({"dados": linha_categoria_licenciaturas, "secao": "licenciaturas_categoria"})


def processar_dados_vagas(todas_linhas):
    """Processa dados de vagas e adiciona às linhas da planilha"""
    
    # Dados de Vagas Totais
    dados_vagas_totais = carregar_dados_por_ano(get_sql_vagas_totais(), "Vagas")
    linha_vagas_totais = criar_linha_dados("Nro de Vagas", "Nenhum", "Global", "Global", dados_vagas_totais)
    todas_linhas.append({"dados": linha_vagas_totais, "secao": "vagas_global"})
    
    # Dados de Vagas por Modalidade de Ensino
    dados_vagas_modalidade = carregar_dados_agrupados(get_sql_vagas_por_modalidade(), "modalidade", "Vagas")
    for modalidade in sorted(dados_vagas_modalidade.keys()):
        dados_modalidade = dados_vagas_modalidade[modalidade]
        linha_modalidade = criar_linha_dados("Nro de Vagas", "Global", "Modalidade", modalidade, dados_modalidade)
        todas_linhas.append({"dados": linha_modalidade, "secao": "vagas_modalidade"})
    
    # Dados de Vagas de Licenciaturas por Modalidade de Ensino
    dados_vagas_licenciaturas_modalidade = carregar_dados_agrupados(get_sql_vagas_licenciaturas_por_modalidade(), "modalidade", "Vagas")
    for modalidade in sorted(dados_vagas_licenciaturas_modalidade.keys()):
        dados_modalidade = dados_vagas_licenciaturas_modalidade[modalidade]
        linha_modalidade = criar_linha_dados("Nro de Vagas", "Licenciaturas", "Modalidade", modalidade, dados_modalidade)
        todas_linhas.append({"dados": linha_modalidade, "secao": "vagas_licenciaturas_modalidade"})
    
    # Dados de Vagas de Licenciaturas por Categoria e Modalidade
    dados_vagas_licenciaturas_categoria_modalidade = carregar_dados_multi_agrupados(
        get_sql_vagas_licenciaturas_por_categoria_modalidade(), 
        "categoria", "modalidade", "Vagas"
    )
    for categoria in sorted(dados_vagas_licenciaturas_categoria_modalidade.keys()):
        dados_categoria = dados_vagas_licenciaturas_categoria_modalidade[categoria]
        for modalidade in sorted(dados_categoria.keys()):
            dados_modalidade = dados_categoria[modalidade]
            linha_categoria_modalidade = criar_linha_dados("Nro de Vagas", "Licenciaturas", categoria, modalidade, dados_modalidade)
            todas_linhas.append({"dados": linha_categoria_modalidade, "secao": "vagas_licenciaturas_categoria_modalidade"})


def processar_dados_inscritos(todas_linhas):
    """Processa dados de inscritos e adiciona às linhas da planilha"""
    
    # Dados de Inscritos Totais
    dados_inscritos_totais = carregar_dados_por_ano(get_sql_inscritos_totais(), "Inscritos")
    linha_inscritos_totais = criar_linha_dados("Nro de Inscritos", "Nenhum", "Global", "Global", dados_inscritos_totais)
    todas_linhas.append({"dados": linha_inscritos_totais, "secao": "inscritos_global"})
    
    # Dados de Inscritos por Modalidade de Ensino
    dados_inscritos_modalidade = carregar_dados_agrupados(get_sql_inscritos_por_modalidade(), "modalidade", "Inscritos")
    for modalidade in sorted(dados_inscritos_modalidade.keys()):
        dados_modalidade = dados_inscritos_modalidade[modalidade]
        linha_modalidade = criar_linha_dados("Nro de Inscritos", "Global", "Modalidade", modalidade, dados_modalidade)
        todas_linhas.append({"dados": linha_modalidade, "secao": "inscritos_modalidade"})
    
    # Dados de Inscritos de Licenciaturas por Modalidade de Ensino
    dados_inscritos_licenciaturas_modalidade = carregar_dados_agrupados(get_sql_inscritos_licenciaturas_por_modalidade(), "modalidade", "Inscritos")
    for modalidade in sorted(dados_inscritos_licenciaturas_modalidade.keys()):
        dados_modalidade = dados_inscritos_licenciaturas_modalidade[modalidade]
        linha_modalidade = criar_linha_dados("Nro de Inscritos", "Licenciaturas", "Modalidade", modalidade, dados_modalidade)
        todas_linhas.append({"dados": linha_modalidade, "secao": "inscritos_licenciaturas_modalidade"})
    
    # Dados de Inscritos de Licenciaturas por Categoria e Modalidade
    dados_inscritos_licenciaturas_categoria_modalidade = carregar_dados_multi_agrupados(
        get_sql_inscritos_licenciaturas_por_categoria_modalidade(), 
        "categoria", "modalidade", "Inscritos"
    )
    for categoria in sorted(dados_inscritos_licenciaturas_categoria_modalidade.keys()):
        dados_categoria = dados_inscritos_licenciaturas_categoria_modalidade[categoria]
        for modalidade in sorted(dados_categoria.keys()):
            dados_modalidade = dados_categoria[modalidade]
            linha_categoria_modalidade = criar_linha_dados("Nro de Inscritos", "Licenciaturas", categoria, modalidade, dados_modalidade)
            todas_linhas.append({"dados": linha_categoria_modalidade, "secao": "inscritos_licenciaturas_categoria_modalidade"})


def processar_dados_ingressos(todas_linhas):
    """Processa dados de ingressos e adiciona às linhas da planilha"""
    
    # Dados de Ingressos Totais
    dados_ingressos_totais = carregar_dados_por_ano(get_sql_ingressos_totais(), "Ingressos")
    linha_ingressos_totais = criar_linha_dados("Nro de Ingressos", "Nenhum", "Global", "Global", dados_ingressos_totais)
    todas_linhas.append({"dados": linha_ingressos_totais, "secao": "ingressos_global"})
    
    # Dados de Ingressos por Modalidade de Ensino
    dados_ingressos_modalidade = carregar_dados_agrupados(get_sql_ingressos_por_modalidade(), "modalidade", "Ingressos")
    for modalidade in sorted(dados_ingressos_modalidade.keys()):
        dados_modalidade = dados_ingressos_modalidade[modalidade]
        linha_modalidade = criar_linha_dados("Nro de Ingressos", "Global", "Modalidade", modalidade, dados_modalidade)
        todas_linhas.append({"dados": linha_modalidade, "secao": "ingressos_modalidade"})
    
    # Dados de Ingressos de Licenciaturas por Modalidade de Ensino
    dados_ingressos_licenciaturas_modalidade = carregar_dados_agrupados(get_sql_ingressos_licenciaturas_por_modalidade(), "modalidade", "Ingressos")
    for modalidade in sorted(dados_ingressos_licenciaturas_modalidade.keys()):
        dados_modalidade = dados_ingressos_licenciaturas_modalidade[modalidade]
        linha_modalidade = criar_linha_dados("Nro de Ingressos", "Licenciaturas", "Modalidade", modalidade, dados_modalidade)
        todas_linhas.append({"dados": linha_modalidade, "secao": "ingressos_licenciaturas_modalidade"})
    
    # Dados de Ingressos de Licenciaturas por Categoria e Modalidade
    dados_ingressos_licenciaturas_categoria_modalidade = carregar_dados_multi_agrupados(
        get_sql_ingressos_licenciaturas_por_categoria_modalidade(), 
        "categoria", "modalidade", "Ingressos"
    )
    for categoria in sorted(dados_ingressos_licenciaturas_categoria_modalidade.keys()):
        dados_categoria = dados_ingressos_licenciaturas_categoria_modalidade[categoria]
        for modalidade in sorted(dados_categoria.keys()):
            dados_modalidade = dados_categoria[modalidade]
            linha_categoria_modalidade = criar_linha_dados("Nro de Ingressos", "Licenciaturas", categoria, modalidade, dados_modalidade)
            todas_linhas.append({"dados": linha_categoria_modalidade, "secao": "ingressos_licenciaturas_categoria_modalidade"})


def processar_dados_matriculas(todas_linhas):
    """Processa dados de matrículas e adiciona às linhas da planilha"""
    
    # Dados de Matrículas Totais
    dados_matriculas_totais = carregar_dados_por_ano(get_sql_matriculas_totais(), "Matriculas")
    linha_matriculas_totais = criar_linha_dados("Nro de Matrículas", "Nenhum", "Global", "Global", dados_matriculas_totais)
    todas_linhas.append({"dados": linha_matriculas_totais, "secao": "matriculas_global"})
    
    # Dados de Matrículas por Modalidade de Ensino
    dados_matriculas_modalidade = carregar_dados_agrupados(get_sql_matriculas_por_modalidade(), "modalidade", "Matriculas")
    for modalidade in sorted(dados_matriculas_modalidade.keys()):
        dados_modalidade = dados_matriculas_modalidade[modalidade]
        linha_modalidade = criar_linha_dados("Nro de Matrículas", "Global", "Modalidade", modalidade, dados_modalidade)
        todas_linhas.append({"dados": linha_modalidade, "secao": "matriculas_modalidade"})
    
    # Dados de Matrículas de Licenciaturas por Modalidade de Ensino
    dados_matriculas_licenciaturas_modalidade = carregar_dados_agrupados(get_sql_matriculas_licenciaturas_por_modalidade(), "modalidade", "Matriculas")
    for modalidade in sorted(dados_matriculas_licenciaturas_modalidade.keys()):
        dados_modalidade = dados_matriculas_licenciaturas_modalidade[modalidade]
        linha_modalidade = criar_linha_dados("Nro de Matrículas", "Licenciaturas", "Modalidade", modalidade, dados_modalidade)
        todas_linhas.append({"dados": linha_modalidade, "secao": "matriculas_licenciaturas_modalidade"})
    
    # Dados de Matrículas de Licenciaturas por Categoria e Modalidade
    dados_matriculas_licenciaturas_categoria_modalidade = carregar_dados_multi_agrupados(
        get_sql_matriculas_licenciaturas_por_categoria_modalidade(), 
        "categoria", "modalidade", "Matriculas"
    )
    for categoria in sorted(dados_matriculas_licenciaturas_categoria_modalidade.keys()):
        dados_categoria = dados_matriculas_licenciaturas_categoria_modalidade[categoria]
        for modalidade in sorted(dados_categoria.keys()):
            dados_modalidade = dados_categoria[modalidade]
            linha_categoria_modalidade = criar_linha_dados("Nro de Matrículas", "Licenciaturas", categoria, modalidade, dados_modalidade)
            todas_linhas.append({"dados": linha_categoria_modalidade, "secao": "matriculas_licenciaturas_categoria_modalidade"})


def processar_dados_concluintes(todas_linhas):
    """Processa dados de concluintes e adiciona às linhas da planilha"""
    
    # Dados de Concluintes Totais
    dados_concluintes_totais = carregar_dados_por_ano(get_sql_concluintes_totais(), "Concluintes")
    linha_concluintes_totais = criar_linha_dados("Nro de Concluíntes", "Nenhum", "Global", "Global", dados_concluintes_totais)
    todas_linhas.append({"dados": linha_concluintes_totais, "secao": "concluintes_global"})
    
    # Dados de Concluintes por Modalidade de Ensino
    dados_concluintes_modalidade = carregar_dados_agrupados(get_sql_concluintes_por_modalidade(), "modalidade", "Concluintes")
    for modalidade in sorted(dados_concluintes_modalidade.keys()):
        dados_modalidade = dados_concluintes_modalidade[modalidade]
        linha_modalidade = criar_linha_dados("Nro de Concluíntes", "Global", "Modalidade", modalidade, dados_modalidade)
        todas_linhas.append({"dados": linha_modalidade, "secao": "concluintes_modalidade"})
    
    # Dados de Concluintes de Licenciaturas por Modalidade de Ensino
    dados_concluintes_licenciaturas_modalidade = carregar_dados_agrupados(get_sql_concluintes_licenciaturas_por_modalidade(), "modalidade", "Concluintes")
    for modalidade in sorted(dados_concluintes_licenciaturas_modalidade.keys()):
        dados_modalidade = dados_concluintes_licenciaturas_modalidade[modalidade]
        linha_modalidade = criar_linha_dados("Nro de Concluíntes", "Licenciaturas", "Modalidade", modalidade, dados_modalidade)
        todas_linhas.append({"dados": linha_modalidade, "secao": "concluintes_licenciaturas_modalidade"})
    
    # Dados de Concluintes de Licenciaturas por Categoria e Modalidade
    dados_concluintes_licenciaturas_categoria_modalidade = carregar_dados_multi_agrupados(
        get_sql_concluintes_licenciaturas_por_categoria_modalidade(), 
        "categoria", "modalidade", "Concluintes"
    )
    for categoria in sorted(dados_concluintes_licenciaturas_categoria_modalidade.keys()):
        dados_categoria = dados_concluintes_licenciaturas_categoria_modalidade[categoria]
        for modalidade in sorted(dados_categoria.keys()):
            dados_modalidade = dados_categoria[modalidade]
            linha_categoria_modalidade = criar_linha_dados("Nro de Concluíntes", "Licenciaturas", categoria, modalidade, dados_modalidade)
            todas_linhas.append({"dados": linha_categoria_modalidade, "secao": "concluintes_licenciaturas_categoria_modalidade"})


def processar_dados_matriculas_trancadas(todas_linhas):
    """Processa dados de matrículas trancadas e adiciona às linhas da planilha"""
    
    # Dados de Matrículas Trancadas Totais
    dados_matriculas_trancadas_totais = carregar_dados_por_ano(get_sql_matriculas_trancadas_totais(), "MatriculasTrancadas")
    linha_matriculas_trancadas_totais = criar_linha_dados("Nro de Mat.Trancadas", "Nenhum", "Global", "Global", dados_matriculas_trancadas_totais)
    todas_linhas.append({"dados": linha_matriculas_trancadas_totais, "secao": "matriculas_trancadas_global"})
    
    # Dados de Matrículas Trancadas por Modalidade de Ensino
    dados_matriculas_trancadas_modalidade = carregar_dados_agrupados(get_sql_matriculas_trancadas_por_modalidade(), "modalidade", "MatriculasTrancadas")
    for modalidade in sorted(dados_matriculas_trancadas_modalidade.keys()):
        dados_modalidade = dados_matriculas_trancadas_modalidade[modalidade]
        linha_modalidade = criar_linha_dados("Nro de Mat.Trancadas", "Global", "Modalidade", modalidade, dados_modalidade)
        todas_linhas.append({"dados": linha_modalidade, "secao": "matriculas_trancadas_modalidade"})
    
    # Dados de Matrículas Trancadas de Licenciaturas por Modalidade de Ensino
    dados_matriculas_trancadas_licenciaturas_modalidade = carregar_dados_agrupados(get_sql_matriculas_trancadas_licenciaturas_por_modalidade(), "modalidade", "MatriculasTrancadas")
    for modalidade in sorted(dados_matriculas_trancadas_licenciaturas_modalidade.keys()):
        dados_modalidade = dados_matriculas_trancadas_licenciaturas_modalidade[modalidade]
        linha_modalidade = criar_linha_dados("Nro de Mat.Trancadas", "Licenciaturas", "Modalidade", modalidade, dados_modalidade)
        todas_linhas.append({"dados": linha_modalidade, "secao": "matriculas_trancadas_licenciaturas_modalidade"})
    
    # Dados de Matrículas Trancadas de Licenciaturas por Categoria e Modalidade
    dados_matriculas_trancadas_licenciaturas_categoria_modalidade = carregar_dados_multi_agrupados(
        get_sql_matriculas_trancadas_licenciaturas_por_categoria_modalidade(), 
        "categoria", "modalidade", "MatriculasTrancadas"
    )
    for categoria in sorted(dados_matriculas_trancadas_licenciaturas_categoria_modalidade.keys()):
        dados_categoria = dados_matriculas_trancadas_licenciaturas_categoria_modalidade[categoria]
        for modalidade in sorted(dados_categoria.keys()):
            dados_modalidade = dados_categoria[modalidade]
            linha_categoria_modalidade = criar_linha_dados("Nro de Mat.Trancadas", "Licenciaturas", categoria, modalidade, dados_modalidade)
            todas_linhas.append({"dados": linha_categoria_modalidade, "secao": "matriculas_trancadas_licenciaturas_categoria_modalidade"})


def processar_dados_evadidos(todas_linhas):
    """Processa dados de evadidos e adiciona às linhas da planilha"""
    
    # Dados de Evadidos Totais
    dados_evadidos_totais = carregar_dados_por_ano(get_sql_evadidos_totais(), "Evadidos")
    linha_evadidos_totais = criar_linha_dados("Nro Evadidos(as)", "Nenhum", "Global", "Global", dados_evadidos_totais)
    todas_linhas.append({"dados": linha_evadidos_totais, "secao": "evadidos_global"})
    
    # Dados de Evadidos por Modalidade de Ensino
    dados_evadidos_modalidade = carregar_dados_agrupados(get_sql_evadidos_por_modalidade(), "modalidade", "Evadidos")
    for modalidade in sorted(dados_evadidos_modalidade.keys()):
        dados_modalidade = dados_evadidos_modalidade[modalidade]
        linha_modalidade = criar_linha_dados("Nro Evadidos(as)", "Global", "Modalidade", modalidade, dados_modalidade)
        todas_linhas.append({"dados": linha_modalidade, "secao": "evadidos_modalidade"})
    
    # Dados de Evadidos de Licenciaturas por Modalidade de Ensino
    dados_evadidos_licenciaturas_modalidade = carregar_dados_agrupados(get_sql_evadidos_licenciaturas_por_modalidade(), "modalidade", "Evadidos")
    for modalidade in sorted(dados_evadidos_licenciaturas_modalidade.keys()):
        dados_modalidade = dados_evadidos_licenciaturas_modalidade[modalidade]
        linha_modalidade = criar_linha_dados("Nro Evadidos(as)", "Licenciaturas", "Modalidade", modalidade, dados_modalidade)
        todas_linhas.append({"dados": linha_modalidade, "secao": "evadidos_licenciaturas_modalidade"})
    
    # Dados de Evadidos de Licenciaturas por Categoria e Modalidade
    dados_evadidos_licenciaturas_categoria_modalidade = carregar_dados_multi_agrupados(
        get_sql_evadidos_licenciaturas_por_categoria_modalidade(), 
        "categoria", "modalidade", "Evadidos"
    )
    for categoria in sorted(dados_evadidos_licenciaturas_categoria_modalidade.keys()):
        dados_categoria = dados_evadidos_licenciaturas_categoria_modalidade[categoria]
        for modalidade in sorted(dados_categoria.keys()):
            dados_modalidade = dados_categoria[modalidade]
            linha_categoria_modalidade = criar_linha_dados("Nro Evadidos(as)", "Licenciaturas", categoria, modalidade, dados_modalidade)
            todas_linhas.append({"dados": linha_categoria_modalidade, "secao": "evadidos_licenciaturas_categoria_modalidade"})


def processar_dados_turno_licenciaturas_presencial(todas_linhas):
    """Processa dados de turno (diurno/noturno) para licenciaturas presenciais"""
    
    # Dados de Ingressos Diurnos de Licenciaturas Presenciais
    dados_ingressos_diurno = carregar_dados_por_ano(get_sql_ingressos_licenciaturas_presencial_diurno(), "Ingressos")
    linha_ingressos_diurno = criar_linha_dados("Nro de Ingressos", "Licenciaturas", "Presencial", "Diurno", dados_ingressos_diurno)
    todas_linhas.append({"dados": linha_ingressos_diurno, "secao": "ingressos_licenciaturas_presencial_diurno"})
    
    # Dados de Ingressos Noturnos de Licenciaturas Presenciais
    dados_ingressos_noturno = carregar_dados_por_ano(get_sql_ingressos_licenciaturas_presencial_noturno(), "Ingressos")
    linha_ingressos_noturno = criar_linha_dados("Nro de Ingressos", "Licenciaturas", "Presencial", "Noturno", dados_ingressos_noturno)
    todas_linhas.append({"dados": linha_ingressos_noturno, "secao": "ingressos_licenciaturas_presencial_noturno"})
    
    # Dados de Matrículas Diurnas de Licenciaturas Presenciais
    dados_matriculas_diurno = carregar_dados_por_ano(get_sql_matriculas_licenciaturas_presencial_diurno(), "Matriculas")
    linha_matriculas_diurno = criar_linha_dados("Nro de Matrículas", "Licenciaturas", "Presencial", "Diurno", dados_matriculas_diurno)
    todas_linhas.append({"dados": linha_matriculas_diurno, "secao": "matriculas_licenciaturas_presencial_diurno"})
    
    # Dados de Matrículas Noturnas de Licenciaturas Presenciais
    dados_matriculas_noturno = carregar_dados_por_ano(get_sql_matriculas_licenciaturas_presencial_noturno(), "Matriculas")
    linha_matriculas_noturno = criar_linha_dados("Nro de Matrículas", "Licenciaturas", "Presencial", "Noturno", dados_matriculas_noturno)
    todas_linhas.append({"dados": linha_matriculas_noturno, "secao": "matriculas_licenciaturas_presencial_noturno"})
    
    # Dados de Concluintes Diurnos de Licenciaturas Presenciais
    dados_concluintes_diurno = carregar_dados_por_ano(get_sql_concluintes_licenciaturas_presencial_diurno(), "Concluintes")
    linha_concluintes_diurno = criar_linha_dados("Nro de Concluíntes", "Licenciaturas", "Presencial", "Diurno", dados_concluintes_diurno)
    todas_linhas.append({"dados": linha_concluintes_diurno, "secao": "concluintes_licenciaturas_presencial_diurno"})
    
    # Dados de Concluintes Noturnos de Licenciaturas Presenciais
    dados_concluintes_noturno = carregar_dados_por_ano(get_sql_concluintes_licenciaturas_presencial_noturno(), "Concluintes")
    linha_concluintes_noturno = criar_linha_dados("Nro de Concluíntes", "Licenciaturas", "Presencial", "Noturno", dados_concluintes_noturno)
    todas_linhas.append({"dados": linha_concluintes_noturno, "secao": "concluintes_licenciaturas_presencial_noturno"})


def processar_dados_genero_presencial(todas_linhas):
    """Processa dados de gênero (masculino/feminino) para licenciaturas presenciais e a distância"""
    
    # Dados de Ingressos Masculinos de Licenciaturas Presenciais
    dados_ingressos_masculino = carregar_dados_por_ano(get_sql_ingressos_presencial_masculino(), "Ingressos")
    linha_ingressos_masculino = criar_linha_dados("Nro de Ingressos", "Licenciaturas", "Presencial", "Masculino", dados_ingressos_masculino)
    todas_linhas.append({"dados": linha_ingressos_masculino, "secao": "ingressos_presencial_masculino"})
    
    # Dados de Ingressos Femininos de Licenciaturas Presenciais
    dados_ingressos_feminino = carregar_dados_por_ano(get_sql_ingressos_presencial_feminino(), "Ingressos")
    linha_ingressos_feminino = criar_linha_dados("Nro de Ingressos", "Licenciaturas", "Presencial", "Feminino", dados_ingressos_feminino)
    todas_linhas.append({"dados": linha_ingressos_feminino, "secao": "ingressos_presencial_feminino"})
    
    # Dados de Ingressos Masculinos de Licenciaturas a Distância
    dados_ingressos_distancia_masculino = carregar_dados_por_ano(get_sql_ingressos_distancia_masculino(), "Ingressos")
    linha_ingressos_distancia_masculino = criar_linha_dados("Nro de Ingressos", "Licenciaturas", "A Distância", "Masculino", dados_ingressos_distancia_masculino)
    todas_linhas.append({"dados": linha_ingressos_distancia_masculino, "secao": "ingressos_distancia_masculino"})
    
    # Dados de Ingressos Femininos de Licenciaturas a Distância
    dados_ingressos_distancia_feminino = carregar_dados_por_ano(get_sql_ingressos_distancia_feminino(), "Ingressos")
    linha_ingressos_distancia_feminino = criar_linha_dados("Nro de Ingressos", "Licenciaturas", "A Distância", "Feminino", dados_ingressos_distancia_feminino)
    todas_linhas.append({"dados": linha_ingressos_distancia_feminino, "secao": "ingressos_distancia_feminino"})
    
    # Dados de Matrículas Masculinas de Licenciaturas Presenciais
    dados_matriculas_masculino = carregar_dados_por_ano(get_sql_matriculas_presencial_masculino(), "Matriculas")
    linha_matriculas_masculino = criar_linha_dados("Nro de Matrículas", "Licenciaturas", "Presencial", "Masculino", dados_matriculas_masculino)
    todas_linhas.append({"dados": linha_matriculas_masculino, "secao": "matriculas_presencial_masculino"})
    
    # Dados de Matrículas Femininas de Licenciaturas Presenciais
    dados_matriculas_feminino = carregar_dados_por_ano(get_sql_matriculas_presencial_feminino(), "Matriculas")
    linha_matriculas_feminino = criar_linha_dados("Nro de Matrículas", "Licenciaturas", "Presencial", "Feminino", dados_matriculas_feminino)
    todas_linhas.append({"dados": linha_matriculas_feminino, "secao": "matriculas_presencial_feminino"})
    
    # Dados de Matrículas Masculinas de Licenciaturas a Distância
    dados_matriculas_distancia_masculino = carregar_dados_por_ano(get_sql_matriculas_distancia_masculino(), "Matriculas")
    linha_matriculas_distancia_masculino = criar_linha_dados("Nro de Matrículas", "Licenciaturas", "A Distância", "Masculino", dados_matriculas_distancia_masculino)
    todas_linhas.append({"dados": linha_matriculas_distancia_masculino, "secao": "matriculas_distancia_masculino"})
    
    # Dados de Matrículas Femininas de Licenciaturas a Distância
    dados_matriculas_distancia_feminino = carregar_dados_por_ano(get_sql_matriculas_distancia_feminino(), "Matriculas")
    linha_matriculas_distancia_feminino = criar_linha_dados("Nro de Matrículas", "Licenciaturas", "A Distância", "Feminino", dados_matriculas_distancia_feminino)
    todas_linhas.append({"dados": linha_matriculas_distancia_feminino, "secao": "matriculas_distancia_feminino"})
    
    # Dados de Concluintes Masculinos de Licenciaturas Presenciais
    dados_concluintes_masculino = carregar_dados_por_ano(get_sql_concluintes_presencial_masculino(), "Concluintes")
    linha_concluintes_masculino = criar_linha_dados("Nro de Concluíntes", "Licenciaturas", "Presencial", "Masculino", dados_concluintes_masculino)
    todas_linhas.append({"dados": linha_concluintes_masculino, "secao": "concluintes_presencial_masculino"})
    
    # Dados de Concluintes Femininos de Licenciaturas Presenciais
    dados_concluintes_feminino = carregar_dados_por_ano(get_sql_concluintes_presencial_feminino(), "Concluintes")
    linha_concluintes_feminino = criar_linha_dados("Nro de Concluíntes", "Licenciaturas", "Presencial", "Feminino", dados_concluintes_feminino)
    todas_linhas.append({"dados": linha_concluintes_feminino, "secao": "concluintes_presencial_feminino"})
    
    # Dados de Concluintes Masculinos de Licenciaturas a Distância
    dados_concluintes_distancia_masculino = carregar_dados_por_ano(get_sql_concluintes_distancia_masculino(), "Concluintes")
    linha_concluintes_distancia_masculino = criar_linha_dados("Nro de Concluíntes", "Licenciaturas", "A Distância", "Masculino", dados_concluintes_distancia_masculino)
    todas_linhas.append({"dados": linha_concluintes_distancia_masculino, "secao": "concluintes_distancia_masculino"})
    
    # Dados de Concluintes Femininos de Licenciaturas a Distância
    dados_concluintes_distancia_feminino = carregar_dados_por_ano(get_sql_concluintes_distancia_feminino(), "Concluintes")
    linha_concluintes_distancia_feminino = criar_linha_dados("Nro de Concluíntes", "Licenciaturas", "A Distância", "Feminino", dados_concluintes_distancia_feminino)
    todas_linhas.append({"dados": linha_concluintes_distancia_feminino, "secao": "concluintes_distancia_feminino"})


def processar_dados_escola_publica(todas_linhas):
    """Processa dados de estudantes vindos de escolas públicas"""
    
    # Dados de Ingressos vindos de Escolas Públicas
    dados_ingressos_escola_publica = carregar_dados_por_ano(get_sql_ingressos_escola_publica(), "Ingressos")
    linha_ingressos_escola_publica = criar_linha_dados("Nro de Ingressos", "Licenciaturas", "Global", "Global-EP", dados_ingressos_escola_publica)
    todas_linhas.append({"dados": linha_ingressos_escola_publica, "secao": "ingressos_escola_publica"})
    
    # Dados de Matrículas vindas de Escolas Públicas
    dados_matriculas_escola_publica = carregar_dados_por_ano(get_sql_matriculas_escola_publica(), "Matriculas")
    linha_matriculas_escola_publica = criar_linha_dados("Nro de Matrículas", "Licenciaturas", "Global", "Global-EP", dados_matriculas_escola_publica)
    todas_linhas.append({"dados": linha_matriculas_escola_publica, "secao": "matriculas_escola_publica"})
    
    # Dados de Concluintes vindos de Escolas Públicas
    dados_concluintes_escola_publica = carregar_dados_por_ano(get_sql_concluintes_escola_publica(), "Concluintes")
    linha_concluintes_escola_publica = criar_linha_dados("Nro de Concluíntes", "Licenciaturas", "Global", "Global-EP", dados_concluintes_escola_publica)
    todas_linhas.append({"dados": linha_concluintes_escola_publica, "secao": "concluintes_escola_publica"})


def processar_dados_raca_cor(todas_linhas):
    """Processa dados de raça/cor (parda, amarela, indígena, preta, branca, cornd) para licenciaturas presenciais e a distância"""
    
    # Lista de raças/cores
    racas = ["parda", "amarela", "indigena", "preta", "branca", "cornd"]
    
    # Processar dados de Ingressos por raça/cor
    for raca in racas:
        # Presencial
        dados_ingressos_presencial = carregar_dados_por_ano(getattr(__import__('sql_queries'), f'get_sql_ingressos_presencial_{raca}')(), "Ingressos")
        linha_ingressos_presencial = criar_linha_dados("Nro de Ingressos", "Licenciaturas", "Presencial", raca.title(), dados_ingressos_presencial)
        todas_linhas.append({"dados": linha_ingressos_presencial, "secao": f"ingressos_presencial_{raca}"})
        
        # A Distância
        dados_ingressos_distancia = carregar_dados_por_ano(getattr(__import__('sql_queries'), f'get_sql_ingressos_distancia_{raca}')(), "Ingressos")
        linha_ingressos_distancia = criar_linha_dados("Nro de Ingressos", "Licenciaturas", "A Distância", raca.title(), dados_ingressos_distancia)
        todas_linhas.append({"dados": linha_ingressos_distancia, "secao": f"ingressos_distancia_{raca}"})
    
    # Processar dados de Matrículas por raça/cor
    for raca in racas:
        # Presencial
        dados_matriculas_presencial = carregar_dados_por_ano(getattr(__import__('sql_queries'), f'get_sql_matriculas_presencial_{raca}')(), "Matriculas")
        linha_matriculas_presencial = criar_linha_dados("Nro de Matrículas", "Licenciaturas", "Presencial", raca.title(), dados_matriculas_presencial)
        todas_linhas.append({"dados": linha_matriculas_presencial, "secao": f"matriculas_presencial_{raca}"})
        
        # A Distância
        dados_matriculas_distancia = carregar_dados_por_ano(getattr(__import__('sql_queries'), f'get_sql_matriculas_distancia_{raca}')(), "Matriculas")
        linha_matriculas_distancia = criar_linha_dados("Nro de Matrículas", "Licenciaturas", "A Distância", raca.title(), dados_matriculas_distancia)
        todas_linhas.append({"dados": linha_matriculas_distancia, "secao": f"matriculas_distancia_{raca}"})
    
    # Processar dados de Concluintes por raça/cor
    for raca in racas:
        # Presencial
        dados_concluintes_presencial = carregar_dados_por_ano(getattr(__import__('sql_queries'), f'get_sql_concluintes_presencial_{raca}')(), "Concluintes")
        linha_concluintes_presencial = criar_linha_dados("Nro de Concluíntes", "Licenciaturas", "Presencial", raca.title(), dados_concluintes_presencial)
        todas_linhas.append({"dados": linha_concluintes_presencial, "secao": f"concluintes_presencial_{raca}"})
        
        # A Distância
        dados_concluintes_distancia = carregar_dados_por_ano(getattr(__import__('sql_queries'), f'get_sql_concluintes_distancia_{raca}')(), "Concluintes")
        linha_concluintes_distancia = criar_linha_dados("Nro de Concluíntes", "Licenciaturas", "A Distância", raca.title(), dados_concluintes_distancia)
        todas_linhas.append({"dados": linha_concluintes_distancia, "secao": f"concluintes_distancia_{raca}"})


def processar_todos_dados():
    """
    Processa todos os dados e retorna uma lista de linhas para a planilha.
    
    Returns:
        list: Lista de dicionários com dados e seções para formatação
    """
    todas_linhas = []
    
    # Processar dados de IES
    processar_dados_ies(todas_linhas, "Global")
    
    # Processar dados de municípios
    processar_dados_municipios(todas_linhas, "Global")
    
    # Processar dados de docentes
    processar_dados_docentes(todas_linhas, "Global")
    
    # Processar dados de cursos
    processar_dados_cursos(todas_linhas, "Global")
    
    # Processar dados de licenciaturas
    processar_dados_licenciaturas(todas_linhas, "Licenciaturas")
    
    # Processar dados de vagas
    processar_dados_vagas(todas_linhas)
    
    # Processar dados de inscritos
    processar_dados_inscritos(todas_linhas)
    
    # Processar dados de ingressos
    processar_dados_ingressos(todas_linhas)
    
    # Processar dados de matrículas
    processar_dados_matriculas(todas_linhas)
    
    # Processar dados de concluintes
    processar_dados_concluintes(todas_linhas)
    
    # Processar dados de matrículas trancadas
    processar_dados_matriculas_trancadas(todas_linhas)
    
    # Processar dados de evadidos
    processar_dados_evadidos(todas_linhas)
    
    # Processar dados de turno para licenciaturas presenciais
    processar_dados_turno_licenciaturas_presencial(todas_linhas)
    
    # Processar dados de gênero para licenciaturas presenciais e a distância
    processar_dados_genero_presencial(todas_linhas)
    
    # Processar dados de raça/cor para licenciaturas presenciais e a distância
    processar_dados_raca_cor(todas_linhas)
    
    # Processar dados de escola pública
    processar_dados_escola_publica(todas_linhas)
    
    return todas_linhas 
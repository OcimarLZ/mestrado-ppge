"""
Exemplo de como adicionar novas consultas SQL ao sistema modular.

Este arquivo demonstra como:
1. Adicionar novas consultas SQL no módulo sql_queries.py
2. Criar funções de processamento no módulo data_processors.py
3. Integrar as novas funcionalidades no script principal
"""

# =============================================================================
# PASSO 1: Adicionar nova consulta SQL em sql_queries.py
# =============================================================================

def exemplo_nova_consulta_sql():
    """
    Exemplo de como adicionar uma nova consulta SQL.
    
    Adicione esta função ao arquivo sql_queries.py:
    """
    
    def get_sql_nova_consulta():
        """Consulta para novos dados"""
        return """
        SELECT
            c.ano_censo AS ano,
            COUNT(DISTINCT c.curso) AS QtdeCursos
        FROM
            curso_censo c
        WHERE
            c.ano_censo > 2004
            AND c.tp_grau_academico = 1  -- Exemplo: apenas bacharelados
        GROUP BY
            c.ano_censo
        ORDER BY
            c.ano_censo
        """
    
    return "Adicione a função acima ao arquivo sql_queries.py"


# =============================================================================
# PASSO 2: Criar função de processamento em data_processors.py
# =============================================================================

def exemplo_nova_funcao_processamento():
    """
    Exemplo de como criar uma nova função de processamento.
    
    Adicione esta função ao arquivo data_processors.py:
    """
    
    def processar_novos_dados(todas_linhas, sub_categoria):
        """Processa novos dados e adiciona às linhas da planilha"""
        
        # Carrega dados da nova consulta
        dados_novos = carregar_dados_por_ano(get_sql_nova_consulta(), "QtdeCursos")
        
        # Cria linha de dados
        linha_nova = criar_linha_dados(
            "Nro de Cursos", 
            "Nenhum", 
            "Bacharelados", 
            sub_categoria, 
            dados_novos
        )
        
        # Adiciona à lista de linhas
        todas_linhas.append({"dados": linha_nova, "secao": "novos_dados"})
    
    return "Adicione a função acima ao arquivo data_processors.py"


# =============================================================================
# PASSO 3: Integrar no processamento principal
# =============================================================================

def exemplo_integracao_principal():
    """
    Exemplo de como integrar a nova funcionalidade no processamento principal.
    
    Modifique a função processar_todos_dados() em data_processors.py:
    """
    
    def processar_todos_dados():
        """
        Processa todos os dados e retorna a lista completa de linhas.
        """
        todas_linhas = []
        sub_categoria_global = "Global"
        sub_categoria_licenciaturas = "Licenciaturas"
        
        # Processa cada categoria de dados
        processar_dados_ies(todas_linhas, sub_categoria_global)
        processar_dados_municipios(todas_linhas, sub_categoria_global)
        processar_dados_docentes(todas_linhas, sub_categoria_global)
        processar_dados_cursos(todas_linhas, sub_categoria_global)
        processar_dados_licenciaturas(todas_linhas, sub_categoria_licenciaturas)
        
        # ADICIONE AQUI SUA NOVA FUNÇÃO:
        processar_novos_dados(todas_linhas, sub_categoria_global)
        
        return todas_linhas
    
    return "Modifique a função processar_todos_dados() conforme acima"


# =============================================================================
# PASSO 4: Adicionar nova seção de cores (opcional)
# =============================================================================

def exemplo_nova_secao_cores():
    """
    Exemplo de como adicionar uma nova seção de cores.
    
    Modifique a função get_cores_por_secao() em excel_formatter.py:
    """
    
    def get_cores_por_secao():
        """
        Retorna um dicionário mapeando seções para cores.
        """
        cores = get_cores_formatacao()
        return {
            # ... cores existentes ...
            "novos_dados": cores["verde_claro"],  # ADICIONE SUA NOVA SEÇÃO
        }
    
    return "Adicione sua nova seção ao dicionário de cores"


# =============================================================================
# EXEMPLO COMPLETO: Nova consulta para dados de discentes
# =============================================================================

def exemplo_completo_discentes():
    """
    Exemplo completo de como adicionar dados de discentes.
    """
    
    # 1. Nova consulta SQL (adicionar em sql_queries.py)
    def get_sql_discentes_global():
        """Consulta para dados globais de discentes"""
        return """
        SELECT
            d.ano_censo AS ano,
            COUNT(DISTINCT d.discente) AS QtdeDiscentes
        FROM
            discente_censo d
        WHERE
            d.ano_censo > 2004
        GROUP BY
            d.ano_censo
        ORDER BY
            d.ano_censo
        """
    
    # 2. Nova função de processamento (adicionar em data_processors.py)
    def processar_dados_discentes(todas_linhas, sub_categoria_global):
        """Processa dados de discentes e adiciona às linhas da planilha"""
        
        # Dados globais de discentes
        dados_discentes = carregar_dados_por_ano(get_sql_discentes_global(), "QtdeDiscentes")
        linha_discentes = criar_linha_dados("Nro de Discentes", "Nenhum", "Global", sub_categoria_global, dados_discentes)
        todas_linhas.append({"dados": linha_discentes, "secao": "discentes"})
    
    # 3. Integração no processamento principal
    def processar_todos_dados():
        todas_linhas = []
        sub_categoria_global = "Global"
        sub_categoria_licenciaturas = "Licenciaturas"
        
        # Processa cada categoria de dados
        processar_dados_ies(todas_linhas, sub_categoria_global)
        processar_dados_municipios(todas_linhas, sub_categoria_global)
        processar_dados_docentes(todas_linhas, sub_categoria_global)
        processar_dados_cursos(todas_linhas, sub_categoria_global)
        processar_dados_licenciaturas(todas_linhas, sub_categoria_licenciaturas)
        
        # NOVA FUNÇÃO ADICIONADA:
        processar_dados_discentes(todas_linhas, sub_categoria_global)
        
        return todas_linhas
    
    # 4. Nova seção de cores (adicionar em excel_formatter.py)
    def get_cores_por_secao():
        cores = get_cores_formatacao()
        return {
            # ... cores existentes ...
            "discentes": cores["verde_claro"],  # Nova seção
        }
    
    return "Exemplo completo de como adicionar dados de discentes"


if __name__ == "__main__":
    print("📋 Exemplos de como adicionar novas consultas SQL:")
    print("=" * 60)
    print("1. Adicione novas consultas em sql_queries.py")
    print("2. Crie funções de processamento em data_processors.py")
    print("3. Integre no processamento principal")
    print("4. Adicione cores para novas seções (opcional)")
    print("=" * 60)
    print("✅ Este arquivo serve como referência para expansões futuras!") 
"""
Módulo para gerenciar a formatação de planilhas Excel.
Contém funções para aplicar formatação, cores e estilos.
"""

from openpyxl.styles import PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


def get_cores_formatacao():
    """
    Retorna um dicionário com as cores de formatação.
    
    Returns:
        dict: Dicionário com as cores definidas
    """
    return {
        "cabecalho": PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid"),
        "cinza_claro": PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid"),
        "verde_claro": PatternFill(start_color="F0FFF0", end_color="F0FFF0", fill_type="solid")
    }


def get_alinhamentos():
    """
    Retorna um dicionário com os alinhamentos.
    
    Returns:
        dict: Dicionário com os alinhamentos definidos
    """
    return {
        "esquerda": Alignment(horizontal="left", vertical="center"),
        "direita": Alignment(horizontal="right", vertical="center")
    }


def get_bordas():
    """
    Retorna o estilo de bordas.
    
    Returns:
        Border: Objeto de bordas finas
    """
    return Border(
        left=Side(style="thin"), right=Side(style="thin"),
        top=Side(style="thin"), bottom=Side(style="thin")
    )


def get_cores_por_secao():
    """
    Retorna um dicionário mapeando seções para cores.
    
    Returns:
        dict: Dicionário com cores por seção
    """
    cores = get_cores_formatacao()
    return {
        "global": cores["cinza_claro"], 
        "rede": cores["verde_claro"], 
        "categoria": cores["cinza_claro"],
        "municipios": cores["verde_claro"], 
        "municipios_cursos": cores["cinza_claro"],
        "municipios_licenciatura": cores["verde_claro"],
        "municipios_licenciatura_modalidade": cores["cinza_claro"],
        "municipios_licenciatura_categoria_modalidade": cores["verde_claro"],
        "docentes": cores["verde_claro"], 
        "docentes_titulacao": cores["cinza_claro"],
        "docentes_filtrados": cores["verde_claro"], 
        "docentes_titulacao_filtrados": cores["cinza_claro"],
        "docentes_por_categoria": cores["verde_claro"], 
        "docentes_titulacao_por_categoria": cores["cinza_claro"],
        "cursos_global": cores["verde_claro"], 
        "cursos_rede": cores["cinza_claro"], 
        "cursos_categoria": cores["verde_claro"],
        "licenciaturas_global": cores["cinza_claro"], 
        "licenciaturas_rede": cores["verde_claro"], 
        "licenciaturas_categoria": cores["cinza_claro"],
        "vagas_global": cores["verde_claro"],
        "vagas_modalidade": cores["cinza_claro"],
        "vagas_licenciaturas_modalidade": cores["verde_claro"],
        "vagas_licenciaturas_categoria_modalidade": cores["cinza_claro"],
        "inscritos_global": cores["verde_claro"],
        "inscritos_modalidade": cores["cinza_claro"],
        "inscritos_licenciaturas_modalidade": cores["verde_claro"],
        "inscritos_licenciaturas_categoria_modalidade": cores["cinza_claro"],
        "ingressos_global": cores["verde_claro"],
        "ingressos_modalidade": cores["cinza_claro"],
        "ingressos_licenciaturas_modalidade": cores["verde_claro"],
        "ingressos_licenciaturas_categoria_modalidade": cores["cinza_claro"],
        "matriculas_global": cores["verde_claro"],
        "matriculas_modalidade": cores["cinza_claro"],
        "matriculas_licenciaturas_modalidade": cores["verde_claro"],
        "matriculas_licenciaturas_categoria_modalidade": cores["cinza_claro"],
        "concluintes_global": cores["verde_claro"],
        "concluintes_modalidade": cores["cinza_claro"],
        "concluintes_licenciaturas_modalidade": cores["verde_claro"],
        "concluintes_licenciaturas_categoria_modalidade": cores["cinza_claro"],
        "matriculas_trancadas_global": cores["verde_claro"],
        "matriculas_trancadas_modalidade": cores["cinza_claro"],
        "matriculas_trancadas_licenciaturas_modalidade": cores["verde_claro"],
        "matriculas_trancadas_licenciaturas_categoria_modalidade": cores["cinza_claro"],
        "evadidos_global": cores["verde_claro"],
        "evadidos_modalidade": cores["cinza_claro"],
        "evadidos_licenciaturas_modalidade": cores["verde_claro"],
        "evadidos_licenciaturas_categoria_modalidade": cores["cinza_claro"],
        "ingressos_licenciaturas_presencial_diurno": cores["verde_claro"],
        "ingressos_licenciaturas_presencial_noturno": cores["cinza_claro"],
        "matriculas_licenciaturas_presencial_diurno": cores["verde_claro"],
        "matriculas_licenciaturas_presencial_noturno": cores["cinza_claro"],
        "concluintes_licenciaturas_presencial_diurno": cores["verde_claro"],
        "concluintes_licenciaturas_presencial_noturno": cores["cinza_claro"],
        "ingressos_presencial_masculino": cores["verde_claro"],
        "ingressos_presencial_feminino": cores["cinza_claro"],
        "ingressos_distancia_masculino": cores["verde_claro"],
        "ingressos_distancia_feminino": cores["cinza_claro"],
        "matriculas_presencial_masculino": cores["verde_claro"],
        "matriculas_presencial_feminino": cores["cinza_claro"],
        "matriculas_distancia_masculino": cores["verde_claro"],
        "matriculas_distancia_feminino": cores["cinza_claro"],
        "concluintes_presencial_masculino": cores["verde_claro"],
        "concluintes_presencial_feminino": cores["cinza_claro"],
        "concluintes_distancia_masculino": cores["verde_claro"],
        "concluintes_distancia_feminino": cores["cinza_claro"],
        # Cores para dados de raça/cor - Presencial
        "ingressos_presencial_parda": cores["verde_claro"],
        "ingressos_presencial_amarela": cores["cinza_claro"],
        "ingressos_presencial_indigena": cores["verde_claro"],
        "ingressos_presencial_preta": cores["cinza_claro"],
        "ingressos_presencial_branca": cores["verde_claro"],
        "ingressos_presencial_cornd": cores["cinza_claro"],
        "matriculas_presencial_parda": cores["verde_claro"],
        "matriculas_presencial_amarela": cores["cinza_claro"],
        "matriculas_presencial_indigena": cores["verde_claro"],
        "matriculas_presencial_preta": cores["cinza_claro"],
        "matriculas_presencial_branca": cores["verde_claro"],
        "matriculas_presencial_cornd": cores["cinza_claro"],
        "concluintes_presencial_parda": cores["verde_claro"],
        "concluintes_presencial_amarela": cores["cinza_claro"],
        "concluintes_presencial_indigena": cores["verde_claro"],
        "concluintes_presencial_preta": cores["cinza_claro"],
        "concluintes_presencial_branca": cores["verde_claro"],
        "concluintes_presencial_cornd": cores["cinza_claro"],
        # Cores para dados de raça/cor - A Distância
        "ingressos_distancia_parda": cores["verde_claro"],
        "ingressos_distancia_amarela": cores["cinza_claro"],
        "ingressos_distancia_indigena": cores["verde_claro"],
        "ingressos_distancia_preta": cores["cinza_claro"],
        "ingressos_distancia_branca": cores["verde_claro"],
        "ingressos_distancia_cornd": cores["cinza_claro"],
        "matriculas_distancia_parda": cores["verde_claro"],
        "matriculas_distancia_amarela": cores["cinza_claro"],
        "matriculas_distancia_indigena": cores["verde_claro"],
        "matriculas_distancia_preta": cores["cinza_claro"],
        "matriculas_distancia_branca": cores["verde_claro"],
        "matriculas_distancia_cornd": cores["cinza_claro"],
        "concluintes_distancia_parda": cores["verde_claro"],
        "concluintes_distancia_amarela": cores["cinza_claro"],
        "concluintes_distancia_indigena": cores["verde_claro"],
        "concluintes_distancia_preta": cores["cinza_claro"],
        "concluintes_distancia_branca": cores["verde_claro"],
        "concluintes_distancia_cornd": cores["cinza_claro"],
        "ingressos_escola_publica": cores["verde_claro"],
        "matriculas_escola_publica": cores["cinza_claro"],
        "concluintes_escola_publica": cores["verde_claro"]
    }


def aplicar_formatacao_cabecalho(ws, colunas):
    """
    Aplica formatação ao cabeçalho da planilha.
    
    Args:
        ws: Worksheet do Excel
        colunas (list): Lista de colunas
    """
    cores = get_cores_formatacao()
    alinhamentos = get_alinhamentos()
    bordas = get_bordas()
    
    for col in range(1, len(colunas) + 1):
        celula = ws.cell(row=1, column=col)
        celula.fill = cores["cabecalho"]
        celula.border = bordas
        celula.alignment = alinhamentos["esquerda"] if col <= 4 else alinhamentos["direita"]


def aplicar_formatacao_linhas(ws, todas_linhas, colunas):
    """
    Aplica formatação às linhas de dados da planilha.
    
    Args:
        ws: Worksheet do Excel
        todas_linhas (list): Lista com todas as linhas de dados
        colunas (list): Lista de colunas
    """
    cores_por_secao = get_cores_por_secao()
    cores = get_cores_formatacao()  # Adiciona acesso às cores básicas
    alinhamentos = get_alinhamentos()
    bordas = get_bordas()
    
    linha_atual = 2
    for linha_info in todas_linhas:
        secao_sql = linha_info["secao"]
        # Corrige o acesso à cor padrão
        cor_linha = cores_por_secao.get(secao_sql, cores["verde_claro"])
        
        for col in range(1, len(colunas) + 1):
            celula = ws.cell(row=linha_atual, column=col)
            celula.fill = cor_linha
            celula.border = bordas
            celula.alignment = alinhamentos["esquerda"] if col <= 4 else alinhamentos["direita"]
        
        linha_atual += 1


def aplicar_formatacao_planilha(ws, todas_linhas, colunas):
    """
    Aplica formatação completa à planilha: cores, alinhamento e bordas.
    
    Args:
        ws: Worksheet do Excel
        todas_linhas (list): Lista com todas as linhas de dados
        colunas (list): Lista de colunas
    """
    aplicar_formatacao_cabecalho(ws, colunas)
    aplicar_formatacao_linhas(ws, todas_linhas, colunas)


def ajustar_largura_colunas(ws, todas_linhas, colunas):
    """
    Ajusta a largura das colunas para melhor visualização.
    
    Args:
        ws: Worksheet do Excel
        todas_linhas (list): Lista com todas as linhas de dados
        colunas (list): Lista de colunas
    """
    for i, coluna in enumerate(colunas, start=1):
        # Calcula a largura máxima considerando cabeçalho e todas as linhas
        max_width = len(str(coluna))
        for linha_info in todas_linhas:
            max_width = max(max_width, len(str(linha_info["dados"][i - 1])))
        
        # Define largura mínima para colunas de anos
        if i > 4:  # Colunas de anos (2005-2024)
            max_width = max(max_width, 8)  # Largura mínima para anos
        
        ws.column_dimensions[get_column_letter(i)].width = max_width + 2


def imprimir_resumo_formatacao(todas_linhas):
    """
    Imprime um resumo da formatação aplicada.
    
    Args:
        todas_linhas (list): Lista com todas as linhas de dados
    """
    print("Formatação aplicada:")
    print("  ✅ Cabeçalho: Amarelo, alinhamento consistente, com bordas")
    print("  ✅ Colunas 1-4: Alinhamento à esquerda (cabeçalho e dados)")
    print("  ✅ Colunas 2005-2024: Alinhamento à direita (cabeçalho e dados)")
    print("  ✅ Bordas finas em todas as células")
    print("  ✅ Cores alternadas por seção SQL")
    
    cores_por_secao = get_cores_por_secao()
    print("Linhas criadas:")
    for i, linha_info in enumerate(todas_linhas, 1):
        dados = linha_info["dados"]
        secao = linha_info["secao"]
        cor_nome = "cinza claro" if secao in [
            "global", "categoria", "municipios_cursos", "docentes_titulacao", 
            "docentes_titulacao_filtrados", "docentes_titulacao_por_categoria", 
            "cursos_rede", "licenciaturas_global", "licenciaturas_categoria"
        ] else "verde claro"
        print(f"  {i}. {dados[0]} - {dados[1]} - {dados[2]} - {dados[3]} (Seção: {secao}, Cor: {cor_nome})") 
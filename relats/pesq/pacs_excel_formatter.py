"""
Módulo para formatação de planilhas Excel com dados PACs.
Contém funções para aplicar cores, bordas e alinhamentos.
"""

from openpyxl.styles import PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


def get_cores_formatacao_pacs():
    """
    Retorna um dicionário com as cores básicas para formatação PACs.
    
    Returns:
        dict: Dicionário com cores básicas
    """
    return {
        "verde_claro": PatternFill(start_color="D4EDDA", end_color="D4EDDA", fill_type="solid"),
        "cinza_claro": PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid"),
        "azul_claro": PatternFill(start_color="D1ECF1", end_color="D1ECF1", fill_type="solid"),
        "amarelo_claro": PatternFill(start_color="FFF3CD", end_color="FFF3CD", fill_type="solid")
    }


def get_alinhamento_pacs():
    """
    Retorna o alinhamento padrão para células PACs.
    
    Returns:
        Alignment: Objeto de alinhamento
    """
    return Alignment(horizontal="center", vertical="center", wrap_text=True)


def get_borda_pacs():
    """
    Retorna a borda padrão para células PACs.
    
    Returns:
        Border: Objeto de borda
    """
    return Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )


def get_cores_por_secao_pacs():
    """
    Retorna um dicionário mapeando seções para cores PACs.
    
    Returns:
        dict: Dicionário com cores por seção
    """
    cores = get_cores_formatacao_pacs()
    return {
        "global": cores["cinza_claro"], 
        "rede": cores["verde_claro"], 
        "categoria": cores["cinza_claro"],
        "campus": cores["verde_claro"],
        "polo": cores["cinza_claro"],
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
        # Vagas
        "vagas_global": cores["verde_claro"],
        "vagas_modalidade": cores["cinza_claro"],
        "vagas_licenciaturas_modalidade": cores["verde_claro"],
        "vagas_licenciaturas_categoria_modalidade": cores["cinza_claro"],
        # Inscritos
        "inscritos_global": cores["verde_claro"],
        "inscritos_modalidade": cores["cinza_claro"],
        "inscritos_licenciaturas_modalidade": cores["verde_claro"],
        "inscritos_licenciaturas_categoria_modalidade": cores["cinza_claro"],
        # Ingressos
        "ingressos_global": cores["verde_claro"],
        "ingressos_modalidade": cores["cinza_claro"],
        "ingressos_licenciaturas_modalidade": cores["verde_claro"],
        "ingressos_licenciaturas_categoria_modalidade": cores["cinza_claro"],
        # Matrículas
        "matriculas_global": cores["verde_claro"],
        "matriculas_modalidade": cores["cinza_claro"],
        "matriculas_licenciaturas_modalidade": cores["verde_claro"],
        "matriculas_licenciaturas_categoria_modalidade": cores["cinza_claro"],
        # Concluintes
        "concluintes_global": cores["verde_claro"],
        "concluintes_modalidade": cores["cinza_claro"],
        "concluintes_licenciaturas_modalidade": cores["verde_claro"],
        "concluintes_licenciaturas_categoria_modalidade": cores["cinza_claro"],
        # Matrículas Trancadas
        "matriculas_trancadas_global": cores["verde_claro"],
        "matriculas_trancadas_modalidade": cores["cinza_claro"],
        "matriculas_trancadas_licenciaturas_modalidade": cores["verde_claro"],
        "matriculas_trancadas_licenciaturas_categoria_modalidade": cores["cinza_claro"],
        # Evadidos
        "evadidos_global": cores["verde_claro"],
        "evadidos_modalidade": cores["cinza_claro"],
        "evadidos_licenciaturas_modalidade": cores["verde_claro"],
        "evadidos_licenciaturas_categoria_modalidade": cores["cinza_claro"],
        # Turno
        "ingressos_licenciaturas_presencial_diurno": cores["verde_claro"],
        "ingressos_licenciaturas_presencial_noturno": cores["cinza_claro"],
        "matriculas_licenciaturas_presencial_diurno": cores["verde_claro"],
        "matriculas_licenciaturas_presencial_noturno": cores["cinza_claro"],
        "concluintes_licenciaturas_presencial_diurno": cores["verde_claro"],
        "concluintes_licenciaturas_presencial_noturno": cores["cinza_claro"],
        # Gênero Presencial
        "ingressos_presencial_masculino": cores["verde_claro"],
        "ingressos_presencial_feminino": cores["cinza_claro"],
        "matriculas_presencial_masculino": cores["verde_claro"],
        "matriculas_presencial_feminino": cores["cinza_claro"],
        "concluintes_presencial_masculino": cores["verde_claro"],
        "concluintes_presencial_feminino": cores["cinza_claro"],
        # Gênero A Distância
        "ingressos_distancia_masculino": cores["verde_claro"],
        "ingressos_distancia_feminino": cores["cinza_claro"],
        "matriculas_distancia_masculino": cores["verde_claro"],
        "matriculas_distancia_feminino": cores["cinza_claro"],
        "concluintes_distancia_masculino": cores["verde_claro"],
        "concluintes_distancia_feminino": cores["cinza_claro"],
        # Escola Pública
        "ingressos_escola_publica": cores["verde_claro"],
        "matriculas_escola_publica": cores["cinza_claro"],
        "concluintes_escola_publica": cores["verde_claro"],
        # Raça/Cor Presencial - Ingressos
        "ingressos_presencial_parda": cores["verde_claro"],
        "ingressos_presencial_amarela": cores["cinza_claro"],
        "ingressos_presencial_indigena": cores["verde_claro"],
        "ingressos_presencial_preta": cores["cinza_claro"],
        "ingressos_presencial_branca": cores["verde_claro"],
        "ingressos_presencial_cornd": cores["cinza_claro"],
        # Raça/Cor A Distância - Ingressos
        "ingressos_distancia_parda": cores["verde_claro"],
        "ingressos_distancia_amarela": cores["cinza_claro"],
        "ingressos_distancia_indigena": cores["verde_claro"],
        "ingressos_distancia_preta": cores["cinza_claro"],
        "ingressos_distancia_branca": cores["verde_claro"],
        "ingressos_distancia_cornd": cores["cinza_claro"],
        # Raça/Cor Presencial - Matrículas
        "matriculas_presencial_parda": cores["verde_claro"],
        "matriculas_presencial_amarela": cores["cinza_claro"],
        "matriculas_presencial_indigena": cores["verde_claro"],
        "matriculas_presencial_preta": cores["cinza_claro"],
        "matriculas_presencial_branca": cores["verde_claro"],
        "matriculas_presencial_cornd": cores["cinza_claro"],
        # Raça/Cor A Distância - Matrículas
        "matriculas_distancia_parda": cores["verde_claro"],
        "matriculas_distancia_amarela": cores["cinza_claro"],
        "matriculas_distancia_indigena": cores["verde_claro"],
        "matriculas_distancia_preta": cores["cinza_claro"],
        "matriculas_distancia_branca": cores["verde_claro"],
        "matriculas_distancia_cornd": cores["cinza_claro"],
        # Raça/Cor Presencial - Concluintes
        "concluintes_presencial_parda": cores["verde_claro"],
        "concluintes_presencial_amarela": cores["cinza_claro"],
        "concluintes_presencial_indigena": cores["verde_claro"],
        "concluintes_presencial_preta": cores["cinza_claro"],
        "concluintes_presencial_branca": cores["verde_claro"],
        "concluintes_presencial_cornd": cores["cinza_claro"],
        # Raça/Cor A Distância - Concluintes
        "concluintes_distancia_parda": cores["verde_claro"],
        "concluintes_distancia_amarela": cores["cinza_claro"],
        "concluintes_distancia_indigena": cores["verde_claro"],
        "concluintes_distancia_preta": cores["cinza_claro"],
        "concluintes_distancia_branca": cores["verde_claro"],
        "concluintes_distancia_cornd": cores["cinza_claro"]
    }


def aplicar_formatacao_cabecalho_pacs(ws):
    """
    Aplica formatação ao cabeçalho da planilha PACs.
    
    Args:
        ws: Worksheet do Excel
    """
    cores = get_cores_formatacao_pacs()
    alinhamento = get_alinhamento_pacs()
    borda = get_borda_pacs()
    
    # Formata o cabeçalho
    for cell in ws[1]:
        cell.fill = cores["azul_claro"]
        cell.alignment = alinhamento
        cell.border = borda
        cell.font = cell.font.copy(bold=True)


def aplicar_formatacao_linhas_pacs(ws, todas_linhas, colunas):
    """
    Aplica formatação às linhas de dados PACs.
    
    Args:
        ws: Worksheet do Excel
        todas_linhas: Lista de dicionários com dados e seções
        colunas: Lista de nomes das colunas
    """
    cores_por_secao = get_cores_por_secao_pacs()
    cores = get_cores_formatacao_pacs()
    alinhamento = get_alinhamento_pacs()
    borda = get_borda_pacs()
    
    # Aplica formatação a cada linha de dados
    for i, linha_info in enumerate(todas_linhas, start=2):  # Começa na linha 2 (após cabeçalho)
        secao_sql = linha_info["secao"]
        
        # Obtém a cor para esta seção
        cor_linha = cores_por_secao.get(secao_sql, cores["verde_claro"])
        
        # Aplica formatação a cada célula da linha
        for j, valor in enumerate(linha_info["dados"], start=1):
            cell = ws.cell(row=i, column=j)
            cell.fill = cor_linha
            cell.alignment = alinhamento
            cell.border = borda


def ajustar_largura_colunas_pacs(ws, todas_linhas, colunas):
    """
    Ajusta a largura das colunas da planilha PACs.
    
    Args:
        ws: Worksheet do Excel
        todas_linhas: Lista de dicionários com dados e seções
        colunas: Lista de nomes das colunas
    """
    # Define larguras específicas para as primeiras colunas
    larguras_colunas = {
        "A": 20,  # Tipo Dado
        "B": 15,  # Agrupamento
        "C": 15,  # Categoria
        "D": 15,  # Sub_Categoria
    }
    
    # Aplica larguras específicas
    for coluna, largura in larguras_colunas.items():
        ws.column_dimensions[coluna].width = largura
    
    # Ajusta largura das colunas de anos (E até Z)
    for i in range(5, len(colunas) + 1):
        coluna_letra = get_column_letter(i)
        ws.column_dimensions[coluna_letra].width = 12


def imprimir_resumo_formatacao_pacs(todas_linhas):
    """
    Imprime um resumo da formatação aplicada PACs.
    
    Args:
        todas_linhas: Lista de dicionários com dados e seções
    """
    print("\n📊 RESUMO DA FORMATAÇÃO PACs:")
    print("=" * 50)
    
    # Conta seções únicas
    secoes_unicas = set()
    for linha_info in todas_linhas:
        secoes_unicas.add(linha_info["secao"])
    
    print(f"�� Seções formatadas: {len(secoes_unicas)}")
    print(f"📋 Total de linhas: {len(todas_linhas)}")
    
    print("\n📋 Seções encontradas:")
    for secao in sorted(secoes_unicas):
        count = sum(1 for linha in todas_linhas if linha["secao"] == secao)
        print(f"   • {secao}: {count} linha(s)")


def aplicar_formatacao_planilha_pacs(ws, todas_linhas, colunas):
    """
    Aplica toda a formatação na planilha PACs.
    
    Args:
        ws: Worksheet do Excel
        todas_linhas: Lista de dicionários com dados e seções
        colunas: Lista de nomes das colunas
    """
    print("🎨 Aplicando formatação PACs...")
    
    # Aplica formatação ao cabeçalho
    aplicar_formatacao_cabecalho_pacs(ws)
    
    # Aplica formatação às linhas de dados
    aplicar_formatacao_linhas_pacs(ws, todas_linhas, colunas)
    
    print("✅ Formatação PACs aplicada com sucesso!") 
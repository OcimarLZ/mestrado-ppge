"""
Script de execução direta para gerar planilha Excel com dados PACs do INEP.
Este script pode ser executado diretamente sem problemas de import.
"""

import sys
import os
from openpyxl import Workbook

# Adiciona o path das dependências ao sistema
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importa os módulos PACs usando imports absolutos
from pacs_data_processors import processar_todos_dados_pacs
from pacs_excel_formatter import aplicar_formatacao_planilha_pacs, ajustar_largura_colunas_pacs, imprimir_resumo_formatacao_pacs


def criar_planilha_com_dados_pacs(output_filename):
    """
    Cria uma planilha Excel PACs com os anos como colunas (2014 a 2024).
    
    Args:
        output_filename (str): Nome do arquivo Excel a ser gerado
    """
    # Estrutura de colunas da planilha PACs
    colunas = ["Tipo Dado", "Agrupamento", "Categoria", "Sub_Categoria"] + [str(ano) for ano in range(2014, 2025)]
    
    print("Iniciando processamento de dados PACs...")
    
    # Processa todos os dados PACs usando o módulo de processamento
    todas_linhas = processar_todos_dados_pacs()
    
    if not todas_linhas:
        print("Erro: Nenhum dado PACs foi processado. Verifique as consultas SQL.")
        return
    
    print(f"Processamento PACs concluído. Total de linhas: {len(todas_linhas)}")
    
    # Cria a planilha Excel
    print("Criando planilha Excel PACs...")
    wb = Workbook()
    ws = wb.active
    ws.title = "Dados PACs"

    # Escreve o cabeçalho
    ws.append(colunas)

    # Escreve todas as linhas de dados
    for linha_info in todas_linhas:
        ws.append(linha_info["dados"])

    # Aplica toda a formatação na planilha
    print("Aplicando formatação PACs...")
    aplicar_formatacao_planilha_pacs(ws, todas_linhas, colunas)

    # Ajusta largura das colunas para melhor visualização
    print("Ajustando largura das colunas PACs...")
    ajustar_largura_colunas_pacs(ws, todas_linhas, colunas)

    # Salva a planilha no arquivo indicado
    try:
        wb.save(output_filename)
        print(f"✅ Planilha PACs '{output_filename}' criada com sucesso!")
        print(f"📊 Total de linhas criadas: {len(todas_linhas) + 1} (incluindo cabeçalho)")
        
        # Imprime resumo da formatação
        imprimir_resumo_formatacao_pacs(todas_linhas)
        
    except Exception as e:
        print(f"❌ Erro ao salvar a planilha PACs: {e}")


def main():
    """
    Função principal para executar a geração da planilha PACs.
    """
    # Nome do arquivo Excel a ser gerado
    output_file = "Dados_PACs.xlsx"

    print("🚀 Iniciando geração da planilha de dados PACs do INEP...")
    print("=" * 60)
    print("📋 Configurações:")
    print("   • Município: 4204202")
    print("   • Período: 2014-2024")
    print("   • Filtros: Aplicados conforme especificação")
    print("=" * 60)
    
    # Cria a planilha com os dados
    criar_planilha_com_dados_pacs(output_file)
    
    print("=" * 60)
    print("✅ Processo PACs concluído!")


# --- Como usar a rotina ---
if __name__ == "__main__":
    main() 
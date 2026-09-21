"""
Script de execução direta para gerar planilha Excel com dados do INEP.
Este script pode ser executado diretamente sem problemas de import.
"""

import sys
import os
from openpyxl import Workbook

# Adiciona o path das dependências ao sistema
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importa os módulos usando imports absolutos
from data_processors import processar_todos_dados
from excel_formatter import aplicar_formatacao_planilha, ajustar_largura_colunas, imprimir_resumo_formatacao


def criar_planilha_com_dados(output_filename):
    """
    Cria uma planilha Excel com os anos como colunas (2005 a 2024).
    
    Args:
        output_filename (str): Nome do arquivo Excel a ser gerado
    """
    # Estrutura de colunas da planilha
    colunas = ["Tipo Dado", "Agrupamento", "Categoria", "Sub_Categoria"] + [str(ano) for ano in range(2005, 2025)]
    
    print("Iniciando processamento de dados...")
    
    # Processa todos os dados usando o módulo de processamento
    todas_linhas = processar_todos_dados()
    
    if not todas_linhas:
        print("Erro: Nenhum dado foi processado. Verifique as consultas SQL.")
        return
    
    print(f"Processamento concluído. Total de linhas: {len(todas_linhas)}")
    
    # Cria a planilha Excel
    print("Criando planilha Excel...")
    wb = Workbook()
    ws = wb.active
    ws.title = "Dados IES"

    # Escreve o cabeçalho
    ws.append(colunas)

    # Escreve todas as linhas de dados
    for linha_info in todas_linhas:
        ws.append(linha_info["dados"])

    # Aplica toda a formatação na planilha
    print("Aplicando formatação...")
    aplicar_formatacao_planilha(ws, todas_linhas, colunas)

    # Ajusta largura das colunas para melhor visualização
    print("Ajustando largura das colunas...")
    ajustar_largura_colunas(ws, todas_linhas, colunas)

    # Salva a planilha no arquivo indicado
    try:
        wb.save(output_filename)
        print(f"✅ Planilha '{output_filename}' criada com sucesso!")
        print(f"📊 Total de linhas criadas: {len(todas_linhas) + 1} (incluindo cabeçalho)")
        
        # Imprime resumo da formatação
        imprimir_resumo_formatacao(todas_linhas)
        
    except Exception as e:
        print(f"❌ Erro ao salvar a planilha: {e}")


def main():
    """
    Função principal para executar a geração da planilha.
    """
    # Nome do arquivo Excel a ser gerado
    output_file = "Dados_IES.xlsx"

    print("🚀 Iniciando geração da planilha de dados do INEP...")
    print("=" * 60)
    
    # Cria a planilha com os dados
    criar_planilha_com_dados(output_file)
    
    print("=" * 60)
    print("✅ Processo concluído!")


# --- Como usar a rotina ---
if __name__ == "__main__":
    main() 
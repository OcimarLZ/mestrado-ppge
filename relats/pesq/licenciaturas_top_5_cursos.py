import pandas as pd
import matplotlib.pyplot as plt
import itertools
import sys
import os

# Adiciona o diretório pai ao sys.path para que os módulos bdados e utilities sejam encontrados
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL (o SQL permanece o mesmo, pois já retorna os totais brutos)
sql = """
WITH NormalizedCourses AS (
  SELECT
    c.ano_censo,
    c2.nome AS nome_curso_original,
    c.qt_ing,
    c.qt_sit_trancada,
    c.qt_conc,
    (c.qt_sit_desvinculado + c.qt_sit_falecido + c.qt_sit_transferido) AS qt_evadidos,
    -- Normaliza o nome do curso: minúsculas, sem espaços e sem acentos
    REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
      LOWER(c2.nome),
      ' ', ''), -- Remove espaços
      'á', 'a'), 'à', 'a'), 'ã', 'a'), 'â', 'a'),
      'é', 'e'), 'ê', 'e'),
      'í', 'i'),
      'ó', 'o'), 'õ', 'o'), 'ô', 'o'),
      'ú', 'u'),
      'ç', 'c'
    ) AS normalized_name
  FROM curso_censo c
  JOIN curso c2 ON c2.codigo = c.curso
  WHERE c.tp_grau_academico = 2
    AND c.categoria IN (1,2,3,5,8,9)
)
SELECT
  nc.ano_censo AS ano,
  -- Define a categoria do curso com base no nome normalizado
  CASE
    WHEN nc.normalized_name LIKE '%letras%' THEN 'Letras'
    WHEN nc.normalized_name LIKE '%pedagogia%' THEN 'Pedagogia'
    WHEN nc.normalized_name LIKE '%matem%' THEN 'Matemática'
    WHEN nc.normalized_name LIKE '%cienciasbiologicas%' THEN 'Ciências Biológicas'
    WHEN nc.normalized_name LIKE '%educacaofisica%' THEN 'Educação Física'
    ELSE 'Outros/Não Classificado' -- Caso algum curso passe pelo WHERE mas não se encaixe nas categorias
  END AS CategoriaCurso,
  SUM(nc.qt_ing) AS QtdeIngressantes,
  SUM(nc.qt_sit_trancada) AS QtdeTrancados,
  SUM(nc.qt_conc) AS QtdeConcluintes,
  SUM(nc.qt_evadidos) AS QtdeEvadidos
FROM NormalizedCourses nc
WHERE
  -- Filtra apenas as categorias que você deseja totalizar
  nc.normalized_name LIKE '%letras%' OR
  nc.normalized_name LIKE '%pedagogia%' OR
  nc.normalized_name LIKE '%matem%' OR
  nc.normalized_name LIKE '%cienciasbiologicas%' OR
  nc.normalized_name LIKE '%educacaofisica%'
GROUP BY nc.ano_censo, CategoriaCurso
ORDER BY CategoriaCurso, nc.ano_censo;
"""

# Carrega os dados do banco de dados para um DataFrame
df = carregar_dataframe(sql)

# --- Geração da Tabela HTML ---
# Prepara DataFrame para tabela - AGORA COM OS VALORES ABSOLUTOS
pivot_df = df[['ano', 'CategoriaCurso', 'QtdeIngressantes', 'QtdeTrancados', 'QtdeConcluintes', 'QtdeEvadidos']].copy()

# Renomeia as colunas para exibição na tabela HTML
colunas_html = ['Ano', 'Categoria do Curso', 'Ingressantes', 'Trancados', 'Concluintes', 'Evadidos']
tam_colunas = ['50px', '180px', '120px', '100px', '100px', '100px']
alinhamentos = ['left', 'left', 'right', 'right', 'right', 'right']
cabecalho_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
linha_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome_tabela = 'licenciaturas_por_area_totais' # Nome do arquivo da tabela ajustado

html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="6" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Totais de Ingressantes, Trancados, Concluintes e Evadidos em Licenciaturas por Área de Conhecimento
        </th>
    </tr>
</table>
"""

html_text = dataframe_to_html(pivot_df, tam_colunas, colunas_html, alinhamentos, cabecalho_style, linha_style)
html_text = html_title + html_text
html_text = html_text.replace('<thead>', '<thead style="background-color: #4CAF50;">')

# Salvando a tabela HTML
arq_output_tabela = 'docs/tabelas/' + arq_nome_tabela + '.html'
os.makedirs(os.path.dirname(arq_output_tabela), exist_ok=True) # Garante que o diretório exista
with open(arq_output_tabela, 'w', encoding='utf-8') as file:
    file.write(html_text)
print(f'Tabela HTML "{arq_output_tabela}" criada com sucesso.')

# --- Geração dos Gráficos ---
# Gráficos separados para cada métrica (Ingressantes, Trancados, Concluintes, Evadidos)
labels_metric = {
    'QtdeIngressantes': 'Ingressantes',
    'QtdeTrancados': 'Trancados',
    'QtdeConcluintes': 'Concluintes',
    'QtdeEvadidos': 'Evadidos'
}

# Paleta de cores para as categorias de curso
palette = [
    '#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5', '#70AD47', '#C00000', '#00B0F0',
    '#FF69B4', '#008080', '#B8860B', '#4682B4', '#8B0000', '#228B22', '#800080', '#FF8C00',
    '#20B2AA', '#B22222', '#DAA520', '#2E8B57', '#6A5ACD', '#D2691E', '#DC143C', '#008B8B'
]

arq_nome_grafico = 'licenciaturas_por_area_metricas' # Nome do arquivo do gráfico ajustado

# Obtém todos os anos únicos e os ordena para garantir consistência no eixo X
all_years_sorted = sorted(df['ano'].unique())

# Itera sobre cada métrica para gerar um gráfico separado
for metric_col, metric_label in labels_metric.items():
    fig, ax = plt.subplots(figsize=(14, 8), facecolor='white')
    ax.set_facecolor('white')

    categorias_curso = df['CategoriaCurso'].unique()
    # Mapeia cada categoria a uma cor da paleta
    color_map = {categoria: palette[i % len(palette)] for i, categoria in enumerate(categorias_curso)}

    for categoria in categorias_curso:
        subdf = df[df['CategoriaCurso'] == categoria].sort_values(by='ano') # Garante a ordenação por ano
        x_years_str = subdf['ano'].astype(str) # Anos como string para rótulos do eixo X
        y_values = subdf[metric_col]

        # Plot the line
        ax.plot(x_years_str, y_values, marker='o', label=f"{categoria}", color=color_map[categoria], linewidth=2)

        # Adiciona os rótulos numéricos aos pontos de dados
        # O x-coordinate para ax.text deve ser o índice numérico da posição do ano no eixo X
        # Para isso, mapeamos os anos de subdf para seus índices em all_years_sorted
        for year_str, value in zip(x_years_str, y_values):
            # Encontra o índice numérico do ano no array de anos do eixo X
            x_pos = all_years_sorted.index(int(year_str)) # Converte year_str para int para buscar em all_years_sorted
            
            # Offset vertical para o texto (ajustável)
            # Um pequeno percentual do valor máximo da métrica para um offset proporcional
            offset = (df[metric_col].max() - df[metric_col].min()) * 0.02 if not df[metric_col].empty else 0.02
            if df[metric_col].max() == df[metric_col].min(): # Evita offset zero se todos os valores forem iguais
                offset = 0.02 * df[metric_col].max() if not df[metric_col].empty and df[metric_col].max() != 0 else 1

            ax.text(x_pos, value + offset, f'{value:.0f}', # Formata como inteiro
                    ha='center', va='bottom', fontsize=9, color=color_map[categoria]) # Cor do texto igual à cor da linha

    # Define os ticks e rótulos do eixo X para garantir que todos os anos apareçam
    ax.set_xticks(range(len(all_years_sorted)))
    ax.set_xticklabels([str(y) for y in all_years_sorted])


    ax.set_xlabel('Ano', fontsize=12)
    ax.set_ylabel(f'Quantidade de {metric_label}', fontsize=12) # Rótulo do eixo Y ajustado
    ax.set_title(f'{metric_label} em Licenciaturas por Área de Conhecimento', color='#000000', fontsize=14) # Título ajustado
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.18), ncol=min(len(categorias_curso), 5), fontsize='small', title='Categoria do Curso', frameon=False) # Ajusta ncol dinamicamente
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Salvando o gráfico
    # O nome do arquivo reflete a métrica (ex: licenciaturas_por_area_metricas_qtdeingressantes.png)
    arq_output_grafico = f'docs/graficos/{arq_nome_grafico}_{metric_col.lower()}.png' # Nome do arquivo ajustado
    os.makedirs(os.path.dirname(arq_output_grafico), exist_ok=True) # Garante que o diretório exista
    plt.savefig(arq_output_grafico, bbox_inches='tight')
    plt.show()
    plt.close()

print('Gráficos criados com sucesso.')
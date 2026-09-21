import pandas as pd
import matplotlib.pyplot as plt
import itertools
import sys
import os

# Adiciona o diretório pai ao sys.path para que os módulos bdados e utilities sejam encontrados
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
WITH NormalizedCourses AS (
  SELECT
    c.ano_censo,
    c2.nome AS nome_curso_original,
    c.qt_ing,
    c.qt_sit_trancada,
    c.qt_conc,
    (c.qt_sit_desvinculado + c.qt_sit_falecido + c.qt_sit_transferido) AS qt_evadidos,
    c.qt_inscrito_total, -- Adicionado aqui para ser usado no SUM
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
  SUM(nc.qt_evadidos) AS QtdeEvadidos,
  SUM(nc.qt_inscrito_total) AS QtdeInscritos -- Adicionado aqui
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
pivot_df = df[['ano', 'CategoriaCurso', 'QtdeInscritos', 'QtdeIngressantes', 'QtdeTrancados', 'QtdeConcluintes', 'QtdeEvadidos']].copy()

# Renomeia as colunas para exibição na tabela HTML
colunas_html = ['Ano', 'Categoria do Curso', 'Inscritos', 'Ingressantes', 'Trancados', 'Concluintes', 'Evadidos']
tam_colunas = ['50px', '180px', '100px', '100px', '100px', '100px', '100px'] # Ajustado para 7 colunas
alinhamentos = ['left', 'left', 'right', 'right', 'right', 'right', 'right'] # Ajustado para 7 alinhamentos
cabecalho_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
linha_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome_tabela = 'licenciaturas_por_area_totais'

html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="7" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Totais de Inscritos, Ingressantes, Trancados, Concluintes e Evadidos em Licenciaturas por Área de Conhecimento
        </th>
    </tr>
</table>
""" # colspan ajustado para 7

html_text = dataframe_to_html(pivot_df, tam_colunas, colunas_html, alinhamentos, cabecalho_style, linha_style)
html_text = html_title + html_text
html_text = html_text.replace('<thead>', '<thead style="background-color: #4CAF50;">')

arq_output_tabela = 'docs/tabelas/' + arq_nome_tabela + '.html'
os.makedirs(os.path.dirname(arq_output_tabela), exist_ok=True)
with open(arq_output_tabela, 'w', encoding='utf-8') as file:
    file.write(html_text)
print(f'Tabela HTML "{arq_output_tabela}" criada com sucesso.')

# --- Geração dos Gráficos ---
# Métricas a serem plotadas em cada gráfico
metrics_to_plot = {
    'QtdeInscritos': 'Inscritos', # Adicionado aqui
    'QtdeIngressantes': 'Ingressantes',
    'QtdeTrancados': 'Trancados',
    'QtdeConcluintes': 'Concluintes',
    'QtdeEvadidos': 'Evadidos'
}

# Paleta de cores para as linhas dentro de cada gráfico (uma cor para cada métrica)
# Ajustei a paleta para ter cores distintas para as 5 métricas
metric_colors = {
    'QtdeInscritos': '#00B0F0',    # Azul claro (nova cor)
    'QtdeIngressantes': '#4472C4', # Azul
    'QtdeTrancados': '#ED7D31',    # Laranja
    'QtdeConcluintes': '#70AD47',  # Verde
    'QtdeEvadidos': '#C00000'      # Vermelho
}

# Estilos de linha para as métricas
linestyles = {
    'QtdeInscritos': '-',          # Estilo para Inscritos
    'QtdeIngressantes': '-',
    'QtdeTrancados': '--',
    'QtdeConcluintes': '-.',
    'QtdeEvadidos': ':'
}

arq_nome_grafico_base = 'licenciaturas_por_area_detalhe'

# Obtém todos os anos únicos e os ordena para garantir consistência no eixo X
all_years_sorted = sorted(df['ano'].unique())

# Itera sobre cada categoria de curso para criar um gráfico separado
categorias_curso = df['CategoriaCurso'].unique()
for categoria in categorias_curso:
    fig, ax = plt.subplots(figsize=(14, 8), facecolor='white')
    ax.set_facecolor('white')

    subdf = df[df['CategoriaCurso'] == categoria].sort_values(by='ano') # Filtra e ordena por ano para a categoria atual

    # Plota cada métrica para a categoria atual
    for metric_col, metric_label in metrics_to_plot.items():
        x_years_str = subdf['ano'].astype(str) # Anos como string para rótulos do eixo X
        y_values = subdf[metric_col]

        # Plota a linha
        ax.plot(x_years_str, y_values, marker='o', label=f"{metric_label}",
                color=metric_colors[metric_col], linestyle=linestyles[metric_col], linewidth=2)

        # Adiciona os rótulos numéricos aos pontos de dados
        # Apenas adiciona rótulos se houver dados para plotar
        if not y_values.empty:
            # Calcula o range dos valores para a métrica atual para um offset mais preciso
            min_val = y_values.min() if not y_values.empty else 0
            max_val = y_values.max() if not y_values.empty else 0
            
            # Evita divisão por zero ou offset zero se todos os valores forem iguais ou zero
            if max_val - min_val == 0:
                offset = 0.05 * (max_val if max_val != 0 else 1) # Pequeno offset fixo se todos os valores forem iguais
            else:
                offset = (max_val - min_val) * 0.02 # 2% do range da métrica

            for year_str, value in zip(x_years_str, y_values):
                # Encontra o índice numérico do ano no array de anos do eixo X
                try:
                    x_pos = all_years_sorted.index(int(year_str))
                except ValueError:
                    continue 
                
                ax.text(x_pos, value + offset, f'{value:.0f}', # Formata como inteiro
                        ha='center', va='bottom', fontsize=8, color=metric_colors[metric_col]) # Cor do texto igual à cor da linha

    # Define os ticks e rótulos do eixo X para garantir que todos os anos apareçam
    ax.set_xticks(range(len(all_years_sorted)))
    ax.set_xticklabels([str(y) for y in all_years_sorted])

    ax.set_xlabel('Ano', fontsize=12)
    ax.set_ylabel('Quantidade', fontsize=12) # Rótulo do eixo Y genérico
    ax.set_title(f'Dados dos Cursps de Licenciaturas para {categoria}', color='#000000', fontsize=14) # Título específico da categoria
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.18), ncol=len(metrics_to_plot), fontsize='small', title='Métrica', frameon=False)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Salvando o gráfico
    arq_output_grafico = f'docs/graficos/{arq_nome_grafico_base}_{categoria.lower().replace(" ", "_")}.png'
    os.makedirs(os.path.dirname(arq_output_grafico), exist_ok=True)
    plt.savefig(arq_output_grafico, bbox_inches='tight')
    plt.show()
    plt.close()

print('Gráficos criados com sucesso.')
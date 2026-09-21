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
    c.qt_inscrito_total,
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
    ELSE 'Outros/Não Classificado'
  END AS CategoriaCurso,
  SUM(nc.qt_ing) AS QtdeIngressantes,
  SUM(nc.qt_sit_trancada) AS QtdeTrancados,
  SUM(nc.qt_conc) AS QtdeConcluintes,
  SUM(nc.qt_evadidos) AS QtdeEvadidos,
  SUM(nc.qt_inscrito_total) AS QtdeInscritos
FROM NormalizedCourses nc
WHERE
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

# --- Geração da Tabela HTML (mantida como no script anterior) ---
pivot_df = df[['ano', 'CategoriaCurso', 'QtdeInscritos', 'QtdeIngressantes', 'QtdeTrancados', 'QtdeConcluintes', 'QtdeEvadidos']].copy()
colunas_html = ['Ano', 'Categoria do Curso', 'Inscritos', 'Ingressantes', 'Trancados', 'Concluintes', 'Evadidos']
tam_colunas = ['50px', '180px', '100px', '100px', '100px', '100px', '100px']
alinhamentos = ['left', 'left', 'right', 'right', 'right', 'right', 'right']
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
"""
html_text = dataframe_to_html(pivot_df, tam_colunas, colunas_html, alinhamentos, cabecalho_style, linha_style)
html_text = html_title + html_text
html_text = html_text.replace('<thead>', '<thead style="background-color: #4CAF50;">')

arq_output_tabela = 'docs/tabelas/' + arq_nome_tabela + '.html'
os.makedirs(os.path.dirname(arq_output_tabela), exist_ok=True)
with open(arq_output_tabela, 'w', encoding='utf-8') as file:
    file.write(html_text)
print(f'Tabela HTML "{arq_output_tabela}" criada com sucesso.')

# --- Geração dos Gráficos ---

# Métricas para o gráfico de Inscritos
inscritos_metric = {'QtdeInscritos': 'Inscritos'}

# Métricas para o gráfico das outras 4
other_metrics = {
    'QtdeIngressantes': 'Ingressantes',
    'QtdeTrancados': 'Trancados',
    'QtdeConcluintes': 'Concluintes',
    'QtdeEvadidos': 'Evadidos'
}

# Paleta de cores para as linhas
metric_colors = {
    'QtdeInscritos': '#00B0F0',    # Azul claro
    'QtdeIngressantes': '#4472C4', # Azul
    'QtdeTrancados': '#ED7D31',    # Laranja
    'QtdeConcluintes': '#70AD47',  # Verde
    'QtdeEvadidos': '#C00000'      # Vermelho
}

# Estilos de linha
linestyles = {
    'QtdeInscritos': '-',
    'QtdeIngressantes': '-',
    'QtdeTrancados': '--',
    'QtdeConcluintes': '-.',
    'QtdeEvadidos': ':'
}

arq_nome_grafico_base = 'licenciaturas_por_area_detalhe'

# Obtém todos os anos únicos e os ordena para garantir consistência no eixo X
all_years_sorted = sorted(df['ano'].unique())

# Itera sobre cada categoria de curso para criar gráficos separados
categorias_curso = df['CategoriaCurso'].unique()
for categoria in categorias_curso:
    subdf = df[df['CategoriaCurso'] == categoria].sort_values(by='ano')
    x_years_str = subdf['ano'].astype(str)

    # --- GRÁFICO 1: APENAS INSCRITOS ---
    fig1, ax1 = plt.subplots(figsize=(14, 8), facecolor='white')
    ax1.set_facecolor('white')

    for metric_col, metric_label in inscritos_metric.items():
        y_values = subdf[metric_col]
        ax1.plot(x_years_str, y_values, marker='o', label=f"{metric_label}",
                 color=metric_colors[metric_col], linestyle=linestyles[metric_col], linewidth=2)
        
        # Adicionar rótulos
        if not y_values.empty:
            min_val = y_values.min() if not y_values.empty else 0
            max_val = y_values.max() if not y_values.empty else 0
            offset = (max_val - min_val) * 0.02 if (max_val - min_val) != 0 else (0.02 * max_val if max_val != 0 else 1)
            for year_str, value in zip(x_years_str, y_values):
                try:
                    x_pos = all_years_sorted.index(int(year_str))
                except ValueError:
                    continue
                ax1.text(x_pos, value + offset, f'{value:.0f}',
                         ha='center', va='bottom', fontsize=8, color=metric_colors[metric_col])

    ax1.set_xticks(range(len(all_years_sorted)))
    ax1.set_xticklabels([str(y) for y in all_years_sorted])
    ax1.set_xlabel('Ano', fontsize=12)
    ax1.set_ylabel('Quantidade de Inscritos', fontsize=12)
    ax1.set_title(f'Inscritos em Licenciaturas para {categoria}', color='#000000', fontsize=14)
    ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.18), ncol=1, fontsize='small', title='Métrica', frameon=False)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Salvando o gráfico de Inscritos
    arq_output_grafico_inscritos = f'docs/graficos/{arq_nome_grafico_base}_{categoria.lower().replace(" ", "_")}_inscritos.png'
    os.makedirs(os.path.dirname(arq_output_grafico_inscritos), exist_ok=True)
    plt.savefig(arq_output_grafico_inscritos, bbox_inches='tight')
    plt.show()
    plt.close(fig1) # Fecha a figura para liberar memória

    # --- GRÁFICO 2: OUTRAS MÉTRICAS ---
    fig2, ax2 = plt.subplots(figsize=(14, 8), facecolor='white')
    ax2.set_facecolor('white')

    for metric_col, metric_label in other_metrics.items():
        y_values = subdf[metric_col]
        ax2.plot(x_years_str, y_values, marker='o', label=f"{metric_label}",
                 color=metric_colors[metric_col], linestyle=linestyles[metric_col], linewidth=2)
        
        # Adicionar rótulos
        if not y_values.empty:
            min_val = y_values.min() if not y_values.empty else 0
            max_val = y_values.max() if not y_values.empty else 0
            offset = (max_val - min_val) * 0.02 if (max_val - min_val) != 0 else (0.02 * max_val if max_val != 0 else 1)
            for year_str, value in zip(x_years_str, y_values):
                try:
                    x_pos = all_years_sorted.index(int(year_str))
                except ValueError:
                    continue
                ax2.text(x_pos, value + offset, f'{value:.0f}',
                         ha='center', va='bottom', fontsize=8, color=metric_colors[metric_col])

    ax2.set_xticks(range(len(all_years_sorted)))
    ax2.set_xticklabels([str(y) for y in all_years_sorted])
    ax2.set_xlabel('Ano', fontsize=12)
    ax2.set_ylabel('Quantidade', fontsize=12)
    ax2.set_title(f'Ingressantes, Trancados, Concluintes e Evadidos em Licenciaturas para {categoria}', color='#000000', fontsize=14)
    ax2.legend(loc='lower center', bbox_to_anchor=(0.5, -0.18), ncol=len(other_metrics), fontsize='small', title='Métrica', frameon=False)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Salvando o gráfico das outras métricas
    arq_output_grafico_outras = f'docs/graficos/{arq_nome_grafico_base}_{categoria.lower().replace(" ", "_")}_outras_metricas.png'
    os.makedirs(os.path.dirname(arq_output_grafico_outras), exist_ok=True)
    plt.savefig(arq_output_grafico_outras, bbox_inches='tight')
    plt.show()
    plt.close(fig2) # Fecha a figura para liberar memória

print('Gráficos criados com sucesso.')
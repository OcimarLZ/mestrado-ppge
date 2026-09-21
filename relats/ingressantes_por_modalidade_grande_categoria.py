import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os

# Adiciona o path das dependências ao sistema
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# SQL para buscar dados de ingressantes por modalidade e grande categoria
sql = """
SELECT
    c.ano_censo AS ano,
    CASE 
        WHEN c.categoria IN (1, 2, 3) THEN 'Pública'
        WHEN c.categoria IN (4, 6) THEN 'Privada com fins lucrativos'
        ELSE 'Privada sem fins lucrativos'
    END AS grande_categoria,
    m.nome AS modalidade,
    SUM(c.qt_ing) AS Ingressantes
FROM
    curso_censo c
JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
WHERE
    c.ano_censo >= 2005
GROUP BY
    c.ano_censo, 
    CASE 
        WHEN c.categoria IN (1, 2, 3) THEN 'Pública'
        WHEN c.categoria IN (4, 6) THEN 'Privada com fins lucrativos'
        ELSE 'Privada sem fins lucrativos'
    END,
    m.nome
ORDER BY
    c.ano_censo, grande_categoria, m.nome
"""

# Carregar dados
df = carregar_dataframe(sql)

# Gerar tabela HTML
column_widths = [100, 250, 150, 120]
column_names = ['Ano', 'Grande Categoria', 'Modalidade', 'Ingressantes']
column_alignments = ['center', 'left', 'left', 'right']
header_style = 'background-color: #4CAF50; color: white; font-weight: bold;'
row_style = 'background-color: #f2f2f2;'

html_table = dataframe_to_html(
    df, 
    column_widths, 
    column_names, 
    column_alignments, 
    header_style, 
    row_style
)

# Criar diretórios se não existirem
os.makedirs('docs/tabelas', exist_ok=True)
os.makedirs('docs/graficos', exist_ok=True)

# Salvar tabela HTML
with open('docs/tabelas/ingressantes_por_modalidade_grande_categoria.html', 'w', encoding='utf-8') as f:
    f.write(html_table)

# Definir cores personalizadas para as grandes categorias
color_map = {
    'Pública': '#2E8B57',  # Verde
    'Privada com fins lucrativos': '#DC143C',  # Vermelho
    'Privada sem fins lucrativos': '#4169E1'  # Azul
}

# Criar coluna combinada para cor baseada na grande categoria
df['cor_categoria'] = df['grande_categoria'].map(color_map)

# Gráfico Plotly interativo - Ingressantes por Modalidade e Grande Categoria
fig = px.line(
    df, 
    x='ano', 
    y='Ingressantes', 
    color='grande_categoria',
    line_dash='modalidade',
    title='Evolução de Ingressantes por Modalidade e Grande Categoria',
    markers=True,
    color_discrete_map=color_map
)

fig.update_layout(
    xaxis_title='Ano',
    yaxis_title='Número de Ingressantes',
    legend_title='Modalidade / Grande Categoria',
    font=dict(size=12),
    title_font_size=16,
    xaxis=dict(
        tickmode='array',
        tickvals=list(range(2005, 2024)),
        ticktext=[str(year) for year in range(2005, 2024)],
        range=[2004.5, 2023.5]
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,
        xanchor="center",
        x=0.5
    )
)

# Salvar gráfico Plotly
fig.write_html('docs/graficos/ingressantes_por_modalidade_grande_categoria.html')

# Gráfico Seaborn estático - Ingressantes por Modalidade e Grande Categoria
plt.figure(figsize=(14, 8))

# Criar DataFrame para o gráfico com nomes adequados
df_plot = df.copy()
df_plot = df_plot.rename(columns={'ano': 'Ano', 'grande_categoria': 'Grande Categoria', 'modalidade': 'Modalidade'})

# Definir paleta de cores para Seaborn
color_palette = ['#2E8B57', '#DC143C', '#4169E1']  # Verde, Vermelho, Azul

# Gráfico de linhas com Seaborn
sns.lineplot(
    data=df_plot, 
    x='Ano', 
    y='Ingressantes', 
    hue='Grande Categoria',
    style='Modalidade',
    markers=True,
    linewidth=2.5,
    palette=color_palette
)

plt.title('Evolução de Ingressantes por Modalidade e Grande Categoria', fontsize=16, fontweight='bold')
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Número de Ingressantes', fontsize=12)
plt.xticks(range(2005, 2024), rotation=45)
plt.grid(True, alpha=0.3)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Salvar gráfico Seaborn
plt.savefig('docs/graficos/ingressantes_por_modalidade_grande_categoria.png', dpi=300, bbox_inches='tight')
plt.close()

print("Relatório de Ingressantes por Modalidade e Grande Categoria gerado com sucesso!")
print("Arquivos salvos:")
print("- docs/tabelas/ingressantes_por_modalidade_grande_categoria.html")
print("- docs/graficos/ingressantes_por_modalidade_grande_categoria.html")
print("- docs/graficos/ingressantes_por_modalidade_grande_categoria.png")
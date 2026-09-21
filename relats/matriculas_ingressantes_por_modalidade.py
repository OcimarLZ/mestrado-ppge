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

# SQL para buscar dados de matrículas e ingressantes por modalidade
sql = """
Select  
 cc.ano_censo, 
 m.nome as modalidade, 
 sum(cc.qt_mat) Matriculados, 
 sum(cc.qt_ing) Ingressantes 
from curso_censo cc  
join tp_modalidade_ensino m on m.codigo = cc.tp_modalidade_ensino 
where cc.ano_censo >= 2005
group by 1,2 
order by 1,2
"""

# Carregar dados
df = carregar_dataframe(sql)

# Gerar tabela HTML
column_widths = [100, 150, 120, 120]
column_names = ['Ano', 'Modalidade', 'Matriculados', 'Ingressantes']
column_alignments = ['center', 'left', 'right', 'right']
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

# Salvar tabela HTML
with open('docs/tabelas/matriculas_ingressantes_por_modalidade.html', 'w', encoding='utf-8') as f:
    f.write(html_table)

# Gráfico Plotly interativo - Matrículas
fig_mat = px.line(
    df, 
    x='ano_censo', 
    y='Matriculados', 
    color='modalidade',
    title='Evolução de Matrículas por Modalidade de Ensino',
    labels={'ano_censo': 'Ano', 'Matriculados': 'Número de Matriculados', 'modalidade': 'Modalidade'},
    markers=True
)

fig_mat.update_layout(
    xaxis_title='Ano',
    yaxis_title='Número de Matriculados',
    legend_title='Modalidade',
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

# Salvar gráfico Plotly de matrículas
fig_mat.write_html('docs/graficos/matriculas_por_modalidade.html')

# Gráfico Plotly interativo - Matrículas e Ingressantes (4 séries)
fig_combined = go.Figure()

# Adicionar séries de matrículas
for modalidade in df['modalidade'].unique():
    df_modal = df[df['modalidade'] == modalidade]
    fig_combined.add_trace(go.Scatter(
        x=df_modal['ano_censo'],
        y=df_modal['Matriculados'],
        mode='lines+markers',
        name=f'Matriculados - {modalidade}',
        line=dict(dash='solid')
    ))

# Adicionar séries de ingressantes
for modalidade in df['modalidade'].unique():
    df_modal = df[df['modalidade'] == modalidade]
    fig_combined.add_trace(go.Scatter(
        x=df_modal['ano_censo'],
        y=df_modal['Ingressantes'],
        mode='lines+markers',
        name=f'Ingressantes - {modalidade}',
        line=dict(dash='dash')
    ))

fig_combined.update_layout(
    title='Evolução de Matrículas e Ingressantes por Modalidade de Ensino',
    xaxis_title='Ano',
    yaxis_title='Número de Estudantes',
    legend_title='Série',
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

# Salvar gráfico Plotly combinado
fig_combined.write_html('docs/graficos/matriculas_ingressantes_por_modalidade.html')

# Gráfico Seaborn estático - Matrículas
plt.figure(figsize=(12, 8))
sns.lineplot(data=df, x='ano_censo', y='Matriculados', hue='modalidade', marker='o')
plt.title('Evolução de Matrículas por Modalidade de Ensino', fontsize=16)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Número de Matriculados', fontsize=12)
plt.legend(title='Modalidade')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('docs/graficos/matriculas_por_modalidade.png', dpi=300, bbox_inches='tight')
plt.close()

# Gráfico Seaborn estático - Matrículas e Ingressantes
# Preparar dados para o gráfico combinado
df_long = pd.melt(
    df, 
    id_vars=['ano_censo', 'modalidade'], 
    value_vars=['Matriculados', 'Ingressantes'],
    var_name='Tipo', 
    value_name='Quantidade'
)

# Criar coluna combinada para diferenciação
df_long['Serie'] = df_long['Tipo'] + ' - ' + df_long['modalidade']

plt.figure(figsize=(14, 8))
sns.lineplot(
    data=df_long, 
    x='ano_censo', 
    y='Quantidade', 
    hue='Serie',
    style='Tipo',
    markers=True,
    markersize=8
)
plt.title('Evolução de Matrículas e Ingressantes por Modalidade de Ensino', fontsize=16)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Número de Estudantes', fontsize=12)
plt.legend(title='Série', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('docs/graficos/matriculas_ingressantes_por_modalidade.png', dpi=300, bbox_inches='tight')
plt.close()

print("Relatório de Matrículas e Ingressantes por Modalidade gerado com sucesso!")
print("Arquivos salvos:")
print("- docs/tabelas/matriculas_ingressantes_por_modalidade.html")
print("- docs/graficos/matriculas_por_modalidade.html")
print("- docs/graficos/matriculas_ingressantes_por_modalidade.html")
print("- docs/graficos/matriculas_por_modalidade.png")
print("- docs/graficos/matriculas_ingressantes_por_modalidade.png")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rotina para gerar relatório de Matrículas por Modalidade e Grande Categoria

Este script gera:
1. Tabela HTML com dados de matrículas por ano, modalidade e grande categoria
2. Gráfico interativo Plotly
3. Gráfico estático PNG com Seaborn

Autor: Sistema de Relatórios INEP
Data: 2024
"""

import os
import sys

# Adicionar o diretório raiz do projeto ao path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from bdados.ler_bdados_to_df import carregar_dataframe

# Configuração do matplotlib para salvar em alta qualidade
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10

# Query SQL para matrículas por modalidade e grande categoria
query = """
SELECT
    c.ano_censo AS ano,
    CASE
        WHEN c.categoria IN (1, 2, 3) THEN 'Pública'
        WHEN c.categoria IN (4, 6) THEN 'Privada com fins lucrativos'
        ELSE 'Privada sem fins lucrativos'
    END AS grande_categoria,
    m.nome AS modalidade,
    SUM(c.qt_mat) AS Matriculas
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
df = carregar_dataframe(query)

# Criar diretórios se não existirem
os.makedirs('docs/tabelas', exist_ok=True)
os.makedirs('docs/graficos', exist_ok=True)

# Gerar tabela HTML
html_table = df.to_html(index=False, classes='table table-striped', table_id='tabela-matriculas')
html_table = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Matrículas por Modalidade e Grande Categoria</title>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .table {{ border-collapse: collapse; width: 100%; }}
        .table th, .table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        .table th {{ background-color: #f2f2f2; }}
        .table-striped tbody tr:nth-child(odd) {{ background-color: #f9f9f9; }}
    </style>
</head>
<body>
    <h1>Matrículas por Modalidade e Grande Categoria</h1>
    {html_table}
</body>
</html>
"""

# Salvar tabela HTML
with open('docs/tabelas/matriculas_por_modalidade_grande_categoria.html', 'w', encoding='utf-8') as f:
    f.write(html_table)

# Definir cores personalizadas para as grandes categorias
color_map = {
    'Pública': '#2E8B57',  # Verde
    'Privada com fins lucrativos': '#DC143C',  # Vermelho
    'Privada sem fins lucrativos': '#4169E1'  # Azul
}

# Criar coluna combinada para cor baseada na grande categoria
df['cor_categoria'] = df['grande_categoria'].map(color_map)

# Gráfico Plotly interativo - Matrículas por Modalidade e Grande Categoria
fig = px.line(
    df, 
    x='ano', 
    y='Matriculas', 
    color='grande_categoria',
    line_dash='modalidade',
    title='Evolução de Matrículas por Modalidade e Grande Categoria',
    markers=True,
    color_discrete_map=color_map
)

# Configurar eixo X para mostrar todos os anos como inteiros
anos = list(range(2005, 2024))
fig.update_xaxes(
    tickmode='array',
    tickvals=anos,
    ticktext=[str(ano) for ano in anos],
    range=[2004.5, 2023.5]
)

# Configurar legenda horizontal na parte inferior
fig.update_layout(
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,
        xanchor="center",
        x=0.5
    ),
    margin=dict(b=100)  # Aumentar margem inferior para acomodar a legenda
)

# Salvar gráfico Plotly como HTML
fig.write_html('docs/graficos/matriculas_por_modalidade_grande_categoria.html')

# Gráfico Seaborn estático - Matrículas por Modalidade e Grande Categoria
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
    y='Matriculas', 
    hue='Grande Categoria',
    style='Modalidade',
    markers=True,
    linewidth=2.5,
    palette=color_palette
)

# Configurar eixo X para mostrar todos os anos
plt.xticks(range(2005, 2024), rotation=45)
plt.xlabel('Ano')
plt.ylabel('Número de Matrículas')
plt.title('Evolução de Matrículas por Modalidade e Grande Categoria', fontsize=14, fontweight='bold')

# Configurar legenda horizontal na parte inferior
plt.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=3)

# Ajustar layout
plt.tight_layout()

# Salvar gráfico como PNG
plt.savefig('docs/graficos/matriculas_por_modalidade_grande_categoria.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print("Relatório de Matrículas por Modalidade e Grande Categoria gerado com sucesso!")
print("Arquivos salvos:")
print("- docs/tabelas/matriculas_por_modalidade_grande_categoria.html")
print("- docs/graficos/matriculas_por_modalidade_grande_categoria.html")
print("- docs/graficos/matriculas_por_modalidade_grande_categoria.png")
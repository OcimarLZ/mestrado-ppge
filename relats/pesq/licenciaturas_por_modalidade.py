import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt                 # novo
import seaborn as sns                           # novo
import sys
import os

# Permite importar utilitários do projeto (mesma lógica do script-base)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# SQL solicitado
SQL = """
SELECT
    c.ano_censo              AS ano,
    me.nome                  AS modalidade,
    SUM(c.qt_mat)            AS matriculas,
    SUM(c.qt_ing)            AS ingressos
FROM curso_censo c
JOIN tp_modalidade_ensino me ON me.codigo = c.tp_modalidade_ensino
WHERE c.ano_censo > 2004
  AND c.tp_grau_academico = 2
GROUP BY c.ano_censo, me.nome
ORDER BY c.ano_censo, me.nome
"""

# Carrega dados num DataFrame
raw_df = carregar_dataframe(SQL)

# Configurações de estilo Seaborn (opcional)
sns.set_style("whitegrid")                      # novo
sns.set_palette("husl")                         # novo

# -------------------------
# 1. Tabela HTML resumida
# -------------------------
# Exibe matrículas por ano/modalidade
pivot_mat = raw_df.pivot_table(index='ano', columns='modalidade', values='matriculas', fill_value=0).astype(int)
# Opcional: salvar tabela
colunas_html = ["Ano"] + list(pivot_mat.columns)
col_widths   = ["70px"] + ["140px"] * pivot_mat.shape[1]
alinhamentos = ["left"] + ["right"] * pivot_mat.shape[1]

cabecalho_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
linha_style     = "font-size: 10px; font-family: Tahoma, sans-serif;"

html_table = dataframe_to_html(
    pivot_mat.reset_index(),
    col_widths,            # column_widths
    colunas_html,          # column_names
    alinhamentos,          # column_alignments
    cabecalho_style,       # header_style
    linha_style            # row_style
)
TABELA_OUT = 'docs/tabelas/licenciaturas_por_modalidade.html'
os.makedirs(os.path.dirname(TABELA_OUT), exist_ok=True)
with open(TABELA_OUT, 'w', encoding='utf-8') as fh:
    fh.write(html_table)
print('Tabela HTML salva em', TABELA_OUT)

# --------------------------------------
# 2. Gráfico interativo (Plotly Express)
# --------------------------------------
# Usaremos matrículas; basta mudar a coluna para ingressos se desejar
fig_df = raw_df.rename(columns={'ano': 'Ano',
                                'modalidade': 'Modalidade',
                                'matriculas': 'Matrículas'})
fig = px.line(fig_df,
              x='Ano', y='Matrículas', color='Modalidade',
              markers=True,
              template='plotly_white',
              title='Licenciaturas – Matrículas por Modalidade (a partir de 2005)')
fig.update_layout(xaxis_title='Ano do Censo',
                  yaxis_title='Número de Matrículas',
                  legend_title='Modalidade')

# Salva figura como HTML autônomo (interativo)
GRAF_OUT = 'docs/graficos/licenciaturas_por_modalidade.html'
fig.write_html(GRAF_OUT)
print('Gráfico interativo salvo em', GRAF_OUT)

# --- Novo gráfico: Matrículas e Ingressos (4 séries) ---
df_long = raw_df.melt(id_vars=['ano', 'modalidade'],
                      value_vars=['matriculas', 'ingressos'],
                      var_name='Tipo', value_name='Quantidade')
df_long = df_long.rename(columns={'ano': 'Ano', 'modalidade': 'Modalidade'})

fig_all = px.line(df_long,
                  x='Ano', y='Quantidade',
                  color='Modalidade',
                  line_dash='Tipo',
                  markers=True,
                  template='plotly_white',
                  title='Licenciaturas – Matrículas e Ingressos por Modalidade')
fig_all.update_layout(xaxis_title='Ano do Censo',
                      yaxis_title='Quantidade',
                      legend_title='Modalidade / Tipo')

GRAF_OUT_ALL = 'docs/graficos/licenciaturas_mat_ing_por_modalidade.html'
fig_all.write_html(GRAF_OUT_ALL)
print('Gráfico (matrículas e ingressos) salvo em', GRAF_OUT_ALL)

# --------------------------------------
# 4. Gráfico estático (Seaborn/Matplotlib) – matrículas + ingressos (4 séries)
# --------------------------------------
fig3, ax3 = plt.subplots(figsize=(14, 8), facecolor='white')
ax3.set_facecolor('white')

# Usa o dataframe “longo” já criado (df_long)
sns.lineplot(data=df_long,
             x='Ano', y='Quantidade',
             hue='Modalidade',      # cor por modalidade
             style='Tipo',          # estilo (tracejado) por tipo
             markers=True, dashes=True,
             ax=ax3)

ax3.set_xlabel('Ano do Censo', fontsize=12)
ax3.set_ylabel('Quantidade', fontsize=12)
ax3.set_title('Licenciaturas – Matrículas e Ingressos por Modalidade (Seaborn)', fontsize=14)
ax3.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25),
           ncol=4, fontsize='medium', frameon=False,
           title='Modalidade / Tipo')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

GRAF_OUT_PNG_ALL = 'docs/graficos/licenciaturas_mat_ing_por_modalidade.png'
os.makedirs(os.path.dirname(GRAF_OUT_PNG_ALL), exist_ok=True)
plt.savefig(GRAF_OUT_PNG_ALL, bbox_inches='tight', dpi=300)
print('Gráfico Seaborn (matrículas + ingressos) salvo em', GRAF_OUT_PNG_ALL)
plt.close()
# Descomente para abrir janela interativa localmente
# fig.show()
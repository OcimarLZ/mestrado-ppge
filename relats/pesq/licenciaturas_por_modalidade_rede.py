import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import sys, os

# Permite importar utilitários do projeto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# ---------------------------------------------------------------------------
# SQL com agrupamento por tipo de rede (tp_rede)                               
# ---------------------------------------------------------------------------
SQL = """
SELECT
    c.ano_censo              AS ano,
    tr.nome                  AS rede,      -- 2º campo solicitado
    me.nome                  AS modalidade,
    SUM(c.qt_mat)            AS matriculas,
    SUM(c.qt_ing)            AS ingressos
FROM curso_censo c
JOIN tp_modalidade_ensino  me ON me.codigo = c.tp_modalidade_ensino
JOIN tp_rede              tr ON tr.codigo  = c.tp_rede          -- novo join
WHERE c.ano_censo > 2004
  AND c.tp_grau_academico = 2
GROUP BY c.ano_censo, tr.nome, me.nome
ORDER BY c.ano_censo, tr.nome, me.nome
"""

# Carrega dados
raw_df = carregar_dataframe(SQL)

# Estilo Seaborn
sns.set_style("whitegrid")

# ---------------------------------------------------------------------------
# 1. Tabela HTML resumida                                                     
# ---------------------------------------------------------------------------
# Pivot: linhas = ano / rede  ·  colunas = modalidade
pivot = raw_df.pivot_table(index=['ano', 'rede'],
                           columns='modalidade',
                           values='matriculas',
                           fill_value=0).astype(int)

# Prepara metadados p/ HTML
modal_cols      = list(pivot.columns)
column_names    = ["Ano", "Rede"] + modal_cols
column_widths   = ["60px", "120px"] + ["120px"] * len(modal_cols)
column_align    = ["left", "left"] + ["right"] * len(modal_cols)
header_style    = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
row_style       = "font-size: 10px;  font-family: Tahoma, sans-serif;"

html_table = dataframe_to_html(
    pivot.reset_index(),
    column_widths,
    column_names,
    column_align,
    header_style,
    row_style
)
TAB_OUT = 'docs/tabelas/licenciaturas_por_modalidade_rede.html'
os.makedirs(os.path.dirname(TAB_OUT), exist_ok=True)
with open(TAB_OUT, 'w', encoding='utf-8') as fh:
    fh.write(html_table)
print('Tabela HTML salva em', TAB_OUT)

# ---------------------------------------------------------------------------
# 2. Gráfico interativo (Plotly) – MATRÍCULAS                                   
# ---------------------------------------------------------------------------
fig_df = raw_df.rename(columns={'ano': 'Ano', 'rede': 'Rede', 'modalidade': 'Modalidade', 'matriculas': 'Matrículas'})
fig = px.line(fig_df,
              x='Ano', y='Matrículas',
              color='Modalidade',           # cor = modalidade
              line_dash='Rede',             # estilo = rede
              markers=True,
              template='plotly_white',
              title='Licenciaturas – Matrículas por Modalidade e Tipo de Rede')
fig.update_layout(xaxis_title='Ano do Censo',
                  yaxis_title='Número de Matrículas',
                  legend_title='Modalidade / Rede')
GRAF_OUT = 'docs/graficos/licenciaturas_por_modalidade_rede.html'
fig.write_html(GRAF_OUT)
print('Gráfico interativo salvo em', GRAF_OUT)

# ---------------------------------------------------------------------------
# 3. Gráfico interativo – MATRÍCULAS + INGRESSOS (4 séries × 2 redes)          
# ---------------------------------------------------------------------------
df_long = raw_df.melt(id_vars=['ano', 'rede', 'modalidade'],
                      value_vars=['matriculas', 'ingressos'],
                      var_name='Tipo', value_name='Quantidade')
fig_all = px.line(df_long.rename(columns={'ano': 'Ano', 'rede': 'Rede', 'modalidade': 'Modalidade'}),
                  x='Ano', y='Quantidade',
                  color='Modalidade',
                  line_dash='Rede',
                  facet_row='Tipo',         # separa matrículas / ingressos
                  markers=True,
                  template='plotly_white',
                  title='Licenciaturas – Matrículas e Ingressos por Modalidade e Tipo de Rede')
fig_all.update_layout(yaxis_title='Quantidade', legend_title='Modalidade / Rede')
GRAF_OUT_ALL = 'docs/graficos/licenciaturas_mat_ing_por_modalidade_rede.html'
fig_all.write_html(GRAF_OUT_ALL)
print('Gráfico (matrículas + ingressos) salvo em', GRAF_OUT_ALL)

# ---------------------------------------------------------------------------
# 4. Gráfico estático (Seaborn) – MATRÍCULAS + INGRESSOS                       
# ---------------------------------------------------------------------------
# Renomeia colunas para facilitar rótulos legíveis no gráfico
df_long_plot = df_long.rename(columns={
    'ano': 'Ano',
    'rede': 'Rede',
    'modalidade': 'Modalidade'
})

plt.figure(figsize=(14, 8))
ax = sns.lineplot(
    data=df_long_plot,          # <- usa o dataframe renomeado
    x='Ano', y='Quantidade',
    hue='Modalidade',
    style='Rede',
    markers=True, dashes=True
)
ax.set_xlabel('Ano do Censo')
ax.set_ylabel('Quantidade')
ax.set_title('Licenciaturas – Matrículas e Ingressos por Modalidade e Rede (Seaborn)')
ax.legend(title='Modalidade / Rede', bbox_to_anchor=(0.5, -0.2), loc='upper center', ncol=3, frameon=False)
plt.tight_layout()
PNG_OUT = 'docs/graficos/licenciaturas_mat_ing_por_modalidade_rede.png'
os.makedirs(os.path.dirname(PNG_OUT), exist_ok=True)
plt.savefig(PNG_OUT, dpi=300, bbox_inches='tight')
plt.close()
print('Gráfico Seaborn salvo em', PNG_OUT)

if __name__ == '__main__':
    print('Rotina concluída.')
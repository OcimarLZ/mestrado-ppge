import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
select
    c.ano_censo as ano,
    g.nome as grau_academico,
    count(DISTINCT c.ies) QtdeIes  
from curso_censo c
join tp_grau_academico g on g.codigo = c.tp_grau_academico 
group by c.ano_censo, g.nome
order by c.ano_censo, g.nome
"""
df = carregar_dataframe(sql)

# Pivotando para ter colunas por grau acadêmico
graus = df['grau_academico'].unique()
pivot_df = df.pivot_table(index='ano', columns='grau_academico', values='QtdeIes', fill_value=0).astype(int)
pivot_df.reset_index(inplace=True)

# Redefinindo a lista de tamanhos para o formato HTML
colunas_html = ['Ano'] + list(pivot_df.columns[1:])
tam_colunas = ['60px'] + ['150px'] * (len(pivot_df.columns) - 1)
alinhamentos = ['left'] + ['right'] * (len(pivot_df.columns) - 1)
cabecalho_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
linha_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'ies_ativas_por_grau_academico'

# HTML para o título da tabela
html_title = f"""
<table style=\"width: 100%; border-collapse: collapse;\">
    <tr style=\"background-color: #2E7D32;\">
        <th colspan=\"{len(pivot_df.columns)}\" style=\"font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;\">
            Quantidade de IES Ativas por Ano e Grau Acadêmico
        </th>
    </tr>
</table>
"""

# Convertendo o DataFrame para texto HTML
html_text = dataframe_to_html(pivot_df, tam_colunas, colunas_html, alinhamentos, cabecalho_style, linha_style)
html_text = html_title + html_text
html_text = html_text.replace('<thead>', '<thead style=\"background-color: #4CAF50;\">')

# Salvando a tabela HTML
arq_output = 'docs/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w', encoding='utf-8') as file:
    file.write(html_text)
print('Tabela HTML criada com sucesso.')

# Gráfico de linhas (um para cada grau)
fig, ax = plt.subplots(figsize=(14, 8), facecolor='white')
ax.set_facecolor('white')

anos = pivot_df['ano'].astype(str)
graus = pivot_df.columns[1:]

# Cores para os graus (estilo Excel)
colors = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5', '#70AD47', '#C00000', '#00B0F0']

for idx, grau in enumerate(graus):
    ax.plot(anos, pivot_df[grau], marker='o', label=grau, color=colors[idx % len(colors)], linewidth=2)
    for i, v in enumerate(pivot_df[grau]):
        if v > 0:
            ax.annotate(f'{int(v)}', xy=(anos[i], v), xytext=(0, 8), textcoords="offset points", ha='center', va='bottom', fontsize=8)

ax.set_xlabel('Ano', fontsize=12)
ax.set_ylabel('Qtde de IES Ativas', fontsize=12)
ax.set_title('IES Ativas por Ano e Grau Acadêmico', color='#000000', fontsize=14)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=3, fontsize='medium', title='Grau Acadêmico', frameon=False)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Salvando o gráfico
arq_output = 'docs/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close() 
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
    m.nome as modalidade,
    count(DISTINCT c.ies) QtdeIes  
from curso_censo c
join tp_grau_academico g on g.codigo = c.tp_grau_academico 
join tp_modalidade_ensino m on m.codigo = c.tp_modalidade_ensino 
where c.tp_grau_academico = 2
group by c.ano_censo, g.nome, m.nome
order by c.ano_censo, g.nome, m.nome
"""
df = carregar_dataframe(sql)

# Filtra apenas licenciatura (grau_academico = 2)
df = df[df['grau_academico'].notnull() & df['modalidade'].notnull()]

# Pivotando para ter colunas por modalidade
tabela = df.pivot_table(index='ano', columns='modalidade', values='QtdeIes', fill_value=0).astype(int)
tabela.reset_index(inplace=True)

# Redefinindo a lista de tamanhos para o formato HTML
colunas_html = ['Ano'] + list(tabela.columns[1:])
tam_colunas = ['60px'] + ['150px'] * (len(tabela.columns) - 1)
alinhamentos = ['left'] + ['right'] * (len(tabela.columns) - 1)
cabecalho_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
linha_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'licenciaturas_por_modalidade_ensino'

# HTML para o título da tabela
html_title = f"""
<table style=\"width: 100%; border-collapse: collapse;\">
    <tr style=\"background-color: #2E7D32;\">
        <th colspan=\"{len(tabela.columns)}\" style=\"font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;\">
            Licenciaturas por Modalidade de Ensino - Qtde de IES por Ano
        </th>
    </tr>
</table>
"""

# Convertendo o DataFrame para texto HTML
html_text = dataframe_to_html(tabela, tam_colunas, colunas_html, alinhamentos, cabecalho_style, linha_style)
html_text = html_title + html_text
html_text = html_text.replace('<thead>', '<thead style=\"background-color: #4CAF50;\">')

# Salvando a tabela HTML
arq_output = 'docs/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w', encoding='utf-8') as file:
    file.write(html_text)
print('Tabela HTML criada com sucesso.')

# Gráfico de linhas (um para cada modalidade)
fig, ax = plt.subplots(figsize=(14, 8), facecolor='white')
ax.set_facecolor('white')

anos = tabela['ano'].astype(str)
modalidades = tabela.columns[1:]

# Cores para as modalidades (estilo Excel)
colors = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5', '#70AD47', '#C00000', '#00B0F0']

for idx, modalidade in enumerate(modalidades):
    ax.plot(anos, tabela[modalidade], marker='o', label=modalidade, color=colors[idx % len(colors)], linewidth=2)
    for i, v in enumerate(tabela[modalidade]):
        if v > 0:
            ax.annotate(f'{int(v)}', xy=(anos[i], v), xytext=(0, 8), textcoords="offset points", ha='center', va='bottom', fontsize=8)

ax.set_xlabel('Ano', fontsize=12)
ax.set_ylabel('Qtde de IES', fontsize=12)
ax.set_title('Licenciaturas por Modalidade de Ensino - Qtde de IES por Ano', color='#000000', fontsize=14)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=3, fontsize='medium', title='Modalidade', frameon=False)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Salvando o gráfico
arq_output = 'docs/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close() 
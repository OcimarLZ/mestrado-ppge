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
i.ano_censo  as ano,
count(DISTINCT i.ies) QtdeIes  
from ies_censo i
group by i.ano_censo
"""
df = carregar_dataframe(sql)

# Ajuste para tabela HTML
colunas_html = ['Ano', 'Qtde de IES Ativas']
tam_colunas = ['60px', '180px']
alinhamentos = ['left', 'right']
cabecalho_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
linha_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'ies'

# HTML para o título da tabela
html_title = f"""
<table style=\"width: 100%; border-collapse: collapse;\">
    <tr style=\"background-color: #2E7D32;\">
        <th colspan=\"2\" style=\"font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;\">
            Quantidade de IES Ativas por Ano
        </th>
    </tr>
</table>
"""

# Convertendo o DataFrame para texto HTML
html_text = dataframe_to_html(df, tam_colunas, colunas_html, alinhamentos, cabecalho_style, linha_style)
html_text = html_title + html_text
html_text = html_text.replace('<thead>', '<thead style=\"background-color: #4CAF50;\">')

# Salvando a tabela HTML
arq_output = 'docs/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w', encoding='utf-8') as file:
    file.write(html_text)
print('Tabela HTML criada com sucesso.')

# Gráfico de linhas
fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')
ax.set_facecolor('white')

anos = df['ano'].astype(str)
qtde_ies = df['QtdeIes']

ax.plot(anos, qtde_ies, marker='o', color='#4472C4', linewidth=2, label='IES Ativas')

for i, v in enumerate(qtde_ies):
    ax.annotate(f'{int(v)}', xy=(anos[i], v), xytext=(0, 8), textcoords="offset points", ha='center', va='bottom', fontsize=9)

ax.set_xlabel('Ano', fontsize=12)
ax.set_ylabel('Qtde de IES Ativas', fontsize=12)
ax.legend(loc='best', fontsize='medium', frameon=False)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Salvando o gráfico
arq_output = 'docs/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close() 
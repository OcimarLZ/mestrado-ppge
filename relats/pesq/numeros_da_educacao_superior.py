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
    c.ano_censo,
    sum(c.qt_vg_total) as vagas,
    sum(c.qt_inscrito_total) as inscritos,
    sum(c.qt_ing) as ingressantes,
    sum(c.qt_mat) as matriculados,
    sum(c.qt_conc) as concluintes,
    sum(c.qt_sit_desvinculado + c.qt_sit_transferido) as evadidos,
    sum(c.qt_sit_trancada) as trancados
from curso_censo c
group by 1
order by 1
"""
df = carregar_dataframe(sql)

# Ajuste para tabela HTML
colunas_html = ['Ano', 'Vagas', 'Inscritos', 'Ingressantes', 'Matriculados', 'Concluintes', 'Evadidos', 'Trancados']
tam_colunas = ['60px'] + ['120px'] * (len(colunas_html) - 1)
alinhamentos = ['left'] + ['right'] * (len(colunas_html) - 1)
cabecalho_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
linha_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'numeros_da_educacao_superior'

# HTML para o título da tabela
html_title = f"""
<table style=\"width: 100%; border-collapse: collapse;\">
    <tr style=\"background-color: #2E7D32;\">
        <th colspan=\"{len(colunas_html)}\" style=\"font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;\">
            Números da Educação Superior por Ano
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

# Gráfico de linhas (um para cada métrica)
fig, ax = plt.subplots(figsize=(14, 8), facecolor='white')
ax.set_facecolor('white')

anos = df['ano_censo'].astype(str)
metricas = colunas_html[1:]
colors = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5', '#70AD47', '#C00000']

for idx, metrica in enumerate(metricas):
    ax.plot(anos, df[metrica.lower()], marker='o', label=metrica, color=colors[idx % len(colors)], linewidth=2)
    for i, v in enumerate(df[metrica.lower()]):
        if v > 0:
            ax.annotate(f'{int(v)}', xy=(anos[i], v), xytext=(0, 8), textcoords="offset points", ha='center', va='bottom', fontsize=8)

ax.set_xlabel('Ano', fontsize=12)
ax.set_ylabel('Quantidade', fontsize=12)
ax.set_title('Números da Educação Superior por Ano', color='#000000', fontsize=14)
ax.legend(loc='upper left', fontsize='medium', title='Indicador', frameon=False)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Salvando o gráfico
arq_output = 'docs/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close() 
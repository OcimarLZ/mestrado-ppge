import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL (filtro a partir de 2005)
sql = """
select
    c.ano_censo as ano,
    case 
        when c.categoria in (1,2,3) then 'Públicas'
        when c.categoria in (4,7) then 'Privadas com Fins Lucrativos'
        else 'Privadas Sem Fins Lucrativos'
    end as rede, 
    count(distinct c.ies) QtdeIes  
from curso_censo c
where c.ano_censo >= 2005
group by c.ano_censo, rede
order by c.ano_censo, rede
"""
df = carregar_dataframe(sql)

# Pivotando para ter colunas por grande categoria
pivot_df = df.pivot_table(index='ano', columns='rede', values='QtdeIes', fill_value=0).astype(int)

# Calculando o total por ano
pivot_df['Total'] = pivot_df.sum(axis=1)

pivot_df.reset_index(inplace=True)

# Redefinindo a lista de tamanhos para o formato HTML (incluindo coluna Total)
colunas_html = ['Ano'] + list(pivot_df.columns[1:])
tam_colunas = ['60px'] + ['180px'] * (len(pivot_df.columns) - 1)
alinhamentos = ['left'] + ['right'] * (len(pivot_df.columns) - 1)
cabecalho_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
linha_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'ies_ativas_por_grande_categoria'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(pivot_df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            IES Ativas por Ano e Grande Categoria Administrativa (a partir de 2005)
        </th>
    </tr>
</table>
"""

# Convertendo o DataFrame para texto HTML
html_text = dataframe_to_html(pivot_df, tam_colunas, colunas_html, alinhamentos, cabecalho_style, linha_style)
html_text = html_title + html_text
html_text = html_text.replace('<thead>', '<thead style="background-color: #4CAF50;">')

# Salvando a tabela HTML
arq_output = 'docs/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w', encoding='utf-8') as file:
    file.write(html_text)
print('Tabela HTML criada com sucesso.')

# Gráfico de linhas (um para cada grande categoria)
fig, ax = plt.subplots(figsize=(14, 8), facecolor='white')
ax.set_facecolor('white')

anos = pivot_df['ano'].astype(str)
categorias = [col for col in pivot_df.columns[1:] if col != 'Total']  # Excluindo Total das categorias

# Mapeamento específico de cores por categoria (Públicas em verde)
cores_categorias = {
    'Públicas': '#008000',  # Verde (mudança de cinza para verde)
    'Privadas com Fins Lucrativos': '#ED7D31',  # Laranja
    'Privadas Sem Fins Lucrativos': '#A5A5A5'  # Cinza
}

# Plotando linhas das categorias
for idx, cat in enumerate(categorias):
    cor = cores_categorias.get(cat, '#4472C4')  # Cor padrão se não encontrar
    ax.plot(anos, pivot_df[cat], marker='o', label=cat, color=cor, linewidth=2)
    for i, v in enumerate(pivot_df[cat]):
        if v > 0:
            ax.annotate(f'{int(v)}', xy=(anos[i], v), xytext=(0, 8), textcoords="offset points", ha='center', va='bottom', fontsize=8)

# Plotando linha do total com destaque em preto
qtde_total = pivot_df['Total']
ax.plot(anos, qtde_total, marker='s', color='black', linewidth=3, 
        label='Total Geral', markersize=8)

# Adicionando anotações para o total (sempre visível)
for i, v in enumerate(qtde_total):
    ax.annotate(f'{int(v)}', xy=(anos[i], v), xytext=(0, 15), 
                textcoords="offset points", ha='center', va='bottom', 
                fontsize=9, fontweight='bold', color='black')

ax.set_xlabel('Ano', fontsize=12)
ax.set_ylabel('Qtde de IES Ativas', fontsize=12)
# Título do gráfico removido
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=4, fontsize='medium', title='Grande Categoria', frameon=False)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Salvando o gráfico
arq_output = 'docs/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Configurando o estilo do Seaborn
sns.set_style("whitegrid")
sns.set_palette("husl")

# Monta o SQL (novo SQL fornecido)
sql = """
select
    i.ano_censo as ano,
    case 
        when i.categoria in (1,2,3) then 'Públicas'
        when i.categoria in (4,7) then 'Privadas com Fins Lucrativo'
        else 'Privadas Sem Fins Lucrativo'
    end as rede, 
    count(distinct i.ies) QtdeIes  
from ies_censo i
where i.ano_censo >= 2005
group by i.ano_censo, rede
order by i.ano_censo, rede
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
arq_nome = 'ies_por_grande_categoria'

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

# ==================== GRÁFICO COM SEABORN ====================

# Configurando o tema e paleta de cores
plt.style.use('default')  # Reset para usar configurações do Seaborn
sns.set_theme(style="whitegrid", palette="deep")

# Criando o gráfico com Seaborn - PROPORÇÃO 16:7
fig, ax = plt.subplots(figsize=(16, 7))

# Preparando dados
anos = pivot_df['ano'].astype(int)  # Convertendo para inteiros
categorias = [col for col in pivot_df.columns[1:] if col != 'Total']  # Excluindo Total das categorias

# Mapeamento específico de cores por categoria
cores_categorias = {
    'Públicas': '#008000',  # Verde
    'Privadas com Fins Lucrativo': '#ED7D31',  # Laranja
    'Privadas Sem Fins Lucrativo': '#0000FF'  # Azul
}

# Mapeamento de rótulos (sem quebra de linha para legenda horizontal)
rotulos_legenda = {
    'Públicas': 'Públicas',
    'Privadas com Fins Lucrativo': 'Privadas com Fins Lucrativo',
    'Privadas Sem Fins Lucrativo': 'Privadas Sem Fins Lucrativo'
}

# Plotando linhas das categorias com Seaborn
for idx, cat in enumerate(categorias):
    cor = cores_categorias.get(cat, '#4472C4')
    rotulo = rotulos_legenda.get(cat, cat)
    
    # Usando sns.lineplot para cada categoria
    sns.lineplot(x=anos, y=pivot_df[cat], marker='o', color=cor, 
                linewidth=3, markersize=8, label=rotulo, alpha=0.9)
    
    # Adicionando anotações nos pontos
    for i, v in enumerate(pivot_df[cat]):
        if v > 0:
            ax.annotate(f'{int(v)}', xy=(anos.iloc[i], v), xytext=(0, 8), 
                       textcoords="offset points", ha='center', va='bottom', 
                       fontsize=9, alpha=0.8)

# Plotando linha do total com destaque
sns.lineplot(x=anos, y=pivot_df['Total'], marker='s', color='black', 
            linewidth=4, markersize=10, label='Total Geral', alpha=1.0)

# Adicionando anotações para o total (sempre visível)
for i, v in enumerate(pivot_df['Total']):
    ax.annotate(f'{int(v)}', xy=(anos.iloc[i], v), xytext=(0, 15), 
                textcoords="offset points", ha='center', va='bottom', 
                fontsize=10, fontweight='bold', color='black')

# Customizações do gráfico
ax.set_xlabel('Ano', fontsize=14, fontweight='bold')
ax.set_ylabel('Qtde de IES Ativas', fontsize=14, fontweight='bold')

# Formatando os eixos
anos_unicos = sorted(pivot_df['ano'].unique())
ax.set_xticks(anos_unicos)
ax.set_xticklabels([str(int(ano)) for ano in anos_unicos], fontsize=12, rotation=45)
ax.tick_params(axis='y', labelsize=12)

# Formatando números no eixo Y
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

# Legenda na parte de baixo, horizontal
handles, labels = ax.get_legend_handles_labels()
legend = ax.legend(handles, labels, 
                  loc='upper center',           # Posição central superior
                  bbox_to_anchor=(0.5, -0.15), # Ajustado para proporção 16:7
                  ncol=4,                       # 4 colunas (3 categorias + total)
                  fontsize=12, 
                  frameon=True, 
                  fancybox=True, 
                  shadow=True,
                  facecolor='white', 
                  edgecolor='gray', 
                  framealpha=0.95,
                  title='Grande Categoria', 
                  title_fontsize=13,
                  columnspacing=2.0)            # Espaçamento entre colunas
legend.get_title().set_fontweight('bold')

# Configurando grade
ax.grid(True, linestyle='--', alpha=0.7, linewidth=0.8)
ax.set_axisbelow(True)

# Ajustando o layout para acomodar a legenda embaixo - AJUSTADO PARA 16:7
plt.tight_layout()
plt.subplots_adjust(bottom=0.25)  # Ajustado para proporção 16:7

# Adicionando uma anotação com informações adicionais
plt.figtext(0.02, 0.02, 
           'Fonte: INEP Censo da Educação Superior | Dados de 2005 a 2024 | Do Autor em relats/pesq/ies_por_grande_categoria.py',
           fontsize=10, style='italic', alpha=0.7)

# Salvando o gráfico
arq_output = 'docs/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight', dpi=300, facecolor='white', edgecolor='none')
plt.show()
plt.close()

print(f'Gráfico salvo como: {arq_output}')
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
i.ano_censo as ano,
ca.nome as categoria,
count(distinct i.ies) QtdeIes  
from ies_censo i
join tp_categoria_administrativa ca on ca.codigo = i.categoria
where i.ano_censo > 2004
group by 1,2
"""
df = carregar_dataframe(sql)

# Criando DataFrame pivot para melhor visualização
df_pivot = df.pivot(index='ano', columns='categoria', values='QtdeIes').fillna(0)

# Calculando o total por ano
df_pivot['Total'] = df_pivot.sum(axis=1)

# Resetando index para facilitar manipulação
df_pivot_reset = df_pivot.reset_index()

# Ajuste para tabela HTML
colunas_html = ['Ano'] + list(df_pivot.columns[:-1]) + ['Total']
tam_colunas = ['60px'] + ['120px'] * (len(df_pivot.columns) - 1) + ['100px']
alinhamentos = ['left'] + ['right'] * (len(df_pivot.columns) - 1) + ['right']
cabecalho_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
linha_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'ies_ativas_por_ano_categoria'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(colunas_html)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Quantidade de IES Ativas por Ano e Categoria Administrativa
        </th>
    </tr>
</table>
"""

# Convertendo o DataFrame para texto HTML
html_text = dataframe_to_html(df_pivot_reset, tam_colunas, colunas_html, alinhamentos, cabecalho_style, linha_style)
html_text = html_title + html_text
html_text = html_text.replace('<thead>', '<thead style="background-color: #4CAF50;">')

# Salvando a tabela HTML
arq_output = 'docs/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w', encoding='utf-8') as file:
    file.write(html_text)
print('Tabela HTML criada com sucesso.')

# Gráfico de linhas
fig, ax = plt.subplots(figsize=(16, 8), facecolor='white')
ax.set_facecolor('white')

anos = df_pivot_reset['ano'].astype(str)
anos_numericos = df_pivot_reset['ano'].values

# Mapeamento específico de cores por categoria (cor alterada para Especial)
cores_categorias = {
    'Especial': '#DA70D6',  # Orquídea (entre rosa e roxo) - era azul ciano
    'Privada - Particular em sentido estrito': '#FFD700',  # Amarelo
    'Privada com fins lucrativos': '#DC143C',  # Vermelho
    'Privada comunitária': '#000080',  # Azul marinho
    'Privada confessional': '#87CEEB',  # Azul celeste
    'Privada sem fins lucrativos': '#4169E1',  # Azul royal
    'Pública Estadual': '#FF8C00',  # Laranja
    'Pública Federal': '#008000',  # Verde
    'Pública Municipal': '#808080'  # Cinza
}

def obter_cor_categoria(categoria):
    return cores_categorias.get(categoria, '#808080')  # Cinza como padrão

# Função para verificar sobreposição de rótulos
def verificar_sobreposicao(posicoes_existentes, nova_posicao, tolerancia=15):
    for pos in posicoes_existentes:
        if abs(pos - nova_posicao) < tolerancia:
            return True
    return False

# Plotando linha para cada categoria
categorias = [col for col in df_pivot.columns if col != 'Total']
for i, categoria in enumerate(categorias):
    qtde_ies = df_pivot_reset[categoria]
    cor = obter_cor_categoria(categoria)
    
    # Substituindo zeros por NaN para quebrar a linha onde não há dados
    valores_plotagem = qtde_ies.replace(0, float('nan'))
    
    # Plotando com anos numéricos para manter ordem cronológica
    ax.plot(anos_numericos, valores_plotagem, marker='o', color=cor, 
            linewidth=2, label=categoria, alpha=0.8)
    
    # Adicionando anotações apenas para valores > 0
    for j, v in enumerate(qtde_ies):
        if v > 0:  # Só mostra se o valor for maior que 0
            # Verifica se há outras anotações próximas nesta posição x
            posicoes_y_existentes = []
            
            # Coleta posições Y de outras categorias no mesmo ano
            for k, outra_categoria in enumerate(categorias[:i]):  # Apenas categorias já processadas
                if df_pivot_reset[outra_categoria].iloc[j] > 0:
                    posicoes_y_existentes.append(df_pivot_reset[outra_categoria].iloc[j])
            
            # Verifica sobreposição e ajusta posição se necessário
            offset_y = 8
            if verificar_sobreposicao(posicoes_y_existentes, v):
                offset_y = -15  # Coloca abaixo se houver sobreposição
            
            ax.annotate(f'{int(v)}', xy=(anos_numericos[j], v), xytext=(0, offset_y), 
                        textcoords="offset points", ha='center', va='bottom' if offset_y > 0 else 'top', 
                        fontsize=7, color=cor, alpha=0.8)

# Plotando linha do total com destaque em preto
qtde_total = df_pivot_reset['Total']
ax.plot(anos_numericos, qtde_total, marker='s', color='black', linewidth=3, 
        label='Total Geral', markersize=8)

# Adicionando anotações para o total (sempre visível)
for i, v in enumerate(qtde_total):
    ax.annotate(f'{int(v)}', xy=(anos_numericos[i], v), xytext=(0, 15), 
                textcoords="offset points", ha='center', va='bottom', 
                fontsize=9, fontweight='bold', color='black')

# Configurando os ticks do eixo X para mostrar os anos como strings em ordem
ax.set_xticks(anos_numericos)
ax.set_xticklabels(anos, rotation=45)

ax.set_xlabel('Ano', fontsize=12)
ax.set_ylabel('Qtde de IES Ativas', fontsize=12)

# Legenda ao lado direito do gráfico, centralizada verticalmente
ax.legend(bbox_to_anchor=(1.05, 0.5), loc='center left', fontsize='small', 
          frameon=True, fancybox=True, shadow=True,
          facecolor='white', edgecolor='gray', framealpha=0.9)

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Salvando o gráfico
arq_output = 'docs/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight', dpi=300)
plt.show()
plt.close()
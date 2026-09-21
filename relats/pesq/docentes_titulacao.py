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
i.tp_rede,
sum(i.qt_doc_ex_dout) Doutores,
sum(i.qt_doc_ex_mest) Mestres,
sum(i.qt_doc_ex_esp) Especialistas,
sum(i.qt_doc_ex_grad + i.qt_doc_ex_sem_grad) Graduados,
sum(i.qt_tec_total) Técnicos
from ies_censo i
where i.ano_censo > 2005 and i.categoria in (1,2,3,5,7,8,9)
group by 1,2 
"""
df = carregar_dataframe(sql)

# Criando coluna de rede com nomes descritivos
df['rede'] = df['tp_rede'].map({1: 'Pública', 2: 'Privada'})

# Reorganizando o DataFrame para formato longo (melting)
df_melted = df.melt(id_vars=['ano', 'rede'], 
                    value_vars=['Doutores', 'Mestres', 'Especialistas', 'Graduados', 'Técnicos'],
                    var_name='categoria_profissional', 
                    value_name='quantidade')

# Criando DataFrame pivot para melhor visualização
df_pivot = df_melted.pivot_table(index=['ano', 'rede'], 
                                columns='categoria_profissional', 
                                values='quantidade', 
                                fill_value=0).reset_index()

# Resetando index para facilitar manipulação
df_pivot_reset = df_pivot.reset_index(drop=True)

# [Código da tabela HTML permanece o mesmo...]
# Ajuste para tabela HTML
colunas_html = ['Ano', 'Rede'] + list(df_pivot.columns[2:])
tam_colunas = ['60px', '80px'] + ['100px'] * (len(df_pivot.columns) - 2)
alinhamentos = ['left', 'left'] + ['right'] * (len(df_pivot.columns) - 2)
cabecalho_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
linha_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'docentes_tecnicos_por_rede'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(colunas_html)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Quantidade de Docentes e Técnicos por Ano e Rede
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

# ==================== GRÁFICO COM SEABORN ====================

# Configurando o tema e paleta de cores
plt.style.use('default')  # Reset para usar configurações do Seaborn
sns.set_theme(style="whitegrid", palette="deep")

# Definindo paleta de cores personalizada mais profissional
cores_categoria = {
    'Doutores': '#2E4057',      # Azul escuro
    'Mestres': '#048A81',       # Verde azulado
    'Especialistas': '#F18F01', # Laranja
    'Graduados': '#C73E1D',        # Vermelho
    'Técnicos': '#7209B7'       # Roxo
}

# Criando o gráfico com Seaborn
fig, ax = plt.subplots(figsize=(16, 10))

# Preparando dados para o gráfico
categorias = ['Doutores', 'Mestres', 'Especialistas', 'Graduados', 'Técnicos']

# Plotando cada categoria para cada rede
for categoria in categorias:
    if categoria in df_melted['categoria_profissional'].values:
        # Dados para rede pública
        dados_publica = df_melted[
            (df_melted['categoria_profissional'] == categoria) & 
            (df_melted['rede'] == 'Pública')
        ]
        
        # Dados para rede privada
        dados_privada = df_melted[
            (df_melted['categoria_profissional'] == categoria) & 
            (df_melted['rede'] == 'Privada')
        ]
        
        cor = cores_categoria.get(categoria, '#808080')
        
        # Plotando linha para rede pública
        if not dados_publica.empty:
            sns.lineplot(data=dados_publica, x='ano', y='quantidade', 
                        color=cor, marker='o', linewidth=3, markersize=8,
                        label=f'{categoria} - Pública', linestyle='-', alpha=0.9)
        
        # Plotando linha para rede privada
        if not dados_privada.empty:
            sns.lineplot(data=dados_privada, x='ano', y='quantidade', 
                        color=cor, marker='s', linewidth=3, markersize=8,
                        label=f'{categoria} - Privada', linestyle='--', alpha=0.7)

# Customizações do gráfico (SEM TÍTULO)
ax.set_xlabel('Ano', fontsize=14, fontweight='bold')
ax.set_ylabel('Quantidade', fontsize=14, fontweight='bold')

# Formatando os eixos
# 3) Anos em inteiros
anos_unicos = sorted(df_melted['ano'].unique())
ax.set_xticks(anos_unicos)
ax.set_xticklabels([str(int(ano)) for ano in anos_unicos], fontsize=12, rotation=45)
ax.tick_params(axis='y', labelsize=12)

# 4) Grade de 20 em 20 mil
from matplotlib.ticker import MultipleLocator
ax.yaxis.set_major_locator(MultipleLocator(20000))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

# 2) Legenda em baixo, na horizontal
handles, labels = ax.get_legend_handles_labels()
legend = ax.legend(handles, labels, 
                  loc='upper center',           # Posição central superior
                  bbox_to_anchor=(0.5, -0.1),  # Abaixo do gráfico
                  ncol=5,                       # 5 colunas (uma para cada categoria)
                  fontsize=11, 
                  frameon=True, 
                  fancybox=True, 
                  shadow=True,
                  facecolor='white', 
                  edgecolor='gray', 
                  framealpha=0.95,
                  title='Categoria - Rede', 
                  title_fontsize=12,
                  columnspacing=1.5)            # Espaçamento entre colunas
legend.get_title().set_fontweight('bold')

# Configurando grade
ax.grid(True, linestyle='--', alpha=0.7, linewidth=0.8)
ax.set_axisbelow(True)

# Ajustando o layout para acomodar a legenda embaixo
plt.tight_layout()
plt.subplots_adjust(bottom=0.2)  # Espaço extra para a legenda

# Adicionando uma anotação com informações adicionais
plt.figtext(0.02, 0.02, 
           'Fonte: Censo da Educação Superior | Linhas sólidas: Rede Pública | Linhas tracejadas: Rede Privada | Do Autor em relats/pesq/docentes_titulacao.py',
           fontsize=10, style='italic', alpha=0.7)

# Salvando o gráfico
arq_output = 'docs/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight', dpi=300, facecolor='white', edgecolor='none')
plt.show()
plt.close()

print(f'Gráfico salvo como: {arq_output}')
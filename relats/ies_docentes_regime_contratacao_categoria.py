import os
import sys

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd
import seaborn as sns

# Adiciona o path das dependências ao sistema
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

sql = """
SELECT 
    i.ano_censo AS ano,
    c.nome AS categoria, 
    SUM(i.qt_doc_ex_hor) AS horistas,
    SUM(i.qt_doc_ex_int_de) AS integralcomde,
    SUM(i.qt_doc_ex_int_sem_de) AS integralsemde,
    SUM(i.qt_doc_ex_parc) AS parcial
FROM ies_censo i  
JOIN tp_categoria_administrativa c 
    ON c.codigo = i.categoria 
WHERE i.ano_censo > 2013
GROUP BY i.ano_censo, c.nome
ORDER BY i.ano_censo, c.nome;
"""

ORDEM_CATEGORIAS = [
    'Pública Federal',
    'Pública Estadual',
    'Pública Municipal',
    'Privada sem fins lucrativos',
    'Privada com fins lucrativos',
    'Especial',
]

RENOMEAR_REGIMES = {
    'horistas': 'Horistas',
    'integralcomde': 'Integral com DE',
    'integralsemde': 'Integral sem DE',
    'parcial': 'Parcial',
}

PALETA = {
    'Horistas': '#D55E00',
    'Integral com DE': '#0072B2',
    'Integral sem DE': '#009E73',
    'Parcial': '#CC79A7',
}



def formatar_numero(valor):
    return f'{int(round(valor)):,}'.replace(',', '.')



def formatar_eixo(valor, _):
    return formatar_numero(valor)



def carregar_dados():
    df = carregar_dataframe(sql).fillna(0)

    colunas_numericas = ['ano', 'horistas', 'integralcomde', 'integralsemde', 'parcial']
    for coluna in colunas_numericas:
        df[coluna] = pd.to_numeric(df[coluna], errors='coerce').fillna(0).astype(int)

    df['categoria'] = pd.Categorical(df['categoria'], categories=ORDEM_CATEGORIAS, ordered=True)
    df = df.sort_values(['categoria', 'ano']).reset_index(drop=True)
    return df



def gerar_tabela_html(df):
    df_tabela = df.copy()
    for coluna in ['horistas', 'integralcomde', 'integralsemde', 'parcial']:
        df_tabela[coluna] = df_tabela[coluna].map(formatar_numero)

    column_widths = ['70px', '220px', '100px', '130px', '130px', '100px']
    column_names = ['Ano', 'Categoria', 'Horistas', 'Integral c/ DE', 'Integral s/ DE', 'Parcial']
    column_alignments = ['center', 'left', 'right', 'right', 'right', 'right']
    header_style = 'background-color: #4CAF50; color: white; font-weight: bold;'
    row_style = 'background-color: #f2f2f2;'

    html_title = f"""
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 10px;">
        <tr style="background-color: #2E7D32;">
            <th colspan="6" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
                Docentes por categoria administrativa e regime de contratação (2014–2024)
            </th>
        </tr>
    </table>
    """

    html_table = dataframe_to_html(
        df_tabela,
        column_widths,
        column_names,
        column_alignments,
        header_style,
        row_style,
    )

    os.makedirs('docs/tabelas', exist_ok=True)
    with open('docs/tabelas/docentes_regime_contratacao_categoria.html', 'w', encoding='utf-8') as f:
        f.write(html_title + html_table)

    df.to_csv('docs/tabelas/docentes_regime_contratacao_categoria.csv', index=False, encoding='utf-8-sig')



def gerar_grafico_facetas(df):
    df_long = df.melt(
        id_vars=['ano', 'categoria'],
        value_vars=['horistas', 'integralcomde', 'integralsemde', 'parcial'],
        var_name='regime',
        value_name='quantidade',
    )
    df_long['regime'] = df_long['regime'].map(RENOMEAR_REGIMES)

    sns.set_theme(style='whitegrid')
    g = sns.relplot(
        data=df_long,
        x='ano',
        y='quantidade',
        hue='regime',
        hue_order=list(PALETA.keys()),
        col='categoria',
        col_wrap=2,
        kind='line',
        marker='o',
        linewidth=2,
        palette=PALETA,
        height=4,
        aspect=1.4,
        facet_kws={'sharey': False, 'sharex': True},
    )

    anos = sorted(df['ano'].unique().tolist())
    for ax in g.axes.flat:
        ax.set_xticks(anos)
        ax.tick_params(axis='x', rotation=45)
        ax.yaxis.set_major_formatter(FuncFormatter(formatar_eixo))
        ax.grid(True, alpha=0.25)
        ax.set_xlabel('Ano')
        ax.set_ylabel('Docentes')

    g.set_titles('{col_name}')
    if g._legend is not None:
        g._legend.set_title('Regime de contratação')
        g._legend.set_bbox_to_anchor((0.5, -0.03))
        g._legend._loc = 8

    g.figure.subplots_adjust(top=0.9, bottom=0.12)
    g.figure.suptitle(
        'Docentes por regime de contratação em cada categoria administrativa (2014–2024)',
        fontsize=16,
        fontweight='bold',
    )

    os.makedirs('docs/graficos', exist_ok=True)
    g.figure.savefig(
        'docs/graficos/docentes_regime_contratacao_categoria_facetas.png',
        dpi=300,
        bbox_inches='tight',
    )
    plt.close(g.figure)



def gerar_grafico_dissertacao(df):
    ano_final = int(df['ano'].max())
    df_final = (
        df[df['ano'] == ano_final]
        .set_index('categoria')[['horistas', 'integralcomde', 'integralsemde', 'parcial']]
        .rename(columns=RENOMEAR_REGIMES)
        .reindex(ORDEM_CATEGORIAS)
        .fillna(0)
    )

    fig, ax = plt.subplots(figsize=(12, 7))
    df_final.plot(
        kind='barh',
        stacked=True,
        color=[PALETA[col] for col in df_final.columns],
        ax=ax,
        width=0.75,
    )

    totais = df_final.sum(axis=1)
    deslocamento = totais.max() * 0.01
    for indice, total in enumerate(totais):
        ax.text(total + deslocamento, indice, formatar_numero(total), va='center', fontsize=9)

    ax.xaxis.set_major_formatter(FuncFormatter(formatar_eixo))
    ax.set_xlabel('Quantidade de docentes')
    ax.set_ylabel('Categoria administrativa')
    ax.set_title(
        f'Distribuição dos regimes de contratação docente por categoria administrativa ({ano_final})',
        fontsize=15,
        fontweight='bold',
    )
    ax.legend(title='Regime', loc='lower right')
    ax.grid(axis='x', alpha=0.25)
    plt.tight_layout()

    fig.savefig(
        'docs/graficos/docentes_regime_contratacao_categoria_dissertacao.png',
        dpi=300,
        bbox_inches='tight',
    )
    plt.close(fig)



def main():
    df = carregar_dados()
    gerar_tabela_html(df)
    gerar_grafico_facetas(df)
    gerar_grafico_dissertacao(df)

    print('Relatório de docentes por regime de contratação e categoria gerado com sucesso!')
    print('Arquivos salvos:')
    print('- docs/tabelas/docentes_regime_contratacao_categoria.html')
    print('- docs/tabelas/docentes_regime_contratacao_categoria.csv')
    print('- docs/graficos/docentes_regime_contratacao_categoria_facetas.png')
    print('- docs/graficos/docentes_regime_contratacao_categoria_dissertacao.png')


if __name__ == '__main__':
    main()

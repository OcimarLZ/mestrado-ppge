"""
Gera 3 imagens do Brasil (2005, 2014 e 2024) colorindo os municípios
onde há cursos vinculados às mantenedoras da YDUQS.

Municípios sem presença ficam em cinza claro; os presentes ficam em
azul marinho fixo, independente do número de cursos.
"""

import os
import sys

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import geobr
import geopandas as gpd

# Adiciona o path das dependências ao sistema
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bdados.ler_bdados_to_df import carregar_dataframe

ANOS = (2005, 2014, 2024)

MANTENEDORAS = (119, 848, 2683)

sql = f"""
SELECT
    c.ano_censo,
    c.municipio AS code_muni
FROM curso_censo c
JOIN ies i ON i.codigo = c.ies
WHERE c.ano_censo IN ({', '.join(str(a) for a in ANOS)})
  AND i.mantenedora IN ({', '.join(str(m) for m in MANTENEDORAS)})
GROUP BY c.ano_censo, c.municipio
ORDER BY c.ano_censo, c.municipio
"""

COR_PRESENTE = '#001F5B'  # azul marinho da YDUQS
COR_AUSENTE  = '#D0D0D0'  # cinza para municípios ausentes
COR_BORDA    = '#FFFFFF'


def normalizar_codigos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['code_muni'] = (
        df['code_muni']
        .astype(str)
        .str.replace('.0', '', regex=False)
        .str.extract(r'(\d+)', expand=False)
    )
    df = df[df['code_muni'].notna()]
    df['code_muni'] = df['code_muni'].str.zfill(7).astype('int64')
    return df


def preparar_malha() -> gpd.GeoDataFrame:
    malha = geobr.read_municipality(code_muni='all', year=2020, simplified=True)
    malha['code_muni'] = malha['code_muni'].astype('int64')
    return malha


def gerar_mapa_ano(
    ano: int,
    df_ano: pd.DataFrame,
    malha: gpd.GeoDataFrame,
    output_path: str,
) -> None:
    base = malha.copy()
    df_ano = df_ano.copy()
    df_ano['presente'] = 1
    selecionados = base.merge(df_ano[['code_muni', 'presente']], on='code_muni', how='left')

    presentes = selecionados[selecionados['presente'].notna()].copy()
    qtd_municipios = len(presentes)

    fig, ax = plt.subplots(figsize=(11, 11))
    ax.set_axis_off()

    base.plot(ax=ax, color=COR_AUSENTE, edgecolor=COR_BORDA, linewidth=0.15)

    if not presentes.empty:
        presentes.plot(
            ax=ax,
            color=COR_PRESENTE,
            edgecolor=COR_BORDA,
            linewidth=0.15,
        )

    ax.set_title(
        f'Presença da YDUQS no Ensino Superior — {ano}\n'
        f'{qtd_municipios} municípios com presença',
        fontsize=14,
        fontweight='bold',
        pad=12,
    )

    legenda_patches = [
        mpatches.Patch(color=COR_AUSENTE, edgecolor='gray', label='Sem presença'),
        mpatches.Patch(color=COR_PRESENTE, label='Com presença (YDUQS)'),
    ]
    ax.legend(handles=legenda_patches, loc='lower left', fontsize=10, framealpha=0.85)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'  Mapa {ano} salvo: {output_path}  ({qtd_municipios} municípios)')


def _plotar_mapa_no_ax(
    ax: plt.Axes,
    ano: int,
    df_ano: pd.DataFrame,
    malha: gpd.GeoDataFrame,
) -> None:
    """Renderiza um mapa de um único ano em um eixo já existente."""
    base = malha.copy()
    df_ano = df_ano.copy()
    df_ano['presente'] = 1
    selecionados = base.merge(df_ano[['code_muni', 'presente']], on='code_muni', how='left')

    presentes = selecionados[selecionados['presente'].notna()].copy()
    qtd_municipios = len(presentes)

    base.plot(ax=ax, color=COR_AUSENTE, edgecolor=COR_BORDA, linewidth=0.1)

    if not presentes.empty:
        presentes.plot(
            ax=ax,
            color=COR_PRESENTE,
            edgecolor=COR_BORDA,
            linewidth=0.1,
        )

    ax.set_axis_off()
    ax.set_title(
        f'{ano}\n{qtd_municipios} municípios',
        fontsize=10,
        fontweight='bold',
        pad=6,
    )


def gerar_painel_a4(df: pd.DataFrame, malha: gpd.GeoDataFrame, output_path: str) -> None:
    """Gera um painel único A4 paisagem com os 3 mapas lado a lado."""
    fig, axes = plt.subplots(
        nrows=1,
        ncols=3,
        figsize=(11.69, 8.27),
        gridspec_kw={'wspace': 0.04},
    )

    for ax, ano in zip(axes, ANOS):
        df_ano = df[df['ano_censo'] == ano].copy()
        _plotar_mapa_no_ax(ax, ano, df_ano, malha)

    fig.suptitle(
        'Expansão territorial da YDUQS no Ensino Superior (2005–2014–2024)',
        fontsize=13,
        fontweight='bold',
        y=0.97,
    )

    legenda_patches = [
        mpatches.Patch(color=COR_AUSENTE, edgecolor='gray', label='Sem presença'),
        mpatches.Patch(color=COR_PRESENTE, label='Com presença (YDUQS)'),
    ]
    fig.legend(
        handles=legenda_patches,
        loc='lower center',
        ncol=2,
        fontsize=10,
        framealpha=0.85,
        bbox_to_anchor=(0.5, 0.01),
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  Painel A4 salvo: {output_path}')


def main() -> None:
    print('Carregando dados do banco...')
    df = carregar_dataframe(sql)
    df = normalizar_codigos(df)

    print('Carregando malha municipal (geobr)...')
    malha = preparar_malha()

    for ano in ANOS:
        df_ano = df[df['ano_censo'] == ano].copy()
        output_path = f'docs/graficos/mapa_yduqs_{ano}.png'
        gerar_mapa_ano(ano, df_ano, malha, output_path)

    output_painel = 'docs/graficos/mapa_yduqs_painel_a4.png'
    gerar_painel_a4(df, malha, output_painel)

    print('\nTodos os arquivos gerados com sucesso!')
    for ano in ANOS:
        print(f'- docs/graficos/mapa_yduqs_{ano}.png')
    print(f'- {output_painel}')


if __name__ == '__main__':
    main()

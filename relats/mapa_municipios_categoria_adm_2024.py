import os
import sys

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd
import geobr
import geopandas as gpd

# Adiciona o path das dependências ao sistema
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bdados.ler_bdados_to_df import carregar_dataframe

ANO_ALVO = 2024

# Interpretação adotada para as categorias pedidas:
# 1 = Federal, 2 = Estadual, 3 = Municipal, > 3 = Privadas.
sql = f"""
SELECT
    c.municipio AS code_muni,
    GROUP_CONCAT(DISTINCT c.categoria) AS categorias,
    COUNT(DISTINCT c.categoria) AS qtd_categorias,
    COUNT(DISTINCT c.ies) AS qtd_ies
FROM curso_censo c
WHERE c.ano_censo = {ANO_ALVO}
  AND c.municipio IS NOT NULL
GROUP BY c.municipio
ORDER BY c.municipio
"""

CORES = {
    'Mais de uma categoria': '#000000',
    'Somente federal (cat. 1)': '#008000',
    'Somente estadual (cat. 2)': '#0000FF',
    'Somente municipal (cat. 3)': '#FFD700',
    'Somente privada (cat. > 3)': '#FF0000',
}

ORDEM_LEGENDA = [
    'Mais de uma categoria',
    'Somente federal (cat. 1)',
    'Somente estadual (cat. 2)',
    'Somente municipal (cat. 3)',
    'Somente privada (cat. > 3)',
]


def normalizar_codigos_municipio(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza códigos IBGE para inteiro de 7 dígitos."""
    df = df.copy()
    df['code_muni'] = (
        df['code_muni']
        .astype(str)
        .str.replace('.0', '', regex=False)
        .str.extract(r'(\d+)', expand=False)
    )
    df = df[df['code_muni'].notna()].copy()
    df['code_muni'] = df['code_muni'].str.zfill(7).astype('int64')
    return df


def extrair_categorias(valor: str) -> set[int]:
    if pd.isna(valor):
        return set()
    return {int(item.strip()) for item in str(valor).split(',') if item and item.strip().isdigit()}



def classificar_municipio(categorias: set[int]) -> str | None:
    """Classifica o município nas 5 cores pedidas."""
    if not categorias:
        return None
    if len(categorias) > 1:
        return 'Mais de uma categoria'

    categoria = next(iter(categorias))
    if categoria == 1:
        return 'Somente federal (cat. 1)'
    if categoria == 2:
        return 'Somente estadual (cat. 2)'
    if categoria == 3:
        return 'Somente municipal (cat. 3)'
    if categoria > 3:
        return 'Somente privada (cat. > 3)'
    return None



def carregar_dados_municipios() -> pd.DataFrame:
    df = carregar_dataframe(sql)
    df = normalizar_codigos_municipio(df)
    df['categorias_set'] = df['categorias'].apply(extrair_categorias)
    df['grupo'] = df['categorias_set'].apply(classificar_municipio)
    return df[df['grupo'].notna()].copy()



def preparar_malha_municipal() -> gpd.GeoDataFrame:
    malha = geobr.read_municipality(code_muni='all', year=2020, simplified=True)
    malha['code_muni'] = malha['code_muni'].astype('int64')
    return malha



def salvar_resumo(df: pd.DataFrame, caminho_csv: str, caminho_html: str) -> None:
    resumo = (
        df.groupby('grupo', observed=False)
        .agg(qtd_municipios=('code_muni', 'nunique'), qtd_ies=('qtd_ies', 'sum'))
        .reset_index()
    )
    resumo['ordem'] = resumo['grupo'].map({grupo: i for i, grupo in enumerate(ORDEM_LEGENDA)})
    resumo = resumo.sort_values('ordem').drop(columns='ordem')

    os.makedirs(os.path.dirname(caminho_csv), exist_ok=True)
    resumo.to_csv(caminho_csv, index=False, encoding='utf-8-sig')
    resumo.to_html(caminho_html, index=False)



def gerar_mapa(df: pd.DataFrame, malha: gpd.GeoDataFrame, output_path: str) -> None:
    mapa = malha.merge(df[['code_muni', 'grupo', 'qtd_ies']], on='code_muni', how='left')

    fig, ax = plt.subplots(figsize=(14, 14))

    mapa.plot(ax=ax, color='#EAEAEA', edgecolor='white', linewidth=0.15)

    for grupo in ORDEM_LEGENDA:
        subset = mapa[mapa['grupo'] == grupo]
        if not subset.empty:
            subset.plot(ax=ax, color=CORES[grupo], edgecolor='white', linewidth=0.15)

    legenda = [
        Patch(facecolor=CORES[grupo], edgecolor='black', label=grupo)
        for grupo in ORDEM_LEGENDA
    ]

    ax.legend(
        handles=legenda,
        title='Classificação dos municípios',
        loc='lower left',
        frameon=True,
        fontsize=10,
        title_fontsize=11,
    )

    ax.set_title(
        f'Brasil - Municípios por categoria administrativa exclusiva das IES ({ANO_ALVO})\n'
        'Preto = município com presença em mais de uma categoria',
        fontsize=15,
    )
    ax.axis('off')

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)



def main() -> None:
    df = carregar_dados_municipios()

    if df.empty:
        print(f'Nenhum município encontrado para o ano {ANO_ALVO}.')
        return

    malha = preparar_malha_municipal()

    output_png = f'docs/graficos/mapa_municipios_categoria_adm_{ANO_ALVO}.png'
    output_csv = f'docs/tabelas/mapa_municipios_categoria_adm_{ANO_ALVO}.csv'
    output_html = f'docs/tabelas/mapa_municipios_categoria_adm_{ANO_ALVO}.html'

    gerar_mapa(df, malha, output_png)
    salvar_resumo(df, output_csv, output_html)

    print('Mapa gerado com sucesso!')
    print(f'- {output_png}')
    print(f'- {output_csv}')
    print(f'- {output_html}')
    print(f'- Municípios classificados: {df["code_muni"].nunique()}')


if __name__ == '__main__':
    main()

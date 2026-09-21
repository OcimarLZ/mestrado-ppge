import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

# Dependencias geoespaciais para gerar mapas estaticos do Brasil
import geobr
import geopandas as gpd

# Adiciona o path das dependencias ao sistema
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bdados.ler_bdados_to_df import carregar_dataframe

ANOS_PADRAO = (2005, 2014, 2024)
TITULO_PAINEL = 'Número de municípíos com presença de polos presenciais - 2006 | 2024'

# SQL parametrizado para recuperar municipios por ano.
# A coluna municipio do curso_censo guarda o codigo IBGE.
sql = """
SELECT
    c.ano_censo,
    c.municipio AS code_muni,
    COUNT(*) AS total_registros
FROM curso_censo c
WHERE c.ano_censo = :ano
    AND c.tp_modalidade_ensino = 1
GROUP BY c.ano_censo, c.municipio
ORDER BY c.ano_censo, c.municipio
"""


def normalizar_codigos_municipio(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza codigos de municipio para inteiro de 7 digitos (padrao IBGE)."""
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


def preparar_malha_municipios() -> gpd.GeoDataFrame:
    """Carrega a malha municipal oficial simplificada para acelerar o plot."""
    malha = geobr.read_municipality(code_muni='all', year=2020, simplified=True)
    malha['code_muni'] = malha['code_muni'].astype('int64')
    return malha


def solicitar_anos() -> list[int]:
    """Solicita 3 anos para gerar os mapas. Enter usa os anos padrao."""
    prompt = (
        'Informe 3 anos separados por virgula '
        '(ex: 2005,2014,2024). Pressione Enter para usar o padrao: '
    )
    entrada = input(prompt).strip()

    if not entrada:
        return list(ANOS_PADRAO)

    anos = []
    for token in entrada.split(','):
        token_limpo = token.strip()
        if not token_limpo.isdigit():
            raise ValueError('Todos os anos precisam ser numericos.')
        anos.append(int(token_limpo))

    if len(anos) != 3:
        raise ValueError('Informe exatamente 3 anos para gerar 3 mapas.')

    return anos


def buscar_dados_por_ano(ano: int) -> pd.DataFrame:
    """Executa SQL parametrizado para retornar municipios de um unico ano."""
    df_ano = carregar_dataframe(sql, params={'ano': ano})
    return normalizar_codigos_municipio(df_ano)


def plotar_mapa_no_eixo(
    ax: plt.Axes,
    ano: int,
    df_ano: pd.DataFrame,
    malha_municipios: gpd.GeoDataFrame,
) -> None:
    """Desenha um mapa do Brasil em um eixo existente para o ano informado."""
    base = malha_municipios
    selecionados = base.merge(df_ano[['code_muni', 'total_registros']], on='code_muni', how='inner')

    base.plot(ax=ax, color='#f5f5f5', edgecolor='white', linewidth=0.2)

    if not selecionados.empty:
        # Centroides em CRS projetado para evitar distorcao de calculo
        selecionados_proj = selecionados.to_crs(epsg=5880).copy()
        selecionados_proj['geometry'] = selecionados_proj.geometry.centroid
        crs_destino = base.crs if base.crs is not None else 'EPSG:4674'
        pontos = selecionados_proj.to_crs(crs_destino)

        # Tamanho do ponto proporcional a quantidade de registros do municipio no ano
        tamanho_base = 10
        fator = 1.6
        tamanhos = tamanho_base + (pontos['total_registros'].clip(lower=1) ** 0.5) * fator

        pontos.plot(
            ax=ax,
            color='#2ca02c',
            markersize=tamanhos,
            alpha=0.85,
            edgecolor='black',
            linewidth=0.2,
        )

    ax.set_title(f'{ano} ({len(df_ano)} municipios)', fontsize=13, pad=3)
    ax.axis('off')


def gerar_painel_16x9(
    anos: list[int],
    dados_por_ano: dict[int, pd.DataFrame],
    malha_municipios: gpd.GeoDataFrame,
    output_path: str,
) -> None:
    """Gera uma unica imagem 16x9 com os 3 anos lado a lado."""
    fig, axes = plt.subplots(
        nrows=1,
        ncols=3,
        figsize=(16, 9),
        gridspec_kw={'wspace': 0.01},
    )

    fig.subplots_adjust(left=0.005, right=0.995, top=0.90, bottom=0.02)

    for ax, ano in zip(axes, anos):
        plotar_mapa_no_eixo(ax, ano, dados_por_ano[ano], malha_municipios)

    fig.suptitle(TITULO_PAINEL, fontsize=18, fontweight='bold', y=0.965)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def main() -> None:
    try:
        anos_alvo = solicitar_anos()
    except ValueError as e:
        print(f'Entrada invalida: {e}')
        return

    malha_municipios = preparar_malha_municipios()

    dados_por_ano: dict[int, pd.DataFrame] = {}
    for ano in anos_alvo:
        df_ano = buscar_dados_por_ano(ano)
        dados_por_ano[ano] = df_ano

        if df_ano.empty:
            print(f'Nenhum municipio encontrado para o ano {ano}. O painel exibira o mapa base sem pontos.')

    output_path = (
        f'docs/graficos/mapa_municipios_presencial_painel_16x9_'
        f'{anos_alvo[0]}_{anos_alvo[1]}_{anos_alvo[2]}.png'
    )
    gerar_painel_16x9(anos_alvo, dados_por_ano, malha_municipios, output_path)

    print(f'Painel 16x9 gerado: {output_path}')


if __name__ == '__main__':
    main()
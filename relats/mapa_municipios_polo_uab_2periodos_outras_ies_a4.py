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

ANOS_PADRAO = (2014, 2024)

# Dimensoes em polegadas — A4 landscape para 2 mapas lado a lado
A4_LANDSCAPE_W = 15.0
A4_LANDSCAPE_H = 10.0

# SQL parametrizado para recuperar municipios por ano.
# A coluna municipio do uab_censo guarda o codigo IBGE.
sql = """
SELECT
    u.ano_censo,
    u.municipio AS code_muni,
    COUNT(*) AS total_registros
FROM uab_censo u
JOIN ies i ON i.codigo = u.ies
WHERE u.ano_censo = :ano
  AND u.tp_grau_academico = 2
  AND u.situacao_polo = 'Ativo'
  AND i.categoria > 1
GROUP BY u.ano_censo, u.municipio
ORDER BY u.ano_censo, u.municipio
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
    """Solicita 2 anos para gerar os mapas. Enter usa os anos padrao."""
    prompt = (
        'Informe 2 anos separados por virgula '
        '(ex: 2014,2024). Pressione Enter para usar o padrao: '
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

    if len(anos) != 2:
        raise ValueError('Informe exatamente 2 anos para gerar 2 mapas.')

    return anos


def buscar_dados_por_ano(ano: int) -> pd.DataFrame:
    """Executa SQL parametrizado para retornar municipios de um unico ano."""
    df_ano = carregar_dataframe(sql, params={'ano': ano})
    return normalizar_codigos_municipio(df_ano)


def plotar_mapa_no_eixo(
    ax,
    ano: int,
    df_ano: pd.DataFrame,
    malha_municipios: gpd.GeoDataFrame,
) -> None:
    """Plota um mapa de municipios num eixo matplotlib existente."""
    base = malha_municipios
    selecionados = base.merge(df_ano[['code_muni', 'total_registros']], on='code_muni', how='inner')

    # Fundo do Brasil
    base.plot(ax=ax, color='#f5f5f5', edgecolor='white', linewidth=0.2)

    if not selecionados.empty:
        # Centroides em CRS projetado para evitar distorcao de calculo
        selecionados_proj = selecionados.to_crs(epsg=5880).copy()
        selecionados_proj['geometry'] = selecionados_proj.geometry.centroid
        crs_destino = base.crs if base.crs is not None else 'EPSG:4674'
        pontos = selecionados_proj.to_crs(crs_destino)

        # Tamanho do ponto proporcional a quantidade de registros do municipio no ano
        tamanho_base = 6
        fator = 1.5
        tamanhos = tamanho_base + (pontos['total_registros'].clip(lower=1) ** 0.5) * fator

        pontos.plot(
            ax=ax,
            color='#d62728',
            markersize=tamanhos,
            alpha=0.85,
            edgecolor='black',
            linewidth=0.15,
        )

    municipios_count = len(df_ano)
    ax.set_title(
        f'{ano}\n({municipios_count} municípios)',
        fontsize=12,
        fontweight='bold',
        pad=4,
    )
    ax.axis('off')


def gerar_mapa_combinado_a4(
    anos: list[int],
    dados_por_ano: dict,
    malha_municipios: gpd.GeoDataFrame,
    output_path: str,
) -> None:
    """Gera uma imagem A4 landscape com 2 mapas lado a lado."""
    fig, axes = plt.subplots(
        nrows=1,
        ncols=2,
        figsize=(A4_LANDSCAPE_W, A4_LANDSCAPE_H),
    )

    ano_ini, ano_fim = anos[0], anos[1]
    fig.suptitle(
        f'Comparativo de Municípios (Polos UAB Ativos e Outras IES): {ano_ini} × {ano_fim}',
        fontsize=13,
        fontweight='bold',
        y=0.97,
    )

    for ax, ano in zip(axes, anos):
        df_ano = dados_por_ano[ano]
        plotar_mapa_no_eixo(ax, ano, df_ano, malha_municipios)

    plt.subplots_adjust(left=0.005, right=0.995, top=0.92, bottom=0.01, wspace=0.03)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', format='png')
    plt.close(fig)


def main() -> None:
    try:
        anos_alvo = solicitar_anos()
    except ValueError as e:
        print(f'Entrada invalida: {e}')
        return

    malha_municipios = preparar_malha_municipios()

    dados_por_ano = {}
    for ano in anos_alvo:
        df_ano = buscar_dados_por_ano(ano)
        if df_ano.empty:
            print(f'Nenhum municipio encontrado para o ano {ano}. Mapa base sera gerado sem pontos.')
        dados_por_ano[ano] = df_ano
        print(f'Dados carregados para {ano}: {len(df_ano)} municipios')

    anos_str = '_'.join(str(a) for a in anos_alvo)
    output_path = f'docs/graficos/mapa_municipios_polo_uab_2periodos_{anos_str}_outras_ies_a4.png'

    gerar_mapa_combinado_a4(anos_alvo, dados_por_ano, malha_municipios, output_path)
    print(f'Mapa A4 comparativo gerado: {output_path}')


if __name__ == '__main__':
    main()

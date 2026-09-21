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

# SQL parametrizado para recuperar municipios por ano.
# A coluna municipio do curso_censo guarda o codigo IBGE.
sql = """
SELECT
    c.ano_censo,
    c.municipio AS code_muni,
    COUNT(*) AS total_registros
FROM curso_censo c
WHERE c.ano_censo = :ano
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


def gerar_mapa_por_ano(
    ano: int,
    df_ano: pd.DataFrame,
    malha_municipios: gpd.GeoDataFrame,
    output_path: str,
) -> None:
    """Gera uma imagem PNG com pontos nos municipios do ano informado."""
    base = malha_municipios
    selecionados = base.merge(df_ano[['code_muni', 'total_registros']], on='code_muni', how='inner')

    fig, ax = plt.subplots(figsize=(10, 10))

    # Fundo do Brasil
    base.plot(ax=ax, color='#f5f5f5', edgecolor='white', linewidth=0.2)

    if not selecionados.empty:
        # Centroides em CRS projetado para evitar distorcao de calculo
        selecionados_proj = selecionados.to_crs(epsg=5880).copy()
        selecionados_proj['geometry'] = selecionados_proj.geometry.centroid
        crs_destino = base.crs if base.crs is not None else 'EPSG:4674'
        pontos = selecionados_proj.to_crs(crs_destino)

        # Tamanho do ponto proporcional a quantidade de registros do municipio no ano
        tamanho_base = 14
        fator = 2
        tamanhos = tamanho_base + (pontos['total_registros'].clip(lower=1) ** 0.5) * fator

        pontos.plot(
            ax=ax,
            color='#d62728',
            markersize=tamanhos,
            alpha=0.85,
            edgecolor='black',
            linewidth=0.2,
        )

    ax.set_title(f'Municipios presentes no curso_censo - {ano}', fontsize=14)
    ax.axis('off')
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)


def main() -> None:
    try:
        anos_alvo = solicitar_anos()
    except ValueError as e:
        print(f'Entrada invalida: {e}')
        return

    malha_municipios = preparar_malha_municipios()

    for ano in anos_alvo:
        df_ano = buscar_dados_por_ano(ano)
        output_path = f'docs/graficos/mapa_municipios_{ano}.png'

        if df_ano.empty:
            print(f'Nenhum municipio encontrado para o ano {ano}. Mapa base sera gerado sem pontos.')

        gerar_mapa_por_ano(ano, df_ano, malha_municipios, output_path)
        print(f'Mapa gerado: {output_path} (municipios: {len(df_ano)})')


if __name__ == '__main__':
    main()

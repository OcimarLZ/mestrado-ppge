import os
import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.patches as mpatches
import pandas as pd
from shapely.geometry import Point

# Dependencias geoespaciais para gerar mapas estaticos do Brasil
import geobr
import geopandas as gpd

# Adiciona o path das dependencias ao sistema
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bdados.ler_bdados_to_df import carregar_dataframe

ANO_PADRAO = 2024
TITULO_MAPA = 'Campi das Universidades Federais - {ano}'

def normalizar_codigos_municipio(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza codigos de municipio para inteiro de 7 digitos (padrao IBGE)."""
    df = df.copy()
    if 'code_muni' not in df.columns:
        return df
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


def preparar_malha_estados() -> gpd.GeoDataFrame:
    """Carrega a malha dos estados com as regioes e divisas."""
    estados = geobr.read_state(code_state='all', year=2020, simplified=True)
    return estados


def solicitar_ano() -> int:
    """Solicita 1 ano para gerar o mapa. Enter usa o ano padrao."""
    prompt = (
        f'Informe o ano para gerar o mapa. Pressione Enter para usar o padrao ({ANO_PADRAO}): '
    )
    entrada = input(prompt).strip()

    if not entrada:
        return ANO_PADRAO

    if not entrada.isdigit():
        raise ValueError('O ano precisa ser numerico.')
        
    return int(entrada)


def buscar_dados_por_ano(ano: int) -> pd.DataFrame:
    """Executa o novo SQL que captura a presenca de campi no municipio pelas IES federais."""
    sql = """
    SELECT DISTINCT
        c.ano_censo,
        c.municipio AS code_muni,
        i.sigla    
    FROM curso_censo c
    JOIN ies i on i.codigo = c.ies
    WHERE c.ano_censo = :ano
        AND c.categoria = 1 and c.org_academica = 1 and c.tp_modalidade_ensino = 1
    ORDER BY c.ano_censo, c.municipio, i.sigla
    """
    df_ano = carregar_dataframe(sql, params={'ano': ano})
    return normalizar_codigos_municipio(df_ano)


def get_cor_map_por_regiao(df_ano: pd.DataFrame) -> dict:
    """
    Gera cores distintas por regiao, garantindo que IES que atuam na mesma 
    regiao brasileira recebam tons radicalmente diferentes da paleta (evitando cores vizinhas iguais).
    """
    df = df_ano.copy()
    # O IBGE usa o 1o digito do municipio para denotar a regiao (1=Norte, 2=Nordeste, etc)
    df['regiao'] = df['code_muni'].astype(str).str[0].astype(int)
    
    # Determinar a regiao predominante de cada sigla (aonde ela tem mais campi)
    regiao_por_sigla = df.groupby('sigla')['regiao'].agg(lambda x: x.mode()[0]).to_dict()
    
    siglas_por_regiao = {1: [], 2: [], 3: [], 4: [], 5: []}
    for sigla, reg in regiao_por_sigla.items():
        if reg in siglas_por_regiao:
            siglas_por_regiao[reg].append(sigla)
        
    cor_map = {}
    cmap = plt.get_cmap('turbo')
    
    for reg, siglas in siglas_por_regiao.items():
        n = len(siglas)
        if n == 0: continue
        
        # Gera n cores que percorrem TODO o espectro do colormap, 
        # garantindo diferenciacao maxima DENTRO da propria regiao.
        cores = cmap(np.linspace(0.05, 0.95, n))
        
        # Embaralhar para evitar que IES de nomes parecidos (alfabeticamente) peguem cores adjacentes
        np.random.seed(reg * 42)
        np.random.shuffle(cores)
        
        siglas_ordenadas = sorted(siglas)
        for i, sigla in enumerate(siglas_ordenadas):
            cor_map[sigla] = cores[i]
            
    return cor_map


def plotar_mapa_no_eixo(
    ax: plt.Axes,
    df_ano: pd.DataFrame,
    malha_municipios: gpd.GeoDataFrame,
    malha_estados: gpd.GeoDataFrame,
) -> None:
    """Desenha o mapa base e plota cada universidade com cor unica e deslocamento lateral em caso de sobreposicao."""
    malha_estados.plot(
        ax=ax, 
        column='name_region', 
        cmap='Pastel2',
        edgecolor='#999999', 
        linewidth=0.5,
        alpha=0.7
    )

    selecionados = malha_municipios.merge(df_ano[['code_muni', 'sigla']], on='code_muni', how='inner')

    if not selecionados.empty:
        # Passar para CRS em metros para deslocamento artificial (jittering)
        selecionados_proj = selecionados.to_crs(epsg=5880).copy()
        selecionados_proj['geometry'] = selecionados_proj.geometry.centroid
        
        selecionados_proj['contagens'] = selecionados_proj.groupby('code_muni').cumcount()
        selecionados_proj['total_mun'] = selecionados_proj.groupby('code_muni')['sigla'].transform('count')

        def offset_point(row):
            geom = row['geometry']
            n = row['total_mun']
            idx = row['contagens']
            if n == 1:
                return geom
            distancia = 35000  # Raio de deslocamento: 35km a partir do centro
            angulo = idx * (2 * np.pi / n)
            return Point(geom.x + np.cos(angulo) * distancia, geom.y + np.sin(angulo) * distancia)
        
        selecionados_proj['geometry'] = selecionados_proj.apply(offset_point, axis=1)

        crs_destino = malha_estados.crs if malha_estados.crs is not None else 'EPSG:4674'
        pontos = selecionados_proj.to_crs(crs_destino)

        # Gerar cores unicas para cada sigla, separadas por regiao
        siglas_unicas = sorted(df_ano['sigla'].unique())
        cor_map = get_cor_map_por_regiao(df_ano)
        
        # Mapeando cores para plotar
        pontos['cor_sigla'] = pontos['sigla'].map(cor_map)

        # Plotar as bolhas
        pontos.plot(
            ax=ax,
            color=pontos['cor_sigla'],
            markersize=15, 
            alpha=1.0,
            edgecolor='black',
            linewidth=0.3,
        )

        legend_handles = []
        for sigla in siglas_unicas:
            legend_handles.append(mpatches.Patch(color=cor_map[sigla], label=sigla, ec='black', lw=0.5))

        # Legenda posicionada na direita do mapa
        if legend_handles:
            ax.legend(
                handles=legend_handles, 
                bbox_to_anchor=(1.05, 1),   # Fica logo apos a borda direita superior do eixo
                loc='upper left',
                ncol=2,                     # 2 colunas solicitadas
                fontsize=7,
                frameon=False,
                handletextpad=0.5,
                handlelength=1.0 
            )

    ax.axis('off')


def gerar_mapa_campi(
    ano: int,
    df_ano: pd.DataFrame,
    malha_municipios: gpd.GeoDataFrame,
    malha_estados: gpd.GeoDataFrame,
    output_path: str,
) -> None:
    """Gera uma unica imagem paisagem (razao 3:2) com mapa e legenda na direita."""
    fig, ax = plt.subplots(figsize=(15, 10)) # Razao proxima a 3:2

    # Espaco lateral para a legenda
    # A direita so vai ate 0.65 (65% da tela) para caber as 2 colunas da legenda nos outros 35%
    fig.subplots_adjust(left=0.01, right=0.65, top=0.90, bottom=0.05)

    plotar_mapa_no_eixo(ax, df_ano, malha_municipios, malha_estados)

    titulo_final = TITULO_MAPA.format(ano=ano)
    fig.suptitle(titulo_final, fontsize=18, fontweight='bold', y=0.95)
    
    # Contagem de presencas unicas vs contagem de municipios com campi
    total_presencas = len(df_ano)
    total_municipios_unicos = df_ano['code_muni'].nunique()
    ax.set_title(f'({total_presencas} campi em {total_municipios_unicos} municípios)', fontsize=14, pad=5)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def main() -> None:
    try:
        ano = solicitar_ano()
    except ValueError as e:
        print(f'Entrada invalida: {e}')
        return

    malha_municipios = preparar_malha_municipios()
    malha_estados = preparar_malha_estados()

    df_ano = buscar_dados_por_ano(ano)

    if df_ano.empty:
        print(f'Nenhum municipio encontrado para o ano {ano}. O mapa sera exibido sem pontos.')

    output_path = f'docs/graficos/mapa_ufs_campi_{ano}.png'
    
    gerar_mapa_campi(ano, df_ano, malha_municipios, malha_estados, output_path)

    print(f'Mapa gerado: {output_path}')


if __name__ == '__main__':
    main()

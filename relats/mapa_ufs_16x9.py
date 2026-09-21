import os
import sys

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.patches as mpatches
import pandas as pd

# Dependencias geoespaciais para gerar mapas estaticos do Brasil
import geobr
import geopandas as gpd

# Adiciona o path das dependencias ao sistema
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bdados.ler_bdados_to_df import carregar_dataframe

ANO_PADRAO = 2024
TITULO_MAPA = 'Municípios com Universidades Federais - {ano}'

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
    """Executa SQL parametrizado para retornar municipios de um unico ano e agrupa siglas."""
    sql = """
    SELECT
        c.ano_censo,
        c.municipio AS code_muni,
        i.sigla
    FROM ies_censo c
    JOIN ies i ON i.codigo = c.ies
    WHERE c.ano_censo = :ano
        AND c.categoria = 1 AND c.org_academica = 1
    """
    df_ano = carregar_dataframe(sql, params={'ano': ano})
    
    if not df_ano.empty:
        df_agrupado = df_ano.groupby(['ano_censo', 'code_muni']).agg(
            total_registros=('sigla', 'size'),
            sigla=('sigla', lambda x: ', '.join(x.dropna().unique()))
        ).reset_index()
        
        # Ordenar os dados pelas siglas para gerar a legenda em ordem alfabetica
        df_agrupado = df_agrupado.sort_values(by='sigla').reset_index(drop=True)
        # Atribuir um numero unico sequencial
        df_agrupado['label_num'] = df_agrupado.index + 1
    else:
        df_agrupado = pd.DataFrame(columns=['ano_censo', 'code_muni', 'total_registros', 'sigla', 'label_num'])

    return normalizar_codigos_municipio(df_agrupado)


def plotar_mapa_no_eixo(
    ax: plt.Axes,
    df_ano: pd.DataFrame,
    malha_municipios: gpd.GeoDataFrame,
    malha_estados: gpd.GeoDataFrame,
) -> None:
    """Desenha o mapa base com fundo por regiao e adiciona os pontos dos municipios."""
    # Plotar o fundo dos estados coloridos por regiao, com linhas de divisa
    malha_estados.plot(
        ax=ax, 
        column='name_region', 
        cmap='Pastel2', # Paleta com cores claras e distintas
        edgecolor='#999999', 
        linewidth=0.5,
        alpha=0.7 # Deixar as cores um pouco mais suaves
    )

    selecionados = malha_municipios.merge(df_ano[['code_muni', 'total_registros', 'sigla', 'label_num']], on='code_muni', how='inner')

    if not selecionados.empty:
        # Centroides em CRS projetado para evitar distorcao de calculo
        selecionados_proj = selecionados.to_crs(epsg=5880).copy()
        selecionados_proj['geometry'] = selecionados_proj.geometry.centroid
        crs_destino = malha_estados.crs if malha_estados.crs is not None else 'EPSG:4674'
        pontos = selecionados_proj.to_crs(crs_destino)

        tamanho_base = 25
        fator = 2.5
        tamanhos = tamanho_base + (pontos['total_registros'].clip(lower=1) ** 0.5) * fator

        pontos.plot(
            ax=ax,
            color='#1f77b4',  # Azul para UFs
            markersize=tamanhos,
            alpha=0.9,
            edgecolor='black',
            linewidth=0.5,
        )

        legend_handles = []

        # Adicionar as siglas das universidades no mapa
        for idx, row in pontos.iterrows():
            numero = str(row['label_num'])
            ax.annotate(
                numero,
                (row.geometry.x, row.geometry.y),
                xytext=(0, 0), 
                textcoords='offset points',
                ha='center', va='center',
                fontsize=7,
                fontweight='bold',
                color='white',
                path_effects=[pe.withStroke(linewidth=1.5, foreground='black')]
            )
            # Preparar o texto para a legenda (ocultando o quadro de cores - marker nulo)
            legend_handles.append(mpatches.Patch(color='none', label=f"{numero.zfill(2)} - {row['sigla']}"))
            
        # Ordenar os handles
        legend_handles = sorted(legend_handles, key=lambda x: int(x.get_label().split(' ')[0]))

        # Adicionar legenda fora do eixo, em 2 colunas para A4
        if legend_handles:
            # 2 colunas de legenda. Assume que "em 2 linhas" talvez significasse "2 colunas" 
            # devido à quantidade de siglas e layout vertical (A4)
            ax.legend(
                handles=legend_handles, 
                bbox_to_anchor=(0.5, -0.05), # Ponto central-inferior do mapa
                loc='upper center',          # Ancorado pelo centro-superior da legenda
                ncol=2,
                fontsize=8,
                frameon=False,
                handlelength=0, 
                handletextpad=0 
            )

    ax.axis('off')


def gerar_mapa_a4(
    ano: int,
    df_ano: pd.DataFrame,
    malha_municipios: gpd.GeoDataFrame,
    malha_estados: gpd.GeoDataFrame,
    output_path: str,
) -> None:
    """Gera uma unica imagem A4 retrato (razao 2:3) com mapa e legenda em baixo."""
    fig, ax = plt.subplots(figsize=(8, 12)) # Razaoz 2:3 (8 largura x 12 altura)

    # Deixar um espaco inferior generoso (40%) para as legendas caso tenham mtas siglas
    fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.40)

    plotar_mapa_no_eixo(ax, df_ano, malha_municipios, malha_estados)

    titulo_final = TITULO_MAPA.format(ano=ano)
    fig.suptitle(titulo_final, fontsize=16, fontweight='bold', y=0.97)
    
    # Adicionando a quantidade de municipios como subtitulo
    ax.set_title(f'({len(df_ano)} municípios)', fontsize=12, pad=3)

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

    output_path = f'docs/graficos/mapa_ufs_16x9_{ano}.png'
    
    gerar_mapa_a4(ano, df_ano, malha_municipios, malha_estados, output_path)

    print(f'Mapa gerado: {output_path}')


if __name__ == '__main__':
    main()

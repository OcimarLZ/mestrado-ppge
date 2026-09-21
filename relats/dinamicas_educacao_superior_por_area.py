import pandas as pd
import sys
import os

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bdados.ler_bdados_to_df import carregar_dataframe

def gerar_tabela_dissertacao_area_chapeco_html():
    """
    Gera um arquivo HTML com uma tabela formatada para dissertação (ABNT),
    mostrando IES, cursos, matriculados e concluintes por ano e área para Chapecó.
    """
    # Consulta SQL
    sql = """
    SELECT
        CASE 
            WHEN cc.area_geral = 1 THEN 'Educação'
            WHEN cc.area_geral = 2 THEN 'Artes'
            WHEN cc.area_geral = 3 THEN 'Sociais'
            WHEN cc.area_geral = 4 THEN 'Administração'
            WHEN cc.area_geral = 5 THEN 'Naturais'
            WHEN cc.area_geral = 6 THEN 'Informática'
            WHEN cc.area_geral = 7 THEN 'Engenharias'
            WHEN cc.area_geral = 8 THEN 'Agrárias'
            WHEN cc.area_geral = 9 THEN 'Saúde'
            WHEN cc.area_geral = 10 THEN 'Serviços'
            ELSE 'Indefinida'
        END AS "Área de Conhecimento",
        cc.ano_censo AS "Ano",

        -- Total Geral
        COUNT(DISTINCT cc.ies) AS "IES_total",
        COUNT(DISTINCT cc.curso) AS "Cursos_total",
        SUM(cc.qt_mat) AS "Matrículas_total",
        SUM(cc.qt_conc) AS "Concluintes_total",

        -- Presencial
        COUNT(DISTINCT CASE WHEN cc.tp_modalidade_ensino = 1 THEN cc.ies END) AS "IES_presencial",
        COUNT(DISTINCT CASE WHEN cc.tp_modalidade_ensino = 1 THEN cc.curso END) AS "Cursos_presencial",
        SUM(CASE WHEN cc.tp_modalidade_ensino = 1 THEN cc.qt_mat ELSE 0 END) AS "Matrículas_presencial",
        SUM(CASE WHEN cc.tp_modalidade_ensino = 1 THEN cc.qt_conc ELSE 0 END) AS "Concluintes_presencial",

        -- A Distância
        COUNT(DISTINCT CASE WHEN cc.tp_modalidade_ensino = 2 THEN cc.ies END) AS "IES_distancia",
        COUNT(DISTINCT CASE WHEN cc.tp_modalidade_ensino = 2 THEN cc.curso END) AS "Cursos_distancia",
        SUM(CASE WHEN cc.tp_modalidade_ensino = 2 THEN cc.qt_mat ELSE 0 END) AS "Matrículas_distancia",
        SUM(CASE WHEN cc.tp_modalidade_ensino = 2 THEN cc.qt_conc ELSE 0 END) AS "Concluintes_distancia"

    FROM curso_censo cc
    WHERE cc.municipio = '4204202' AND cc.ano_censo > 2013
    GROUP BY "Área de Conhecimento", cc.ano_censo
    ORDER BY "Área de Conhecimento", cc.ano_censo;
    """

    df = carregar_dataframe(sql)

    # Criar MultiIndex para as colunas
    df.columns = pd.MultiIndex.from_tuples([
        ('', 'Área de Conhecimento'),
        ('', 'Ano'),
        ('Total Geral', 'IES'),
        ('Total Geral', 'Cursos'),
        ('Total Geral', 'Matrículas'),
        ('Total Geral', 'Concluintes'),
        ('Presencial', 'IES'),
        ('Presencial', 'Cursos'),
        ('Presencial', 'Matrículas'),
        ('Presencial', 'Concluintes'),
        ('A Distância', 'IES'),
        ('A Distância', 'Cursos'),
        ('A Distância', 'Matrículas'),
        ('A Distância', 'Concluintes')
    ])

    if not df.empty:
        # Salvar em Excel
        excel_output_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'tabelas', 'dinamicas_area.xlsx')
        try:
            os.makedirs(os.path.dirname(excel_output_path), exist_ok=True)
            # Flatten MultiIndex columns for Excel export
            df_excel = df.copy()
            df_excel.columns = ['_'.join(col).strip() for col in df_excel.columns.values]
            df_excel.to_excel(excel_output_path, index=False)
            print(f"Arquivo Excel gerado com sucesso em: {excel_output_path}")
        except IOError as e:
            print(f"Erro ao salvar o arquivo Excel: {e}")

        # Define formatadores para alinhamento e formatação de número
        formatters = {
            'Ano': lambda x: f'<p style="text-align: left;">{x}</p>',
            'Área de Conhecimento': lambda x: f'<p style="text-align: left;">{x}</p>',
            'IES_total': lambda x: f'<p style="text-align: right;">{x:,}</p>'.replace(',', '.'),
            'Cursos_total': lambda x: f'<p style="text-align: right;">{x:,}</p>'.replace(',', '.'),
            'Matrículas_total': lambda x: f'<p style="text-align: right;">{x:,}</p>'.replace(',', '.'),
            'Concluintes_total': lambda x: f'<p style="text-align: right;">{x:,}</p>'.replace(',', '.'),
            'IES_presencial': lambda x: f'<p style="text-align: right;">{x:,}</p>'.replace(',', '.'),
            'Cursos_presencial': lambda x: f'<p style="text-align: right;">{x:,}</p>'.replace(',', '.'),
            'Matrículas_presencial': lambda x: f'<p style="text-align: right;">{x:,}</p>'.replace(',', '.'),
            'Concluintes_presencial': lambda x: f'<p style="text-align: right;">{x:,}</p>'.replace(',', '.'),
            'IES_distancia': lambda x: f'<p style="text-align: right;">{x:,}</p>'.replace(',', '.'),
            'Cursos_distancia': lambda x: f'<p style="text-align: right;">{x:,}</p>'.replace(',', '.'),
            'Matrículas_distancia': lambda x: f'<p style="text-align: right;">{x:,}</p>'.replace(',', '.'),
            'Concluintes_distancia': lambda x: f'<p style="text-align: right;">{x:,}</p>'.replace(',', '.'),
        }

        # Gerar HTML com formatação ABNT
        # Manually create the HTML table header for multi-level columns
        header_html = """
        <thead>
            <tr>
                <th rowspan="2">Área de Conhecimento</th>
                <th rowspan="2">Ano</th>
                <th colspan="4">Total Geral</th>
                <th colspan="4">Presencial</th>
                <th colspan="4">A Distância</th>
            </tr>
            <tr>
                <th>IES</th>
                <th>Cursos</th>
                <th>Matrículas</th>
                <th>Concluintes</th>
                <th>IES</th>
                <th>Cursos</th>
                <th>Matrículas</th>
                <th>Concluintes</th>
                <th>IES</th>
                <th>Cursos</th>
                <th>Matrículas</th>
                <th>Concluintes</th>
            </tr>
        </thead>
        """
        # Generate the table body
        tabela_body_html = df.to_html(
            index=False,
            na_rep='-',
            formatters=formatters,
            escape=False, # Permite que as tags de estilo sejam renderizadas
            header=False # Do not generate header, we will add it manually
        )
        # Combine header and body
                        tabela_html = f"<table class=\"table table-striped table-bordered\">{header_html}<tbody>{body_rows_html}</tbody></table>"

    else:
        tabela_html = "<p>Não foram encontrados dados para a análise em Chapecó.</p>"

    # Novo texto de análise
    analise_texto = """
    <div class="row justify-content-center mt-4">
        <div class="col-lg-10 col-xl-8">
            <p class="text-justify chart-commentary">A análise dos dados do ensino superior em Chapecó, abrangendo o período de 2014 a 2023, revela um panorama complexo e dinâmico, marcado por tendências de consolidação, crescimento exponencial e desalinhamentos estratégicos entre a oferta de cursos e a demanda discente. A evolução das matrículas e da oferta de vagas por área de conhecimento reflete não apenas as aspirações profissionais da população, mas também as transformações do mercado de trabalho e a forte influência da matriz econômica regional, ancorada na agroindústria. Uma leitura crítica dos números permite identificar movimentos setoriais distintos que delineiam os desafios e as oportunidades para o desenvolvimento do capital humano na região.</p>
            <p class="text-justify chart-commentary mt-3">A área de Administração e Negócios demonstra uma hegemonia consolidada ao longo de toda a década, posicionando-se como o principal polo de atração de estudantes. Com um número de matrículas que ultrapassou 8.200 em 2023 e uma expansão notável na oferta de cursos, que saltou de 79 para 364, este campo evidencia sua centralidade. Tal predominância pode ser atribuída à sua natureza transversal e à percepção de alta empregabilidade, sendo uma formação essencial para a gestão dos mais diversos setores econômicos, desde o comércio e serviços até as complexas cadeias produtivas da agroindústria local. A pulverização da oferta, possivelmente associada à expansão do ensino a distância (EAD), democratizou o acesso, respondendo a uma demanda por qualificações gerenciais que sustentam a pujança econômica regional.</p>
            <p class="text-justify chart-commentary mt-3">Em paralelo, um crescimento exponencial é observado nas áreas de Saúde e Informática, que se destacam como os vetores mais potentes da expansão do ensino superior no período. A área da Saúde mais do que dobrou seu número de matriculados, enquanto a oferta de cursos se multiplicou por oito. De forma similar, a área de Informática duplicou suas matrículas e experimentou uma explosão na oferta de cursos, que cresceu quase dez vezes. Este fenômeno está intrinsecamente ligado a macrotendências contemporâneas: o aumento da expectativa de vida e da preocupação com o bem-estar impulsionam a Saúde, enquanto a transformação digital de todos os setores da economia, incluindo a modernização do agronegócio (Agro 4.0), gera uma demanda crescente e urgente por profissionais de tecnologia da informação.</p>
            <p class="text-justify chart-commentary mt-3">Um movimento paradoxal, contudo, caracteriza a área das Engenharias. Enquanto as instituições de ensino superior promoveram uma massiva expansão na oferta de cursos, que aumentou de 24 para 116, a demanda discente seguiu a trajetória oposta, com uma retração superior a 30% no número de matrículas desde o pico registrado em 2015. Este desalinhamento entre oferta e procura pode ser interpretado como um reflexo de crises econômicas passadas que impactaram setores como a construção civil, além de uma possível migração de talentos para a área de TI, percebida como mais dinâmica e com barreiras de entrada mais flexíveis. O cenário aponta para uma capacidade ociosa e a necessidade de reavaliar a atratividade e o alinhamento desses cursos com as novas demandas do mercado.</p>
            <p class="text-justify chart-commentary mt-3">Por fim, as Ciências Agrárias, embora estratégicas para a identidade econômica de Chapecó, apresentam números de matrícula estáveis, porém modestos, que parecem desproporcionais à sua importância regional. A estabilidade na casa dos 1.300 alunos, mesmo com um leve aumento na oferta de cursos, sugere um potencial de crescimento ainda inexplorado. Tal fato pode indicar uma percepção defasada sobre as carreiras do agronegócio ou uma desconexão entre os currículos tradicionais e as competências exigidas pela agricultura moderna, que é cada vez mais tecnológica e digital. Simultaneamente, a área da Educação mantém uma base sólida e constante de alunos, cumprindo seu papel perene na formação de profissionais essenciais para a sociedade, com sua expansão na oferta de cursos atendendo a uma demanda contínua e vocacional.</p>
            <p class="text-justify chart-commentary mt-3">Em síntese, o ecossistema de ensino superior de Chapecó encontra-se em uma encruzilhada, sustentado por áreas tradicionais como a Administração, mas impulsionado por novos motores de crescimento como Saúde e TI. Os dados revelam um alinhamento bem-sucedido entre mercado e formação nessas áreas ascendentes, mas também expõem desequilíbrios críticos, como o paradoxo das Engenharias e, principalmente, o potencial subaproveitado das Ciências Agrárias. A oportunidade estratégica para a região reside na promoção de sinergias interdisciplinares, notadamente na intersecção entre agronegócio, tecnologia e engenharia, a fim de fortalecer sua vocação econômica com inovação e atrair os talentos necessários para garantir seu desenvolvimento sustentável no cenário contemporâneo.</p>
        </div>
    </div>
    """

    # Conteúdo HTML final
    html_content = f"""
    <div class="table-responsive">
        {tabela_html}
    </div>
    {analise_texto}
    """

    # Salvar o arquivo HTML
    output_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'tabelas', 'dinamicas_area.html')
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"Arquivo HTML (formato dissertação) gerado com sucesso em: {output_path}")
    except IOError as e:
        print(f"Erro ao salvar o arquivo HTML: {e}")

if __name__ == '__main__':
    gerar_tabela_dissertacao_area_chapeco_html()
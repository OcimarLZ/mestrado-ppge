"""
Módulo de consultas SQL para dados PACs.
Todas as consultas filtram por município = "4204202" e período 2014-2024.
"""

def get_sql_pacs_ies_global():
    """Consulta para dados globais de IES PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        COUNT(DISTINCT c.ies) AS QtdeIes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_ies_por_rede():
    """Consulta para dados de IES PACs por rede"""
    return """
    SELECT
        c.ano_censo AS ano,
        r.nome AS rede,
        COUNT(DISTINCT c.ies) AS QtdeIes
    FROM
        curso_censo c
    JOIN tp_rede r ON r.codigo = c.tp_rede
    WHERE
        c.ano_censo >= 2014 
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, r.nome
    ORDER BY
        c.ano_censo, r.nome
    """

def get_sql_pacs_ies_por_categoria():
    """Consulta para dados de IES PACs por categoria administrativa"""
    return """
    SELECT
        c.ano_censo AS ano,
        ca.nome AS categoria,
        COUNT(DISTINCT c.ies) AS QtdeIes
    FROM
        curso_censo c
    JOIN tp_categoria_administrativa ca ON ca.codigo = c.categoria
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, ca.nome
    ORDER BY
        c.ano_censo, ca.nome
    """

def get_sql_pacs_ies_campus():
    """Consulta para dados de campus (IES presenciais) PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        COUNT(DISTINCT c.ies) AS QtdeIes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_ies_polo():
    """Consulta para dados de polo (IES a distância) PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        COUNT(DISTINCT c.ies) AS QtdeIes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """



def get_sql_pacs_docentes_global():
    """Consulta para dados globais de docentes PACs"""
    return """
    SELECT
        d.ano_censo AS ano,
        SUM(d.qt_doc_total) AS Docentes
    FROM
        ies_censo d
    WHERE
        d.ano_censo >= 2014
        AND d.municipio = '4204202'
    GROUP BY
        d.ano_censo
    ORDER BY
        d.ano_censo
    """

def get_sql_pacs_docentes_por_titulacao(tipo_titulacao):
    """Consulta para dados de docentes PACs por titulação"""
    mapeamento_titulacao = {
        'dout': 'qt_doc_ex_dout',
        'mest': 'qt_doc_ex_mest', 
        'esp': 'qt_doc_ex_esp',
        'grad': 'COALESCE(qt_doc_ex_grad, 0) + COALESCE(qt_doc_ex_sem_grad, 0)'
    }
    
    campo = mapeamento_titulacao.get(tipo_titulacao, 'qt_doc_ex_dout')
    
    return f"""
    SELECT
        d.ano_censo AS ano,
        SUM({campo}) AS Docentes
    FROM
        ies_censo d
    WHERE
        d.ano_censo >= 2014
        AND d.municipio = '4204202'
    GROUP BY
        d.ano_censo
    ORDER BY
        d.ano_censo
    """

def get_sql_pacs_docentes_filtrados():
    """Consulta para dados de docentes PACs filtrados por categoria"""
    return """
    SELECT
        d.ano_censo AS ano,
        SUM(d.qt_doc_total) AS Docentes
    FROM
        ies_censo d
    WHERE
        d.ano_censo >= 2014
        AND d.municipio = '4204202'
    GROUP BY
        d.ano_censo
    ORDER BY
        d.ano_censo
    """

def get_sql_pacs_docentes_por_titulacao_filtrados(tipo_titulacao):
    """Consulta para dados de docentes PACs por titulação filtrados"""
    mapeamento_titulacao = {
        'dout': 'qt_doc_ex_dout',
        'mest': 'qt_doc_ex_mest', 
        'esp': 'qt_doc_ex_esp',
        'grad': 'COALESCE(qt_doc_ex_grad, 0) + COALESCE(qt_doc_ex_sem_grad, 0)'
    }
    
    campo = mapeamento_titulacao.get(tipo_titulacao, 'qt_doc_ex_dout')
    
    return f"""
    SELECT
        d.ano_censo AS ano,
        SUM({campo}) AS Docentes
    FROM
        ies_censo d
    WHERE
        d.ano_censo >= 2014
        AND d.municipio = '4204202'
    GROUP BY
        d.ano_censo
    ORDER BY
        d.ano_censo
    """

def get_sql_pacs_docentes_por_categoria():
    """Consulta para dados de docentes PACs por categoria"""
    return """
    SELECT
        d.ano_censo AS ano,
        c.nome AS categoria,
        SUM(d.qt_doc_total) AS Docentes
    FROM
        ies_censo d
    JOIN tp_categoria_administrativa c ON c.codigo = d.categoria
    WHERE
        d.ano_censo >= 2014
        AND d.municipio = '4204202'
    GROUP BY
        d.ano_censo, c.nome
    ORDER BY
        d.ano_censo, c.nome
    """

def get_sql_pacs_docentes_por_titulacao_por_categoria(tipo_titulacao):
    """Consulta para dados de docentes PACs por titulação e categoria"""
    mapeamento_titulacao = {
        'dout': 'qt_doc_ex_dout',
        'mest': 'qt_doc_ex_mest', 
        'esp': 'qt_doc_ex_esp',
        'grad': 'COALESCE(qt_doc_ex_grad, 0) + COALESCE(qt_doc_ex_sem_grad, 0)'
    }
    
    campo = mapeamento_titulacao.get(tipo_titulacao, 'qt_doc_ex_dout')
    
    return f"""
    SELECT
        d.ano_censo AS ano,
        c.nome AS categoria,
        SUM({campo}) AS Docentes
    FROM
        ies_censo d
    JOIN tp_categoria_administrativa c ON c.codigo = d.categoria
    WHERE
        d.ano_censo >= 2014
        AND d.municipio = '4204202'
    GROUP BY
        d.ano_censo, c.nome
    ORDER BY
        d.ano_censo, c.nome
    """

def get_sql_pacs_cursos_global():
    """Consulta para dados globais de cursos PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        COUNT(DISTINCT c.codigo) AS QtdeCursos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_cursos_por_rede():
    """Consulta para dados de cursos PACs por rede"""
    return """
    SELECT
        c.ano_censo AS ano,
        r.nome AS rede,
        COUNT(DISTINCT c.codigo) AS QtdeCursos
    FROM
        curso_censo c
    JOIN tp_rede r ON r.codigo = c.tp_rede
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, r.nome
    ORDER BY
        c.ano_censo, r.nome
    """

def get_sql_pacs_cursos_por_categoria():
    """Consulta para dados de cursos PACs por categoria"""
    return """
    SELECT
        c.ano_censo AS ano,
        ca.nome AS categoria,
        COUNT(DISTINCT c.codigo) AS QtdeCursos
    FROM
        curso_censo c
    JOIN tp_categoria_administrativa ca ON ca.codigo = c.categoria
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, ca.nome
    ORDER BY
        c.ano_censo, ca.nome
    """

def get_sql_pacs_licenciaturas_global():
    """Consulta para dados globais de licenciaturas PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        COUNT(DISTINCT c.codigo) AS QtdeCursos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_licenciaturas_por_rede():
    """Consulta para dados de licenciaturas PACs por rede"""
    return """
    SELECT
        c.ano_censo AS ano,
        r.nome AS rede,
        COUNT(DISTINCT c.codigo) AS QtdeCursos
    FROM
        curso_censo c
    JOIN tp_rede r ON r.codigo = c.tp_rede
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, r.nome
    ORDER BY
        c.ano_censo, r.nome
    """

def get_sql_pacs_licenciaturas_por_categoria():
    """Consulta para dados de licenciaturas PACs por categoria"""
    return """
    SELECT
        c.ano_censo AS ano,
        ca.nome AS categoria,
        COUNT(DISTINCT c.codigo) AS QtdeCursos
    FROM
        curso_censo c
    JOIN tp_categoria_administrativa ca ON ca.codigo = c.categoria
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, ca.nome
    ORDER BY
        c.ano_censo, ca.nome
    """

# Adicionar consultas para vagas, inscritos, ingressos, matrículas, concluintes, evadidos, etc.

# Consultas para vagas
def get_sql_pacs_vagas_totais():
    """Consulta para dados de vagas totais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_vg_total) AS Vagas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_vagas_por_modalidade():
    """Consulta para dados de vagas PACs por modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_vg_total) AS Vagas
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_pacs_vagas_licenciaturas_por_modalidade():
    """Consulta para dados de vagas de licenciaturas PACs por modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_vg_total) AS Vagas
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_pacs_vagas_licenciaturas_por_categoria_modalidade():
    """Consulta para dados de vagas de licenciaturas PACs por categoria e modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        ca.nome AS categoria,
        m.nome AS modalidade,
        SUM(c.qt_vg_total) AS Vagas
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    JOIN tp_categoria_administrativa ca ON ca.codigo = c.categoria
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, ca.nome, m.nome
    ORDER BY
        c.ano_censo, ca.nome, m.nome
    """

# Consultas para inscritos
def get_sql_pacs_inscritos_totais():
    """Consulta para dados de inscritos totais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_inscrito_total) AS Inscritos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_inscritos_por_modalidade():
    """Consulta para dados de inscritos PACs por modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_inscrito_total) AS Inscritos
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_pacs_inscritos_licenciaturas_por_modalidade():
    """Consulta para dados de inscritos de licenciaturas PACs por modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_inscrito_total) AS Inscritos
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_pacs_inscritos_licenciaturas_por_categoria_modalidade():
    """Consulta para dados de inscritos de licenciaturas PACs por categoria e modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        ca.nome AS categoria,
        m.nome AS modalidade,
        SUM(c.qt_inscrito_total) AS Inscritos
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    JOIN tp_categoria_administrativa ca ON ca.codigo = c.categoria
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, ca.nome, m.nome
    ORDER BY
        c.ano_censo, ca.nome, m.nome
    """

# Consultas para ingressos
def get_sql_pacs_ingressos_totais():
    """Consulta para dados de ingressos totais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing) AS Ingressos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_ingressos_por_modalidade():
    """Consulta para dados de ingressos PACs por modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_ing) AS Ingressos
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_pacs_ingressos_licenciaturas_por_modalidade():
    """Consulta para dados de ingressos de licenciaturas PACs por modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_ing) AS Ingressos
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_pacs_ingressos_licenciaturas_por_categoria_modalidade():
    """Consulta para dados de ingressos de licenciaturas PACs por categoria e modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        ca.nome AS categoria,
        m.nome AS modalidade,
        SUM(c.qt_ing) AS Ingressos
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    JOIN tp_categoria_administrativa ca ON ca.codigo = c.categoria
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, ca.nome, m.nome
    ORDER BY
        c.ano_censo, ca.nome, m.nome
    """

# Consultas para matrículas
def get_sql_pacs_matriculas_totais():
    """Consulta para dados de matrículas totais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat) AS Matriculas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_por_modalidade():
    """Consulta para dados de matrículas PACs por modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_mat) AS Matriculas
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo >= 2014
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_pacs_matriculas_licenciaturas_por_modalidade():
    """Consulta para dados de matrículas de licenciaturas PACs por modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_mat) AS Matriculas
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_pacs_matriculas_licenciaturas_por_categoria_modalidade():
    """Consulta para dados de matrículas de licenciaturas PACs por categoria e modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        ca.nome AS categoria,
        m.nome AS modalidade,
        SUM(c.qt_mat) AS Matriculas
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    JOIN tp_categoria_administrativa ca ON ca.codigo = c.categoria
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, ca.nome, m.nome
    ORDER BY
        c.ano_censo, ca.nome, m.nome
    """

# Consultas para concluintes
def get_sql_pacs_concluintes_totais():
    """Consulta para dados de concluintes totais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc) AS Concluintes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_concluintes_por_modalidade():
    """Consulta para dados de concluintes PACs por modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_conc) AS Concluintes
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_pacs_concluintes_licenciaturas_por_modalidade():
    """Consulta para dados de concluintes de licenciaturas PACs por modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_conc) AS Concluintes
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_pacs_concluintes_licenciaturas_por_categoria_modalidade():
    """Consulta para dados de concluintes de licenciaturas PACs por categoria e modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        ca.nome AS categoria,
        m.nome AS modalidade,
        SUM(c.qt_conc) AS Concluintes
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    JOIN tp_categoria_administrativa ca ON ca.codigo = c.categoria
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, ca.nome, m.nome
    ORDER BY
        c.ano_censo, ca.nome, m.nome
    """

# Consultas para matrículas trancadas
def get_sql_pacs_matriculas_trancadas_totais():
    """Consulta para dados de matrículas trancadas totais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_sit_trancada) AS MatriculasTrancadas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_trancadas_por_modalidade():
    """Consulta para dados de matrículas trancadas PACs por modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_sit_trancada) AS MatriculasTrancadas
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_pacs_matriculas_trancadas_licenciaturas_por_modalidade():
    """Consulta para dados de matrículas trancadas de licenciaturas PACs por modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_sit_trancada) AS MatriculasTrancadas
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_pacs_matriculas_trancadas_licenciaturas_por_categoria_modalidade():
    """Consulta para dados de matrículas trancadas de licenciaturas PACs por categoria e modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        ca.nome AS categoria,
        m.nome AS modalidade,
        SUM(c.qt_sit_trancada) AS MatriculasTrancadas
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    JOIN tp_categoria_administrativa ca ON ca.codigo = c.categoria
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, ca.nome, m.nome
    ORDER BY
        c.ano_censo, ca.nome, m.nome
    """

# Consultas para evadidos
def get_sql_pacs_evadidos_totais():
    """Consulta para dados de evadidos totais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_sit_desvinculado + c.qt_sit_transferido + c.qt_sit_falecido) AS Evadidos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_evadidos_por_modalidade():
    """Consulta para dados de evadidos PACs por modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_sit_desvinculado + c.qt_sit_transferido + c.qt_sit_falecido) AS Evadidos
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_pacs_evadidos_licenciaturas_por_modalidade():
    """Consulta para dados de evadidos de licenciaturas PACs por modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_sit_desvinculado + c.qt_sit_transferido + c.qt_sit_falecido) AS Evadidos
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_pacs_evadidos_licenciaturas_por_categoria_modalidade():
    """Consulta para dados de evadidos de licenciaturas PACs por categoria e modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        ca.nome AS categoria,
        m.nome AS modalidade,
        SUM(c.qt_sit_desvinculado + c.qt_sit_transferido + c.qt_sit_falecido) AS Evadidos
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    JOIN tp_categoria_administrativa ca ON ca.codigo = c.categoria
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo, ca.nome, m.nome
    ORDER BY
        c.ano_censo, ca.nome, m.nome
    """

# Consultas para turno (diurno/noturno) - licenciaturas presenciais
def get_sql_pacs_ingressos_licenciaturas_presencial_diurno():
    """Consulta para dados de ingressos diurnos de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_diurno) AS Ingressos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_ingressos_licenciaturas_presencial_noturno():
    """Consulta para dados de ingressos noturnos de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_noturno) AS Ingressos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_licenciaturas_presencial_diurno():
    """Consulta para dados de matrículas diurnas de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_diurno) AS Matriculas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_licenciaturas_presencial_noturno():
    """Consulta para dados de matrículas noturnas de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_noturno) AS Matriculas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_concluintes_licenciaturas_presencial_diurno():
    """Consulta para dados de concluintes diurnos de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_diurno) AS Concluintes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_concluintes_licenciaturas_presencial_noturno():
    """Consulta para dados de concluintes noturnos de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_noturno) AS Concluintes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
        P BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

# Consultas para gênero - presencial e a distância
def get_sql_pacs_ingressos_presencial_masculino():
    """Consulta para dados de ingressos masculinos presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_masc) AS Ingressos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_ingressos_presencial_feminino():
    """Consulta para dados de ingressos femininos presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_fem) AS Ingressos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_ingressos_distancia_masculino():
    """Consulta para dados de ingressos masculinos a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_masc) AS Ingressos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_ingressos_distancia_feminino():
    """Consulta para dados de ingressos femininos a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_fem) AS Ingressos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_presencial_masculino():
    """Consulta para dados de matrículas masculinas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_masc) AS Matriculas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_presencial_feminino():
    """Consulta para dados de matrículas femininas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_fem) AS Matriculas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_distancia_masculino():
    """Consulta para dados de matrículas masculinas a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_masc) AS Matriculas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_distancia_feminino():
    """Consulta para dados de matrículas femininas a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_fem) AS Matriculas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_concluintes_presencial_masculino():
    """Consulta para dados de concluintes masculinos presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_masc) AS Concluintes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_concluintes_presencial_feminino():
    """Consulta para dados de concluintes femininos presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_fem) AS Concluintes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_concluintes_distancia_masculino():
    """Consulta para dados de concluintes masculinos a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_masc) AS Concluintes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_concluintes_distancia_feminino():
    """Consulta para dados de concluintes femininos a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_fem) AS Concluintes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

# Consultas para escola pública
def get_sql_pacs_ingressos_escola_publica():
    """Consulta para dados de ingressos de escola pública PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_rvredepublica) AS Ingressos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_escola_publica():
    """Consulta para dados de matrículas de escola pública PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_rvredepublica) AS Matriculas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_concluintes_escola_publica():
    """Consulta para dados de concluintes de escola pública PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_rvredepublica) AS Concluintes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

# Consultas para raça/cor - presencial e a distância
def get_sql_pacs_ingressos_presencial_parda():
    """Consulta para dados de ingressos pardos de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_parda) AS Ingressos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_ingressos_presencial_amarela():
    """Consulta para dados de ingressos amarelos de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_amarela) AS Ingressos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_ingressos_presencial_indigena():
    """Consulta para dados de ingressos indígenas de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_indigena) AS Ingressos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_ingressos_presencial_preta():
    """Consulta para dados de ingressos pretos de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_preta) AS Ingressos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_ingressos_presencial_branca():
    """Consulta para dados de ingressos brancos de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_branca) AS Ingressos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_ingressos_presencial_cornd():
    """Consulta para dados de ingressos cornd de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_cornd) AS Ingressos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_ingressos_distancia_parda():
    """Consulta para dados de ingressos pardos de licenciaturas a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_parda) AS Ingressos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_ingressos_distancia_amarela():
    """Consulta para dados de ingressos amarelos de licenciaturas a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_amarela) AS Ingressos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_ingressos_distancia_indigena():
    """Consulta para dados de ingressos indígenas de licenciaturas a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_indigena) AS Ingressos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_ingressos_distancia_preta():
    """Consulta para dados de ingressos pretos de licenciaturas a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_preta) AS Ingressos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_ingressos_distancia_branca():
    """Consulta para dados de ingressos brancos de licenciaturas a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_branca) AS Ingressos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_ingressos_distancia_cornd():
    """Consulta para dados de ingressos cornd de licenciaturas a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_cornd) AS Ingressos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_presencial_parda():
    """Consulta para dados de matrículas pardas de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_parda) AS Matriculas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_presencial_amarela():
    """Consulta para dados de matrículas amarelas de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_amarela) AS Matriculas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_presencial_indigena():
    """Consulta para dados de matrículas indígenas de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_indigena) AS Matriculas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_presencial_preta():
    """Consulta para dados de matrículas pretas de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_preta) AS Matriculas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_presencial_branca():
    """Consulta para dados de matrículas brancas de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_branca) AS Matriculas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_presencial_cornd():
    """Consulta para dados de matrículas cornd de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_cornd) AS Matriculas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_distancia_parda():
    """Consulta para dados de matrículas pardas de licenciaturas a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_parda) AS Matriculas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_distancia_amarela():
    """Consulta para dados de matrículas amarelas de licenciaturas a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_amarela) AS Matriculas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_distancia_indigena():
    """Consulta para dados de matrículas indígenas de licenciaturas a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_indigena) AS Matriculas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_distancia_preta():
    """Consulta para dados de matrículas pretas de licenciaturas a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_preta) AS Matriculas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_distancia_branca():
    """Consulta para dados de matrículas brancas de licenciaturas a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_branca) AS Matriculas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_matriculas_distancia_cornd():
    """Consulta para dados de matrículas cornd de licenciaturas a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_cornd) AS Matriculas
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_concluintes_presencial_parda():
    """Consulta para dados de concluintes pardos de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_parda) AS Concluintes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_concluintes_presencial_amarela():
    """Consulta para dados de concluintes amarelos de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_amarela) AS Concluintes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_concluintes_presencial_indigena():
    """Consulta para dados de concluintes indígenas de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_indigena) AS Concluintes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_concluintes_presencial_preta():
    """Consulta para dados de concluintes pretos de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_preta) AS Concluintes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_concluintes_presencial_branca():
    """Consulta para dados de concluintes brancos de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_branca) AS Concluintes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_concluintes_presencial_cornd():
    """Consulta para dados de concluintes cornd de licenciaturas presenciais PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_cornd) AS Concluintes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_concluintes_distancia_parda():
    """Consulta para dados de concluintes pardos de licenciaturas a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_parda) AS Concluintes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_concluintes_distancia_amarela():
    """Consulta para dados de concluintes amarelos de licenciaturas a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_amarela) AS Concluintes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_concluintes_distancia_indigena():
    """Consulta para dados de concluintes indígenas de licenciaturas a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_indigena) AS Concluintes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_concluintes_distancia_preta():
    """Consulta para dados de concluintes pretos de licenciaturas a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_preta) AS Concluintes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_concluintes_distancia_branca():
    """Consulta para dados de concluintes brancos de licenciaturas a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_branca) AS Concluintes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_pacs_concluintes_distancia_cornd():
    """Consulta para dados de concluintes cornd de licenciaturas a distância PACs"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_cornd) AS Concluintes
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2014 AND c.ano_censo <= 2024
        AND c.municipio = '4204202'
        AND c.tp_modalidade_ensino = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """ 
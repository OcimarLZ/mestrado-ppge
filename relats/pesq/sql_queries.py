"""
Módulo contendo todas as consultas SQL organizadas por categoria.
Facilita a manutenção e reutilização das consultas.
"""

# =============================================================================
# CONSULTAS SQL PARA DADOS DE IES
# =============================================================================

def get_sql_ies_global():
    """Consulta para dados globais de IES"""
    return """
    SELECT
        i.ano_censo AS ano,
        COUNT(DISTINCT i.ies) AS QtdeIes
    FROM
        ies_censo i
    WHERE
        i.ano_censo >= 2005
    GROUP BY
        i.ano_censo
    ORDER BY
        i.ano_censo
    """

def get_sql_ies_por_rede():
    """Consulta para dados de IES por rede"""
    return """
    SELECT
        i.ano_censo AS ano,
        CASE 
            WHEN i.categoria IN (1,2,3) THEN 'Públicas'
            WHEN i.categoria IN (4,7) THEN 'Privadas com Fins Lucrativo'
            ELSE 'Privadas Sem Fins Lucrativo'
        END AS rede, 
        COUNT(DISTINCT i.ies) AS QtdeIes  
    FROM
        ies_censo i
    WHERE
        i.ano_censo >= 2005
    GROUP BY
        i.ano_censo, rede
    ORDER BY
        i.ano_censo, rede
    """

def get_sql_ies_por_categoria():
    """Consulta para dados de IES por categoria administrativa"""
    return """
    SELECT
        i.ano_censo AS ano,
        ca.nome AS categoria,
        COUNT(DISTINCT i.ies) AS QtdeIes  
    FROM
        ies_censo i
    JOIN tp_categoria_administrativa ca ON ca.codigo = i.categoria
    WHERE
        i.ano_censo >= 2005
    GROUP BY
        i.ano_censo, ca.nome
    ORDER BY
        i.ano_censo, ca.nome
    """

# =============================================================================
# CONSULTAS SQL PARA DADOS DE MUNICÍPIOS
# =============================================================================

def get_sql_municipios_com_ies():
    """Consulta para dados de municípios com IES"""
    return """
    SELECT
        i.ano_censo AS ano,
        COUNT(DISTINCT i.municipio) AS QtdeMunicipios  
    FROM
        ies_censo i
    WHERE
        i.ano_censo >= 2005
    GROUP BY
        i.ano_censo
    ORDER BY
        i.ano_censo
    """

def get_sql_municipios_com_cursos():
    """Consulta para dados de municípios com cursos"""
    return """
    SELECT
        c.ano_censo AS ano,
        COUNT(DISTINCT c.municipio) AS QtdeMunicipios  
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2005
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_municipios_com_cursos_licenciatura():
    """Consulta para dados de municípios com cursos de licenciatura"""
    return """
    SELECT
        c.ano_censo AS ano,
        COUNT(DISTINCT c.municipio) AS QtdeMunicipios  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004 
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_municipios_com_cursos_licenciatura_por_modalidade():
    """Consulta para dados de municípios com cursos de licenciatura por modalidade de ensino"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        COUNT(DISTINCT c.municipio) AS QtdeMunicipios  
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo > 2004 
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_municipios_com_cursos_licenciatura_por_categoria_modalidade():
    """Consulta para dados de municípios com cursos de licenciatura por categoria administrativa e modalidade"""
    return """
    SELECT
        c.ano_censo AS ano,
        ca.nome AS categoria,
        m.nome AS modalidade,
        COUNT(DISTINCT c.municipio) AS QtdeMunicipios  
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    JOIN tp_categoria_administrativa ca ON ca.codigo = c.categoria  
    WHERE
        c.ano_censo > 2004 
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo, ca.nome, m.nome
    ORDER BY
        c.ano_censo, ca.nome, m.nome
    """

# =============================================================================
# CONSULTAS SQL PARA DADOS DE DOCENTES
# =============================================================================

def get_sql_docentes_global():
    """Consulta para dados globais de docentes"""
    return """
    SELECT
        i.ano_censo AS ano,
        SUM(i.qt_doc_total) AS Docentes
    FROM
        ies_censo i
    WHERE
        i.ano_censo >= 2005 
    GROUP BY
        i.ano_censo
    ORDER BY
        i.ano_censo
    """

def get_sql_docentes_por_titulacao(tipo_titulacao):
    """
    Consulta para dados de docentes por titulação
    
    Args:
        tipo_titulacao (str): Tipo de titulação ('dout', 'mest', 'esp', 'grad')
    """
    mapeamento_titulacao = {
        'dout': 'qt_doc_ex_dout',
        'mest': 'qt_doc_ex_mest', 
        'esp': 'qt_doc_ex_esp',
        'grad': 'COALESCE(qt_doc_ex_grad, 0) + COALESCE(qt_doc_ex_sem_grad, 0)'
    }
    
    campo = mapeamento_titulacao.get(tipo_titulacao, 'qt_doc_ex_dout')
    
    return f"""
    SELECT
        i.ano_censo AS ano,
        SUM({campo}) AS Docentes
    FROM
        ies_censo i
    WHERE
        i.ano_censo >= 2005 
    GROUP BY
        i.ano_censo
    ORDER BY
        i.ano_censo
    """

def get_sql_docentes_filtrados():
    """Consulta para dados de docentes filtrados (categorias específicas)"""
    return """
    SELECT
        i.ano_censo AS ano,
        SUM(i.qt_doc_total) AS Docentes
    FROM
        ies_censo i
    WHERE
        i.ano_censo >= 2005 
        AND i.categoria IN (1,2,3,5,7,8,9)
    GROUP BY
        i.ano_censo
    ORDER BY
        i.ano_censo
    """

def get_sql_docentes_por_titulacao_filtrados(tipo_titulacao):
    """
    Consulta para dados de docentes por titulação filtrados
    
    Args:
        tipo_titulacao (str): Tipo de titulação ('dout', 'mest', 'esp', 'grad')
    """
    mapeamento_titulacao = {
        'dout': 'qt_doc_ex_dout',
        'mest': 'qt_doc_ex_mest', 
        'esp': 'qt_doc_ex_esp',
        'grad': 'COALESCE(qt_doc_ex_grad, 0) + COALESCE(qt_doc_ex_sem_grad, 0)'
    }
    
    campo = mapeamento_titulacao.get(tipo_titulacao, 'qt_doc_ex_dout')
    
    return f"""
    SELECT
        i.ano_censo AS ano,
        SUM({campo}) AS Docentes
    FROM
        ies_censo i
    WHERE
        i.ano_censo >= 2005 
        AND i.categoria IN (1,2,3,5,7,8,9)
    GROUP BY
        i.ano_censo
    ORDER BY
        i.ano_censo
    """

def get_sql_docentes_por_categoria():
    """Consulta para dados de docentes por categoria administrativa"""
    return """
    SELECT
        i.ano_censo AS ano,
        ca.nome AS categoria,
        SUM(i.qt_doc_total) AS Docentes
    FROM
        ies_censo i
    JOIN tp_categoria_administrativa ca ON ca.codigo = i.categoria
    WHERE
        i.ano_censo >= 2005 
        AND i.categoria IN (1,2,3,5,7,8,9)
    GROUP BY
        i.ano_censo, ca.nome
    ORDER BY
        i.ano_censo, ca.nome
    """

def get_sql_docentes_por_titulacao_por_categoria(tipo_titulacao):
    """
    Consulta para dados de docentes por titulação e categoria
    
    Args:
        tipo_titulacao (str): Tipo de titulação ('dout', 'mest', 'esp', 'grad')
    """
    mapeamento_titulacao = {
        'dout': 'qt_doc_ex_dout',
        'mest': 'qt_doc_ex_mest', 
        'esp': 'qt_doc_ex_esp',
        'grad': 'COALESCE(qt_doc_ex_grad, 0) + COALESCE(qt_doc_ex_sem_grad, 0)'
    }
    
    campo = mapeamento_titulacao.get(tipo_titulacao, 'qt_doc_ex_dout')
    
    return f"""
    SELECT
        i.ano_censo AS ano,
        ca.nome AS categoria,
        SUM({campo}) AS Docentes
    FROM
        ies_censo i
    JOIN tp_categoria_administrativa ca ON ca.codigo = i.categoria
    WHERE
        i.ano_censo >= 2005 
        AND i.categoria IN (1,2,3,5,7,8,9)
    GROUP BY
        i.ano_censo, ca.nome
    ORDER BY
        i.ano_censo, ca.nome
    """

# =============================================================================
# CONSULTAS SQL PARA DADOS DE CURSOS
# =============================================================================

def get_sql_cursos_global():
    """Consulta para dados globais de cursos"""
    return """
    SELECT
        c.ano_censo AS ano,
        COUNT(DISTINCT c.curso) AS QtdeCursos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2005
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_cursos_por_rede():
    """Consulta para dados de cursos por rede"""
    return """
    SELECT
        c.ano_censo AS ano,
        CASE 
            WHEN c.categoria IN (1,2,3) THEN 'Públicas'
            WHEN c.categoria IN (4,7) THEN 'Privadas com Fins Lucrativo'
            ELSE 'Privadas Sem Fins Lucrativo'
        END AS rede, 
        COUNT(DISTINCT c.curso) AS QtdeCursos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2005
    GROUP BY
        c.ano_censo, rede
    ORDER BY
        c.ano_censo, rede
    """

def get_sql_cursos_por_categoria():
    """Consulta para dados de cursos por categoria administrativa"""
    return """
    SELECT
        c.ano_censo AS ano,
        ca.nome AS categoria,
        COUNT(DISTINCT c.curso) AS QtdeCursos  
    FROM
        curso_censo c
    JOIN tp_categoria_administrativa ca ON ca.codigo = c.categoria
    WHERE
        c.ano_censo >= 2005
    GROUP BY
        c.ano_censo, ca.nome
    ORDER BY
        c.ano_censo, ca.nome
    """

# =============================================================================
# CONSULTAS SQL PARA DADOS DE LICENCIATURAS
# =============================================================================

def get_sql_licenciaturas_global():
    """Consulta para dados globais de licenciaturas"""
    return """
    SELECT
        c.ano_censo AS ano,
        COUNT(DISTINCT c.curso) AS QtdeCursos
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2005
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_licenciaturas_por_rede():
    """Consulta para dados de licenciaturas por rede"""
    return """
    SELECT
        c.ano_censo AS ano,
        CASE 
            WHEN c.categoria IN (1,2,3) THEN 'Públicas'
            WHEN c.categoria IN (4,7) THEN 'Privadas com Fins Lucrativo'
            ELSE 'Privadas Sem Fins Lucrativo'
        END AS rede, 
        COUNT(DISTINCT c.curso) AS QtdeCursos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo >= 2005
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo, rede
    ORDER BY
        c.ano_censo, rede
    """

def get_sql_licenciaturas_por_categoria():
    """Consulta para dados de licenciaturas por categoria administrativa"""
    return """
    SELECT
        c.ano_censo AS ano,
        ca.nome AS categoria,
        COUNT(DISTINCT c.curso) AS QtdeCursos  
    FROM
        curso_censo c
    JOIN tp_categoria_administrativa ca ON ca.codigo = c.categoria
    WHERE
        c.ano_censo >= 2005
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo, ca.nome
    ORDER BY
        c.ano_censo, ca.nome
    """ 

def get_sql_vagas_totais():
    """Consulta para dados de vagas totais por ano"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_vg_total) AS Vagas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """ 

def get_sql_vagas_por_modalidade():
    """Consulta para dados de vagas por modalidade de ensino"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_vg_total) AS Vagas  
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo > 2004
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """ 

def get_sql_vagas_licenciaturas_por_modalidade():
    """Consulta para dados de vagas de licenciaturas por modalidade de ensino"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_vg_total) AS Vagas  
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo > 2004
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """ 

def get_sql_vagas_licenciaturas_por_categoria_modalidade():
    """Consulta para dados de vagas de licenciaturas por categoria administrativa e modalidade"""
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
        c.ano_censo > 2004
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo, ca.nome, m.nome
    ORDER BY
        c.ano_censo, ca.nome, m.nome
    """ 

def get_sql_inscritos_totais():
    """Consulta para dados de inscritos totais por ano"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_inscrito_total) AS Inscritos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_inscritos_por_modalidade():
    """Consulta para dados de inscritos por modalidade de ensino"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_inscrito_total) AS Inscritos  
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo > 2004
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_inscritos_licenciaturas_por_modalidade():
    """Consulta para dados de inscritos de licenciaturas por modalidade de ensino"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_inscrito_total) AS Inscritos  
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo > 2004
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_inscritos_licenciaturas_por_categoria_modalidade():
    """Consulta para dados de inscritos de licenciaturas por categoria administrativa e modalidade"""
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
        c.ano_censo > 2004
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo, ca.nome, m.nome
    ORDER BY
        c.ano_censo, ca.nome, m.nome
    """ 

def get_sql_ingressos_totais():
    """Consulta para dados de ingressos totais por ano"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing) AS Ingressos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_ingressos_por_modalidade():
    """Consulta para dados de ingressos por modalidade de ensino"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_ing) AS Ingressos  
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo > 2004
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_ingressos_licenciaturas_por_modalidade():
    """Consulta para dados de ingressos de licenciaturas por modalidade de ensino"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_ing) AS Ingressos  
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo > 2004
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_ingressos_licenciaturas_por_categoria_modalidade():
    """Consulta para dados de ingressos de licenciaturas por categoria administrativa e modalidade"""
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
        c.ano_censo > 2004
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo, ca.nome, m.nome
    ORDER BY
        c.ano_censo, ca.nome, m.nome
    """ 

def get_sql_matriculas_totais():
    """Consulta para dados de matrículas totais por ano"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat) AS Matriculas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_matriculas_por_modalidade():
    """Consulta para dados de matrículas por modalidade de ensino"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_mat) AS Matriculas  
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo > 2004
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_matriculas_licenciaturas_por_modalidade():
    """Consulta para dados de matrículas de licenciaturas por modalidade de ensino"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_mat) AS Matriculas  
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo > 2004
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_matriculas_licenciaturas_por_categoria_modalidade():
    """Consulta para dados de matrículas de licenciaturas por categoria administrativa e modalidade"""
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
        c.ano_censo > 2004
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo, ca.nome, m.nome
    ORDER BY
        c.ano_censo, ca.nome, m.nome
    """ 

def get_sql_concluintes_totais():
    """Consulta para dados de concluintes totais por ano"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc) AS Concluintes  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_concluintes_por_modalidade():
    """Consulta para dados de concluintes por modalidade de ensino"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_conc) AS Concluintes  
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo > 2004
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_concluintes_licenciaturas_por_modalidade():
    """Consulta para dados de concluintes de licenciaturas por modalidade de ensino"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_conc) AS Concluintes  
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo > 2004
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_concluintes_licenciaturas_por_categoria_modalidade():
    """Consulta para dados de concluintes de licenciaturas por categoria administrativa e modalidade"""
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
        c.ano_censo > 2004
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo, ca.nome, m.nome
    ORDER BY
        c.ano_censo, ca.nome, m.nome
    """ 

def get_sql_matriculas_trancadas_totais():
    """Consulta para dados de matrículas trancadas totais por ano"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_sit_trancada) AS MatriculasTrancadas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_matriculas_trancadas_por_modalidade():
    """Consulta para dados de matrículas trancadas por modalidade de ensino"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_sit_trancada) AS MatriculasTrancadas  
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo > 2004
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_matriculas_trancadas_licenciaturas_por_modalidade():
    """Consulta para dados de matrículas trancadas de licenciaturas por modalidade de ensino"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_sit_trancada) AS MatriculasTrancadas  
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo > 2004
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_matriculas_trancadas_licenciaturas_por_categoria_modalidade():
    """Consulta para dados de matrículas trancadas de licenciaturas por categoria administrativa e modalidade"""
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
        c.ano_censo > 2004
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo, ca.nome, m.nome
    ORDER BY
        c.ano_censo, ca.nome, m.nome
    """ 

def get_sql_evadidos_totais():
    """Consulta para dados de evadidos totais por ano"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_sit_desvinculado + c.qt_sit_transferido + c.qt_sit_falecido) AS Evadidos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_evadidos_por_modalidade():
    """Consulta para dados de evadidos por modalidade de ensino"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_sit_desvinculado + c.qt_sit_transferido + c.qt_sit_falecido) AS Evadidos  
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo > 2004
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_evadidos_licenciaturas_por_modalidade():
    """Consulta para dados de evadidos de licenciaturas por modalidade de ensino"""
    return """
    SELECT
        c.ano_censo AS ano,
        m.nome AS modalidade,
        SUM(c.qt_sit_desvinculado + c.qt_sit_transferido + c.qt_sit_falecido) AS Evadidos  
    FROM
        curso_censo c
    JOIN tp_modalidade_ensino m ON m.codigo = c.tp_modalidade_ensino
    WHERE
        c.ano_censo > 2004
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo, m.nome
    ORDER BY
        c.ano_censo, m.nome
    """

def get_sql_evadidos_licenciaturas_por_categoria_modalidade():
    """Consulta para dados de evadidos de licenciaturas por categoria administrativa e modalidade"""
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
        c.ano_censo > 2004
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo, ca.nome, m.nome
    ORDER BY
        c.ano_censo, ca.nome, m.nome
    """ 

def get_sql_ingressos_licenciaturas_presencial_diurno():
    """Consulta para dados de ingressos diurnos de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_diurno) AS Ingressos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_grau_academico = 2
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_ingressos_licenciaturas_presencial_noturno():
    """Consulta para dados de ingressos noturnos de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_noturno) AS Ingressos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_grau_academico = 2
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_matriculas_licenciaturas_presencial_diurno():
    """Consulta para dados de matrículas diurnas de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_diurno) AS Matriculas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_grau_academico = 2
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_matriculas_licenciaturas_presencial_noturno():
    """Consulta para dados de matrículas noturnas de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_noturno) AS Matriculas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_grau_academico = 2
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_concluintes_licenciaturas_presencial_diurno():
    """Consulta para dados de concluintes diurnos de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_diurno) AS Concluintes  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_grau_academico = 2
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_concluintes_licenciaturas_presencial_noturno():
    """Consulta para dados de concluintes noturnos de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_noturno) AS Concluintes  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_grau_academico = 2
        AND c.tp_modalidade_ensino = 1
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """ 

def get_sql_ingressos_presencial_masculino():
    """Consulta para dados de ingressos masculinos de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_masc) AS Ingressos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_ingressos_presencial_feminino():
    """Consulta para dados de ingressos femininos de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_fem) AS Ingressos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_matriculas_presencial_masculino():
    """Consulta para dados de matrículas masculinas de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_masc) AS Matriculas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_matriculas_presencial_feminino():
    """Consulta para dados de matrículas femininas de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_fem) AS Matriculas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_concluintes_presencial_masculino():
    """Consulta para dados de concluintes masculinos de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_masc) AS Concluintes  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_concluintes_presencial_feminino():
    """Consulta para dados de concluintes femininos de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_fem) AS Concluintes  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """ 

def get_sql_ingressos_escola_publica():
    """Consulta para dados de ingressos vindos de escolas públicas"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_rvredepublica) AS Ingressos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_matriculas_escola_publica():
    """Consulta para dados de matrículas vindas de escolas públicas"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_rvredepublica) AS Matriculas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_concluintes_escola_publica():
    """Consulta para dados de concluintes vindos de escolas públicas"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_rvredepublica) AS Concluintes  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """ 

def get_sql_ingressos_distancia_masculino():
    """Consulta para dados de ingressos masculinos de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_masc) AS Ingressos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_ingressos_distancia_feminino():
    """Consulta para dados de ingressos femininos de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_fem) AS Ingressos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_matriculas_distancia_masculino():
    """Consulta para dados de matrículas masculinas de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_masc) AS Matriculas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_matriculas_distancia_feminino():
    """Consulta para dados de matrículas femininas de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_fem) AS Matriculas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_concluintes_distancia_masculino():
    """Consulta para dados de concluintes masculinos de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_masc) AS Concluintes  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_concluintes_distancia_feminino():
    """Consulta para dados de concluintes femininos de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_fem) AS Concluintes  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """ 

# Consultas para dados de raça/cor - Presencial
def get_sql_ingressos_presencial_parda():
    """Consulta para dados de ingressos pardos de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_parda) AS Ingressos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_ingressos_presencial_amarela():
    """Consulta para dados de ingressos amarelos de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_amarela) AS Ingressos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_ingressos_presencial_indigena():
    """Consulta para dados de ingressos indígenas de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_indigena) AS Ingressos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_ingressos_presencial_preta():
    """Consulta para dados de ingressos pretos de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_preta) AS Ingressos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_ingressos_presencial_branca():
    """Consulta para dados de ingressos brancos de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_branca) AS Ingressos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_ingressos_presencial_cornd():
    """Consulta para dados de ingressos cornd de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_cornd) AS Ingressos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

# Consultas para dados de raça/cor - A Distância
def get_sql_ingressos_distancia_parda():
    """Consulta para dados de ingressos pardos de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_parda) AS Ingressos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_ingressos_distancia_amarela():
    """Consulta para dados de ingressos amarelos de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_amarela) AS Ingressos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_ingressos_distancia_indigena():
    """Consulta para dados de ingressos indígenas de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_indigena) AS Ingressos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_ingressos_distancia_preta():
    """Consulta para dados de ingressos pretos de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_preta) AS Ingressos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_ingressos_distancia_branca():
    """Consulta para dados de ingressos brancos de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_branca) AS Ingressos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_ingressos_distancia_cornd():
    """Consulta para dados de ingressos cornd de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_ing_cornd) AS Ingressos  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

# Consultas para matrículas por raça/cor - Presencial
def get_sql_matriculas_presencial_parda():
    """Consulta para dados de matrículas pardas de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_parda) AS Matriculas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_matriculas_presencial_amarela():
    """Consulta para dados de matrículas amarelas de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_amarela) AS Matriculas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_matriculas_presencial_indigena():
    """Consulta para dados de matrículas indígenas de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_indigena) AS Matriculas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_matriculas_presencial_preta():
    """Consulta para dados de matrículas pretas de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_preta) AS Matriculas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_matriculas_presencial_branca():
    """Consulta para dados de matrículas brancas de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_branca) AS Matriculas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_matriculas_presencial_cornd():
    """Consulta para dados de matrículas cornd de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_cornd) AS Matriculas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

# Consultas para matrículas por raça/cor - A Distância
def get_sql_matriculas_distancia_parda():
    """Consulta para dados de matrículas pardas de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_parda) AS Matriculas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_matriculas_distancia_amarela():
    """Consulta para dados de matrículas amarelas de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_amarela) AS Matriculas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_matriculas_distancia_indigena():
    """Consulta para dados de matrículas indígenas de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_indigena) AS Matriculas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_matriculas_distancia_preta():
    """Consulta para dados de matrículas pretas de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_preta) AS Matriculas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_matriculas_distancia_branca():
    """Consulta para dados de matrículas brancas de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_branca) AS Matriculas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_matriculas_distancia_cornd():
    """Consulta para dados de matrículas cornd de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_mat_cornd) AS Matriculas  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

# Consultas para concluintes por raça/cor - Presencial
def get_sql_concluintes_presencial_parda():
    """Consulta para dados de concluintes pardos de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_parda) AS Concluintes  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_concluintes_presencial_amarela():
    """Consulta para dados de concluintes amarelos de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_amarela) AS Concluintes  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_concluintes_presencial_indigena():
    """Consulta para dados de concluintes indígenas de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_indigena) AS Concluintes  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_concluintes_presencial_preta():
    """Consulta para dados de concluintes pretos de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_preta) AS Concluintes  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_concluintes_presencial_branca():
    """Consulta para dados de concluintes brancos de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_branca) AS Concluintes  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_concluintes_presencial_cornd():
    """Consulta para dados de concluintes cornd de licenciaturas presenciais"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_cornd) AS Concluintes  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 1
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

# Consultas para concluintes por raça/cor - A Distância
def get_sql_concluintes_distancia_parda():
    """Consulta para dados de concluintes pardos de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_parda) AS Concluintes  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_concluintes_distancia_amarela():
    """Consulta para dados de concluintes amarelos de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_amarela) AS Concluintes  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_concluintes_distancia_indigena():
    """Consulta para dados de concluintes indígenas de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_indigena) AS Concluintes  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_concluintes_distancia_preta():
    """Consulta para dados de concluintes pretos de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_preta) AS Concluintes  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_concluintes_distancia_branca():
    """Consulta para dados de concluintes brancos de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_branca) AS Concluintes  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """

def get_sql_concluintes_distancia_cornd():
    """Consulta para dados de concluintes cornd de licenciaturas a distância"""
    return """
    SELECT
        c.ano_censo AS ano,
        SUM(c.qt_conc_cornd) AS Concluintes  
    FROM
        curso_censo c
    WHERE
        c.ano_censo > 2004
        AND c.tp_modalidade_ensino = 2
        AND c.tp_grau_academico = 2
    GROUP BY
        c.ano_censo
    ORDER BY
        c.ano_censo
    """ 
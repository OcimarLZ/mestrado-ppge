# -*- coding: utf-8 -*-
"""Script INDIVIDUAL para o Power Query (Get Data > Python script). Gera SO a tabela
dim_curso. Ver README.md na pasta powerbi/.
"""
import sqlite3

import pandas as pd

DB_PATH = "D:/Mestrado/Dados/bdados/INEP.db"

con = sqlite3.connect(DB_PATH)

# Oferta especifica do curso, com o nome bruto dado pela propria instituicao (ex: "3
# cursos de Pedagogia" na mesma IES tem 3 codigos de curso diferentes aqui, mesmo
# compartilhando o mesmo cine_rotulo). A ligacao curso -> cine_rotulo (tipo padronizado)
# ja vem direto na FATO (fato_curso_censo.codigo_cine_rotulo), nao precisa repetir aqui.
dim_curso = pd.read_sql_query(
    """
    SELECT
        codigo          AS codigo_curso,
        nome            AS nome_curso,
        fl_uab
    FROM superior_curso
    """,
    con,
)
con.close()

# -*- coding: utf-8 -*-
"""Script INDIVIDUAL para o Power Query (Get Data > Python script). Gera SO a tabela
dim_territorio. Ver README.md na pasta powerbi/ para o porque de cada tabela ter seu
proprio script em vez de um unico script com todas as variaveis.
"""
import sqlite3

import pandas as pd

DB_PATH = "D:/Mestrado/Dados/bdados/INEP.db"

con = sqlite3.connect(DB_PATH)

# Hierarquia territorial completa (municipio -> microrregiao -> mesorregiao -> UF ->
# regiao) numa UNICA tabela ja achatada -- modelo em estrela: liga direto na fato por
# codigo_municipio, sem nenhuma dimensao encadeada em outra dimensao.
dim_territorio = pd.read_sql_query(
    """
    SELECT
        CAST(m.codigo AS INTEGER) AS codigo_municipio,
        m.nome          AS nome_municipio,
        mic.codigo      AS codigo_microrregiao,
        mic.nome        AS nome_microrregiao,
        mes.codigo      AS codigo_mesorregiao,
        mes.nome        AS nome_mesorregiao,
        uf.sigla        AS sigla_uf,
        uf.nome         AS nome_uf,
        r.codigo        AS codigo_regiao,
        r.nome          AS nome_regiao,
        m.regiao_intermediaria,
        m.regiao_imediata
    FROM comum_municipio m
    LEFT JOIN comum_microrregiao mic ON mic.codigo = m.microrregiao
    LEFT JOIN comum_mesorregiao mes ON mes.codigo = m.mesorregiao
    LEFT JOIN comum_uf uf ON uf.sigla = m.uf
    LEFT JOIN comum_regiao r ON r.codigo = uf.regiao
    """,
    con,
)
con.close()

dim_territorio["codigo_municipio"] = pd.to_numeric(dim_territorio["codigo_municipio"], downcast="integer")

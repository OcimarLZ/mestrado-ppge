# -*- coding: utf-8 -*-
"""Script INDIVIDUAL para o Power Query (Get Data > Python script). Gera SO a tabela
dim_organizacao_academica. Ver README.md na pasta powerbi/.
"""
import sqlite3

import pandas as pd

DB_PATH = "D:/Mestrado/Dados/bdados/INEP.db"

con = sqlite3.connect(DB_PATH)
dim_organizacao_academica = pd.read_sql_query(
    "SELECT codigo AS codigo_organizacao_academica, nome AS nome_organizacao_academica FROM superior_tp_organizacao_academica",
    con,
)
con.close()

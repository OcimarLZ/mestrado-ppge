# -*- coding: utf-8 -*-
"""Script INDIVIDUAL para o Power Query (Get Data > Python script). Gera SO a tabela
dim_grau_academico. Ver README.md na pasta powerbi/.
"""
import sqlite3

import pandas as pd

DB_PATH = "D:/Mestrado/Dados/bdados/INEP.db"

con = sqlite3.connect(DB_PATH)
dim_grau_academico = pd.read_sql_query(
    "SELECT codigo AS codigo_grau_academico, nome AS nome_grau_academico FROM superior_tp_grau_academico",
    con,
)
con.close()

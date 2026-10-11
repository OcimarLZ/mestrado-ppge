# -*- coding: utf-8 -*-
"""Script INDIVIDUAL para o Power Query (Get Data > Python script). Gera SO a tabela
dim_mantenedora (entidade mantenedora da IES). Ver README.md na pasta powerbi/.
"""
import sqlite3

import pandas as pd

DB_PATH = "D:/Mestrado/Dados/bdados/INEP.db"

con = sqlite3.connect(DB_PATH)
dim_mantenedora = pd.read_sql_query(
    "SELECT codigo AS codigo_mantenedora, nome AS nome_mantenedora FROM superior_mantenedora",
    con,
)
con.close()

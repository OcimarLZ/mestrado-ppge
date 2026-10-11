# -*- coding: utf-8 -*-
"""Script INDIVIDUAL para o Power Query (Get Data > Python script). Gera SO a tabela
dim_rede. Ver README.md na pasta powerbi/.
"""
import sqlite3

import pandas as pd

DB_PATH = "D:/Mestrado/Dados/bdados/INEP.db"

con = sqlite3.connect(DB_PATH)
dim_rede = pd.read_sql_query(
    "SELECT codigo AS codigo_rede, nome AS nome_rede FROM superior_tp_rede",
    con,
)
con.close()

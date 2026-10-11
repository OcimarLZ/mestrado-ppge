# -*- coding: utf-8 -*-
"""Script INDIVIDUAL para o Power Query (Get Data > Python script). Gera SO a tabela
dim_modalidade_ensino. Ver README.md na pasta powerbi/.
"""
import sqlite3

import pandas as pd

DB_PATH = "D:/Mestrado/Dados/bdados/INEP.db"

con = sqlite3.connect(DB_PATH)
dim_modalidade_ensino = pd.read_sql_query(
    "SELECT codigo AS codigo_modalidade_ensino, nome AS nome_modalidade_ensino FROM superior_tp_modal_ensino",
    con,
)
con.close()

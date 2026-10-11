# -*- coding: utf-8 -*-
"""Script INDIVIDUAL para o Power Query (Get Data > Python script). Gera SO a tabela
dim_ano (tabela calendario simplificada -- so ano, sem mes/dia). Ver README.md na pasta
powerbi/.
"""
import pandas as pd

ANO_MIN = 2005
ANO_MAX = 2024

dim_ano = pd.DataFrame({"codigo_ano": range(ANO_MIN, ANO_MAX + 1)})
dim_ano["decada"] = (dim_ano["codigo_ano"] // 10 * 10).astype(str) + "s"
dim_ano["periodo_pne_2014_2024"] = dim_ano["codigo_ano"].between(2014, 2024)

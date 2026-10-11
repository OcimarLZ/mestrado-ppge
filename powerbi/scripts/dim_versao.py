# -*- coding: utf-8 -*-
"""Script INDIVIDUAL para o Power Query (Get Data > Python script). Gera SO a tabela
dim_versao (rastreabilidade: quando os dados foram extraidos do banco). Ver README.md na
pasta powerbi/.
"""
from datetime import datetime, timezone

import pandas as pd

ANO_MIN = 2005
ANO_MAX = 2024

dim_versao = pd.DataFrame(
    {
        "data_extracao": [datetime.now(timezone.utc).isoformat()],
        "fonte": ["INEP - Censo da Educação Superior (microdados)"],
        "ano_min": [ANO_MIN],
        "ano_max": [ANO_MAX],
    }
)

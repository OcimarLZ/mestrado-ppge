import pandas as pd
import json
from bdados.ler_bdados_to_df import carregar_dataframe

# Monta o SQL para dados por turno
sql = """
SELECT 
    cc.ano_censo AS ano,
    SUM(CASE WHEN cc.tp_turno = 1 THEN cc.qt_ing ELSE 0 END) AS ingressantes_diurno,
    SUM(CASE WHEN cc.tp_turno = 2 THEN cc.qt_ing ELSE 0 END) AS ingressantes_noturno,
    SUM(CASE WHEN cc.tp_turno = 1 THEN cc.qt_conc ELSE 0 END) AS concluintes_diurno,
    SUM(CASE WHEN cc.tp_turno = 2 THEN cc.qt_conc ELSE 0 END) AS concluintes_noturno,
    SUM(CASE WHEN cc.tp_turno = 1 THEN cc.qt_mat ELSE 0 END) AS matriculas_diurno,
    SUM(CASE WHEN cc.tp_turno = 2 THEN cc.qt_mat ELSE 0 END) AS matriculas_noturno
FROM 
    curso_censo cc
WHERE 
    cc.municipio = 4204202 AND cc.ano_censo > 2013
GROUP BY 
    cc.ano_censo
ORDER BY 
    cc.ano_censo;
"""

df = carregar_dataframe(sql)

# Preparar dados para o JSON
dados_json = {
    "anos": df['ano'].tolist(),
    "ingressantes_diurno": df['ingressantes_diurno'].tolist(),
    "ingressantes_noturno": df['ingressantes_noturno'].tolist(),
    "concluintes_diurno": df['concluintes_diurno'].tolist(),
    "concluintes_noturno": df['concluintes_noturno'].tolist(),
    "matriculas_diurno": df['matriculas_diurno'].tolist(),
    "matriculas_noturno": df['matriculas_noturno'].tolist()
}

# Salvar como JSON
with open('../acs/dados_discentes_turno.json', 'w', encoding='utf-8') as f:
    json.dump(dados_json, f, ensure_ascii=False, indent=2)

print('Arquivo dados_discentes_turno.json criado com sucesso!')
print(f'Dados gerados para os anos: {dados_json["anos"]}')
print(f'Total de registros: {len(dados_json["anos"])}')
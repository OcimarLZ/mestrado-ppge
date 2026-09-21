import configparser
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

def carregar_engine() -> object:
    root = Path(__file__).resolve().parents[2]
    config_path = root / "config.ini"
    default_sqlite = root / "INEP.db"

    if not config_path.exists():
        return create_engine(f"sqlite:///{default_sqlite.as_posix()}")

    parser = configparser.ConfigParser()
    parser.read(config_path, encoding="utf-8")

    if "BD_INEP" not in parser:
        return create_engine(f"sqlite:///{default_sqlite.as_posix()}")

    bd = parser["BD_INEP"]
    sgdb = bd.get("SGDB", "sqlite").strip().lower()

    if sgdb == "sqlite":
        pasta_local = bd.get("PASTA_LOCAL", "").replace("\\", "/")
        arquivo = bd.get("DW", "INEP.db").strip()
        if pasta_local:
            sqlite_path = Path(pasta_local.strip("/")) / arquivo
        else:
            sqlite_path = default_sqlite

        if not sqlite_path.exists():
            sqlite_path = default_sqlite

        return create_engine(f"sqlite:///{sqlite_path.as_posix()}")

    return create_engine(f"sqlite:///{default_sqlite.as_posix()}")

def main():
    engine = carregar_engine()
    print("Executando a consulta e gerando a planilha...")
    
    sql = """
    WITH base AS (
        SELECT DISTINCT
            i.codigo AS ies_codigo,
            i.nome AS ies_nome,
            i.sigla,
            i.estado
        FROM ies i
        LEFT JOIN uab_censo uc ON i.codigo = uc.ies 
                               AND uc.tp_grau_academico = 2 
                               AND uc.ano_censo > 2013
        WHERE i.categoria = 1 
          AND i.org_academica = 1
          AND i.nome NOT LIKE 'Universidade codigo%'
    ),
    ult_ano_presencial AS (
        SELECT ies, MAX(ano_censo) as ult_ano
        FROM curso_censo
        WHERE tp_grau_academico = 2 AND tp_modalidade_ensino = 1
        GROUP BY ies
    ),
    mun_presencial_ult_ano AS (
        SELECT c.ies, COUNT(DISTINCT c.municipio) as qtd_mun_presencial, COUNT(DISTINCT c.curso) as qtd_cursos_presencial
        FROM curso_censo c
        JOIN ult_ano_presencial u ON c.ies = u.ies AND c.ano_censo = u.ult_ano
        WHERE c.tp_grau_academico = 2 AND c.tp_modalidade_ensino = 1
        GROUP BY c.ies
    ),
    ult_ano_ead AS (
        SELECT ies, MAX(ano_censo) as ult_ano
        FROM curso_censo
        WHERE tp_grau_academico = 2 AND tp_modalidade_ensino = 2
        GROUP BY ies
    ),
    mun_ead_ult_ano AS (
        SELECT c.ies, COUNT(DISTINCT c.municipio) as qtd_mun_ead, COUNT(DISTINCT c.curso) as qtd_cursos_ead
        FROM curso_censo c
        JOIN ult_ano_ead u ON c.ies = u.ies AND c.ano_censo = u.ult_ano
        WHERE c.tp_grau_academico = 2 AND c.tp_modalidade_ensino = 2
        GROUP BY c.ies
    ),
    ult_ano_uab AS (
        SELECT ies, MAX(ano_censo) as ult_ano
        FROM uab_censo
        WHERE tp_grau_academico = 2 AND situacao_polo = 'Ativo'
        GROUP BY ies
    ),
    polos_uab_ult_ano AS (
        SELECT c.ies, COUNT(DISTINCT c.id_polo) as qtd_polos_uab, COUNT(DISTINCT c.nm_curso) as qtd_cursos_uab
        FROM uab_censo c
        JOIN ult_ano_uab u ON c.ies = u.ies AND c.ano_censo = u.ult_ano
        WHERE c.tp_grau_academico = 2 AND c.situacao_polo = 'Ativo'
        GROUP BY c.ies
    ),
    matriculas_2024 AS (
        SELECT 
            c.ies,
            SUM(c.qt_mat) AS tot_mat,
            SUM(CASE WHEN c.tp_grau_academico = 2 THEN c.qt_mat ELSE 0 END) AS tot_mat_lic,
            SUM(CASE WHEN c.tp_grau_academico = 2 AND c.tp_modalidade_ensino = 2 AND u.municipio IS NULL THEN c.qt_mat ELSE 0 END) AS tot_mat_lic_ead_proprios,
            SUM(CASE WHEN c.tp_grau_academico = 2 AND c.tp_modalidade_ensino = 2 AND u.municipio IS NOT NULL THEN c.qt_mat ELSE 0 END) AS tot_mat_lic_ead_uab
        FROM curso_censo c
        LEFT JOIN (
            SELECT DISTINCT ies, ano_censo, municipio 
            FROM uab_censo 
            WHERE tp_grau_academico = 2
        ) u ON c.ies = u.ies AND c.ano_censo = u.ano_censo AND c.municipio = u.municipio
        WHERE c.ano_censo = 2024
        GROUP BY c.ies
    )
    SELECT 
        b.ies_nome,
        b.sigla,
        b.estado,
        CASE WHEN up.ult_ano = 2024 THEN 'Sim' WHEN up.ult_ano IS NULL THEN 'Não' ELSE 'Até ' || CAST(up.ult_ano AS VARCHAR) END AS a_ultimo_ano_presencial,
        COALESCE(mp.qtd_mun_presencial, 0) AS b_qtd_mun_presencial,
        COALESCE(mp.qtd_cursos_presencial, 0) AS b_qtd_cursos_presencial,
        CASE WHEN ue.ult_ano = 2024 THEN 'Sim' WHEN ue.ult_ano IS NULL THEN 'Não' ELSE 'Até ' || CAST(ue.ult_ano AS VARCHAR) END AS c_ultimo_ano_ead,
        COALESCE(me.qtd_mun_ead, 0) AS d_qtd_mun_ead,
        COALESCE(me.qtd_cursos_ead, 0) AS d_qtd_cursos_ead,
        CASE WHEN uu.ult_ano = 2024 THEN 'Sim' WHEN uu.ult_ano IS NULL THEN 'Não' ELSE 'Até ' || CAST(uu.ult_ano AS VARCHAR) END AS e_ultimo_ano_uab,
        COALESCE(pu.qtd_polos_uab, 0) AS f_qtd_polos_uab,
        COALESCE(pu.qtd_cursos_uab, 0) AS f_qtd_cursos_uab,
        COALESCE(m24.tot_mat, 0) AS g_total_matriculas_2024,
        COALESCE(m24.tot_mat_lic, 0) AS h_total_matriculas_lic_2024,
        COALESCE(m24.tot_mat_lic_ead_proprios, 0) AS i_mat_lic_ead_proprios,
        COALESCE(m24.tot_mat_lic_ead_uab, 0) AS j_mat_lic_ead_uab
    FROM base b
    LEFT JOIN ult_ano_presencial up ON b.ies_codigo = up.ies
    LEFT JOIN mun_presencial_ult_ano mp ON b.ies_codigo = mp.ies
    LEFT JOIN ult_ano_ead ue ON b.ies_codigo = ue.ies
    LEFT JOIN mun_ead_ult_ano me ON b.ies_codigo = me.ies
    LEFT JOIN ult_ano_uab uu ON b.ies_codigo = uu.ies
    LEFT JOIN polos_uab_ult_ano pu ON b.ies_codigo = pu.ies
    LEFT JOIN matriculas_2024 m24 ON b.ies_codigo = m24.ies
    ORDER BY b.estado, b.ies_nome, b.sigla;
    """
    
    df = pd.read_sql(text(sql), engine)
    
    if df.empty:
        print("Nenhum dado retornado pela consulta.")
        return

    # Percentual de Licenciatura
    df['k_perc_licenciatura'] = (df['h_total_matriculas_lic_2024'] / df['g_total_matriculas_2024'].replace(0, 1) * 100).round(2).astype(str) + '%'
    df.loc[df['g_total_matriculas_2024'] == 0, 'k_perc_licenciatura'] = '0.00%'

    # a) e b) já estão em df['i_mat_lic_ead_proprios'] e df['j_mat_lic_ead_uab']
    
    # c) Percentual de A (Próprios) em relação a coluna 14 (Total Matrículas Licenciatura)
    df['l_perc_ead_proprios'] = (df['i_mat_lic_ead_proprios'] / df['h_total_matriculas_lic_2024'].replace(0, 1) * 100).round(2).astype(str) + '%'
    df.loc[df['h_total_matriculas_lic_2024'] == 0, 'l_perc_ead_proprios'] = '0.00%'

    # d) Percentual de B (UAB) em relação a coluna 14 (Total Matrículas Licenciatura)
    df['m_perc_ead_uab'] = (df['j_mat_lic_ead_uab'] / df['h_total_matriculas_lic_2024'].replace(0, 1) * 100).round(2).astype(str) + '%'
    df.loc[df['h_total_matriculas_lic_2024'] == 0, 'm_perc_ead_uab'] = '0.00%'

    # Reordenando para deixar os percentuais de licenciatura logo depois de suas contagens brutas
    # Ou seguir a ordem exata solicitada "crie mais 4 colunas ao final"
    # A ordem será: 1 a 15 (como antes) + as 4 novas colunas
    df = df[[
        'ies_nome', 'sigla', 'estado', 
        'a_ultimo_ano_presencial', 'b_qtd_mun_presencial', 'b_qtd_cursos_presencial',
        'c_ultimo_ano_ead', 'd_qtd_mun_ead', 'd_qtd_cursos_ead',
        'e_ultimo_ano_uab', 'f_qtd_polos_uab', 'f_qtd_cursos_uab',
        'g_total_matriculas_2024', 'h_total_matriculas_lic_2024', 'k_perc_licenciatura',
        'i_mat_lic_ead_proprios', 'j_mat_lic_ead_uab', 'l_perc_ead_proprios', 'm_perc_ead_uab'
    ]]

    # Renomeando colunas para um output mais amigável
    df.columns = [
        'IES Nome', 'Sigla', 'Estado', 
        'Último Ano Presencial', 'Qtd Mun Presencial', 'Qtd Cursos Presencial',
        'Último Ano EaD', 'Qtd Mun EaD', 'Qtd Cursos EaD',
        'Último Ano UAB', 'Qtd Polos UAB', 'Qtd Cursos UAB',
        'Total Matrículas (2024)', 'Total Matrículas Licenciatura (2024)', '% Licenciatura',
        'Matrículas Lic EaD (Próprios)', 'Matrículas Lic EaD (UAB)',
        '% Lic EaD (Próprios)', '% Lic EaD (UAB)'
    ]

    arquivo_saida = Path(__file__).parent / "planilha_lic_ies_geral_completa.xlsx"
    
    # Gerar o excel com auto-ajuste básico usando pandas excel writer
    with pd.ExcelWriter(arquivo_saida, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Resumo_Geral')
        worksheet = writer.sheets['Resumo_Geral']
        for col in worksheet.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column].width = adjusted_width

    print(f"Planilha gerada com sucesso: {arquivo_saida}")

if __name__ == "__main__":
    main()

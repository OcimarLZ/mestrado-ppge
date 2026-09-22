"""
Exporta o resultado de sqls/cap5/lic_ies_geral.sql (panorama das IES federais que ofertam
licenciatura: presenca por modalidade, abrangencia territorial e matriculas 2024) para um
JSON estatico consumido pela tabela interativa em Pesquisa > Dados por IES.

bdados/INEP.db tem 2,8 GB e esta no .gitignore (nao existe no runner do GitHub Actions),
entao este script roda localmente e o JSON gerado e commitado pronto no repositorio --
mesmo padrao ja usado por web_app/content_export/export_static_site.py para site-content.json.
Sempre que os microdados do INEP forem atualizados, rode este script de novo e comite o JSON.

Roda com sqlite3 puro (stdlib), sem depender do pacote bdados nem do config.ini.
Rode a partir da raiz do repo: python web_app/content_export/export_lic_ies_geral.py
"""
import json
import os
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SQL_PATH = os.path.join(ROOT, "sqls", "cap5", "lic_ies_geral.sql")
DB_PATH = os.path.join(ROOT, "bdados", "INEP.db")
OUT_JSON = os.path.join(ROOT, "web_app", "frontend", "src", "data", "lic_ies_geral.json")

# ies_nome/sigla/estado ficam como estao; as demais colunas do SQL (prefixadas a_/b_/.../j_)
# viram estas chaves mais legiveis no JSON exportado, na mesma ordem em que aparecem na tabela.
COLUMN_LABELS = {
    "ies_nome": "IES Nome",
    "sigla": "Sigla",
    "estado": "Estado",
    "a_ultimo_ano_presencial": "Último Ano Presencial",
    "b_qtd_mun_presencial": "Qtd Municípios Presencial",
    "b_qtd_cursos_presencial": "Qtd Cursos Presencial",
    "c_ultimo_ano_ead": "Último Ano EaD",
    "d_qtd_mun_ead": "Qtd Municípios EaD",
    "d_qtd_cursos_ead": "Qtd Cursos EaD",
    "e_ultimo_ano_uab": "Último Ano UAB",
    "f_qtd_polos_uab": "Qtd Polos UAB",
    "f_qtd_cursos_uab": "Qtd Cursos UAB",
    "g_total_matriculas_2024": "Total Matrículas (2024)",
    "h_total_matriculas_lic_2024": "Matrículas Licenciatura (2024)",
    "i_mat_lic_ead_proprios": "Matrículas Lic. EaD (Polo Próprio)",
    "j_mat_lic_ead_uab": "Matrículas Lic. EaD (UAB)",
}


def main():
    if not os.path.exists(DB_PATH):
        raise SystemExit(
            f"bdados/INEP.db nao encontrado em {DB_PATH}. Este script precisa rodar em uma "
            "maquina com o banco local (nao roda no CI - veja o docstring deste arquivo)."
        )

    sql = open(SQL_PATH, encoding="utf-8").read()
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(sql)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    con.close()

    registros = [dict(zip(cols, row)) for row in rows]

    # Percentuais derivados, uteis para a tabela interativa (evita recalcular no front-end
    # e mantem a mesma logica ja usada em sqls/cap5/gerar_excel_lic_ies_geral.py)
    for r in registros:
        total_lic = r["h_total_matriculas_lic_2024"] or 0
        total_ies = r["g_total_matriculas_2024"] or 0
        r["k_perc_licenciatura"] = round(total_lic / total_ies * 100, 2) if total_ies else 0.0
        r["l_perc_ead_proprios"] = round(r["i_mat_lic_ead_proprios"] / total_lic * 100, 2) if total_lic else 0.0
        r["m_perc_ead_uab"] = round(r["j_mat_lic_ead_uab"] / total_lic * 100, 2) if total_lic else 0.0

    payload = {
        "gerado_em": None,  # preenchido abaixo, sem depender de timezone do runner
        "fonte": "Elaborado pelo autor a partir dos microdados do INEP (Censo da Educação Superior, 2024)",
        "colunas": {**COLUMN_LABELS, "k_perc_licenciatura": "% Licenciatura", "l_perc_ead_proprios": "% Lic. EaD Próprio", "m_perc_ead_uab": "% Lic. EaD UAB"},
        "registros": registros,
    }

    import datetime
    payload["gerado_em"] = datetime.date.today().isoformat()

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"OK: {len(registros)} IES exportadas para {OUT_JSON}")


if __name__ == "__main__":
    main()

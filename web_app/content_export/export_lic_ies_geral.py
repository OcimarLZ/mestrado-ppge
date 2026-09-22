"""
Exporta o resultado de sqls/cap5/lic_ies_geral.sql (panorama das IES federais que ofertam
licenciatura -- matriculas, cursos, campus e polos EaD/UAB, comparando 2014 e 2024) para um
JSON estatico consumido pelos indicadores/graficos/tabela em Pesquisa > Dados por IES.

bdados/INEP.db tem 2,8 GB e esta no .gitignore (nao existe no runner do GitHub Actions),
entao este script roda localmente e o JSON gerado e commitado pronto no repositorio --
mesmo padrao ja usado por web_app/content_export/export_static_site.py para site-content.json.
Sempre que os microdados do INEP forem atualizados, rode este script de novo e comite o JSON.

Roda com sqlite3 puro (stdlib), sem depender do pacote bdados nem do config.ini.
Rode a partir da raiz do repo: python web_app/content_export/export_lic_ies_geral.py
"""
import datetime
import json
import os
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SQL_PATH = os.path.join(ROOT, "sqls", "cap5", "lic_ies_geral.sql")
DB_PATH = os.path.join(ROOT, "bdados", "INEP.db")
OUT_JSON = os.path.join(ROOT, "web_app", "frontend", "src", "data", "lic_ies_geral.json")

COLUMN_LABELS = {
    "ies_nome": "IES Nome",
    "sigla": "Sigla",
    "estado": "Estado",
    "ano_censo": "Ano do Censo",
    "total_matriculas": "Total de Matrículas",
    "total_matriculas_lic": "Matrículas em Licenciatura",
    "num_cursos_lic": "Cursos de Licenciatura",
    "num_campus_presencial": "Campus Presenciais",
    "num_polos_ead_proprio": "Polos EaD Próprio",
    "num_polos_uab": "Polos UAB",
    "mat_lic_presencial": "Matrículas Presencial",
    "mat_lic_ead_proprio": "Matrículas EaD Próprio",
    "mat_lic_uab": "Matrículas UAB",
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

    # Percentuais derivados, uteis para indicadores/tabela (evita recalcular no front-end)
    for r in registros:
        total_lic = r["total_matriculas_lic"] or 0
        total_ies = r["total_matriculas"] or 0
        r["perc_licenciatura"] = round(total_lic / total_ies * 100, 2) if total_ies else 0.0
        r["perc_lic_uab"] = round(r["mat_lic_uab"] / total_lic * 100, 2) if total_lic else 0.0
        r["perc_lic_ead_proprio"] = round(r["mat_lic_ead_proprio"] / total_lic * 100, 2) if total_lic else 0.0

    payload = {
        "gerado_em": datetime.date.today().isoformat(),
        "fonte": "Elaborado pelo autor a partir dos microdados do INEP (Censo da Educação Superior, 2014 e 2024)",
        "anos": [2014, 2024],
        "colunas": {
            **COLUMN_LABELS,
            "perc_licenciatura": "% Licenciatura",
            "perc_lic_uab": "% Lic. UAB",
            "perc_lic_ead_proprio": "% Lic. EaD Próprio",
        },
        "registros": registros,
    }

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"OK: {len(registros)} registros (IES x ano) exportados para {OUT_JSON}")


if __name__ == "__main__":
    main()

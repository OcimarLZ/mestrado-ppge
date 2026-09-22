"""
Exporta o resultado de sqls/cap5/lic_polos_cursos.sql (uma linha por IES x ano x municipio
x tipo de polo x curso, com matriculas) para um JSON estatico consumido pela expansao de
cada polo/campus na pagina de detalhamento (Pesquisa > Detalhamento por campus e polo),
mostrando quais cursos existem em cada polo e quantos matriculados cada um tem.

Mesmo padrao/motivo de export_lic_polos_detalhe.py: bdados/INEP.db (2,8 GB) esta no
.gitignore e nao existe no runner do GitHub Actions, entao este script roda localmente e o
JSON gerado e commitado pronto.

Rode a partir da raiz do repo: python web_app/content_export/export_lic_polos_cursos.py
"""
import datetime
import json
import os
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SQL_PATH = os.path.join(ROOT, "sqls", "cap5", "lic_polos_cursos.sql")
DB_PATH = os.path.join(ROOT, "bdados", "INEP.db")
OUT_JSON = os.path.join(ROOT, "web_app", "frontend", "src", "data", "lic_polos_cursos.json")


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

    payload = {
        "gerado_em": datetime.date.today().isoformat(),
        "fonte": "Elaborado pelo autor a partir dos microdados do INEP (Censo da Educação Superior, 2014 e 2024)",
        "anos": [2014, 2024],
        "registros": registros,
    }

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"OK: {len(registros)} registros (IES x ano x polo x curso) exportados para {OUT_JSON}")


if __name__ == "__main__":
    main()

"""
Congela o conteudo de site_cms.db (+ eventuais consultas sql_query contra bdados/INEP.db)
em um unico JSON estatico, e copia os assets referenciados para web_app/frontend/public/assets/,
para o build do GitHub Pages nao depender de nenhum backend rodando.

Roda com sqlite3 puro (stdlib); so importa pandas se algum sql_query realmente existir.
Rode a partir da raiz do repo: python web_app/content_export/export_static_site.py
"""
import json
import os
import shutil
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKEND_DIR = os.path.join(ROOT, "web_app", "backend")
FRONTEND_DIR = os.path.join(ROOT, "web_app", "frontend")
CMS_DB_PATH = os.path.join(BACKEND_DIR, "site_cms.db")
MICRODATA_DB_PATH = os.path.join(ROOT, "bdados", "INEP.db")
BACKEND_STATIC_DIR = os.path.join(BACKEND_DIR, "static")
FRONTEND_ASSETS_DIR = os.path.join(FRONTEND_DIR, "public", "assets")
OUT_JSON = os.path.join(FRONTEND_DIR, "src", "data", "site-content.json")

# A versao oficial da dissertacao e a que esta em docs/ (nao a copia antiga em
# web_app/backend/static/, que pode ficar desatualizada).
DISSERTACAO_PDF_SRC = os.path.join(ROOT, "docs", "OLZ_Defesa_V_2.03.pdf")

# Os graficos curados sao copiados direto de docs/graficos/ (rastreado no git), nao da
# copia intermediaria em web_app/backend/static/graficos/ (que e local/gitignorada e
# nao existe num checkout limpo do CI).
DOCS_GRAFICOS_DIR = os.path.join(ROOT, "docs", "graficos")

BACKEND_STATIC_PREFIX = "http://127.0.0.1:8000/static/"
GRAFICOS_URL_PREFIX = BACKEND_STATIC_PREFIX + "graficos/"
ASSET_PREFIX = "assets/"  # combinado em runtime com import.meta.env.BASE_URL


def rows_as_dicts(cur, sql, params=()):
    cur.execute(sql, params)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def rewrite_asset_url(url):
    if url and url.startswith(BACKEND_STATIC_PREFIX):
        return ASSET_PREFIX + url[len(BACKEND_STATIC_PREFIX):]
    return url


def run_sql_query(sql):
    import pandas as pd  # import tardio: so precisa existir se algum sql_query estiver setado

    engine_con = sqlite3.connect(MICRODATA_DB_PATH)
    try:
        df = pd.read_sql_query(sql, engine_con)
        return json.loads(df.to_json(orient="records"))
    finally:
        engine_con.close()


def build_tree(items, parent_id=None):
    tree = []
    for item in items:
        if item["parent_id"] == parent_id:
            node = dict(item)
            node["children"] = build_tree(items, item["id"])
            tree.append(node)
    return sorted(tree, key=lambda x: x["order"] or 0)


def get_descendants_flat(items, parent_id):
    result = []
    for item in sorted([i for i in items if i["parent_id"] == parent_id], key=lambda x: x["order"] or 0):
        result.append(item)
        result.extend(get_descendants_flat(items, item["id"]))
    return result


def copy_asset(rel_name):
    src = os.path.join(BACKEND_STATIC_DIR, rel_name)
    dst = os.path.join(FRONTEND_ASSETS_DIR, rel_name)
    if not os.path.exists(src):
        print(f"AVISO: asset nao encontrado, pulando copia: {src}")
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)


def main():
    con = sqlite3.connect(CMS_DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    site_settings = rows_as_dicts(cur, "SELECT * FROM site_settings LIMIT 1")
    site_settings = site_settings[0] if site_settings else {}

    dashboard_summary = rows_as_dicts(cur, "SELECT * FROM dashboard_summary LIMIT 1")
    dashboard_summary = dashboard_summary[0] if dashboard_summary else {}

    home_cards = rows_as_dicts(cur, 'SELECT * FROM home_cards ORDER BY "order" ASC')

    all_pages = rows_as_dicts(cur, 'SELECT * FROM page_content ORDER BY parent_id ASC, "order" ASC')
    all_visuals = rows_as_dicts(cur, 'SELECT * FROM section_visuals ORDER BY "order" ASC')

    grafico_filenames = set()
    for row in all_pages + all_visuals:
        url = row.get("image_url")
        if url and url.startswith(GRAFICOS_URL_PREFIX):
            grafico_filenames.add(url[len(GRAFICOS_URL_PREFIX):])

    visuals_by_page = {}
    for v in all_visuals:
        if v.get("sql_query"):
            v["data"] = run_sql_query(v["sql_query"])
        v["image_url"] = rewrite_asset_url(v.get("image_url"))
        visuals_by_page.setdefault(v["page_content_id"], []).append(v)

    for p in all_pages:
        p["image_url"] = rewrite_asset_url(p.get("image_url"))
        if p.get("sql_query"):
            p["data"] = run_sql_query(p["sql_query"])

    tree = build_tree(all_pages)

    chapters_out = {}
    chapter_rows = [p for p in all_pages if p["parent_id"] is None]
    for chap in chapter_rows:
        descendants = get_descendants_flat(all_pages, chap["id"])
        rows = [chap] + descendants
        chapters_out[chap["slug"]] = [
            {**row, "visuals": visuals_by_page.get(row["id"], [])} for row in rows
        ]

    # Copia os assets referenciados (logos, dissertacao em pdf, graficos curados).
    os.makedirs(FRONTEND_ASSETS_DIR, exist_ok=True)
    if os.path.exists(DISSERTACAO_PDF_SRC):
        shutil.copyfile(DISSERTACAO_PDF_SRC, os.path.join(FRONTEND_ASSETS_DIR, "dissertacao.pdf"))
    else:
        print(f"AVISO: dissertacao nao encontrada em {DISSERTACAO_PDF_SRC}, pulando copia")
    for name in ("logo_uffs.png", "logo_uffs_horizontal.png", "logo_ppge.png"):
        copy_asset(name)
    os.makedirs(os.path.join(FRONTEND_ASSETS_DIR, "graficos"), exist_ok=True)
    for fname in sorted(grafico_filenames):
        src = os.path.join(DOCS_GRAFICOS_DIR, fname)
        if not os.path.exists(src):
            print(f"AVISO: grafico referenciado mas nao encontrado em docs/graficos/: {fname}")
            continue
        shutil.copyfile(src, os.path.join(FRONTEND_ASSETS_DIR, "graficos", fname))

    output = {
        "site_settings": site_settings,
        "dashboard_summary": dashboard_summary,
        "home_cards": home_cards,
        "tree": tree,
        "chapters": chapters_out,
    }

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    con.close()
    print(f"OK: export estatico gerado em {OUT_JSON}")
    print(f"OK: assets copiados para {FRONTEND_ASSETS_DIR}")


if __name__ == "__main__":
    main()

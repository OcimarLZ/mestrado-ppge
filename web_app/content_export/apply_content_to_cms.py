"""
Carrega o conteudo real extraido do .odt (dissertacao_conteudo.json) e os graficos
curados (graficos_selecionados.json) dentro do site_cms.db existente, substituindo os
capitulos placeholder de seed_data.py.

Roda com sqlite3 puro (stdlib) para nao depender do ambiente virtual do backend.
Rode a partir da raiz do repo: python web_app/content_export/apply_content_to_cms.py
"""
import json
import os
import shutil
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTENT_EXPORT = os.path.join(ROOT, "web_app", "content_export")
BACKEND_DIR = os.path.join(ROOT, "web_app", "backend")
DB_PATH = os.path.join(BACKEND_DIR, "site_cms.db")
GRAFICOS_SRC_DIR = os.path.join(ROOT, "docs", "graficos")
GRAFICOS_DST_DIR = os.path.join(BACKEND_DIR, "static", "graficos")

CHAPTER_ICONS = {
    "introducao": "BookOpen",
    "procedimentos-metodologicos": "FlaskConical",
    "as-politicas-de-educacao-superior-como-campo-de-disputas": "Landmark",
    "as-politicas-de-ead-e-a-reconfiguracao-da-educacao-superior-brasileira": "MonitorPlay",
    "a-modalidade-ead-nas-universidades-publicas-federais-analise-dos-indicadores-dos-cursos-de-licenciaturas-2014-2024": "Building2",
    "as-universidades-federais-e-a-ead-politicas-e-estrategias-institucionais": "Users",
    "consideracoes-finais": "Flag",
    "referencias": "Library",
}


def ensure_columns(cur):
    for table, col, coltype in [
        ("page_content", "pdf_page", "INTEGER"),
        ("section_visuals", "pdf_page", "INTEGER"),
    ]:
        try:
            cur.execute(f"ALTER TABLE {table} ADD COLUMN {col} {coltype}")
            print(f"Coluna adicionada: {table}.{col}")
        except sqlite3.OperationalError as e:
            print(f"Coluna {table}.{col} ja existe (ok): {e}")


def load_chapters():
    with open(os.path.join(CONTENT_EXPORT, "dissertacao_conteudo.json"), encoding="utf-8") as f:
        return json.load(f)


def load_visual_selection():
    with open(os.path.join(CONTENT_EXPORT, "graficos_selecionados.json"), encoding="utf-8") as f:
        return json.load(f)


def copy_selected_images(selection):
    os.makedirs(GRAFICOS_DST_DIR, exist_ok=True)
    for item in selection:
        src = os.path.join(GRAFICOS_SRC_DIR, item["file"])
        dst = os.path.join(GRAFICOS_DST_DIR, item["file"])
        if not os.path.exists(src):
            print(f"AVISO: imagem nao encontrada, pulando: {src}")
            continue
        shutil.copyfile(src, dst)


def main():
    chapters = load_chapters()
    selection = load_visual_selection()
    copy_selected_images(selection)

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    ensure_columns(cur)

    # Repopula page_content do zero (hoje so tem placeholders de seed_data.py).
    cur.execute("DELETE FROM section_visuals")
    cur.execute("DELETE FROM page_content")

    slug_to_id = {}
    # Passo 1: insere capitulos e secoes, guarda o id de cada slug.
    for chap in chapters:
        icon = CHAPTER_ICONS.get(chap["slug"])
        cur.execute(
            """INSERT INTO page_content
               (parent_id, slug, title, content, "order", icon_name, content_type)
               VALUES (NULL, ?, ?, ?, ?, ?, 'text')""",
            (chap["slug"], chap["title"], chap["content_html"], chap["order"], icon),
        )
        chap_id = cur.lastrowid
        slug_to_id[chap["slug"]] = chap_id
        for sec in chap["sections"]:
            cur.execute(
                """INSERT INTO page_content
                   (parent_id, slug, title, content, "order", icon_name, content_type)
                   VALUES (?, ?, ?, ?, ?, NULL, 'text')""",
                (chap_id, sec["slug"], sec["title"], sec["content_html"], sec["order"]),
            )
            slug_to_id[sec["slug"]] = cur.lastrowid

    # Passo 2: insere os visuais curados e injeta o token [v:ID] no content do alvo.
    for item in selection:
        target = item["target"]
        target_slug = target.split(":", 1)[1]
        page_id = slug_to_id.get(target_slug)
        if page_id is None:
            print(f"AVISO: slug alvo nao encontrado, pulando visual: {target}")
            continue

        image_url = f"http://127.0.0.1:8000/static/graficos/{item['file']}"
        cur.execute(
            """INSERT INTO section_visuals
               (page_content_id, type, title, source, "order", image_url, pdf_page)
               VALUES (?, 'image', ?, ?, 0, ?, ?)""",
            (page_id, item["title"], item["source"], image_url, item["pdf_page"]),
        )
        visual_id = cur.lastrowid
        cur.execute("SELECT content FROM page_content WHERE id = ?", (page_id,))
        (content,) = cur.fetchone()
        content = (content or "") + f"<p>[v:{visual_id}]</p>"
        cur.execute("UPDATE page_content SET content = ? WHERE id = ?", (content, page_id))

    con.commit()
    cur.execute("SELECT COUNT(*) FROM page_content")
    n_pages = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM section_visuals")
    n_visuals = cur.fetchone()[0]
    con.close()
    print(f"OK: {n_pages} linhas em page_content, {n_visuals} visuais aplicados.")


if __name__ == "__main__":
    main()

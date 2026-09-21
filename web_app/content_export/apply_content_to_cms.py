"""
Carrega o conteudo real extraido do .odt (dissertacao_conteudo.json) e as figuras reais
da dissertacao (dissertacao_figuras_extraidas.json, ver extract_odt_all.py) dentro do
site_cms.db existente, substituindo os capitulos placeholder de seed_data.py.

O content_html de cada capitulo/secao ja vem com marcadores [FIG:chave] no lugar exato
onde o texto referencia a figura (nao no fim da secao) -- este script so precisa trocar
cada [FIG:chave] pelo [v:ID] real depois de inserir a SectionVisual correspondente.

Roda com sqlite3 puro (stdlib) para nao depender do ambiente virtual do backend.
Rode a partir da raiz do repo: python web_app/content_export/apply_content_to_cms.py
"""
import json
import os
import re
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTENT_EXPORT = os.path.join(ROOT, "web_app", "content_export")
BACKEND_DIR = os.path.join(ROOT, "web_app", "backend")
DB_PATH = os.path.join(BACKEND_DIR, "site_cms.db")

# Marcador reconhecido por export_static_site.py para copiar de docs/graficos_originais/
# (as figuras reais extraidas do .odt) em vez de docs/graficos/ (rascunhos exploratorios).
GRAFICOS_ORIGINAIS_URL_PREFIX = "http://127.0.0.1:8000/static/graficos_originais/"

DEFAULT_FONTE = "Elaborado pelo autor com base nos dados da pesquisa."

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

# Capitulos que abrem com epigrafe (citacao + autoria) logo apos o titulo -- todos
# exceto Referencias, que e so a lista bibliografica.
EPIGRAFE_SLUGS = set(CHAPTER_ICONS) - {"referencias"}
EPIGRAFE_RE = re.compile(r"^<p>(.*?)</p><p>([^<]{0,80})</p>", re.S)


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


def load_figures_manifest():
    with open(os.path.join(CONTENT_EXPORT, "dissertacao_figuras_extraidas.json"), encoding="utf-8") as f:
        figures = json.load(f)
    # Descarta so as que nao tem nenhum capitulo (apareceriam antes do 1o heading -- nao
    # deveria acontecer, mas nao ha pagina para anexar a SectionVisual nesse caso).
    return [f for f in figures if f["capitulo_slug"] is not None]


def wrap_epigrafe(content):
    m = EPIGRAFE_RE.match(content)
    if not m:
        return content, False
    quote, autor = m.group(1), m.group(2)
    replacement = (
        f'<blockquote class="epigrafe"><p>{quote}</p>'
        f'<p class="epigrafe-autor">{autor}</p></blockquote>'
    )
    return EPIGRAFE_RE.sub(replacement, content, count=1), True


def main():
    chapters = load_chapters()
    figures = load_figures_manifest()

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    ensure_columns(cur)

    # Repopula page_content do zero.
    cur.execute("DELETE FROM section_visuals")
    cur.execute("DELETE FROM page_content")

    slug_to_id = {}
    for chap in chapters:
        icon = CHAPTER_ICONS.get(chap["slug"])
        content = chap["content_html"]
        if chap["slug"] in EPIGRAFE_SLUGS:
            content, ok = wrap_epigrafe(content)
            if not ok:
                print(f"AVISO: padrao de epigrafe nao encontrado em: {chap['slug']}")
        cur.execute(
            """INSERT INTO page_content
               (parent_id, slug, title, content, "order", icon_name, content_type)
               VALUES (NULL, ?, ?, ?, ?, ?, 'text')""",
            (chap["slug"], chap["title"], content, chap["order"], icon),
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

    # Insere as figuras reais e troca o marcador [FIG:chave] (ja no lugar certo do texto,
    # vindo do extract_odt_all.py) pelo [v:ID] real da SectionVisual criada.
    skipped = 0
    for fig in figures:
        target_slug = fig["secao_slug"] or fig["capitulo_slug"]
        page_id = slug_to_id.get(target_slug)
        if page_id is None:
            print(f"AVISO: slug alvo nao encontrado, pulando figura: {target_slug} ({fig['tipo']} {fig['numero']})")
            skipped += 1
            continue

        image_url = GRAFICOS_ORIGINAIS_URL_PREFIX + fig["arquivo"]
        titulo = f"{fig['tipo']} {fig['numero']} - {fig['legenda']}"
        fonte = fig.get("fonte") or DEFAULT_FONTE
        cur.execute(
            """INSERT INTO section_visuals
               (page_content_id, type, title, source, "order", image_url, pdf_page)
               VALUES (?, 'image', ?, ?, 0, ?, ?)""",
            (page_id, titulo, fonte, image_url, fig["pagina"]),
        )
        visual_id = cur.lastrowid
        marker = f"[FIG:{fig['chave']}]"
        cur.execute("SELECT content FROM page_content WHERE id = ?", (page_id,))
        (content,) = cur.fetchone()
        if marker not in (content or ""):
            print(f"AVISO: marcador {marker} nao encontrado no texto de {target_slug}, anexando no fim")
            content = (content or "") + f"<p>[v:{visual_id}]</p>"
        else:
            content = content.replace(marker, f"[v:{visual_id}]")
        cur.execute("UPDATE page_content SET content = ? WHERE id = ?", (content, page_id))

    con.commit()
    cur.execute("SELECT COUNT(*) FROM page_content")
    n_pages = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM section_visuals")
    n_visuals = cur.fetchone()[0]
    con.close()
    print(f"OK: {n_pages} linhas em page_content, {n_visuals} figuras aplicadas ({skipped} puladas).")


if __name__ == "__main__":
    main()

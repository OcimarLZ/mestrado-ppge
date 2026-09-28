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
import html
import json
import os
import re
import sqlite3
import unicodedata

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
    "apendice-i": "Paperclip",
}

# Capitulos que abrem com epigrafe (citacao + autoria) logo apos o titulo -- todos
# exceto Referencias (lista bibliografica) e Apendice I (galeria de figuras).
EPIGRAFE_SLUGS = set(CHAPTER_ICONS) - {"referencias", "apendice-i"}
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


# Citacoes autor-data no padrao ABNT: "Bourdieu (1989)" (narrativa) ou "(Bourdieu, 1989)"
# (parentetica), com suporte a multiplos autores -- "Bianchetti; Sguissardi (2017)",
# "Dardot e Laval (2017)", e o padrao de 3+ autores com virgula entre os primeiros e "e"
# antes do ultimo: "Morosini, Kohls-Santos e Bittencourt (2021)" -- e sufixo de letra para
# mesmo autor/ano ("2015b").
#
# O separador entre autores usa (?:\s*[,;]\s*|\s+e\s+) -- exige espaco dos dois lados da
# conjuncao "e" -- e nao a classe de caracteres `[;e]` (que casava ';' OU a letra 'e'
# SOLTA). Com `[;e]`, uma citacao como "Pierre Bourdieu (1989)" fazia o regex, ao dar
# backtrack, tratar o 'e' final de "Pierre" como se fosse a conjuncao "e" ligando dois
# autores, produzindo n_authors="Pierre Bourdieu" (nome completo) em vez de so o
# sobrenome -- e a busca no indice de referencias (chaveado so pelo sobrenome) falhava.
# O nome de cada autor tambem aceita sobrenome composto por hifen com a SEGUNDA parte
# tambem capitalizada (ex: "Kohls-Santos") -- so "-[a-z]" nao bastava, pois em nomes assim
# as duas metades comecam com maiuscula.
_NOME = r"[A-ZÀ-Ü][a-zà-ÿ']+(?:-[A-ZÀ-Ü][a-zà-ÿ']+)?"
# Sufixo de pagina opcional (ABNT: "(Amaral, 2019, p. 73)", "(Chaui, 2003, p. 7)") -- sem
# isso o ano deixava de ser o ultimo token antes do ")" e a citacao inteira nao casava,
# perdendo o tooltip mesmo com a referencia presente no indice.
_PAGINA = r"(?:,\s*pp?\.?\s*\d+(?:[-–]\d+)?)?"
CITATION_RE = re.compile(
    r"(?P<n_authors>" + _NOME + r"(?:(?:\s*[,;]\s*|\s+e\s+)" + _NOME + r")*)"
    r"\s*\((?P<n_years>\d{4}[a-z]?(?:[,;]\s*\d{4}[a-z]?)*)" + _PAGINA + r"\)"
    r"|"
    r"\((?P<p_authors>[A-ZÀ-Ü][A-Za-zà-ÿ';\s-]+?),\s*(?P<p_years>\d{4}[a-z]?(?:[,;]\s*\d{4}[a-z]?)*)" + _PAGINA + r"\)"
)

REF_ENTRY_LEAD_AUTHOR_RE = re.compile(r"^([A-ZÀ-Ü][A-ZÀ-Üa-zà-ÿ\-'\s]*?),")
# Permite espaco dentro do nome (ex: "SER EDUCACIONAL.") -- a versao anterior so casava
# uma unica palavra em maiusculas, entao entidades de dois nomes nunca entravam no indice.
REF_ENTRY_ORG_RE = re.compile(r"^([A-ZÀ-Ü][A-ZÀ-Ü\s]*[A-ZÀ-Ü])\.")
REF_ENTRY_EXTRA_AUTHOR_RE = re.compile(r";\s*([A-ZÀ-Ü][A-ZÀ-Üa-zà-ÿ\-']*)")
# Aceita o ano precedido de virgula OU ponto (",  2005." e tambem "dez. 2004.", quando o
# ano vem logo apos uma abreviatura de mes) -- so exigir virgula deixava referencias assim
# de fora do indice (ex: "BALL... Educação & Sociedade... p. 1105-1126, set./dez. 2004.").
REF_ENTRY_YEAR_RE = re.compile(r"[,.]\s*(\d{4}[a-z]?)\.")


def normalize_surname(s: str) -> str:
    """Remove acentos e caixa para comparar sobrenomes -- o texto da dissertacao as
    vezes cita o mesmo autor ora acentuado ora nao (ex: "Chaui" e "Chauí"), o que fazia
    a busca por igualdade exata no indice falhar para uma das grafias."""
    sem_acento = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return sem_acento.strip().upper()


def build_reference_index(referencias_content_html):
    """Le os paragrafos da lista de referencias e monta {(SOBRENOME, ano): texto da
    referencia}, para o hover das citacoes no texto apontar a referencia certa."""
    index = {}
    entries = re.findall(r"<p>(.*?)</p>", referencias_content_html, re.S)
    for entry in entries:
        plain = re.sub(r"<[^>]+>", "", entry).strip()
        if not plain:
            continue
        year_match = REF_ENTRY_YEAR_RE.search(plain)
        if not year_match:
            continue
        year = year_match.group(1)

        surnames = []
        m = REF_ENTRY_LEAD_AUTHOR_RE.match(plain)
        if m:
            surnames.append(normalize_surname(m.group(1)))
        else:
            m2 = REF_ENTRY_ORG_RE.match(plain)
            if m2:
                surnames.append(normalize_surname(m2.group(1)))
        for m3 in REF_ENTRY_EXTRA_AUTHOR_RE.finditer(plain[:200]):
            surnames.append(normalize_surname(m3.group(1)))

        for surname in surnames:
            index.setdefault((surname, year), plain)
    return index


def link_citations(content, ref_index):
    def replace(m):
        whole = m.group(0)
        authors_raw = m.group("n_authors") or m.group("p_authors")
        years_raw = m.group("n_years") or m.group("p_years")
        # Bug corrigido: `[;e]` eh uma CLASSE de caracteres (';' OU a letra 'e'), nao a
        # palavra "e" como conjuncao -- isso truncava qualquer sobrenome que contivesse um
        # "e" solto (Bourdieu -> "Bourdi", Chaves -> "Chav", Ferreira -> "F", etc.), fazendo
        # a busca no indice de referencias falhar silenciosamente. `\s+e\s+` exige espaco
        # dos dois lados, so casando a conjuncao de verdade ("Dardot e Laval").
        first_author = normalize_surname(re.split(r"\s*[,;]\s*|\s+e\s+", authors_raw)[0])
        # Uma citacao pode reunir varias obras do mesmo autor (ex: "Sguissardi (2008;
        # 2009; 2017)") -- busca a referencia de CADA ano citado, nao so do primeiro, e
        # mostra todas no tooltip (uma por linha).
        years = [y.strip() for y in re.split(r"[,;]\s*", years_raw) if y.strip()]
        ref_texts = []
        for year in years:
            ref_text = ref_index.get((first_author, year))
            if ref_text and ref_text not in ref_texts:
                ref_texts.append(ref_text)
        if not ref_texts:
            return whole
        if len(ref_texts) > 1:
            data_ref = "\n".join(f"{i}) {t}" for i, t in enumerate(ref_texts, start=1))
        else:
            data_ref = ref_texts[0]
        return f'<span class="cite-hint" tabindex="0" data-ref="{html.escape(data_ref)}">{whole}</span>'

    return CITATION_RE.sub(replace, content)


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

    referencias_chap = next((c for c in chapters if c["slug"] == "referencias"), None)
    ref_index = build_reference_index(referencias_chap["content_html"]) if referencias_chap else {}
    citation_chapters = set(CHAPTER_ICONS) - {"referencias", "apendice-i"}

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    ensure_columns(cur)

    # Repopula page_content do zero.
    cur.execute("DELETE FROM section_visuals")
    cur.execute("DELETE FROM page_content")

    slug_to_id = {}
    n_citations_linked = 0
    for chap in chapters:
        icon = CHAPTER_ICONS.get(chap["slug"])
        content = chap["content_html"]
        link_here = chap["slug"] in citation_chapters
        # A epigrafe precisa ser isolada ANTES do link de citacoes: algumas autorias de
        # epigrafe sao no formato "Sobrenome (Ano)", que e exatamente o padrao de citacao
        # narrativa -- se linkado primeiro, o <span> inserido quebra o regex da epigrafe
        # (que exige a linha de autoria sem nenhuma tag).
        if chap["slug"] in EPIGRAFE_SLUGS:
            content, ok = wrap_epigrafe(content)
            if not ok:
                print(f"AVISO: padrao de epigrafe nao encontrado em: {chap['slug']}")
        if link_here:
            content = link_citations(content, ref_index)
            n_citations_linked += content.count('class="cite-hint"')
        cur.execute(
            """INSERT INTO page_content
               (parent_id, slug, title, content, "order", icon_name, content_type)
               VALUES (NULL, ?, ?, ?, ?, ?, 'text')""",
            (chap["slug"], chap["title"], content, chap["order"], icon),
        )
        chap_id = cur.lastrowid
        slug_to_id[chap["slug"]] = chap_id
        for sec in chap["sections"]:
            sec_content = sec["content_html"]
            if link_here:
                sec_content = link_citations(sec_content, ref_index)
                n_citations_linked += sec_content.count('class="cite-hint"')
            cur.execute(
                """INSERT INTO page_content
                   (parent_id, slug, title, content, "order", icon_name, content_type)
                   VALUES (?, ?, ?, ?, ?, NULL, 'text')""",
                (chap_id, sec["slug"], sec["title"], sec_content, sec["order"]),
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
    print(f"OK: {n_pages} linhas em page_content, {n_visuals} figuras aplicadas ({skipped} puladas), {n_citations_linked} citações linkadas.")


if __name__ == "__main__":
    main()

"""
Extrai da dissertacao (docs/OLZ_Defesa_V_2.03.odt) o conteudo real para a landing page estatica.

Um .odt e um zip com content.xml (OpenDocument XML). Este script nao precisa de nenhuma
biblioteca externa: usa zipfile + xml.etree da stdlib.

Gera dois arquivos:
  web_app/content_export/dissertacao_conteudo.json
      Arvore de capitulos/secoes (niveis 1 e 2 dos titulos) com o texto real dos paragrafos.
      Titulos de nivel 3 entram como subtitulo embutido (<h4>) dentro do conteudo da secao pai,
      para casar com o modelo de 2 niveis (capitulo -> secao) do PageContent atual.

  web_app/content_export/dissertacao_figuras.json
      Indice de Graficos/Figuras/Quadros/Tabelas com legenda + numero de pagina real, extraido
      diretamente das listas (Lista de Graficos, Lista de Figuras, ...) que o LibreOffice/Word
      ja mantem no proprio documento — nao precisa abrir o PDF nem instalar lib de PDF.

Rode a partir da raiz do repo: python web_app/content_export/extract_odt_content.py
"""
import json
import os
import re
import zipfile
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ODT_PATH = os.path.join(ROOT, "docs", "OLZ_Defesa_V_2.03.odt")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

NS = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
}
OFFICE_BODY = f"{{{NS['office']}}}body"
OFFICE_TEXT = f"{{{NS['office']}}}text"
H_TAG = f"{{{NS['text']}}}h"
P_TAG = f"{{{NS['text']}}}p"
LIST_TAG = f"{{{NS['text']}}}list"
NOTE_TAG = f"{{{NS['text']}}}note"
OUTLINE_LEVEL_ATTR = f"{{{NS['text']}}}outline-level"

INDEX_WRAPPER_TAGS = {
    f"{{{NS['text']}}}table-of-content",
    f"{{{NS['text']}}}illustration-index",
    f"{{{NS['text']}}}alphabetical-index",
    f"{{{NS['text']}}}bibliography",
    f"{{{NS['text']}}}user-index",
    f"{{{NS['text']}}}object-index",
}


def local_text(elem, skip_tags=(NOTE_TAG,)):
    """Texto visivel de um elemento, pulando notas de rodape."""
    parts = []

    def walk(e):
        if e.tag in skip_tags:
            return
        if e.text:
            parts.append(e.text)
        for c in e:
            walk(c)
            if c.tail:
                parts.append(c.tail)

    walk(elem)
    return re.sub(r"\s+", " ", "".join(parts)).strip()


def slugify(text):
    text = text.strip().lower()
    repl = {
        "á": "a", "à": "a", "â": "a", "ã": "a", "ä": "a",
        "é": "e", "ê": "e", "è": "e", "ë": "e",
        "í": "i", "ì": "i", "î": "i",
        "ó": "o", "ô": "o", "õ": "o", "ò": "o",
        "ú": "u", "ù": "u", "û": "u",
        "ç": "c", "ñ": "n",
    }
    for a, b in repl.items():
        text = text.replace(a, b)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "secao"


def extract_body_tree(root):
    """Percorre office:body/office:text em ordem de documento, montando a arvore
    capitulo (nivel 1) -> secao (nivel 2), com nivel 3 embutido como <h4> no HTML da secao."""
    body = root.find(f".//{OFFICE_BODY}/{OFFICE_TEXT}")
    if body is None:
        raise RuntimeError("office:body/office:text nao encontrado no content.xml")

    chapters = []
    current_chapter = None
    current_section = None
    used_slugs = set()

    def unique_slug(base):
        slug = base
        i = 2
        while slug in used_slugs:
            slug = f"{base}-{i}"
            i += 1
        used_slugs.add(slug)
        return slug

    def new_para_html(elem):
        txt = local_text(elem)
        return f"<p>{txt}</p>" if txt else ""

    def walk(elem, in_index=False):
        nonlocal current_chapter, current_section
        for child in elem:
            tag = child.tag
            if tag in INDEX_WRAPPER_TAGS:
                continue  # pula listas de figuras/graficos/sumario etc.
            if tag == H_TAG:
                level = child.get(OUTLINE_LEVEL_ATTR)
                level = int(level) if level else 1
                title = local_text(child)
                if not title:
                    continue
                if level == 1:
                    current_chapter = {
                        "slug": unique_slug(slugify(title)),
                        "title": title,
                        "order": len(chapters) + 1,
                        "sections": [],
                    }
                    chapters.append(current_chapter)
                    current_section = None
                elif level == 2 and current_chapter is not None:
                    current_section = {
                        "slug": unique_slug(slugify(title)),
                        "title": title,
                        "order": len(current_chapter["sections"]) + 1,
                        "content_html": [],
                    }
                    current_chapter["sections"].append(current_section)
                elif level >= 3 and current_section is not None:
                    current_section["content_html"].append(f"<h4>{title}</h4>")
                continue
            if tag == P_TAG:
                html = new_para_html(child)
                if html:
                    if current_section is not None:
                        current_section["content_html"].append(html)
                    elif current_chapter is not None:
                        current_chapter.setdefault("intro_html", []).append(html)
                continue
            if tag == LIST_TAG:
                items_html = []
                for p in child.iter(P_TAG):
                    t = local_text(p)
                    if t:
                        items_html.append(f"<li>{t}</li>")
                if items_html:
                    html = "<ul>" + "".join(items_html) + "</ul>"
                    if current_section is not None:
                        current_section["content_html"].append(html)
                    elif current_chapter is not None:
                        current_chapter.setdefault("intro_html", []).append(html)
                continue
            # Recorre em qualquer outro wrapper (text:section, frame, etc.)
            walk(child, in_index)

    walk(body)

    for chap in chapters:
        chap["content_html"] = "".join(chap.pop("intro_html", []))
        for sec in chap["sections"]:
            sec["content_html"] = "".join(sec["content_html"])

    return chapters


def extract_figure_index(raw_xml):
    """Le as Listas de Graficos/Figuras/Quadros/Tabelas (indices que o LibreOffice
    grava com legenda + numero de pagina real) direto do XML bruto."""
    labels = ["Gráfico", "Figura", "Quadro", "Tabela", "Mapa"]
    result = {}
    for label in labels:
        pattern = re.compile(
            r'office:name="(' + re.escape(label) + r' \d+[^"]*)"[^>]*>'
            r"(?:(?!</text:a>).)*?<text:tab/>(\d+)</text:a>",
            re.S,
        )
        entries = []
        for caption, page in pattern.findall(raw_xml):
            entries.append({"caption": caption.strip(), "page": int(page)})
        if entries:
            result[label] = entries
    return result


def main():
    with zipfile.ZipFile(ODT_PATH) as z:
        raw_xml = z.read("content.xml").decode("utf-8")

    root = ET.fromstring(raw_xml)
    chapters = extract_body_tree(root)
    figure_index = extract_figure_index(raw_xml)

    content_out = os.path.join(OUT_DIR, "dissertacao_conteudo.json")
    with open(content_out, "w", encoding="utf-8") as f:
        json.dump(chapters, f, ensure_ascii=False, indent=2)

    figures_out = os.path.join(OUT_DIR, "dissertacao_figuras.json")
    with open(figures_out, "w", encoding="utf-8") as f:
        json.dump(figure_index, f, ensure_ascii=False, indent=2)

    n_sections = sum(len(c["sections"]) for c in chapters)
    n_figs = sum(len(v) for v in figure_index.values())
    print(f"OK: {len(chapters)} capitulos, {n_sections} secoes -> {content_out}")
    print(f"OK: {n_figs} legendas com pagina ({', '.join(f'{k}={len(v)}' for k, v in figure_index.items())}) -> {figures_out}")


if __name__ == "__main__":
    main()

"""
Extrai da dissertacao (docs/OLZ_Defesa_V_2.03.odt) tanto o texto real quanto as figuras
reais (as coladas do Excel), num UNICO passe pelo documento, para que cada figura fique
exatamente no lugar em que o texto a referencia -- nao jogada no fim da secao.

Um .odt e um zip com content.xml (OpenDocument XML). So precisa de Pillow (para aparar a
margem branca das imagens convertidas) alem da stdlib; LibreOffice (soffice) e usado via
subprocess para converter EMF/SVM (vetorial, navegador nao abre) em PNG.

Como a legenda de uma figura pode vir ANTES ou DEPOIS da sua imagem no documento (os dois
padroes coexistem -- confirmado inspecionando o XML bruto), a associacao e feita por
"vizinho mais proximo" (menor distancia de posicao no documento) com casamento guloso 1:1.
O bloco de texto mais proximo (legenda ou imagem, o que vier primeiro) vira o marcador
[FIG:chave] inserido no HTML da secao; o outro bloco (a legenda OU a linha "Fonte: ...")
e removido do texto corrido para nao duplicar.

Saida:
  docs/graficos_originais/<tipo>_<numero>.png
  web_app/content_export/dissertacao_conteudo.json
      Arvore de capitulos/secoes com o texto real + marcadores [FIG:chave] inline.
  web_app/content_export/dissertacao_figuras_extraidas.json
      Manifesto: tipo, numero, legenda, chave, arquivo, fonte, pagina, capitulo_slug,
      secao_slug.

Rode a partir da raiz do repo: python web_app/content_export/extract_odt_all.py
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET

from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ODT_PATH = os.path.join(ROOT, "docs", "OLZ_Defesa_V_2.03.odt")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_IMAGES_DIR = os.path.join(ROOT, "docs", "graficos_originais")

SOFFICE_CANDIDATES = [
    "soffice",
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
]

NS = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
    "draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
    "xlink": "http://www.w3.org/1999/xlink",
}


def tag(name, ns="text"):
    return f"{{{NS[ns]}}}{name}"


H_TAG = tag("h")
P_TAG = tag("p")
LIST_TAG = tag("list")
NOTE_TAG = tag("note")
FRAME_TAG = tag("frame", "draw")
IMAGE_TAG = tag("image", "draw")
OUTLINE_LEVEL_ATTR = tag("outline-level")

INDEX_WRAPPER_TAGS = {
    tag("table-of-content"),
    tag("illustration-index"),
    tag("alphabetical-index"),
    tag("bibliography"),
    tag("user-index"),
    tag("object-index"),
}

CAPTION_RE = re.compile(r"^(Gráfico|Figura|Quadro|Tabela)\s+(\d+)\s*-\s*(.+)$")
TIPO_SLUG = {"Gráfico": "grafico", "Figura": "figura", "Quadro": "quadro", "Tabela": "tabela"}


def local_text(elem, skip_tags=(NOTE_TAG,)):
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


def frame_hrefs_within(elem):
    hrefs = []
    for frame in elem.iter(FRAME_TAG):
        img = frame.find(IMAGE_TAG)
        if img is not None:
            href = img.get(f"{{{NS['xlink']}}}href")
            if href:
                hrefs.append(href)
    return hrefs


def slugify(text_):
    text_ = text_.strip().lower()
    repl = {
        "á": "a", "à": "a", "â": "a", "ã": "a", "ä": "a",
        "é": "e", "ê": "e", "è": "e", "ë": "e",
        "í": "i", "ì": "i", "î": "i",
        "ó": "o", "ô": "o", "õ": "o", "ò": "o",
        "ú": "u", "ù": "u", "û": "u",
        "ç": "c", "ñ": "n",
    }
    for a, b in repl.items():
        text_ = text_.replace(a, b)
    text_ = re.sub(r"[^a-z0-9]+", "-", text_).strip("-")
    return text_ or "secao"


def extract_fonte(paragraph_text):
    """Da paragraph_text ('Fonte: elaborado pelo autor...'), extrai so o trecho apos
    'Fonte:'. Retorna None se o paragrafo nao comecar com 'Fonte'."""
    m = re.match(r"^Fonte\s*:?\s*(.+)$", paragraph_text, re.IGNORECASE)
    return m.group(1).strip() if m else None


class Walker:
    """Um unico passe pelo body do .odt que monta:
    - self.chapters: arvore capitulo -> secao, cada um com uma lista de block_ids (em
      self.blocks) representando paragrafos/listas/figuras em ordem de documento.
    - self.captions / self.images: eventos de legenda/imagem, cada um referenciando o
      block_id do paragrafo onde apareceu (usado tanto para posicao quanto para
      localizar o bloco a mutar depois do casamento)."""

    def __init__(self):
        self.blocks = []  # cada item: {'kind': 'p'|'h4'|'ul'|'removed'|'figure', ...}
        self.chapters = []
        self.current_chapter = None
        self.current_section = None
        self.used_slugs = set()
        self.captions = []  # {block_id, tipo, numero, legenda}
        self.images = []  # {block_id, href, fonte}

    def unique_slug(self, base):
        s = base
        i = 2
        while s in self.used_slugs:
            s = f"{base}-{i}"
            i += 1
        self.used_slugs.add(s)
        return s

    def new_block(self, block):
        self.blocks.append(block)
        block_id = len(self.blocks) - 1
        target = self.current_section if self.current_section is not None else self.current_chapter
        if target is not None:
            target["block_ids"].append(block_id)
        return block_id

    def walk(self, elem):
        for child in elem:
            et = child.tag
            if et in INDEX_WRAPPER_TAGS:
                continue
            if et == H_TAG:
                level = child.get(OUTLINE_LEVEL_ATTR)
                level = int(level) if level else 1
                title = local_text(child)
                if not title:
                    continue
                if level == 1:
                    self.current_chapter = {
                        "slug": self.unique_slug(slugify(title)),
                        "title": title,
                        "order": len(self.chapters) + 1,
                        "block_ids": [],
                    }
                    self.chapters.append(self.current_chapter)
                    self.current_section = None
                elif level == 2 and self.current_chapter is not None:
                    self.current_section = {
                        "slug": self.unique_slug(slugify(title)),
                        "title": title,
                        "order": len(self.current_chapter.setdefault("sections", [])) + 1,
                        "block_ids": [],
                    }
                    self.current_chapter["sections"].append(self.current_section)
                elif level >= 3 and self.current_section is not None:
                    self.new_block({"kind": "h4", "html": f"<h4>{title}</h4>"})
                continue
            if et == P_TAG:
                txt = local_text(child)
                block_id = self.new_block({"kind": "p", "html": f"<p>{txt}</p>" if txt else ""})

                hrefs = frame_hrefs_within(child)
                if hrefs:
                    fonte = extract_fonte(txt)
                    for href in hrefs:
                        self.images.append({"block_id": block_id, "href": href, "fonte": fonte})

                m = CAPTION_RE.match(txt)
                if m:
                    self.captions.append({
                        "block_id": block_id,
                        "tipo": m.group(1),
                        "numero": int(m.group(2)),
                        "legenda": m.group(3),
                        "capitulo_slug": self.current_chapter["slug"] if self.current_chapter else None,
                        "secao_slug": self.current_section["slug"] if self.current_section else None,
                    })
                continue
            if et == LIST_TAG:
                items_html = []
                for p in child.iter(P_TAG):
                    t = local_text(p)
                    if t:
                        items_html.append(f"<li>{t}</li>")
                if items_html:
                    self.new_block({"kind": "ul", "html": "<ul>" + "".join(items_html) + "</ul>"})
                continue
            if et == FRAME_TAG:
                # draw:frame fora de qualquer text:p (raro, mas cobre o caso).
                img = child.find(IMAGE_TAG)
                if img is not None:
                    href = img.get(f"{{{NS['xlink']}}}href")
                    if href:
                        block_id = self.new_block({"kind": "p", "html": ""})
                        self.images.append({"block_id": block_id, "href": href, "fonte": None})
                continue
            self.walk(child)


def match_captions_to_images(captions, images):
    """Casamento guloso 1:1 por menor distancia de block_id (posicao no documento)."""
    pairs = []
    for ci, cap in enumerate(captions):
        for ii, img in enumerate(images):
            pairs.append((abs(cap["block_id"] - img["block_id"]), ci, ii))
    pairs.sort(key=lambda t: t[0])

    claimed_c, claimed_i, matches = set(), set(), {}
    for _dist, ci, ii in pairs:
        if ci in claimed_c or ii in claimed_i:
            continue
        claimed_c.add(ci)
        claimed_i.add(ii)
        matches[ci] = ii
    return matches


def load_page_index(raw_xml):
    labels = ["Gráfico", "Figura", "Quadro", "Tabela"]
    index = {}
    for label in labels:
        pattern = re.compile(
            r'office:name="(' + re.escape(label) + r' \d+)[^"]*"[^>]*>'
            r"(?:(?!</text:a>).)*?<text:tab/>(\d+)</text:a>",
            re.S,
        )
        for name, page in pattern.findall(raw_xml):
            m = re.match(r"^(.+) (\d+)$", name)
            if m:
                index[(m.group(1), int(m.group(2)))] = int(page)
    return index


def find_soffice():
    for cand in SOFFICE_CANDIDATES:
        if os.path.sep in cand:
            if os.path.exists(cand):
                return cand
        else:
            path = shutil.which(cand)
            if path:
                return path
    return None


def trim_whitespace(path, padding=12):
    img = Image.open(path)
    rgb = img.convert("RGB")
    bg = Image.new("RGB", rgb.size, (255, 255, 255))
    diff = ImageChops.difference(rgb, bg)
    bbox = diff.getbbox()
    if not bbox:
        return
    left, top, right, bottom = bbox
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(img.width, right + padding)
    bottom = min(img.height, bottom + padding)
    if (left, top, right, bottom) == (0, 0, img.width, img.height):
        return
    img.crop((left, top, right, bottom)).save(path)


def main():
    with zipfile.ZipFile(ODT_PATH) as z:
        raw_xml = z.read("content.xml").decode("utf-8")
        root = ET.fromstring(raw_xml)
        body = root.find(f".//{tag('body', 'office')}/{tag('text', 'office')}")

        w = Walker()
        w.walk(body)
        page_index = load_page_index(raw_xml)
        matches = match_captions_to_images(w.captions, w.images)

        manifest = []
        os.makedirs(OUT_IMAGES_DIR, exist_ok=True)
        with tempfile.TemporaryDirectory() as tmp:
            to_convert = []  # (tmp_src_path, out_name)
            for ci, cap in enumerate(w.captions):
                ii = matches.get(ci)
                if ii is None:
                    continue
                img_event = w.images[ii]
                key = f"{TIPO_SLUG[cap['tipo']]}_{cap['numero']:02d}"
                out_name = key

                insertion_id = min(cap["block_id"], img_event["block_id"])
                other_id = max(cap["block_id"], img_event["block_id"])
                w.blocks[insertion_id] = {"kind": "figure", "key": key}
                if other_id != insertion_id:
                    w.blocks[other_id] = {"kind": "removed"}

                href = img_event["href"]
                ext = href.rsplit(".", 1)[-1].lower()
                if ext == "png":
                    with z.open(href) as src, open(os.path.join(OUT_IMAGES_DIR, f"{out_name}.png"), "wb") as dst:
                        shutil.copyfileobj(src, dst)
                else:
                    tmp_src = os.path.join(tmp, os.path.basename(href))
                    with z.open(href) as src, open(tmp_src, "wb") as dst:
                        shutil.copyfileobj(src, dst)
                    to_convert.append((tmp_src, out_name))

                manifest.append({
                    "tipo": cap["tipo"],
                    "numero": cap["numero"],
                    "legenda": cap["legenda"],
                    "chave": key,
                    "arquivo": f"{out_name}.png",
                    "fonte": img_event.get("fonte"),
                    "pagina": page_index.get((cap["tipo"], cap["numero"])),
                    "capitulo_slug": cap["capitulo_slug"],
                    "secao_slug": cap["secao_slug"],
                })

            if to_convert:
                soffice_path = find_soffice()
                if not soffice_path:
                    print("AVISO: LibreOffice (soffice) nao encontrado; imagens vetoriais nao convertidas.")
                else:
                    cmd = [soffice_path, "--headless", "--convert-to", "png", "--outdir", tmp] + [p for p, _ in to_convert]
                    subprocess.run(cmd, check=True, capture_output=True)
                    for tmp_src, out_name in to_convert:
                        converted = os.path.splitext(tmp_src)[0] + ".png"
                        final_path = os.path.join(OUT_IMAGES_DIR, f"{out_name}.png")
                        if os.path.exists(converted):
                            shutil.move(converted, final_path)
                        else:
                            print(f"AVISO: conversao falhou para {tmp_src}")

    for m in manifest:
        final_path = os.path.join(OUT_IMAGES_DIR, m["arquivo"])
        if os.path.exists(final_path):
            try:
                trim_whitespace(final_path)
            except Exception as e:
                print(f"AVISO: falha ao aparar margens de {m['arquivo']}: {e}")

    # Monta o content_html final de cada capitulo/secao a partir dos blocos resolvidos.
    def render_blocks(block_ids):
        parts = []
        for bid in block_ids:
            b = w.blocks[bid]
            if b["kind"] == "removed":
                continue
            if b["kind"] == "figure":
                parts.append(f"[FIG:{b['key']}]")
            elif b.get("html"):
                parts.append(b["html"])
        return "".join(parts)

    chapters_out = []
    for chap in w.chapters:
        chapters_out.append({
            "slug": chap["slug"],
            "title": chap["title"],
            "order": chap["order"],
            "content_html": render_blocks(chap["block_ids"]),
            "sections": [
                {
                    "slug": sec["slug"],
                    "title": sec["title"],
                    "order": sec["order"],
                    "content_html": render_blocks(sec["block_ids"]),
                }
                for sec in chap.get("sections", [])
            ],
        })

    content_out = os.path.join(OUT_DIR, "dissertacao_conteudo.json")
    with open(content_out, "w", encoding="utf-8") as f:
        json.dump(chapters_out, f, ensure_ascii=False, indent=2)

    manifest_out = os.path.join(OUT_DIR, "dissertacao_figuras_extraidas.json")
    with open(manifest_out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    n_sections = sum(len(c["sections"]) for c in chapters_out)
    print(f"OK: {len(chapters_out)} capitulos, {n_sections} secoes -> {content_out}")
    print(f"OK: {len(manifest)}/{len(w.captions)} legendas casadas com imagem -> {manifest_out}")


if __name__ == "__main__":
    sys.exit(main())

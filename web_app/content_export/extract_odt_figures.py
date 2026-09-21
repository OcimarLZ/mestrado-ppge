"""
Extrai as imagens REAIS embutidas em docs/OLZ_Defesa_V_2.03.odt (as que o autor colou do
Excel na hora de montar a dissertacao) e mapeia cada uma para: tipo+numero (Grafico 10,
Figura 3, ...), pagina no PDF (via Lista de Graficos/Figuras/... que o LibreOffice mantem),
e o capitulo/secao exatos de onde ela foi extraida (por posicao no documento).

As imagens .emf/.svm (formatos vetoriais que navegador nao abre) sao convertidas para .png
via LibreOffice headless. As .png embutidas sao copiadas como estao.

Saida:
  docs/graficos_originais/<tipo>_<numero>.png   (as imagens reais, prontas pra web)
  web_app/content_export/dissertacao_figuras_extraidas.json  (manifesto: tipo, numero,
      legenda, pagina, capitulo_slug, secao_slug, arquivo)

Rode a partir da raiz do repo: python web_app/content_export/extract_odt_figures.py
Requer LibreOffice instalado (usa soffice --headless --convert-to png) so para EMF/SVM.
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
OUT_IMAGES_DIR = os.path.join(ROOT, "docs", "graficos_originais")
OUT_MANIFEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dissertacao_figuras_extraidas.json")
PAGES_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dissertacao_figuras.json")

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


def local_text(elem):
    parts = []

    def walk(e):
        if e.text:
            parts.append(e.text)
        for c in e:
            walk(c)
            if c.tail:
                parts.append(c.tail)

    walk(elem)
    return re.sub(r"\s+", " ", "".join(parts)).strip()


CAPTION_RE = re.compile(r"^(Gráfico|Figura|Quadro|Tabela)\s+(\d+)\s*-\s*(.+)$")

TIPO_SLUG = {
    "Gráfico": "grafico",
    "Figura": "figura",
    "Quadro": "quadro",
    "Tabela": "tabela",
}


def find_figure_positions(root):
    """Percorre o body em ordem de documento coletando dois trilhos de eventos (legendas
    e imagens) com uma posicao ordinal comum. A legenda de uma figura pode vir ANTES ou
    DEPOIS da sua imagem (o documento mistura os dois padroes -- verificado manualmente),
    entao a associacao final e feita por vizinho mais proximo (menor distancia de posicao),
    com casamento guloso 1:1 entre legendas e imagens.

    Retorna uma lista de dicts: {tipo, numero, legenda, href, capitulo_slug, secao_slug}.
    """
    body = root.find(f".//{tag('body', 'office')}/{tag('text', 'office')}")
    captions = []  # {pos, tipo, numero, legenda, capitulo_slug, secao_slug}
    images = []  # {pos, href}
    state = {"chapter_slug": None, "section_slug": None, "pos": 0}
    used_slugs = set()

    def unique_slug(base):
        s = base
        i = 2
        while s in used_slugs:
            s = f"{base}-{i}"
            i += 1
        used_slugs.add(s)
        return s

    def frame_hrefs_within(elem):
        hrefs = []
        for frame in elem.iter(tag("frame", "draw")):
            img = frame.find(tag("image", "draw"))
            if img is not None:
                href = img.get(f"{{{NS['xlink']}}}href")
                if href:
                    hrefs.append(href)
        return hrefs

    def walk(elem):
        for child in elem:
            et = child.tag
            if et == tag("h"):
                level = child.get(tag("outline-level"))
                level = int(level) if level else 1
                title = local_text(child)
                if not title:
                    continue
                if level == 1:
                    state["chapter_slug"] = unique_slug(slugify(title))
                    state["section_slug"] = None
                elif level == 2:
                    state["section_slug"] = unique_slug(slugify(title))
                continue
            if et == tag("p"):
                state["pos"] += 1
                for href in frame_hrefs_within(child):
                    images.append({"pos": state["pos"], "href": href})
                txt = local_text(child)
                m = CAPTION_RE.match(txt)
                if m:
                    captions.append({
                        "pos": state["pos"],
                        "tipo": m.group(1),
                        "numero": int(m.group(2)),
                        "legenda": m.group(3),
                        "capitulo_slug": state["chapter_slug"],
                        "secao_slug": state["section_slug"],
                    })
                continue
            if et == tag("frame", "draw"):
                state["pos"] += 1
                img = child.find(tag("image", "draw"))
                if img is not None:
                    href = img.get(f"{{{NS['xlink']}}}href")
                    if href:
                        images.append({"pos": state["pos"], "href": href})
                continue
            walk(child)

    walk(body)

    # Casamento guloso: para cada par (legenda, imagem), calcula a distancia de posicao;
    # ordena por distancia crescente; atribui greedily, sem reusar legenda nem imagem.
    pairs = []
    for ci, cap in enumerate(captions):
        for ii, img in enumerate(images):
            pairs.append((abs(cap["pos"] - img["pos"]), ci, ii))
    pairs.sort(key=lambda t: t[0])

    claimed_captions = set()
    claimed_images = set()
    matches = {}  # ci -> ii
    for _dist, ci, ii in pairs:
        if ci in claimed_captions or ii in claimed_images:
            continue
        claimed_captions.add(ci)
        claimed_images.add(ii)
        matches[ci] = ii

    results = []
    for ci, cap in enumerate(captions):
        ii = matches.get(ci)
        if ii is None:
            continue
        results.append({
            "tipo": cap["tipo"],
            "numero": cap["numero"],
            "legenda": cap["legenda"],
            "href": images[ii]["href"],
            "capitulo_slug": cap["capitulo_slug"],
            "secao_slug": cap["secao_slug"],
        })
    return results


def load_page_index():
    if not os.path.exists(PAGES_JSON):
        return {}
    with open(PAGES_JSON, encoding="utf-8") as f:
        data = json.load(f)
    index = {}
    for tipo, entries in data.items():
        for e in entries:
            m = re.match(r"^(Gráfico|Figura|Quadro|Tabela)\s+(\d+)", e["caption"])
            if m:
                index[(m.group(1), int(m.group(2)))] = e["page"]
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


def convert_to_png(soffice_path, src_files, out_dir):
    if not src_files:
        return
    cmd = [soffice_path, "--headless", "--convert-to", "png", "--outdir", out_dir] + src_files
    subprocess.run(cmd, check=True, capture_output=True)


def trim_whitespace(path, padding=12):
    """Remove a margem branca/transparente ao redor do conteudo real (comum na conversao
    de EMF, cujo canvas costuma ser bem maior que o grafico em si)."""
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
        raw = z.read("content.xml").decode("utf-8")
        root = ET.fromstring(raw)
        figures = find_figure_positions(root)
        page_index = load_page_index()

        os.makedirs(OUT_IMAGES_DIR, exist_ok=True)

        with tempfile.TemporaryDirectory() as tmp:
            to_convert = []  # (tmp_src_path, tipo, numero)
            manifest = []
            for fig in figures:
                href = fig["href"]
                ext = href.rsplit(".", 1)[-1].lower()
                out_name = f"{TIPO_SLUG[fig['tipo']]}_{fig['numero']:02d}"

                entry = {
                    "tipo": fig["tipo"],
                    "numero": fig["numero"],
                    "legenda": fig["legenda"],
                    "pagina": page_index.get((fig["tipo"], fig["numero"])),
                    "capitulo_slug": fig["capitulo_slug"],
                    "secao_slug": fig["secao_slug"],
                    "arquivo": f"{out_name}.png",
                }
                manifest.append(entry)

                if ext == "png":
                    with z.open(href) as src, open(os.path.join(OUT_IMAGES_DIR, f"{out_name}.png"), "wb") as dst:
                        shutil.copyfileobj(src, dst)
                else:
                    tmp_src = os.path.join(tmp, os.path.basename(href))
                    with z.open(href) as src, open(tmp_src, "wb") as dst:
                        shutil.copyfileobj(src, dst)
                    to_convert.append((tmp_src, out_name))

            if to_convert:
                soffice_path = find_soffice()
                if not soffice_path:
                    print("AVISO: LibreOffice (soffice) nao encontrado no PATH nem nos locais padrao.")
                    print(f"AVISO: {len(to_convert)} imagens vetoriais (.emf/.svm) NAO foram convertidas.")
                else:
                    convert_to_png(soffice_path, [p for p, _ in to_convert], tmp)
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

    with open(OUT_MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    ok = sum(1 for m in manifest if os.path.exists(os.path.join(OUT_IMAGES_DIR, m["arquivo"])))
    print(f"OK: {len(manifest)} figuras mapeadas, {ok} arquivos de imagem prontos em {OUT_IMAGES_DIR}")
    print(f"OK: manifesto em {OUT_MANIFEST}")


if __name__ == "__main__":
    sys.exit(main())

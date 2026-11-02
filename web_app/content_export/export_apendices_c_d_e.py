# -*- coding: utf-8 -*-
"""
Converte as planilhas dos Apendices C, D e E (planilhas/*.xlsx) em JSON estatico
para os paineis interativos da secao Pesquisa do site.

Fonte: planilhas/Apendice C - Indicadores dos cursos licenciaturas_federais em 2024.xlsx
       planilhas/Apendice D - Resumo cursos licenciaturas_federais.xlsx
       planilhas/Apendice E - Cursos licenciaturas_federais.xlsx

Gera:
  web_app/frontend/src/data/apendice_c_indicadores_2024.json
  web_app/frontend/src/data/apendice_perfil_institucional.json  (fusao de D + E, por IES)

Nao roda em CI (planilhas/ nao esta no runner). Rodar localmente e commitar o JSON
gerado sempre que as planilhas forem atualizadas.
"""
import json
import os

import openpyxl

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLANILHAS_DIR = os.path.join(ROOT, "planilhas")
DATA_DIR = os.path.join(ROOT, "web_app", "frontend", "src", "data")

ARQ_C = os.path.join(PLANILHAS_DIR, "Apêndice C - Indicadores dos cursos licenciaturas_federais em 2024.xlsx")
ARQ_D = os.path.join(PLANILHAS_DIR, "Apêndice D - Resumo cursos licenciaturas_federais.xlsx")
ARQ_E = os.path.join(PLANILHAS_DIR, "Apêndice E - Cursos licenciaturas_federais.xlsx")

LIC_IES_GERAL = os.path.join(DATA_DIR, "lic_ies_geral.json")


def sim_nao(v):
    if v is None:
        return None
    return str(v).strip().lower() == "sim"


def to_num_or_none(v):
    if v is None or v == "N.S.A.":
        return None
    return v


def exportar_apendice_c():
    wb = openpyxl.load_workbook(ARQ_C, data_only=True, read_only=True)
    ws = wb["VersaoDissertação"]
    registros = []
    for r in ws.iter_rows(min_row=3, values_only=True):
        if r[0] is None:
            break
        registros.append({
            "sigla": r[0],
            "estado": r[1],
            "oferece_licenciatura": sim_nao(r[2]),
            "num_campus_presencial_licenciatura": r[3],
            "num_polos_licenciatura": r[4],
            "ead_propria_oferece": sim_nao(r[5]),
            "ead_propria_num_polos": r[6],
            "ead_propria_num_cursos": r[7],
            "uab_oferece": sim_nao(r[8]),
            "uab_num_polos": r[9],
            "uab_num_cursos": r[10],
            "matriculas_total_ies": r[11],
            "matriculas_licenciatura": r[12],
            "perc_licenciatura_no_total": r[13],
            "matriculas_ead_propria_lic": r[14],
            "matriculas_uab_lic": r[15],
            "perc_ead_propria_na_lic": r[16],
            "perc_uab_na_lic": r[17],
            "perc_ead_total_na_lic": r[18],
            "indice_dependencia_uab": to_num_or_none(r[19]),
            "perc_presencial_na_lic": r[20],
        })
    out = {
        "gerado_em": "2026-10-29",
        "fonte": "Apêndice C da dissertação — elaborado pelo autor a partir dos microdados do INEP (Censo da Educação Superior, 2024)",
        "ano": 2024,
        "registros": registros,
    }
    path = os.path.join(DATA_DIR, "apendice_c_indicadores_2024.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"OK: {len(registros)} registros -> {path}")


def parse_apendice_d():
    wb = openpyxl.load_workbook(ARQ_D, data_only=True, read_only=True)
    ws = wb["Resumo Todas IES"]
    rows = list(ws.iter_rows(min_row=1, values_only=True))
    blank_idxs = [i for i, r in enumerate(rows) if all(c is None for c in r)]
    starts = [blank_idxs[0] + 1] + [b + 1 for b in blank_idxs[1:]]
    ends = blank_idxs[1:] + [len(rows)]

    def rotulo(lbl):
        l = (lbl or "").lower()
        if "total de matr" in l:
            return "matriculas_total"
        if "matr" in l and "licenciatura" in l:
            return "matriculas_licenciatura"
        if "cursos de licenciatura" in l:
            return "num_cursos_licenciatura"
        if "campus" in l:
            return "num_campus"
        if "polos ead pr" in l:
            return "num_polos_proprios"
        if "polos ead" in l:
            return "num_polos_ead"
        if "uab" in l:
            return "num_polos_uab"
        return None

    blocos = {}
    for s, e in zip(starts, ends):
        block_rows = rows[s:e]
        if len(block_rows) < 3:
            continue
        nome = block_rows[0][0]
        header_idx = None
        for i, r in enumerate(block_rows):
            if r[0] == "Cursos" and r[1] == "Campus":
                header_idx = i
                break
        if header_idx is None:
            continue
        resumo = {"2014": {}, "2024": {}}
        for r in block_rows[2:header_idx]:
            lbl14, v14, _, lbl24, v24, _ = r
            k14, k24 = rotulo(lbl14), rotulo(lbl24)
            if k14:
                resumo["2014"][k14] = v14
            if k24:
                resumo["2024"][k24] = v24
        blocos[nome] = resumo
    return blocos


def parse_apendice_e():
    wb = openpyxl.load_workbook(ARQ_E, data_only=True, read_only=True)
    ws = wb["Dados"]
    rows = list(ws.iter_rows(min_row=1, values_only=True))
    header_idxs = [
        i for i, r in enumerate(rows)
        if r[0] is not None and r[1] is None and r[2] is None and r[3] is None
        and "NDICE" not in (r[0] or "")
    ]
    starts = header_idxs
    ends = header_idxs[1:] + [len(rows)]

    blocos = {}
    for s, e in zip(starts, ends):
        nome = rows[s][0]
        block = rows[s:e]
        cursos14, cursos24 = [], []
        for r in block[3:]:
            c14, loc14, c24, loc24 = r
            if c14:
                cursos14.append({"curso": c14, "local": loc14})
            if c24:
                cursos24.append({"curso": c24, "local": loc24})
        blocos[nome] = {"2014": cursos14, "2024": cursos24}
    return blocos


def carregar_sigla_estado_por_nome():
    with open(LIC_IES_GERAL, encoding="utf-8") as f:
        data = json.load(f)
    mapa = {}
    for r in data["registros"]:
        mapa.setdefault(r["ies_nome"], (r["sigla"], r["estado"]))
    return mapa


def exportar_perfil_institucional():
    resumos = parse_apendice_d()
    cursos = parse_apendice_e()
    nome_para_sigla = carregar_sigla_estado_por_nome()

    nomes = sorted(set(resumos.keys()) | set(cursos.keys()))
    registros = []
    sem_sigla = []
    for nome in nomes:
        sigla, estado = nome_para_sigla.get(nome, (None, None))
        if sigla is None:
            sem_sigla.append(nome)
        registros.append({
            "nome_ies": nome,
            "sigla": sigla,
            "estado": estado,
            "resumo": resumos.get(nome, {"2014": {}, "2024": {}}),
            "cursos": cursos.get(nome, {"2014": [], "2024": []}),
        })

    if sem_sigla:
        print("AVISO: IES sem sigla/estado encontrados (nao bateu com lic_ies_geral.json):")
        for n in sem_sigla:
            print("  -", n)

    out = {
        "gerado_em": "2026-10-29",
        "fonte": "Apêndices IV (resumo 2014 x 2024) e III (cursos e locais) da dissertação — elaborado pelo autor a partir dos microdados do INEP",
        "anos": [2014, 2024],
        "registros": registros,
    }
    path = os.path.join(DATA_DIR, "apendice_perfil_institucional.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"OK: {len(registros)} IES -> {path}")


if __name__ == "__main__":
    exportar_apendice_c()
    exportar_perfil_institucional()

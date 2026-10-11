# -*- coding: utf-8 -*-
"""Gera o projeto Power BI painel_matriculas (PBIP/TMDL) a partir do painel_cursos.

Mesmo modelo conceitual do painel_cursos (mesma fato, dimensoes e filtros em tabelas),
com tres diferencas:
  a) sem o grafico de quantidade de cursos;
  b) o grafico de linhas por ano_censo ficou mais alto e perdeu o slicer de metrica unica:
     no lugar entra um slicer MULTIPLO sobre um parametro de campos (field parameter) com as
     metricas (matriculas, ingressantes, vagas, concluintes, trancadas, desligados). Cada
     metrica marcada vira uma linha no eixo Y; o eixo X e sempre o ano do Censo;
  c) filtros novos, sempre pela descricao: cine_rotulo, grande area (area geral CINE) e
     area detalhada, vindos de dim_cine.

Reaproveita as tabelas (.tmdl com as particoes M/Python) e os visuais do painel_cursos; so
reescreve o que muda. Uso: python powerbi/build_pbip_matriculas.py -> abre painel_matriculas.pbip.
"""
import json
import shutil
import uuid
from pathlib import Path

HERE = Path(__file__).parent
NOME = "painel_matriculas"
SRC_MODEL = HERE / "painel_cursos.SemanticModel"
SRC_REP = HERE / "painel_cursos.Report"
OUT_MODEL = HERE / f"{NOME}.SemanticModel"
OUT_REP = HERE / f"{NOME}.Report"
TEMPLATE = SRC_REP / "definition" / "pages" / "pagina1" / "visuals"
FATO = "fato_curso_censo"
PARAM = "Metricas Parametro"

V_CURSOS = "1bdfedacee426762d527"      # grafico de cursos (removido)
V_LINHAS = "ea3da53062d058018a0f"      # grafico de linhas (modelo do novo grafico)
V_SLICER = "b971dd5897f664e4c061"      # slicer de metrica (vira multiplo)
V_MODELO_FILTRO = "309c7c98db9dab5e8810"  # tabela-filtro usada como modelo dos novos

# (nome da medida / rotulo no slicer, coluna da fato)
METRICAS = [
    ("Qtde Matrículas", "qt_vg_mat"),
    ("Qtde Ingressantes", "qt_vg_ing"),
    ("Qtde Vagas Totais", "qt_vg_total"),
    ("Qtde Concluintes", "qt_vg_conc"),
    ("Situação Trancada", "qt_sit_trancada"),
    ("Situação Desligado", "qt_sit_desligado"),
]
PADRAO = ["Qtde Matrículas", "Qtde Concluintes"]  # marcadas ao abrir

# Campos que aparecem no subtitulo ("filtros selecionados") dos graficos.
CAMPOS_FILTRO = [
    ("dim_territorio", "nome_regiao"),
    ("dim_territorio", "sigla_uf"),
    ("dim_territorio", "nome_mesorregiao"),
    ("dim_territorio", "nome_microrregiao"),
    ("dim_territorio", "nome_municipio"),
    ("dim_rede", "nome_rede"),
    ("dim_categoria_administrativa", "nome_categoria_administrativa"),
    ("dim_modalidade_ensino", "nome_modalidade_ensino"),
    ("dim_organizacao_academica", "nome_organizacao_academica"),
    ("dim_grau_academico", "nome_grau_academico"),
    ("dim_cine", "nome_area_geral"),
    ("dim_cine", "nome_area_detalhada"),
    ("dim_cine", "nome_cine_rotulo"),
]

# Novas tabelas-filtro: (id, tabela, coluna, rotulo, x, y, largura, altura)
NOVOS_FILTROS = [
    ("filtro_grande_area", "dim_cine", "nome_area_geral", "Grande área", 0, 305, 300, 108),
    ("filtro_area_detalhada", "dim_cine", "nome_area_detalhada", "Área detalhada", 300, 305, 420, 108),
    ("filtro_cine_rotulo", "dim_cine", "nome_cine_rotulo", "CINE rótulo", 720, 305, 560, 108),
]

# ---------------------------------------------------------------- modelo
def ler(p):
    return p.read_text(encoding="utf-8-sig")


def gravar(p, txt):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(txt, encoding="utf-8", newline="\n")


def tag():
    return str(uuid.uuid4())


def dax_filtros():
    def var(i, t, c):
        col = f"{t}[{c}]"
        return (
            f"VAR _v{i} = IF(ISFILTERED({col}), IF(COUNTROWS(VALUES({col})) <= 3, "
            f'CONCATENATEX(VALUES({col}), {col}, ", "), COUNTROWS(VALUES({col})) & " itens"), "")'
        )

    partes = " ".join(var(i, t, c) for i, (t, c) in enumerate(CAMPOS_FILTRO))
    junta = " & ".join(f'IF(_v{i} <> "", _v{i} & "/", "")' for i in range(len(CAMPOS_FILTRO)))
    return f'{partes} VAR _a = {junta} RETURN IF(_a = "", "", LEFT(_a, LEN(_a) - 1))'


def medidas_tmdl():
    def m(nome, dax, fmt=None):
        s = f"\tmeasure '{nome}' = {dax}\n"
        if fmt:
            s += f"\t\tformatString: {fmt}\n"
        return s + f"\t\tlineageTag: {tag()}\n\n"

    return (
        "".join(m(n, f"SUMX({FATO}, VALUE({FATO}[{c}]))", "#,0") for n, c in METRICAS)
        + m("Filtros Selecionados", dax_filtros())
        + m("Subtitulo Filtros", 'VAR _f = [Filtros Selecionados] RETURN IF(_f = "", "", "(" & _f & ")")')
    )


def tabela_parametro():
    itens = ",\n\t\t\t\t".join(f'("{n}", NAMEOF({FATO}[{n}]), {i})' for i, (n, _) in enumerate(METRICAS))
    return (
        f"table '{PARAM}'\n\tlineageTag: {tag()}\n\n"
        f"\tcolumn '{PARAM}'\n\t\tlineageTag: {tag()}\n\t\tsummarizeBy: none\n\t\tsourceColumn: [Value1]\n"
        f"\t\tsortByColumn: '{PARAM} Order'\n\n"
        f"\t\trelatedColumnDetails\n\t\t\tgroupByColumn: '{PARAM} Fields'\n\n"
        f"\tcolumn '{PARAM} Fields'\n\t\tisHidden\n\t\tlineageTag: {tag()}\n\t\tsummarizeBy: none\n"
        f"\t\tsourceColumn: [Value2]\n\t\textendedProperty ParameterMetadata =\n"
        '\t\t\t\t{\n\t\t\t\t  "version": 3,\n\t\t\t\t  "kind": 2\n\t\t\t\t}\n\n'
        f"\tcolumn '{PARAM} Order'\n\t\tisHidden\n\t\tformatString: 0\n\t\tlineageTag: {tag()}\n"
        f"\t\tsummarizeBy: sum\n\t\tsourceColumn: [Value3]\n\n"
        f"\tpartition '{PARAM}' = calculated\n\t\tmode: import\n\t\tsource =\n"
        f"\t\t\t\t{{\n\t\t\t\t{itens}\n\t\t\t\t}}\n\n"
    )


def gerar_modelo():
    shutil.rmtree(OUT_MODEL, ignore_errors=True)
    d_src = SRC_MODEL / "definition"
    d_out = OUT_MODEL / "definition"
    # tabelas: copia todas, menos dim_metricas (substituida pelo parametro de campos)
    for f in (d_src / "tables").glob("*.tmdl"):
        if f.stem == "dim_metricas":
            continue
        txt = ler(f)
        if f.stem == FATO:
            i, j = txt.index("\tmeasure 'Valor Selecionado'"), txt.index("\tcolumn codigo_ano")
            txt = txt[:i] + medidas_tmdl() + txt[j:]
        gravar(d_out / "tables" / f.name, txt)
    gravar(d_out / "tables" / f"{PARAM}.tmdl", tabela_parametro())
    gravar(d_out / "relationships.tmdl", ler(d_src / "relationships.tmdl"))
    gravar(d_out / "database.tmdl", ler(d_src / "database.tmdl"))
    model = ler(d_src / "model.tmdl").replace("ref table dim_metricas", f"ref table '{PARAM}'")
    gravar(d_out / "model.tmdl", model)
    gravar(d_out / "cultures" / "pt-BR.tmdl", "cultureInfo pt-BR\n")
    shutil.copy(SRC_MODEL / "definition.pbism", OUT_MODEL / "definition.pbism")
    gravar(OUT_MODEL / ".platform", json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
        "metadata": {"type": "SemanticModel", "displayName": NOME},
        "config": {"version": "2.0", "logicalId": tag()}}, indent=2))
    print("modelo: tabelas", sorted(p.stem for p in (d_out / "tables").glob("*.tmdl")))


# ---------------------------------------------------------------- relatorio
S = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition"
L = lambda v: {"expr": {"Literal": {"Value": v}}}


def carregar_visual(vid):
    return json.loads(ler(TEMPLATE / vid / "visual.json"))


def gravar_visual(vid, j):
    gravar(OUT_REP / "definition" / "pages" / "pagina1" / "visuals" / vid / "visual.json",
           json.dumps(j, indent=2, ensure_ascii=False))


def col(entidade, prop):
    return {"Column": {"Expression": {"SourceRef": {"Entity": entidade}}, "Property": prop}}


def gerar_relatorio():
    shutil.rmtree(OUT_REP, ignore_errors=True)
    d = OUT_REP / "definition"
    gravar(OUT_REP / "definition.pbir", json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
        "version": "4.0", "datasetReference": {"byPath": {"path": f"../{NOME}.SemanticModel"}}}, indent=2))
    gravar(OUT_REP / ".platform", json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
        "metadata": {"type": "Report", "displayName": NOME},
        "config": {"version": "2.0", "logicalId": tag()}}, indent=2))
    for f in ("report.json", "version.json"):
        gravar(d / f, ler(SRC_REP / "definition" / f))
    gravar(d / "pages" / "pages.json", json.dumps(
        {"$schema": f"{S}/pagesMetadata/1.0.0/schema.json", "pageOrder": ["pagina1"], "activePageName": "pagina1"}, indent=2))
    gravar(d / "pages" / "pagina1" / "page.json", json.dumps(
        {"$schema": f"{S}/page/1.0.0/schema.json", "name": "pagina1", "displayName": "Painel de Matrículas",
         "displayOption": "FitToPage", "height": 720, "width": 1280}, indent=2))

    # tabelas-filtro existentes: copiadas como estao (menos o grafico de cursos e os dois que mudam)
    for p in TEMPLATE.iterdir():
        if p.name not in (V_CURSOS, V_LINHAS, V_SLICER):
            gravar_visual(p.name, carregar_visual(p.name))

    # novos filtros (cine_rotulo, grande area, area detalhada), a partir da tabela de modalidade
    modelo = ler(TEMPLATE / V_MODELO_FILTRO / "visual.json")
    for i, (vid, ent, prop, rotulo, x, y, w, h) in enumerate(NOVOS_FILTROS):
        txt = (modelo.replace("dim_modalidade_ensino", ent).replace("nome_modalidade_ensino", prop)
               .replace(V_MODELO_FILTRO, vid).replace('"Modalidade"', f'"{rotulo}"').replace('"Descending"', '"Ascending"'))
        j = json.loads(txt)
        j["position"].update(x=x, y=y, width=w, height=h, z=14000 + i, tabOrder=14000 + i)
        gravar_visual(vid, j)

    # grafico de linhas: X = ano, Y = metricas marcadas no slicer (parametro de campos)
    j = carregar_visual(V_LINHAS)
    j["name"] = "grafico_linhas"
    j["position"].update(x=0, y=418, height=302, width=1089.36)
    j["visual"]["query"]["queryState"]["Y"] = {"projections": [{
        "field": col(PARAM, f"{PARAM} Fields"),
        "queryRef": f"{PARAM}.{PARAM} Fields", "nativeQueryRef": f"{PARAM} Fields", "active": True}]}
    j["visual"]["objects"]["legend"] = [{"properties": {
        "show": L("true"), "position": L("'Top'"), "fontSize": L("9D")}}]
    j["visual"]["visualContainerObjects"]["title"][0]["properties"]["text"] = L("'Evolução anual por ano do Censo'")
    gravar_visual("grafico_linhas", j)
    shutil.rmtree(OUT_REP / "definition" / "pages" / "pagina1" / "visuals" / V_LINHAS, ignore_errors=True)

    # slicer: selecao multipla sobre o parametro de campos
    j = carregar_visual(V_SLICER)
    j["name"] = "slicer_metricas"
    j["position"].update(x=1089.36, y=418, height=302, width=190.64)
    proj = j["visual"]["query"]["queryState"]["Values"]["projections"][0]
    proj.update(field=col(PARAM, PARAM), queryRef=f"{PARAM}.{PARAM}", nativeQueryRef=PARAM)
    sel = j["visual"]["objects"]["selection"][0]["properties"]
    sel.update(singleSelect=L("false"), selectAllCheckboxEnabled=L("false"))
    sel.pop("strictSingleSelect", None)
    flt = j["visual"]["objects"]["general"][0]["properties"]["filter"]["filter"]
    flt["From"][0]["Entity"] = PARAM
    cond = flt["Where"][0]["Condition"]["In"]
    cond["Expressions"][0]["Column"]["Property"] = PARAM
    cond["Values"] = [[{"Literal": {"Value": f"'{n}'"}}] for n in PADRAO]
    j["visual"]["visualContainerObjects"]["title"][0]["properties"]["text"] = L("'Métricas (marque até 5)'")
    j["filterConfig"]["filters"][0]["field"] = col(PARAM, PARAM)
    gravar_visual("slicer_metricas", j)
    print("relatorio:", f"{NOME}.Report")


gerar_modelo()
gerar_relatorio()
gravar(HERE / f"{NOME}.pbip", json.dumps(
    {"$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
     "version": "1.0", "artifacts": [{"report": {"path": f"{NOME}.Report"}}],
     "settings": {"enableAutoRecovery": True}}, indent=2))
print(f"ok: {NOME}.pbip")

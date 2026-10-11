# -*- coding: utf-8 -*-
"""Gera o projeto Power BI painel_comparativo (PBIP/TMDL) a partir do painel_matriculas.

Mesmo modelo conceitual (fato_curso_censo + dimensoes). Diferencas em relacao ao painel_matriculas:
  - filtros removidos: modalidade, categoria administrativa, area detalhada e rede;
  - nova disposicao dos filtros: [PNE / ano] [organizacao] [grau] [grande area] [cine rotulo] [territorio];
  - o grafico compara ate 5 linhas. Cada linha = uma combinacao de tres grupos de metricas:
      1) modalidade (Presencial, Curso a distancia, Ambas)
      2) categoria (publica federal/estadual/municipal, privadas..., Ambas)
      3) valor (matriculas, ingressantes, vagas, inscritos, concluintes, trancadas, desligados)
    Os tres slicers sao multiplos e atuam sobre dim_comparacao (todas as combinacoes); cada
    combinacao marcada vira uma linha, com a marcacao na legenda. Acima de 5 combinacoes o
    grafico mostra as 5 primeiras (ordem dos grupos) e o titulo avisa.

Le o painel_matriculas como esta no disco (preserva ajustes feitos no Desktop) e NAO o altera.
Uso: python powerbi/build_pbip_comparativo.py -> abre powerbi/painel_comparativo.pbip.
"""
import json
import shutil
import sqlite3
import uuid
from pathlib import Path

HERE = Path(__file__).parent
NOME = "painel_comparativo"
ORIGEM = "painel_matriculas"
SRC_MODEL = HERE / f"{ORIGEM}.SemanticModel"
SRC_REP = HERE / f"{ORIGEM}.Report"
OUT_MODEL = HERE / f"{NOME}.SemanticModel"
OUT_REP = HERE / f"{NOME}.Report"
SRC_VIS = SRC_REP / "definition" / "pages" / "pagina1" / "visuals"
DB = Path("D:/Mestrado/Dados/bdados/INEP.db")
FATO = "fato_curso_censo"
COMP = "dim_comparacao"
MAX_LINHAS = 5

MODALIDADES = ["Presencial", "Curso a distância", "Ambas"]
# Rotulos "(todas)" agrupam por tp_rede (dim_rede); "Ambas" = sem filtro.
CATEGORIAS = [
    "Pública (todas)", "Pública Federal", "Pública Estadual", "Pública Municipal",
    "Privada (todas)", "Privada com fins lucrativos", "Privada sem fins lucrativos",
    "Privada - Particular em sentido estrito", "Privada comunitária", "Privada confessional",
    "Especial", "Ambas",
]
AGRUPAMENTOS = {"Pública (todas)": "Pública", "Privada (todas)": "Privada"}
METRICAS = [
    ("Qtde Matrículas", "qt_vg_mat"),
    ("Qtde Ingressantes", "qt_vg_ing"),
    ("Qtde Vagas Totais", "qt_vg_total"),
    ("Qtde Inscritos", "qt_inscrito_total"),
    ("Qtde Concluintes", "qt_vg_conc"),
    ("Situação Trancada", "qt_sit_trancada"),
    ("Situação Desligado", "qt_sit_desligado"),
]
PADRAO = {"Modalidade": "Presencial", "Categoria": "Ambas", "Metrica": "Qtde Matrículas"}

CAMPOS_FILTRO = [
    ("dim_territorio", "nome_regiao"),
    ("dim_territorio", "sigla_uf"),
    ("dim_territorio", "nome_mesorregiao"),
    ("dim_territorio", "nome_microrregiao"),
    ("dim_territorio", "nome_municipio"),
    ("dim_organizacao_academica", "nome_organizacao_academica"),
    ("dim_grau_academico", "nome_grau_academico"),
    ("dim_cine", "nome_area_geral"),
    ("dim_cine", "nome_cine_rotulo"),
]


def ler(p):
    return p.read_text(encoding="utf-8-sig")


def gravar(p, txt):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(txt, encoding="utf-8", newline="\n")


def tag():
    return str(uuid.uuid4())


def conferir_nomes_no_banco():
    """Os rotulos de modalidade/categoria precisam ser identicos aos das dimensoes."""
    con = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    modal = {r[0] for r in con.execute("SELECT nome FROM superior_tp_modal_ensino")}
    cat = {r[0] for r in con.execute("SELECT nome FROM superior_tp_categoria_administrativa")}
    rede = {r[0] for r in con.execute("SELECT nome FROM superior_tp_rede")}
    con.close()
    falta = ([m for m in MODALIDADES if m != "Ambas" and m not in modal]
             + [c for c in CATEGORIAS if c != "Ambas" and c not in AGRUPAMENTOS and c not in cat]
             + [r for r in AGRUPAMENTOS.values() if r not in rede])
    assert not falta, f"nomes que nao existem no banco: {falta}"
    sobra = cat - set(CATEGORIAS)
    assert not sobra, f"categorias do banco sem opcao no painel: {sobra}"


# ---------------------------------------------------------------- DAX
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


DAX_VALOR_BASE = "SWITCH(SELECTEDVALUE(%s[Metrica]), %s, BLANK())" % (
    COMP, ", ".join(f'"{n}", [{n}]' for n, _ in METRICAS))

_MOD = "dim_modalidade_ensino[nome_modalidade_ensino]"
_CAT = "dim_categoria_administrativa[nome_categoria_administrativa]"
_REDE = "dim_rede[nome_rede]"
_TODAS = ", ".join(f'"{c}"' for c in ["Ambas"] + list(AGRUPAMENTOS))
_REDES = ", ".join(f'"{k}", "{v}"' for k, v in AGRUPAMENTOS.items())
# Filtros do CALCULATE = FILTER(ALL(coluna), condicao sobre UMA coluna); variaveis de tabela
# montadas com IF/SWITCH geram o erro "expressao True/False nao especifica uma coluna".
# Medida unica (sem medida auxiliar): o Desktop descartou uma medida "Valor Bruto" separada.
# Limite: acima de MAX_LINHAS combinacoes marcadas nada e desenhado e o titulo pede para reduzir.
DAX_VALOR_COMP = (
    f"VAR _n = CALCULATE(COUNTROWS({COMP}), REMOVEFILTERS({COMP}[Rotulo])) "
    f"VAR _mod = SELECTEDVALUE({COMP}[Modalidade]) "
    f"VAR _cat = SELECTEDVALUE({COMP}[Categoria]) "
    f"VAR _catTodas = _cat IN {{{_TODAS}}} "
    f'VAR _rede = SWITCH(_cat, {_REDES}, "") '
    f"RETURN IF(_n > {MAX_LINHAS} || ISBLANK(_mod) || ISBLANK(_cat), BLANK(), CALCULATE([Valor Base], "
    f'FILTER(ALL({_MOD}), _mod = "Ambas" || {_MOD} = _mod), '
    f"FILTER(ALL({_CAT}), _catTodas || {_CAT} = _cat), "
    f'FILTER(ALL({_REDE}), _rede = "" || {_REDE} = _rede)))'
)
DAX_TITULO = (
    f"VAR _n = COUNTROWS({COMP}) "
    f'RETURN IF(_n > {MAX_LINHAS}, "Comparativo anual: " & _n & " combinações marcadas — marque no máximo {MAX_LINHAS}", '
    f'"Comparativo anual por ano do Censo (" & _n & IF(_n = 1, " linha)", " linhas)"))'
)


def medidas_tmdl():
    def m(nome, dax, fmt=None):
        s = f"\tmeasure '{nome}' = {dax}\n"
        if fmt:
            s += f"\t\tformatString: {fmt}\n"
        return s + f"\t\tlineageTag: {tag()}\n\n"

    return (
        "".join(m(n, f"SUMX({FATO}, VALUE({FATO}[{c}]))", "#,0") for n, c in METRICAS)
        + m("Valor Base", DAX_VALOR_BASE, "#,0")
        + m("Valor Comparativo", DAX_VALOR_COMP, "#,0")
        + m("Titulo Comparativo", DAX_TITULO)
        + m("Filtros Selecionados", dax_filtros())
        + m("Subtitulo Filtros", 'VAR _f = [Filtros Selecionados] RETURN IF(_f = "", "", "(" & _f & ")")')
    )


MOD_CURTO = {"Presencial": "Presencial", "Curso a distância": "A distância", "Ambas": "Ambas"}
CAT_CURTO = {
    "Pública (todas)": "Todas públicas", "Pública Federal": "Púb. Federal", "Pública Estadual": "Púb. Estadual",
    "Pública Municipal": "Púb. Municipal", "Privada (todas)": "Todas privadas",
    "Privada com fins lucrativos": "Priv. c/ fins lucr.", "Privada sem fins lucrativos": "Priv. s/ fins lucr.",
    "Privada - Particular em sentido estrito": "Priv. particular", "Privada comunitária": "Priv. comunitária",
    "Privada confessional": "Priv. confessional", "Especial": "Especial", "Ambas": "Ambas",
}
MET_CURTO = {"Qtde Matrículas": "Matrículas", "Qtde Ingressantes": "Ingressantes", "Qtde Vagas Totais": "Vagas",
             "Qtde Inscritos": "Inscritos", "Qtde Concluintes": "Concluintes",
             "Situação Trancada": "Trancadas", "Situação Desligado": "Desligados"}


def dax_comparacao(modalidades, categorias, metricas):
    """Tabela de combinacoes. Slicers usam os nomes completos; a legenda (Rotulo) usa os curtos,
    porque a legenda do Power BI nao quebra linha e trunca rotulos longos com reticencias."""
    def dt(col, ordcol, curta, itens, mapa):
        linhas = ", ".join(f'{{"{v}", {i + 1}, "{mapa[v]}"}}' for i, v in enumerate(itens))
        return f'DATATABLE("{col}", STRING, "{ordcol}", INTEGER, "{curta}", STRING, {{{linhas}}})'

    sel = ", ".join(f'"{c}", [{c}]' for c in
                    ["Modalidade", "OrdM", "Categoria", "OrdC", "Metrica", "OrdK", "Rotulo", "Ordem"])
    ind = "\n\t\t\t\t"
    return (
        f"VAR _m = {dt('Modalidade', 'OrdM', 'ModC', modalidades, MOD_CURTO)}{ind}"
        f"VAR _c = {dt('Categoria', 'OrdC', 'CatC', categorias, CAT_CURTO)}{ind}"
        f"VAR _k = {dt('Metrica', 'OrdK', 'MetC', metricas, MET_CURTO)}{ind}"
        f"RETURN SELECTCOLUMNS(ADDCOLUMNS(CROSSJOIN(_m, _c, _k), "
        f'"Rotulo", [ModC] & " · " & [CatC] & " · " & [MetC], '
        f'"Ordem", [OrdM] * 10000 + [OrdC] * 100 + [OrdK]), {sel})'
    )


def tabela_comparacao():
    dax = dax_comparacao(MODALIDADES, CATEGORIAS, [n for n, _ in METRICAS])

    def col(nome, tipo, ordem=None, oculta=False):
        s = f"\tcolumn {nome}\n\t\tdataType: {tipo}\n"
        if oculta:
            s += "\t\tisHidden\n"
        if tipo == "int64":
            s += "\t\tformatString: 0\n"
        s += f"\t\tlineageTag: {tag()}\n\t\tsummarizeBy: none\n\t\tsourceColumn: [{nome}]\n"
        if ordem:
            s += f"\t\tsortByColumn: {ordem}\n"
        return s + "\n"

    return (
        f"table {COMP}\n\tlineageTag: {tag()}\n\n"
        + col("Modalidade", "string", "OrdM") + col("OrdM", "int64", oculta=True)
        + col("Categoria", "string", "OrdC") + col("OrdC", "int64", oculta=True)
        + col("Metrica", "string", "OrdK") + col("OrdK", "int64", oculta=True)
        + col("Rotulo", "string", "Ordem") + col("Ordem", "int64", oculta=True)
        + f"\tpartition {COMP} = calculated\n\t\tmode: import\n\t\tsource =\n\t\t\t\t{dax}\n"
    )


# ---------------------------------------------------------------- modelo
def gerar_modelo():
    shutil.rmtree(OUT_MODEL, ignore_errors=True)
    d_src, d_out = SRC_MODEL / "definition", OUT_MODEL / "definition"
    for f in (d_src / "tables").glob("*.tmdl"):
        if f.stem == "Metricas Parametro":
            continue
        txt = ler(f)
        if f.stem == FATO:
            i, j = txt.index("\tmeasure "), txt.index("\tcolumn codigo_ano")
            txt = txt[:i] + medidas_tmdl() + txt[j:]
            assert "column qt_inscrito_total" in txt and "qt_inscrito_total,#(lf)" in txt
        gravar(d_out / "tables" / f.name, txt)
    gravar(d_out / "tables" / f"{COMP}.tmdl", tabela_comparacao())
    for f in ("relationships.tmdl", "database.tmdl"):
        gravar(d_out / f, ler(d_src / f))
    gravar(d_out / "model.tmdl", ler(d_src / "model.tmdl").replace("ref table 'Metricas Parametro'", f"ref table {COMP}"))
    gravar(d_out / "cultures" / "pt-BR.tmdl", "cultureInfo pt-BR\n")
    shutil.copy(SRC_MODEL / "definition.pbism", OUT_MODEL / "definition.pbism")
    gravar(OUT_MODEL / ".platform", json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
        "metadata": {"type": "SemanticModel", "displayName": NOME},
        "config": {"version": "2.0", "logicalId": tag()}}, indent=2))
    print("modelo:", sorted(p.stem for p in (d_out / "tables").glob("*.tmdl")))


# ---------------------------------------------------------------- relatorio
S = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition"
L = lambda v: {"expr": {"Literal": {"Value": v}}}


def vis(vid):
    return json.loads(ler(SRC_VIS / vid / "visual.json"))


def gravar_visual(vid, j):
    gravar(OUT_REP / "definition" / "pages" / "pagina1" / "visuals" / vid / "visual.json",
           json.dumps(j, indent=2, ensure_ascii=False))


def col(entidade, prop):
    return {"Column": {"Expression": {"SourceRef": {"Entity": entidade}}, "Property": prop}}


# id do visual -> (x, y, largura, altura). Linha de filtros: y=0, altura 300.
H = 299.4
LAYOUT = {
    "59874fb5d812c584e207": (0, 0, 100, 80),            # periodo PNE
    "ba8d6b871b69f5525472": (0, 80, 100, H - 80),       # ano (abaixo do PNE)
    "d446ed6b54510e064385": (100, 0, 150, H),           # organizacao academica
    "2e0536257dcd97524152": (250, 0, 150, H),           # grau academico
    "filtro_grande_area": (400, 0, 150, H),
    "filtro_cine_rotulo": (550, 0, 250, H),
    "58ca5435197c55fb501e": (800, 0, 100, H),           # regiao
    "a52b48f84bfa23870a6f": (900, 0, 50, H),            # UF
    "edff9ccbecabb85c9b25": (950, 0, 110, H),           # mesorregiao
    "e71e2521c986af848283": (1060, 0, 110, H),          # microrregiao
    "9059b435f66d5d353d3b": (1170, 0, 110, H),          # municipio
}
REMOVER = {"309c7c98db9dab5e8810",   # modalidade
           "be3fc304e4f6c0bf00a0",   # categoria administrativa
           "9f0d5db67bf2d68d31c4",   # rede
           "filtro_area_detalhada", "slicer_metricas", "grafico_linhas"}

Y_GRAF, H_GRAF = 310, 410
SLICERS = [  # (id, coluna, titulo, x, largura)
    ("slicer_modalidade", "Modalidade", "Modalidade", 800, 130),
    ("slicer_categoria", "Categoria", "Categoria", 930, 200),
    ("slicer_metrica", "Metrica", "Valor (métrica)", 1130, 150),
]


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
        {"$schema": f"{S}/page/1.0.0/schema.json", "name": "pagina1", "displayName": "Painel Comparativo",
         "displayOption": "FitToPage", "height": 720, "width": 1280}, indent=2, ensure_ascii=False))

    # filtros que ficam: copia do painel_matriculas e reposiciona
    for vid, (x, y, w, h) in LAYOUT.items():
        j = vis(vid)
        j["position"].update(x=x, y=y, width=w, height=h)
        gravar_visual(vid, j)
    sobras = {p.name for p in SRC_VIS.iterdir()} - set(LAYOUT) - REMOVER
    assert not sobras, f"visuais da origem sem destino: {sobras}"

    # grafico: X = ano, legenda = combinacao marcada, Y = valor da combinacao
    j = vis("grafico_linhas")
    j["name"] = "grafico_comparativo"
    j["position"].update(x=0, y=Y_GRAF, width=800, height=H_GRAF)
    q = j["visual"]["query"]["queryState"]
    q["Series"] = {"projections": [{"field": col(COMP, "Rotulo"), "queryRef": f"{COMP}.Rotulo",
                                    "nativeQueryRef": "Rotulo", "active": True}]}
    q["Y"] = {"projections": [{"field": {"Measure": {"Expression": {"SourceRef": {"Entity": FATO}},
                                                     "Property": "Valor Comparativo"}},
                               "queryRef": f"{FATO}.Valor Comparativo", "nativeQueryRef": "Valor Comparativo"}]}
    j["visual"]["objects"]["legend"] = [{"properties": {
        "show": L("true"), "position": L("'Right'"), "showTitle": L("false"), "fontSize": L("9D")}}]
    j["visual"]["visualContainerObjects"]["title"][0]["properties"]["text"] = {"expr": {"Measure": {
        "Expression": {"SourceRef": {"Entity": FATO}}, "Property": "Titulo Comparativo"}}}
    gravar_visual("grafico_comparativo", j)

    # tres slicers multiplos sobre dim_comparacao (a partir do slicer de metricas)
    base = vis("slicer_metricas")
    for vid, coluna, titulo, x, w in SLICERS:
        j = json.loads(json.dumps(base))
        j["name"] = vid
        j["position"].update(x=x, y=Y_GRAF, width=w, height=H_GRAF)
        proj = j["visual"]["query"]["queryState"]["Values"]["projections"][0]
        proj.update(field=col(COMP, coluna), queryRef=f"{COMP}.{coluna}", nativeQueryRef=coluna)
        flt = j["visual"]["objects"]["general"][0]["properties"]["filter"]["filter"]
        flt["From"][0]["Entity"] = COMP
        w0 = flt["Where"][0]
        w0.pop("Annotations", None)
        w0["Condition"]["In"]["Expressions"][0]["Column"]["Property"] = coluna
        w0["Condition"]["In"]["Values"] = [[{"Literal": {"Value": f"'{PADRAO[coluna]}'"}}]]
        sel = j["visual"]["objects"]["selection"][0]["properties"]
        sel.update(singleSelect=L("false"), selectAllCheckboxEnabled=L("false"))
        sel.pop("strictSingleSelect", None)
        j["visual"]["visualContainerObjects"]["title"][0]["properties"]["text"] = L(f"'{titulo}'")
        j["filterConfig"]["filters"] = [{"name": uuid.uuid4().hex[:20], "field": col(COMP, coluna), "type": "Categorical"}]
        gravar_visual(vid, j)
    print("relatorio:", f"{NOME}.Report")


conferir_nomes_no_banco()
gerar_modelo()
gerar_relatorio()
gravar(HERE / f"{NOME}.pbip", json.dumps(
    {"$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
     "version": "1.0", "artifacts": [{"report": {"path": f"{NOME}.Report"}}],
     "settings": {"enableAutoRecovery": True}}, indent=2))
print(f"ok: {NOME}.pbip")

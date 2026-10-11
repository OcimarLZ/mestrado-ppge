# -*- coding: utf-8 -*-
"""Gera o projeto Power BI painel_ies_cursos (PBIP/TMDL) a partir de scripts_ies_cursos/*.py.

Fato = fato_curso_censo (curso x IES x ano). A pagina tem os mesmos filtros do
painel_cursos e UMA matriz: IES que respondem aos filtros, com drill-down (+) para os
cursos de cada IES. Os valores da matriz usam o ULTIMO ANO selecionado no filtro de ano
(sem filtro = ano mais recente), porque somar matriculas de anos diferentes nao faz sentido.

Estrutura de geracao igual a de build_pbip_ies.py (um script Python por tabela).
Uso: python powerbi/build_pbip_ies_cursos.py -> abre powerbi/painel_ies_cursos.pbip.
"""
import importlib.util
import json
import shutil
import uuid
from pathlib import Path

HERE = Path(__file__).parent
SCRIPTS_DIR = HERE / "scripts_ies_cursos"
OUT = HERE / "painel_ies_cursos.SemanticModel"
REP = HERE / "painel_ies_cursos.Report"
TEMPLATE = HERE / "painel_cursos.Report" / "definition" / "pages" / "pagina1" / "visuals"
FATO = "fato_curso_censo"

# Colunas da matriz: (nome da medida, formula do valor no ultimo ano). None = Qtde Cursos.
MEDIDAS_MATRIZ = [
    ("Qtde Cursos", None),
    ("Vagas Totais", "qt_vg_total"),
    ("Ingressantes", "qt_vg_ing"),
    ("Matrículas", "qt_vg_mat"),
    ("Concluintes", "qt_vg_conc"),
    ("Trancadas", "qt_sit_trancada"),
    ("Desligados", "qt_sit_desligado"),
]

RELACIONAMENTOS = [
    ("codigo_ano", "dim_ano", "codigo_ano"),
    ("codigo_municipio", "dim_territorio", "codigo_municipio"),
    ("codigo_ies", "dim_ies", "codigo_ies"),
    ("codigo_curso", "dim_curso", "codigo_curso"),
    ("codigo_grau_academico", "dim_grau_academico", "codigo_grau_academico"),
    ("codigo_modalidade_ensino", "dim_modalidade_ensino", "codigo_modalidade_ensino"),
    ("codigo_organizacao_academica", "dim_organizacao_academica", "codigo_organizacao_academica"),
    ("codigo_categoria_administrativa", "dim_categoria_administrativa", "codigo_categoria_administrativa"),
    ("codigo_rede", "dim_rede", "codigo_rede"),
]

CAMPOS_FILTRO = [
    ("dim_territorio", "nome_regiao"),
    ("dim_territorio", "sigla_uf"),
    ("dim_territorio", "nome_mesorregiao"),
    ("dim_territorio", "nome_microrregiao"),
    ("dim_territorio", "nome_municipio"),
    ("dim_rede", "nome_rede"),
    ("dim_categoria_administrativa", "nome_categoria_administrativa"),
    ("dim_organizacao_academica", "nome_organizacao_academica"),
    ("dim_grau_academico", "nome_grau_academico"),
    ("dim_modalidade_ensino", "nome_modalidade_ensino"),
]

SUM_COLS = {c for _, c in MEDIDAS_MATRIZ if c}


def tipo_tmdl(dtype):
    s = str(dtype).lower()
    if s.startswith("int") or s.startswith("uint"):
        return "int64"
    if s.startswith("float"):
        return "double"
    if s == "bool":
        return "boolean"
    return "string"


def carregar_dataframe(nome, caminho):
    spec = importlib.util.spec_from_file_location(f"script_iescursos_{nome}", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return getattr(modulo, nome)


def to_m_string(texto):
    return texto.replace('"', '""').replace("\r\n", "\n").replace("\n", "#(lf)")


def m_expr(nome, codigo_script):
    m_str = to_m_string(codigo_script)
    return (
        f'let\n\t\t\t\tSource = Python.Execute("{m_str}"),\n'
        f'\t\t\t\tTabela = Source{{[Name="{nome}"]}}[Value]\n\t\t\tin\n\t\t\t\tTabela'
    )


# ---------------------------------------------------------------- DAX
def dax_medida(coluna):
    # Ultimo ano do filtro; BLANK quando a IES/curso nao tem registro nesse ano (a matriz
    # so lista linhas com algum valor). VALUE() evita o erro "SUM com String".
    if coluna is None:
        soma = f"DISTINCTCOUNT({FATO}[codigo_curso])"
    else:
        soma = f"SUMX({FATO}, VALUE({FATO}[{coluna}]))"
    return (
        f"VAR _ano = MAX(dim_ano[codigo_ano]) "
        f"VAR _n = CALCULATE(COUNTROWS({FATO}), dim_ano[codigo_ano] = _ano) "
        f"RETURN IF(_n = 0, BLANK(), CALCULATE({soma}, dim_ano[codigo_ano] = _ano))"
    )


_BASE_ANO = (
    "VAR _ano = MAX(dim_ano[codigo_ano]) "
    f"VAR _n = CALCULATE(COUNTROWS({FATO}), dim_ano[codigo_ano] = _ano) "
)
# Colunas de texto antes dos numeros. BLANK sem registro no ano de referencia, para a
# matriz continuar listando so IES/cursos com dados.
DAX_SIGLA = (
    _BASE_ANO
    + "RETURN IF(_n = 0, BLANK(), IF(ISINSCOPE(dim_ies[nome_ies]), SELECTEDVALUE(dim_ies[sigla_ies]), "
    + f'FORMAT(CALCULATE(DISTINCTCOUNT({FATO}[codigo_ies]), dim_ano[codigo_ano] = _ano), "#,0") & " IES"))'
)
# UF do CADASTRO da IES (dim_ies[sigla_uf_ies]); vazia no total (fora do escopo de uma IES).
DAX_UF = (
    _BASE_ANO
    + "RETURN IF(_n = 0 || NOT ISINSCOPE(dim_ies[nome_ies]) , BLANK(), SELECTEDVALUE(dim_ies[sigla_uf_ies]))"
)

DAX_TITULO = '"IES e cursos (ano de referência: " & MAX(dim_ano[codigo_ano]) & ")"'
DAX_SUBTITULO = 'VAR _f = [Filtros Selecionados] RETURN IF(_f = "", "", "(" & _f & ")")'


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
        return s + f"\t\tlineageTag: {uuid.uuid4()}\n\n"

    return (
        m("Sigla", DAX_SIGLA)
        + m("UF", DAX_UF)
        + "".join(m(n, dax_medida(c), "#,0") for n, c in MEDIDAS_MATRIZ)
        + m("Titulo Matriz", DAX_TITULO)
        + m("Filtros Selecionados", dax_filtros())
        + m("Subtitulo Filtros", DAX_SUBTITULO)
    )


# ---------------------------------------------------------------- modelo
def col_block(nome_coluna, dtype, soma):
    dt = tipo_tmdl(dtype)
    lines = [f"\tcolumn {nome_coluna}", f"\t\tdataType: {dt}"]
    if dt in ("int64", "double"):
        lines.append("\t\tformatString: 0")
    lines += [f"\t\tlineageTag: {uuid.uuid4()}", f"\t\tsummarizeBy: {'sum' if soma else 'none'}",
              f"\t\tsourceColumn: {nome_coluna}", ""]
    return "\n".join(lines)


def gerar_modelo():
    (OUT / "definition" / "tables").mkdir(parents=True, exist_ok=True)
    (OUT / "definition" / "cultures").mkdir(exist_ok=True)
    nomes = []
    for caminho in sorted(SCRIPTS_DIR.glob("*.py")):
        nome = caminho.stem
        nomes.append(nome)
        df = carregar_dataframe(nome, caminho)
        codigo = caminho.read_text(encoding="utf-8")
        txt = (
            f"table {nome}\n\tlineageTag: {uuid.uuid4()}\n\n"
            + "\n".join(col_block(c, dt, nome == FATO and c in SUM_COLS) for c, dt in df.dtypes.items())
            + "\n"
            + (medidas_tmdl() if nome == FATO else "")
            + f"\tpartition {nome} = m\n\t\tmode: import\n\t\tsource =\n\t\t\t{m_expr(nome, codigo)}\n"
        )
        (OUT / "definition" / "tables" / f"{nome}.tmdl").write_text(txt, encoding="utf-8", newline="\n")
        print(f"  tabela {nome}: {df.shape[0]} linhas, {df.shape[1]} colunas")

    rel = [f"relationship {uuid.uuid4()}\n\tfromColumn: {FATO}.{a}\n\ttoColumn: {t}.{b}\n" for a, t, b in RELACIONAMENTOS]
    (OUT / "definition" / "relationships.tmdl").write_text("\n".join(rel), encoding="utf-8", newline="\n")
    model = ("model Model\n\tculture: pt-BR\n\tdefaultPowerBIDataSourceVersion: powerBI_V3\n\n"
             + "\n".join(f"ref table {n}" for n in sorted(nomes)) + "\n\nref culture pt-BR\n")
    (OUT / "definition" / "model.tmdl").write_text(model, encoding="utf-8", newline="\n")
    (OUT / "definition" / "cultures" / "pt-BR.tmdl").write_text("cultureInfo pt-BR\n", encoding="utf-8", newline="\n")
    (OUT / "definition.pbism").write_text(json.dumps({"version": "4.0", "settings": {}}, indent=2), encoding="utf-8")
    (OUT / ".platform").write_text(json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
        "metadata": {"type": "SemanticModel", "displayName": "painel_ies_cursos"},
        "config": {"version": "2.0", "logicalId": str(uuid.uuid4())}}, indent=2), encoding="utf-8")
    print("modelo:", ", ".join(sorted(nomes)))


# ---------------------------------------------------------------- relatorio
S = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition"
L = lambda v: {"expr": {"Literal": {"Value": v}}}
COL = lambda t, c: {"Column": {"Expression": {"SourceRef": {"Entity": t}}, "Property": c}}
MED = lambda n: {"Measure": {"Expression": {"SourceRef": {"Entity": FATO}}, "Property": n}}

# Tabelas-filtro copiadas do painel_cursos, na mesma posicao (todas fazem sentido aqui).
FILTROS = ["ba8d6b871b69f5525472", "59874fb5d812c584e207", "9f0d5db67bf2d68d31c4", "309c7c98db9dab5e8810",
           "2e0536257dcd97524152", "d446ed6b54510e064385", "58ca5435197c55fb501e", "a52b48f84bfa23870a6f",
           "edff9ccbecabb85c9b25", "e71e2521c986af848283", "9059b435f66d5d353d3b"]


def gravar_visual(vid, j):
    d = REP / "definition" / "pages" / "pagina1" / "visuals" / vid
    d.mkdir(parents=True, exist_ok=True)
    (d / "visual.json").write_text(json.dumps(j, indent=2, ensure_ascii=False), encoding="utf-8")


def proj(field, ref, nome, ativo=False):
    p = {"field": field, "queryRef": ref, "nativeQueryRef": nome}
    if ativo:
        p["active"] = True
    return p


def gerar_relatorio():
    shutil.rmtree(REP, ignore_errors=True)
    pagina = REP / "definition" / "pages" / "pagina1"
    pagina.mkdir(parents=True)
    (REP / "definition.pbir").write_text(json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
        "version": "4.0", "datasetReference": {"byPath": {"path": "../painel_ies_cursos.SemanticModel"}}}, indent=2), encoding="utf-8")
    (REP / ".platform").write_text(json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
        "metadata": {"type": "Report", "displayName": "painel_ies_cursos"},
        "config": {"version": "2.0", "logicalId": str(uuid.uuid4())}}, indent=2), encoding="utf-8")
    for f in ("report.json", "version.json"):
        shutil.copy(HERE / "painel_cursos.Report" / "definition" / f, REP / "definition" / f)
    (REP / "definition" / "pages" / "pages.json").write_text(json.dumps(
        {"$schema": f"{S}/pagesMetadata/1.0.0/schema.json", "pageOrder": ["pagina1"], "activePageName": "pagina1"}, indent=2), encoding="utf-8")
    (pagina / "page.json").write_text(json.dumps(
        {"$schema": f"{S}/page/1.0.0/schema.json", "name": "pagina1", "displayName": "Painel de IES e Cursos",
         "displayOption": "FitToPage", "height": 720, "width": 1280}, indent=2), encoding="utf-8")

    for vid in FILTROS:
        j = json.loads((TEMPLATE / vid / "visual.json").read_text(encoding="utf-8"))
        if vid == "d446ed6b54510e064385":  # Organizacao academica: estreita para abrir espaco
            j["position"].update(x=546, width=152)
        gravar_visual(vid, j)

    # Categoria administrativa: copia do filtro de modalidade, trocando a dimensao
    txt = (TEMPLATE / "309c7c98db9dab5e8810" / "visual.json").read_text(encoding="utf-8")
    txt = txt.replace("dim_modalidade_ensino", "dim_categoria_administrativa")              .replace("nome_modalidade_ensino", "nome_categoria_administrativa")              .replace("309c7c98db9dab5e8810", "filtro_categoria_adm").replace('"Modalidade"', '"Categoria"')
    j = json.loads(txt)
    j["position"].update(x=396, y=0, width=150, height=300, z=13000, tabOrder=13000)
    gravar_visual("filtro_categoria_adm", j)

    # Matriz: linhas = IES > curso (drill-down com +/-), valores = medidas do ultimo ano
    valores = [proj(MED(n), f"{FATO}.{n}", n) for n in ["Sigla", "UF"] + [n for n, _ in MEDIDAS_MATRIZ]]
    mat = {
        "$schema": f"{S}/visualContainer/2.13.0/schema.json",
        "name": "matriz_ies_cursos",
        "position": {"x": 0, "y": 310, "z": 20000, "height": 410, "width": 1280, "tabOrder": 20000},
        "visual": {
            "visualType": "pivotTable",
            "query": {
                "queryState": {
                    "Rows": {"projections": [
                        proj(COL("dim_ies", "nome_ies"), "dim_ies.nome_ies", "IES", True),
                        proj(COL("dim_curso", "nome_curso"), "dim_curso.nome_curso", "Curso", True)]},
                    "Values": {"projections": valores},
                },
                "sortDefinition": {"sort": [{"field": MED("Matrículas"), "direction": "Descending"}]},
            },
            "objects": {
                "rowHeaders": [{"properties": {"showExpandCollapseButtons": L("true")}}],
                "grid": [{"properties": {"textSize": L("10D")}}],
            },
            "visualContainerObjects": {
                "title": [{"properties": {"show": L("true"), "text": {"expr": {"Measure": MED("Titulo Matriz")["Measure"]}},
                                          "fontSize": L("13D")}}],
                "subTitle": [{"properties": {"show": L("true"), "text": {"expr": {"Measure": MED("Subtitulo Filtros")["Measure"]}},
                                             "fontSize": L("9D"), "fontColor": {"solid": {"color": L("'#4A5F7A'")}}}}],
                "background": [{"properties": {"color": {"solid": {"color": L("'#CDDFF1'")}}}}],
                "border": [{"properties": {"show": L("true")}}],
            },
        },
    }
    gravar_visual("matriz_ies_cursos", mat)
    print("relatorio: painel_ies_cursos.Report")


gerar_modelo()
gerar_relatorio()
(HERE / "painel_ies_cursos.pbip").write_text(json.dumps(
    {"$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
     "version": "1.0", "artifacts": [{"report": {"path": "painel_ies_cursos.Report"}}],
     "settings": {"enableAutoRecovery": True}}, indent=2), encoding="utf-8")
print("ok: painel_ies_cursos.pbip")

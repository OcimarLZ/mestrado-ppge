# -*- coding: utf-8 -*-
"""Gera o projeto Power BI painel_ies (PBIP/TMDL) a partir de scripts_ies/*.py.

Mesma ideia do build_pbip.py (painel_cursos): um script Python por tabela, cada um vira
uma particao M com Python.Execute, e os tipos de coluna sao inferidos rodando o script.
Aqui a fato e fato_ies_censo (IES x ano, docentes) e as dimensoes sao as da IES.

Relatorio: parte do layout do painel_cursos (visuais copiados de painel_cursos.Report),
trocando a fato, a medida e removendo/ajustando os filtros que so fazem sentido para curso.

Uso: python powerbi/build_pbip_ies.py  ->  abre powerbi/painel_ies.pbip no Power BI Desktop.
"""
import importlib.util
import json
import shutil
import uuid
from pathlib import Path

HERE = Path(__file__).parent
SCRIPTS_DIR = HERE / "scripts_ies"
OUT = HERE / "painel_ies.SemanticModel"
REP = HERE / "painel_ies.Report"
TEMPLATE_VISUALS = HERE / "painel_cursos.Report" / "definition" / "pages" / "pagina1" / "visuals"
FATO = "fato_ies_censo"

# Metrica exibida no slicer -> coluna da fato somada pela medida 'Valor Selecionado'.
METRICAS = [
    ("Docentes (total)", "qt_doc_total"),
    ("Docentes em exercício", "qt_doc_exe"),
    ("Docentes mulheres", "qt_doc_ex_femi"),
    ("Docentes homens", "qt_doc_ex_masc"),
    ("Doutores", "qt_doc_ex_dout"),
    ("Mestres", "qt_doc_ex_mest"),
    ("Especialistas", "qt_doc_ex_esp"),
    ("Graduados", "qt_doc_ex_grad"),
    ("Sem graduação", "qt_doc_ex_sem_grad"),
    ("Regime integral", "qt_doc_ex_int"),
    ("Integral com DE", "qt_doc_ex_int_de"),
    ("Regime parcial", "qt_doc_ex_parc"),
    ("Horistas", "qt_doc_ex_hor"),
    ("Com deficiência", "qt_doc_ex_com_deficiencia"),
    ("Estrangeiros", "qt_doc_ex_est"),
]
METRICA_PADRAO = METRICAS[0][0]

# (coluna na fato, tabela dim, coluna na dim)
RELACIONAMENTOS = [
    ("codigo_ano", "dim_ano", "codigo_ano"),
    ("codigo_municipio", "dim_territorio", "codigo_municipio"),
    ("codigo_ies", "dim_ies", "codigo_ies"),
    ("codigo_mantenedora", "dim_mantenedora", "codigo_mantenedora"),
    ("codigo_organizacao_academica", "dim_organizacao_academica", "codigo_organizacao_academica"),
    ("codigo_categoria_administrativa", "dim_categoria_administrativa", "codigo_categoria_administrativa"),
    ("codigo_rede", "dim_rede", "codigo_rede"),
]

# Campos que entram no subtitulo dos graficos (ordem do texto).
CAMPOS_FILTRO = [
    ("dim_territorio", "nome_regiao"),
    ("dim_territorio", "sigla_uf"),
    ("dim_territorio", "nome_mesorregiao"),
    ("dim_territorio", "nome_microrregiao"),
    ("dim_territorio", "nome_municipio"),
    ("dim_rede", "nome_rede"),
    ("dim_categoria_administrativa", "nome_categoria_administrativa"),
    ("dim_organizacao_academica", "nome_organizacao_academica"),
]


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
    spec = importlib.util.spec_from_file_location(f"script_ies_{nome}", caminho)
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
def dax_dim_metricas():
    itens = ", ".join(f'{{"{nome}", {ordem}}}' for ordem, (nome, _c) in enumerate(METRICAS, start=1))
    return f'DATATABLE("Metrica", STRING, "Ordem", INTEGER, {{{itens}}})'


def dax_valor_selecionado():
    # Cada soma vai numa VAR antes do SWITCH; VALUE() garante soma numerica mesmo se o
    # Desktop tipar a coluna como texto (erro "SUM nao pode trabalhar com String").
    nomes = [f"_{c}" for _, c in METRICAS]
    decl = " ".join(f"VAR {v} = SUMX({FATO}, VALUE({FATO}[{c}]))" for v, (_, c) in zip(nomes, METRICAS))
    casos = ", ".join(f'"{n}", {v}' for v, (n, _) in zip(nomes, METRICAS))
    return f"VAR _metrica = SELECTEDVALUE(dim_metricas[Metrica]) {decl} RETURN SWITCH(_metrica, {casos}, {nomes[0]})"


DAX_ACUMULADO = (
    "VAR _ano = MAX(dim_ano[codigo_ano]) RETURN CALCULATE([Valor Selecionado], "
    "FILTER(ALL(dim_ano[codigo_ano]), dim_ano[codigo_ano] <= _ano))"
)
DAX_QTDE_IES = f"CALCULATE(DISTINCTCOUNT({FATO}[codigo_ies]), {FATO}[codigo_ies] <> 0)"
DAX_TITULO = f'SELECTEDVALUE(dim_metricas[Metrica], "{METRICA_PADRAO}")'
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
        m("Valor Selecionado", dax_valor_selecionado(), "#,0")
        + m("Valor Acumulado", DAX_ACUMULADO, "#,0")
        + m("Qtde IES", DAX_QTDE_IES, "#,0")
        + m("Titulo Metrica", DAX_TITULO)
        + m("Filtros Selecionados", dax_filtros())
        + m("Subtitulo Filtros", DAX_SUBTITULO)
    )


# ---------------------------------------------------------------- modelo
def col_block(nome_coluna, dtype, soma):
    dt = tipo_tmdl(dtype)
    lines = [f"\tcolumn {nome_coluna}", f"\t\tdataType: {dt}"]
    if dt in ("int64", "double"):
        lines.append("\t\tformatString: 0")
    summ = "sum" if soma else "none"
    lines += [f"\t\tlineageTag: {uuid.uuid4()}", f"\t\tsummarizeBy: {summ}", f"\t\tsourceColumn: {nome_coluna}", ""]
    return "\n".join(lines)


def gerar_modelo():
    (OUT / "definition" / "tables").mkdir(parents=True, exist_ok=True)
    (OUT / "definition" / "cultures").mkdir(exist_ok=True)
    soma_cols = {c for _, c in METRICAS}
    nomes = []
    for caminho in sorted(SCRIPTS_DIR.glob("*.py")):
        nome = caminho.stem
        nomes.append(nome)
        df = carregar_dataframe(nome, caminho)
        codigo = caminho.read_text(encoding="utf-8")
        txt = (
            f"table {nome}\n\tlineageTag: {uuid.uuid4()}\n\n"
            + "\n".join(col_block(c, dt, c in soma_cols and nome == FATO) for c, dt in df.dtypes.items())
            + "\n"
            + (medidas_tmdl() if nome == FATO else "")
            + f"\tpartition {nome} = m\n\t\tmode: import\n\t\tsource =\n\t\t\t{m_expr(nome, codigo)}\n"
        )
        (OUT / "definition" / "tables" / f"{nome}.tmdl").write_text(txt, encoding="utf-8", newline="\n")
        print(f"  tabela {nome}: {df.shape[0]} linhas, {df.shape[1]} colunas")

    txt = (
        f"table dim_metricas\n\tlineageTag: {uuid.uuid4()}\n\n"
        f"\tcolumn Metrica\n\t\tdataType: string\n\t\tlineageTag: {uuid.uuid4()}\n\t\tsummarizeBy: none\n\t\tsourceColumn: Metrica\n\n"
        f"\tcolumn Ordem\n\t\tdataType: int64\n\t\tformatString: 0\n\t\tlineageTag: {uuid.uuid4()}\n\t\tsummarizeBy: none\n\t\tsourceColumn: Ordem\n\n"
        f"\tpartition dim_metricas = calculated\n\t\tmode: import\n\t\tsource = {dax_dim_metricas()}\n"
    )
    (OUT / "definition" / "tables" / "dim_metricas.tmdl").write_text(txt, encoding="utf-8", newline="\n")
    nomes.append("dim_metricas")

    rel = [
        f"relationship {uuid.uuid4()}\n\tfromColumn: {FATO}.{a}\n\ttoColumn: {t}.{b}\n"
        for a, t, b in RELACIONAMENTOS
    ]
    (OUT / "definition" / "relationships.tmdl").write_text("\n".join(rel), encoding="utf-8", newline="\n")
    model = (
        "model Model\n\tculture: pt-BR\n\tdefaultPowerBIDataSourceVersion: powerBI_V3\n\n"
        + "\n".join(f"ref table {n}" for n in sorted(nomes))
        + "\n\nref culture pt-BR\n"
    )
    (OUT / "definition" / "model.tmdl").write_text(model, encoding="utf-8", newline="\n")
    (OUT / "definition" / "cultures" / "pt-BR.tmdl").write_text("cultureInfo pt-BR\n", encoding="utf-8", newline="\n")
    (OUT / "definition.pbism").write_text(json.dumps({"version": "4.0", "settings": {}}, indent=2), encoding="utf-8")
    (OUT / ".platform").write_text(json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
        "metadata": {"type": "SemanticModel", "displayName": "painel_ies"},
        "config": {"version": "2.0", "logicalId": str(uuid.uuid4())}}, indent=2), encoding="utf-8")
    print("modelo:", ", ".join(sorted(nomes)))


# ---------------------------------------------------------------- relatorio
S = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition"
L = lambda v: {"expr": {"Literal": {"Value": v}}}
MEDIDA = lambda n: {"expr": {"Measure": {"Expression": {"SourceRef": {"Entity": FATO}}, "Property": n}}}

# id do visual no painel_cursos -> (x, y, largura, altura). None = nao existe no painel_ies.
LAYOUT_FILTROS = {
    "ba8d6b871b69f5525472": (10, 0, 62, 299),      # Ano
    "59874fb5d812c584e207": (72, 0, 133, 101),     # periodo PNE
    "9f0d5db67bf2d68d31c4": (72, 101, 133, 88),    # Rede
    "309c7c98db9dab5e8810": (72, 189, 133, 111),   # (era Modalidade) -> Categoria administrativa
    "2e0536257dcd97524152": None,                  # Grau academico: so faz sentido para curso
    "d446ed6b54510e064385": (205, 0, 302, 300),    # Organizacao academica
    "58ca5435197c55fb501e": (507, 0, 107, 299),    # Regiao
    "a52b48f84bfa23870a6f": (614, 0, 57, 305),     # UF
    "edff9ccbecabb85c9b25": (671, 0, 139, 305),    # Mesorregiao
    "e71e2521c986af848283": (810, 0, 133, 305),    # Microrregiao
    "9059b435f66d5d353d3b": (943, 0, 337, 306),    # Municipio
}


def carregar_visual(vid):
    txt = (TEMPLATE_VISUALS / vid / "visual.json").read_text(encoding="utf-8")
    txt = txt.replace("fato_curso_censo", FATO)
    return json.loads(txt)


def salvar_visual(vid, j, pos):
    x, y, w, h = pos
    j["position"].update(x=x, y=y, width=w, height=h)
    d = REP / "definition" / "pages" / "pagina1" / "visuals" / vid
    d.mkdir(parents=True, exist_ok=True)
    (d / "visual.json").write_text(json.dumps(j, indent=2, ensure_ascii=False), encoding="utf-8")


def gerar_relatorio():
    shutil.rmtree(REP, ignore_errors=True)
    pagina = REP / "definition" / "pages" / "pagina1"
    pagina.mkdir(parents=True)
    (REP / "definition.pbir").write_text(json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
        "version": "4.0", "datasetReference": {"byPath": {"path": "../painel_ies.SemanticModel"}}}, indent=2), encoding="utf-8")
    (REP / ".platform").write_text(json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
        "metadata": {"type": "Report", "displayName": "painel_ies"},
        "config": {"version": "2.0", "logicalId": str(uuid.uuid4())}}, indent=2), encoding="utf-8")
    shutil.copy(HERE / "painel_cursos.Report" / "definition" / "report.json", REP / "definition" / "report.json")
    shutil.copy(HERE / "painel_cursos.Report" / "definition" / "version.json", REP / "definition" / "version.json")
    (REP / "definition" / "pages" / "pages.json").write_text(json.dumps(
        {"$schema": f"{S}/pagesMetadata/1.0.0/schema.json", "pageOrder": ["pagina1"], "activePageName": "pagina1"}, indent=2), encoding="utf-8")
    (pagina / "page.json").write_text(json.dumps(
        {"$schema": f"{S}/page/1.0.0/schema.json", "name": "pagina1", "displayName": "Painel de IES",
         "displayOption": "FitToPage", "height": 720, "width": 1280}, indent=2), encoding="utf-8")

    # Tabelas-filtro (copiadas do painel_cursos)
    for vid, pos in LAYOUT_FILTROS.items():
        if pos is None:
            continue
        j = carregar_visual(vid)
        if vid == "309c7c98db9dab5e8810":  # Modalidade -> Categoria administrativa
            txt = json.dumps(j).replace("dim_modalidade_ensino", "dim_categoria_administrativa") \
                               .replace("nome_modalidade_ensino", "nome_categoria_administrativa").replace('"Modalidade"', '"Categoria"')
            j = json.loads(txt)
        salvar_visual(vid, j, pos)

    # Grafico 1: quantidade de IES por ano
    j = carregar_visual("1bdfedacee426762d527")
    qs = j["visual"]["query"]["queryState"]
    qs["Y"]["projections"] = [{"field": {"Measure": {"Expression": {"SourceRef": {"Entity": FATO}}, "Property": "Qtde IES"}},
                               "queryRef": f"{FATO}.Qtde IES", "nativeQueryRef": "Qtde IES"}]
    ano_fato = {"Column": {"Expression": {"SourceRef": {"Entity": FATO}}, "Property": "codigo_ano"}}
    j["visual"]["query"]["sortDefinition"] = {"sort": [{"field": ano_fato, "direction": "Ascending"}]}
    vc = j["visual"]["visualContainerObjects"]
    vc["title"][0]["properties"]["text"] = L("'Quantidade de IES'")
    vc["subTitle"] = [{"properties": {"show": L("true"), "text": MEDIDA("Subtitulo Filtros"), "fontSize": L("9D"),
                                      "fontColor": {"solid": {"color": L("'#4A5F7A'")}}}}]
    j.pop("filterConfig", None)
    salvar_visual("1bdfedacee426762d527", j, (0, 305, 1280, 150))

    # Grafico 2: valor da metrica escolhida no slicer, por ano
    j = carregar_visual("ea3da53062d058018a0f")
    vc = j["visual"]["visualContainerObjects"]
    vc["title"][0]["properties"]["text"] = MEDIDA("Titulo Metrica")
    vc["subTitle"] = [{"properties": {"show": L("true"), "text": MEDIDA("Subtitulo Filtros"), "fontSize": L("9D"),
                                      "fontColor": {"solid": {"color": L("'#4A5F7A'")}}}}]
    j["filterConfig"]["filters"] = [f for f in j["filterConfig"]["filters"] if f["type"] == "Categorical"]
    salvar_visual("ea3da53062d058018a0f", j, (0, 455, 1000, 265))

    # Slicer de metrica (selecao unica, sempre uma marcada)
    j = carregar_visual("b971dd5897f664e4c061")
    j["visual"]["objects"]["general"] = [{"properties": {"filter": {"filter": {
        "Version": 2, "From": [{"Name": "d", "Entity": "dim_metricas", "Type": 0}],
        "Where": [{"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "Metrica"}}],
                                        "Values": [[{"Literal": {"Value": f"'{METRICA_PADRAO}'"}}]]}}}]}}}}]
    salvar_visual("b971dd5897f664e4c061", j, (1000, 455, 280, 265))
    print("relatorio: painel_ies.Report")


gerar_modelo()
gerar_relatorio()
(HERE / "painel_ies.pbip").write_text(json.dumps(
    {"$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
     "version": "1.0", "artifacts": [{"report": {"path": "painel_ies.Report"}}],
     "settings": {"enableAutoRecovery": True}}, indent=2), encoding="utf-8")
print("ok: painel_ies.pbip")

# -*- coding: utf-8 -*-
"""Gera o projeto Power BI (PBIP/TMDL) a partir dos scripts individuais em scripts/*.py.

Cada tabela do modelo tem seu proprio arquivo em scripts/ (ver scripts/README ou
powerbi/README.md para o porque de serem scripts separados, nao um unico arquivo
monolitico). Este script le o CONTEUDO LITERAL de cada um, embute como uma particao M
com Python.Execute (cada tabela roda sua propria conexao/consulta, isolada das demais --
evita que carregar uma dimensao pequena force reler a fato de ~3,9M linhas), e infere os
tipos de coluna REAIS rodando cada script e inspecionando o DataFrame resultante (em vez
de uma lista hardcoded de nomes de coluna, que fica desatualizada a cada mudanca nos
scripts).

Uso: python powerbi/build_pbip.py  ->  abre powerbi/painel_cursos.pbip no Power BI Desktop.
"""
import importlib.util
import json
import uuid
from pathlib import Path

HERE = Path(__file__).parent
SCRIPTS_DIR = HERE / "scripts"
OUT = HERE / "painel_cursos.SemanticModel"
REP = HERE / "painel_cursos.Report"

SUM_COLS = {"qt_vg_total", "qt_vg_mat", "qt_vg_ing", "qt_vg_conc", "qt_sit_trancada", "qt_sit_desligado"}

# Tabela de metricas DESCONECTADA (sem relacionamento com a fato) + medida DAX que troca
# qual coluna somar conforme a metrica selecionada num slicer -- permite um unico grafico
# alternar entre "Qtde Matriculas", "Qtde Ingressantes" etc. sem duplicar visuais.
METRICAS = [
    ("Qtde Matrículas", "qt_vg_mat"),
    ("Qtde Ingressantes", "qt_vg_ing"),
    ("Qtde Vagas Totais", "qt_vg_total"),
    ("Qtde Concluintes", "qt_vg_conc"),
    ("Situação Trancada", "qt_sit_trancada"),
    ("Situação Desligado", "qt_sit_desligado"),
]

# (coluna na fato, tabela dim, coluna na dim) -- nomes ja normalizados com prefixo
# "codigo_" nos dois lados (ver scripts/fato_curso_censo.py).
RELACIONAMENTOS = [
    ("codigo_ano", "dim_ano", "codigo_ano"),
    ("codigo_municipio", "dim_territorio", "codigo_municipio"),
    ("codigo_ies", "dim_ies", "codigo_ies"),
    ("codigo_curso", "dim_curso", "codigo_curso"),
    ("codigo_cine_rotulo", "dim_cine", "codigo_cine_rotulo"),
    ("codigo_grau_academico", "dim_grau_academico", "codigo_grau_academico"),
    ("codigo_modalidade_ensino", "dim_modalidade_ensino", "codigo_modalidade_ensino"),
    ("codigo_organizacao_academica", "dim_organizacao_academica", "codigo_organizacao_academica"),
    ("codigo_categoria_administrativa", "dim_categoria_administrativa", "codigo_categoria_administrativa"),
    ("codigo_rede", "dim_rede", "codigo_rede"),
]


def carregar_dataframe(nome, caminho):
    spec = importlib.util.spec_from_file_location(f"script_{nome}", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return getattr(modulo, nome)


def tipo_tmdl(dtype):
    s = str(dtype).lower()  # cobre tambem os nulaveis do pandas: "Int64", "Int32" etc.
    if s.startswith("int") or s.startswith("uint"):
        return "int64"
    if s.startswith("float"):
        return "double"
    if s == "bool":
        return "boolean"
    return "string"  # object, string, category


def to_m_string(texto):
    return texto.replace('"', '""').replace("\r\n", "\n").replace("\n", "#(lf)")


def m_expr(nome, codigo_script):
    m_str = to_m_string(codigo_script)
    return (
        f'let\n\t\t\t\tSource = Python.Execute("{m_str}"),\n'
        f'\t\t\t\tTabela = Source{{[Name="{nome}"]}}[Value]\n\t\t\tin\n\t\t\t\tTabela'
    )


def dax_dim_metricas():
    itens = ", ".join(f'{{"{nome}", {ordem}}}' for ordem, (nome, _col) in enumerate(METRICAS, start=1))
    return f'DATATABLE("Metrica", STRING, "Ordem", INTEGER, {{{itens}}})'


def dax_medida_valor_selecionado():
    # VAR/RETURN em vez de SUM(...) direto dentro de cada ramo do SWITCH: calcula cada
    # soma ANTES, numa variavel, e o SWITCH só compara/retorna valores ja numericos --
    # evita qualquer ambiguidade de inferencia de tipo do motor DAX ao misturar
    # comparacoes de string com agregacoes na mesma expressao (visto na pratica: um
    # SWITCH direto com SUM() em cada ramo disparava "SUM nao pode trabalhar com
    # String", mesmo com a coluna confirmada como int64 no modelo).
    nomes_var = [f"_{col}" for _, col in METRICAS]
    declaracoes = " ".join(
        f"VAR {var} = SUMX(fato_curso_censo, VALUE(fato_curso_censo[{col}]))" for var, (_, col) in zip(nomes_var, METRICAS)
    )
    casos = ", ".join(f'"{nome}", {var}' for var, (nome, _) in zip(nomes_var, METRICAS))
    padrao = nomes_var[0]
    return (
        f"VAR _metrica = SELECTEDVALUE(dim_metricas[Metrica]) {declaracoes} "
        f"RETURN SWITCH(_metrica, {casos}, {padrao})"
    )


def gerar_dim_metricas():
    txt = (
        f"table dim_metricas\n\tlineageTag: {uuid.uuid4()}\n\n"
        f"\tcolumn Metrica\n\t\tdataType: string\n\t\tlineageTag: {uuid.uuid4()}\n"
        f"\t\tsummarizeBy: none\n\t\tsourceColumn: Metrica\n\n"
        f"\tcolumn Ordem\n\t\tdataType: int64\n\t\tformatString: 0\n\t\tlineageTag: {uuid.uuid4()}\n"
        f"\t\tsummarizeBy: none\n\t\tsourceColumn: Ordem\n\n"
        f"\tpartition dim_metricas = calculated\n\t\tmode: import\n\t\tsource = {dax_dim_metricas()}\n"
    )
    (OUT / "definition" / "tables" / "dim_metricas.tmdl").write_text(txt, encoding="utf-8", newline="\n")


ACUMULADO = (
    "VAR _ano = MAX(dim_ano[codigo_ano]) RETURN CALCULATE([Valor Selecionado], "
    "FILTER(ALL(dim_ano[codigo_ano]), dim_ano[codigo_ano] <= _ano))"
)


M_FILTROS = 'VAR _v0 = IF(ISFILTERED(dim_territorio[nome_regiao]), IF(COUNTROWS(VALUES(dim_territorio[nome_regiao])) <= 3, CONCATENATEX(VALUES(dim_territorio[nome_regiao]), dim_territorio[nome_regiao], ", "), COUNTROWS(VALUES(dim_territorio[nome_regiao])) & " itens"), "") VAR _v1 = IF(ISFILTERED(dim_territorio[sigla_uf]), IF(COUNTROWS(VALUES(dim_territorio[sigla_uf])) <= 3, CONCATENATEX(VALUES(dim_territorio[sigla_uf]), dim_territorio[sigla_uf], ", "), COUNTROWS(VALUES(dim_territorio[sigla_uf])) & " itens"), "") VAR _v2 = IF(ISFILTERED(dim_territorio[nome_mesorregiao]), IF(COUNTROWS(VALUES(dim_territorio[nome_mesorregiao])) <= 3, CONCATENATEX(VALUES(dim_territorio[nome_mesorregiao]), dim_territorio[nome_mesorregiao], ", "), COUNTROWS(VALUES(dim_territorio[nome_mesorregiao])) & " itens"), "") VAR _v3 = IF(ISFILTERED(dim_territorio[nome_microrregiao]), IF(COUNTROWS(VALUES(dim_territorio[nome_microrregiao])) <= 3, CONCATENATEX(VALUES(dim_territorio[nome_microrregiao]), dim_territorio[nome_microrregiao], ", "), COUNTROWS(VALUES(dim_territorio[nome_microrregiao])) & " itens"), "") VAR _v4 = IF(ISFILTERED(dim_territorio[nome_municipio]), IF(COUNTROWS(VALUES(dim_territorio[nome_municipio])) <= 3, CONCATENATEX(VALUES(dim_territorio[nome_municipio]), dim_territorio[nome_municipio], ", "), COUNTROWS(VALUES(dim_territorio[nome_municipio])) & " itens"), "") VAR _v5 = IF(ISFILTERED(dim_rede[nome_rede]), IF(COUNTROWS(VALUES(dim_rede[nome_rede])) <= 3, CONCATENATEX(VALUES(dim_rede[nome_rede]), dim_rede[nome_rede], ", "), COUNTROWS(VALUES(dim_rede[nome_rede])) & " itens"), "") VAR _v6 = IF(ISFILTERED(dim_modalidade_ensino[nome_modalidade_ensino]), IF(COUNTROWS(VALUES(dim_modalidade_ensino[nome_modalidade_ensino])) <= 3, CONCATENATEX(VALUES(dim_modalidade_ensino[nome_modalidade_ensino]), dim_modalidade_ensino[nome_modalidade_ensino], ", "), COUNTROWS(VALUES(dim_modalidade_ensino[nome_modalidade_ensino])) & " itens"), "") VAR _v7 = IF(ISFILTERED(dim_organizacao_academica[nome_organizacao_academica]), IF(COUNTROWS(VALUES(dim_organizacao_academica[nome_organizacao_academica])) <= 3, CONCATENATEX(VALUES(dim_organizacao_academica[nome_organizacao_academica]), dim_organizacao_academica[nome_organizacao_academica], ", "), COUNTROWS(VALUES(dim_organizacao_academica[nome_organizacao_academica])) & " itens"), "") VAR _v8 = IF(ISFILTERED(dim_grau_academico[nome_grau_academico]), IF(COUNTROWS(VALUES(dim_grau_academico[nome_grau_academico])) <= 3, CONCATENATEX(VALUES(dim_grau_academico[nome_grau_academico]), dim_grau_academico[nome_grau_academico], ", "), COUNTROWS(VALUES(dim_grau_academico[nome_grau_academico])) & " itens"), "") VAR _a = IF(_v0 <> "", _v0 & "/", "") & IF(_v1 <> "", _v1 & "/", "") & IF(_v2 <> "", _v2 & "/", "") & IF(_v3 <> "", _v3 & "/", "") & IF(_v4 <> "", _v4 & "/", "") & IF(_v5 <> "", _v5 & "/", "") & IF(_v6 <> "", _v6 & "/", "") & IF(_v7 <> "", _v7 & "/", "") & IF(_v8 <> "", _v8 & "/", "") RETURN IF(_a = "", "", LEFT(_a, LEN(_a) - 1))'
M_TITULO_METRICA = 'SELECTEDVALUE(dim_metricas[Metrica], "Qtde Matrículas")'
M_SUBTITULO = 'VAR _f = [Filtros Selecionados] RETURN IF(_f = "", "", "(" & _f & ")")'


def medida_valor_selecionado_tmdl():
    return (
        f"\tmeasure 'Valor Selecionado' = {dax_medida_valor_selecionado()}\n"
        f"\t\tformatString: 0\n"
        f"\t\tlineageTag: {uuid.uuid4()}\n\n"
        f"\tmeasure 'Valor Acumulado' = {ACUMULADO}\n"
        f"\t\tformatString: 0\n"
        f"\t\tlineageTag: {uuid.uuid4()}\n\n"
        f"\tmeasure 'Titulo Metrica' = {M_TITULO_METRICA}\n"
        f"\t\tlineageTag: {uuid.uuid4()}\n\n"
        f"\tmeasure 'Filtros Selecionados' = {M_FILTROS}\n"
        f"\t\tlineageTag: {uuid.uuid4()}\n\n"
        f"\tmeasure 'Subtitulo Filtros' = {M_SUBTITULO}\n"
        f"\t\tlineageTag: {uuid.uuid4()}\n\n"
    )


def col_block(nome_coluna, dtype):
    dt = tipo_tmdl(dtype)
    fmt = "0" if dt == "int64" or dt == "double" else None
    summ = "sum" if nome_coluna in SUM_COLS else "none"
    lines = [f"\tcolumn {nome_coluna}", f"\t\tdataType: {dt}"]
    if fmt:
        lines.append(f"\t\tformatString: {fmt}")
    lines += [f"\t\tlineageTag: {uuid.uuid4()}", f"\t\tsummarizeBy: {summ}", f"\t\tsourceColumn: {nome_coluna}", ""]
    return "\n".join(lines)


(OUT / "definition" / "tables").mkdir(parents=True, exist_ok=True)

nomes_tabelas = []
for caminho_script in sorted(SCRIPTS_DIR.glob("*.py")):
    nome = caminho_script.stem
    nomes_tabelas.append(nome)
    df = carregar_dataframe(nome, caminho_script)
    codigo_script = caminho_script.read_text(encoding="utf-8")

    medida = medida_valor_selecionado_tmdl() if nome == "fato_curso_censo" else ""
    txt = (
        f"table {nome}\n\tlineageTag: {uuid.uuid4()}\n\n"
        + "\n".join(col_block(c, dt) for c, dt in df.dtypes.items())
        + "\n" + medida
        + f"\tpartition {nome} = m\n\t\tmode: import\n\t\tsource =\n\t\t\t{m_expr(nome, codigo_script)}\n"
    )
    (OUT / "definition" / "tables" / f"{nome}.tmdl").write_text(txt, encoding="utf-8", newline="\n")
    print(f"  tabela {nome}: {df.shape[0]} linhas, {df.shape[1]} colunas")

gerar_dim_metricas()
nomes_tabelas.append("dim_metricas")
print("  tabela dim_metricas: 6 linhas, 2 colunas (calculada via DAX, desconectada)")

rel_linhas = [
    f"relationship {uuid.uuid4()}\n\tfromColumn: fato_curso_censo.{a}\n\ttoColumn: {t}.{b}\n"
    for a, t, b in RELACIONAMENTOS
]
(OUT / "definition" / "relationships.tmdl").write_text("\n".join(rel_linhas), encoding="utf-8", newline="\n")

model = (
    "model Model\n\tculture: pt-BR\n\tdefaultPowerBIDataSourceVersion: powerBI_V3\n\n"
    + "\n".join(f"ref table {n}" for n in nomes_tabelas)
    + "\n\nref culture pt-BR\n"
)
(OUT / "definition" / "model.tmdl").write_text(model, encoding="utf-8", newline="\n")
(OUT / "definition" / "cultures").mkdir(exist_ok=True)
(OUT / "definition" / "cultures" / "pt-BR.tmdl").write_text("cultureInfo pt-BR\n", encoding="utf-8", newline="\n")
(OUT / "definition.pbism").write_text(json.dumps({"version": "4.0", "settings": {}}, indent=2), encoding="utf-8")

S = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition"
(REP / "definition" / "pages" / "pagina1").mkdir(parents=True, exist_ok=True)
(REP / "definition.pbir").write_text(json.dumps(
    {"version": "4.0", "datasetReference": {"byPath": {"path": "../painel_cursos.SemanticModel"}}}, indent=2), encoding="utf-8")
(REP / "definition" / "version.json").write_text(json.dumps(
    {"$schema": f"{S}/versionMetadata/1.0.0/schema.json", "version": "2.0.0"}, indent=2), encoding="utf-8")
(REP / "definition" / "report.json").write_text(json.dumps(
    {"$schema": f"{S}/report/1.0.0/schema.json",
     "themeCollection": {"baseTheme": {"name": "CY24SU10", "reportVersionAtImport": "5.59", "type": "SharedResources"}},
     "layoutOptimization": "None"}, indent=2), encoding="utf-8")
(REP / "definition" / "pages" / "pages.json").write_text(json.dumps(
    {"$schema": f"{S}/pagesMetadata/1.0.0/schema.json", "pageOrder": ["pagina1"], "activePageName": "pagina1"}, indent=2), encoding="utf-8")
(REP / "definition" / "pages" / "pagina1" / "page.json").write_text(json.dumps(
    {"$schema": f"{S}/page/1.0.0/schema.json", "name": "pagina1", "displayName": "Painel de Cursos",
     "displayOption": "FitToPage", "height": 720, "width": 1280}, indent=2), encoding="utf-8")
(HERE / "painel_cursos.pbip").write_text(json.dumps(
    {"version": "1.0", "artifacts": [{"report": {"path": "painel_cursos.Report"}}],
     "settings": {"enableAutoRecovery": True}}, indent=2), encoding="utf-8")
print("ok:", ", ".join(nomes_tabelas))

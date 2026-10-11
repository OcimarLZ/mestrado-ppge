# -*- coding: utf-8 -*-
"""Torna recolhivel o painel de metricas do painel_comparativo (edita IN PLACE o Report).

- botao "Ocultar metricas" (sobre o canto do grafico estreito) -> favorito `met_fechado`:
  esconde os 3 slicers, o grafico estreito e o proprio botao; mostra o grafico LARGO e o botao
  "Escolher metricas";
- botao "Escolher metricas" (sobre o canto do grafico largo) -> favorito `met_aberto`: o inverso.
- Os favoritos so alternam visibilidade (suppressData): as marcacoes dos slicers sao mantidas e a
  legenda do grafico continua mostrando o que esta marcado.
- O grafico largo e uma copia do estreito (x=0, largura da pagina). Estado inicial: painel aberto.

Idempotente: pode rodar de novo (recria o grafico largo, os botoes e os favoritos a partir do
grafico estreito atual; posicoes/formatacao do estreito e dos slicers nao sao alteradas).
Rode DEPOIS de build_pbip_comparativo.py se o painel for regerado. Feche o Desktop antes.
No Desktop, os botoes so respondem com Ctrl+clique (no modo de leitura/publicado, clique normal).
"""
import copy
import json
from pathlib import Path

REP = Path(__file__).parent / "painel_comparativo.Report" / "definition"
VIS = REP / "pages" / "pagina1" / "visuals"
S = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition"
L = lambda v: {"expr": {"Literal": {"Value": v}}}

GRAF, LARGO = "grafico_comparativo", "grafico_comparativo_largo"
SLICERS = ["slicer_modalidade", "slicer_categoria", "slicer_metrica"]
BTN_OCULTAR, BTN_MOSTRAR = "btn_ocultar_metricas", "btn_mostrar_metricas"
BK_ABERTO, BK_FECHADO = "met_aberto", "met_fechado"
LARG_BTN, ALT_BTN = 190, 24


def ler(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def gravar(p, j):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(j, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")


def botao(nome, texto, bookmark, dica, x, y, z, oculto):
    j = {
        "$schema": f"{S}/visualContainer/2.12.0/schema.json",
        "name": nome,
        "position": {"x": x, "y": y, "z": z, "height": ALT_BTN, "width": LARG_BTN, "tabOrder": z},
        "visual": {
            "visualType": "actionButton",
            "objects": {
                "icon": [{"properties": {"shapeType": L("'blank'")}, "selector": {"id": "default"}}],
                "text": [{"properties": {
                    "show": L("true"), "text": L(f"'{texto}'"), "fontSize": L("10D"), "bold": L("true"),
                    "fontColor": {"solid": {"color": L("'#FFFFFF'")}}, "horizontalAlignment": L("'Center'")},
                    "selector": {"id": "default"}}],
                "fill": [{"properties": {"show": L("true"), "fillColor": {"solid": {"color": L("'#1F3A5F'")}}},
                          "selector": {"id": "default"}}],
                "outline": [{"properties": {"show": L("false")}, "selector": {"id": "default"}}],
            },
            "visualContainerObjects": {
                "visualLink": [{"properties": {
                    "show": L("true"), "type": L("'Bookmark'"), "bookmark": L(f"'{bookmark}'"),
                    "tooltip": L(f"'{dica}'")}}],
            },
        },
    }
    if oculto:
        j["isHidden"] = True
    return j


def estado(visivel):
    """visivel: ids visiveis; os demais ficam ocultos. Tipo de cada visual vem do disco."""
    vc = {}
    for vid in [GRAF, LARGO, *SLICERS, BTN_OCULTAR, BTN_MOSTRAR]:
        tipo = ler(VIS / vid / "visual.json")["visual"]["visualType"]
        s = {"visualType": tipo}
        if vid not in visivel:
            s["display"] = {"mode": "hidden"}
        vc[vid] = {"singleVisual": s}
    return vc


def favorito(nome, titulo, visivel):
    return {
        "$schema": f"{S}/bookmark/2.1.0/schema.json",
        "displayName": titulo,
        "name": nome,
        "options": {"applyOnlyToTargetVisuals": True, "suppressData": True, "suppressActiveSection": True,
                    "targetVisualNames": [GRAF, LARGO, *SLICERS, BTN_OCULTAR, BTN_MOSTRAR]},
        "explorationState": {"version": "1.3", "activeSection": "pagina1",
                             "sections": {"pagina1": {"visualContainers": estado(visivel)}}},
    }


def main():
    estreito = ler(VIS / GRAF / "visual.json")
    pe = estreito["position"]
    y_graf, h_graf = pe["y"], pe["height"]
    page_w = ler(REP / "pages" / "pagina1" / "page.json")["width"]

    # grafico largo: copia do estreito, ocupando a largura da pagina; so aparece com o painel oculto
    largo = copy.deepcopy(estreito)
    largo["name"] = LARGO
    largo["position"].update(x=0, width=page_w, z=pe["z"] + 1, tabOrder=pe["z"] + 1)
    largo["isHidden"] = True
    gravar(VIS / LARGO / "visual.json", largo)

    # botoes no canto superior direito de cada grafico (linha do titulo)
    gravar(VIS / BTN_OCULTAR / "visual.json", botao(
        BTN_OCULTAR, "▲ Ocultar métricas", BK_FECHADO, "Esconde modalidade, categoria e valor",
        pe["x"] + pe["width"] - LARG_BTN - 6, y_graf + 3, 20000, oculto=False))
    gravar(VIS / BTN_MOSTRAR / "visual.json", botao(
        BTN_MOSTRAR, "▼ Escolher métricas", BK_ABERTO, "Mostra modalidade, categoria e valor",
        page_w - LARG_BTN - 6, y_graf + 3, 20001, oculto=True))

    pasta = REP / "bookmarks"
    gravar(pasta / f"{BK_ABERTO}.bookmark.json",
           favorito(BK_ABERTO, "Métricas visíveis", {GRAF, *SLICERS, BTN_OCULTAR}))
    gravar(pasta / f"{BK_FECHADO}.bookmark.json",
           favorito(BK_FECHADO, "Métricas ocultas", {LARGO, BTN_MOSTRAR}))
    gravar(pasta / "bookmarks.json", {
        "$schema": f"{S}/bookmarksMetadata/1.0.0/schema.json",
        "items": [{"name": BK_ABERTO}, {"name": BK_FECHADO}]})
    print("ok: grafico largo, 2 botoes e 2 favoritos em", REP)


main()

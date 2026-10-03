# ---------------------------------------------------------------- políticas afirmativas e apoio (nova aba)
FMT["milhões de famílias"] = '#,##0.0'
FMT["R$ por mês"] = '#,##0.00'
PT = "Portal da Transparência – ação {a} (S40)"


def RA(id, cod, ind, conc, amb, un, vals, fts, tipo, obs, tys=None):
    r = R(id, cod, ind, conc, amb, un, None, None, "", "", tipo, obs)
    r["V"] = dict(zip(YEARS, vals)); r["FT"] = dict(zip(YEARS, fts)); r["TY"] = dict(zip(YEARS, tys or [None] * 4))
    for y in YEARS:
        v = r["V"][y]
        if v == NL or (isinstance(v, str) and v.startswith("não se aplica")):
            r["TY"][y] = "NÃO LOCALIZADO"
    return r


BF_F = [PT.format(a="8442"), PT.format(a="8442"), PT.format(a="21DP – Auxílio Brasil"), PT.format(a="8442")]
DA_OBS = ("Orçamento atualizado conforme o Portal; em 2025 o Portal mostra empenho acima do orçamento "
          "atualizado (base do Portal defasada em relação a créditos adicionais).")


def st(prefix, cod, nome, un, data, fonte, obs_pago=""):
    lab = [("da", "Orçamento atualizado"), ("emp", "Empenhado"), ("liq", "Liquidado"),
           ("pago", "Pago no exercício (sem RAP)"), ("rap", "Restos a pagar pagos no ano")]
    out = []
    for i, (k, l) in enumerate(lab):
        obs = obs_pago if k == "pago" else (DA_OBS if k == "da" else "")
        out.append(RA(f"{prefix}_{k}", cod, nome, l, "União", un, [d[i] for d in data], fonte, "OFICIAL", obs))
    return out


SEG_SHEET = "Segurança e polít. afirmativas"
sr = {k: LOC[k][1] for k in ("pa_da", "pa_emp", "pa_liq", "pa_pago")}
NA21 = "não se aplica – programa criado em 2021"
NA24 = "não se aplica – programa criado em 2024"
AFF_ROWS = (
    st("bf", "PA.1", "Transferência de renda – Bolsa Família (2016, 2019, 2025) / Auxílio Brasil (2022)", "R$ bi",
       [[27.49159, 27.49159, 27.49159, 27.49159, 0.04616], [32.48162, 32.48162, 32.48162, 32.48162, 0.0],
        [113.85056, 113.03283, 113.02915, 113.02915, 0.0], [158.21813, 171.83567, 171.82365, 171.82365, 0.0]], BF_F,
       "2022 = ação 21DP (Auxílio Brasil, inclui o adicional de R$ 200 aprovado pela EC 123/2022). 2025 = novo Bolsa Família (Lei 14.601/2023).")
    + [
        RA("bf_rtn", "PA.1.1", "Bolsa Família e Auxílio Brasil – pago (RTN, caixa)", "Linha 4.4.1.2 do RTN", "Governo Central", "R$ bi",
           [28.707, 32.981, 88.119, 158.126], ["STN – RTN tab. 2.2 (S41)"] * 4, "OFICIAL",
           "Divergência com o Portal: em 2022 o RTN (88,1) não inclui o adicional pago por crédito extraordinário (Portal: 113,0); "
           "em 2025 o Portal (171,8) supera o RTN (158,1) por diferenças de classificação e critério (caixa × pago no exercício). Não somar as duas fontes."),
        RA("bf_fam", "PA.1.2", "Famílias atendidas pelo Bolsa Família / Auxílio Brasil", "Posição mensal (mês indicado na fonte)", "Brasil",
           "milhões de famílias", [13.9, 13.5, 21.6, 18.7],
           ["MDS via imprensa – set/2016 (S42)", "MDS – out/2019 (S42)", "MDS/Casa Civil – dez/2022 (S42)", "MDS – dez/2025 (S42)"],
           "APROXIMAÇÃO", "Estoque mensal, não média anual; meses diferentes em 2016 (set) e 2019 (out).", ["IMPRENSA/SETORIAL", None, None, None]),
        RA("bf_med", "PA.1.3", "Benefício médio por família", "Valor mensal no mês de referência", "Brasil", "R$ por mês",
           [NL, NL, 607.14, 691.37], ["—", "—", "MDS/Casa Civil – dez/2022 (S42)", "MDS – dez/2025 (S42)"], "OFICIAL",
           "Valor nominal mensal; 2016 e 2019 não localizados com precisão (fontes secundárias divergentes)."),
        RA("bpc_aff", "PA.2", "Benefício de Prestação Continuada (BPC/LOAS) e RMV – pago",
           "RTN, caixa (idosos e pessoas com deficiência de baixa renda)", "Governo Central", "R$ bi",
           [48.990, 59.728, 78.827, 127.236], ["STN – RTN tab. 2.1 (S04)"] * 4, "OFICIAL", "Mesma série da aba 'Despesas públicas' (linha 11.3)."),
    ]
    + st("pnaes", "PA.3", "Assistência estudantil no ensino superior – PNAES (ação 4002)", "R$ mi",
         [[1006.67, 951.87, 814.25, 810.10, 133.37], [1060.91, 1053.04, 881.67, 867.39, 124.22],
          [985.75, 983.97, 826.78, 818.34, 167.92], [1322.53, 1443.22, 1270.90, 1242.07, 185.32]], [PT.format(a="4002")] * 4)
    + st("ept", "PA.4", "Assistência estudantil na rede federal de EPT – institutos federais (ação 2994)", "R$ mi",
         [[442.28, 420.67, 345.74, 340.18, 64.16], [492.61, 487.06, 399.44, 391.60, 69.88],
          [531.99, 528.12, 429.14, 421.17, 93.41], [627.91, 688.86, 591.02, 575.20, 106.50]], [PT.format(a="2994")] * 4)
    + st("bp", "PA.5", "Bolsa Permanência no ensino superior – indígenas, quilombolas e baixa renda (ação 0A12)", "R$ mi",
         [[162.00, 161.51, 151.59, 151.59, 13.48], [184.58, 181.01, 162.93, 162.93, 12.40],
          [144.03, 143.60, 133.85, 132.69, 0.02], [377.74, 441.80, 397.29, 406.45, 22.42]], [PT.format(a="0A12")] * 4,
         "2025: pago acima do liquidado na base do Portal (inclui liquidações de exercícios anteriores).")
    + [
        RA("rac_da", "PA.6", "Igualdade racial – programas 2034 (2016, 2019) e 5804 (2025)", "Orçamento atualizado", "União", "R$ mi",
           [f"={q(SEG_SHEET)}!{{C}}{sr['pa_da']}"] * 4, ["Vínculo com a aba 'Segurança e polít. afirmativas'"] * 4, "APROXIMAÇÃO",
           "Mesmos valores da aba de segurança e políticas afirmativas (vínculo).", [None, None, "NÃO LOCALIZADO", None]),
        RA("rac_emp", "PA.6", "Igualdade racial – programas 2034 (2016, 2019) e 5804 (2025)", "Empenhado", "União", "R$ mi",
           [f"={q(SEG_SHEET)}!{{C}}{sr['pa_emp']}"] * 4, ["Vínculo"] * 4, "APROXIMAÇÃO", "", [None, None, "NÃO LOCALIZADO", None]),
        RA("rac_pago", "PA.6", "Igualdade racial – programas 2034 (2016, 2019) e 5804 (2025)", "Pago no exercício (sem RAP)", "União", "R$ mi",
           [f"={q(SEG_SHEET)}!{{C}}{sr['pa_pago']}"] * 4, ["Vínculo"] * 4, "APROXIMAÇÃO",
           "2022: sem programa específico no PPA 2020–23.", [None, None, "NÃO LOCALIZADO", None]),
        RA("gas", "PA.7", "Auxílio Gás (vale-gás)", "2022: orçamento; 2025: gasto previsto do novo programa", "União", "R$ bi",
           [NA21, NA21, 2.8, 2.6], ["—", "—", "MDS (S43)", "Gazeta do Povo (S43)"], "APROXIMAÇÃO",
           "Valores de orçamento/previsão, não de pagamento; 2025 inclui a transição para o novo programa de gás.",
           [None, None, None, "IMPRENSA/SETORIAL"]),
        RA("pdm", "PA.8", "Pé-de-Meia (incentivo à permanência no ensino médio)", "Recursos previstos para o ano",
           "União (fundo Fipem, fora do orçamento em 2025)", "R$ bi", [NA24, NA24, NA24, 13.0], ["—", "—", "—", "MEC/TCU via imprensa (S44)"],
           "IMPRENSA/SETORIAL",
           "Previsão anual (R$ 13 bi, dos quais R$ 6 bi foram bloqueados e liberados pelo TCU em fev/2025); pagos via fundo Fipem, fora da LOA. "
           "Valor efetivamente pago em 2025 não localizado."),
        RA("aff_sub", "PA.9", "Subtotal – políticas afirmativas e de apoio (pago no exercício, Portal)",
           "Soma de PA.1 + PA.3 + PA.4 + PA.5 + PA.6 (mesma fonte e conceito)", "União", "R$ bi",
           ["={C}{bf_pago}+SUM({C}{pnaes_pago},{C}{ept_pago},{C}{bp_pago},{C}{rac_pago})/1000"] * 4, ["Cálculo sobre S40"] * 4,
           "ESTIMADO",
           "Não inclui BPC (fonte RTN, critério distinto), Auxílio Gás e Pé-de-Meia (orçamento/previsão). Para incluir o BPC, somar PA.2 só como ordem de grandeza."),
    ]
)
wb.create_sheet("Políticas afirmativas e apoio", index=wb.sheetnames.index(SEG_SHEET) + 1)
FONTES += [
    ("S40", "Portal da Transparência – execução por ação orçamentária (8442, 21DP, 4002, 2994, 0A12)", "CGU – Portal da Transparência",
     "https://portaldatransparencia.gov.br/programas-e-acoes/acao/8442?ano=2025", "Consulta 22/09/2026", "2016, 2019, 2022 e 2025",
     "Orçamento atualizado, empenho, liquidação, pagamento e RAP pagos", "Painel 'Execução das despesas da ação no ano corrente'",
     "Consulta interrompida depois por verificação humana (CAPTCHA) do Portal, que não foi contornada.", "Alta"),
    ("S41", "RTN – Tabela 2.2 (Bolsa Família e Auxílio Brasil)", "Tesouro Nacional",
     "https://www.tesourotransparente.gov.br/publicacoes/boletim-resultado-do-tesouro-nacional-rtn/2025/12", "29/01/2026", "1997–2025",
     "Linha 4.4.1.2", "Tabela 2.2", "Critério caixa.", "Alta"),
    ("S42", "MDS/Casa Civil – famílias atendidas e benefício médio", "MDS / Casa Civil (via gov.br e imprensa)",
     "https://www.gov.br/mds/pt-br/noticias-e-conteudos/desenvolvimento-social/noticias-desenvolvimento-social/em-novo-recorde-mais-de-21-6-milhoes-de-familias-recebem-o-auxilio-brasil-em-dezembro",
     "2016–2025", "set/2016, out/2019, dez/2022, dez/2025", "Famílias e benefício médio", "Notícias",
     "2022: 21,6 mi famílias, R$ 607,14; 2025: 18,7 mi famílias, R$ 691,37; 2019: 13,5 mi (out); 2016: 13,9 mi (set, imprensa).", "Alta / Média (2016)"),
    ("S43", "Auxílio Gás – orçamento 2022 e novo programa 2025", "MDS; Gazeta do Povo",
     "https://www.gazetadopovo.com.br/republica/governo-novo-vale-gas-custo-2-6-bilhoes-em-2025/", "2023 e 2025", "2022 e 2025",
     "Recursos do Auxílio Gás", "Notícias", "2022: R$ 2,8 bi (MDS, orçamento); 2025: R$ 2,6 bi (custo previsto).", "Média"),
    ("S44", "Pé-de-Meia – recursos de 2025 e decisão do TCU", "MEC / TCU (via Rádio Senado e imprensa)",
     "https://www12.senado.leg.br/radio/1/noticia/2025/02/13/tcu-libera-retomada-do-programa-pe-de-meia-incentivo-a-conclusao-do-ensino-medio",
     "02/2025", "2025", "Recursos do Pé-de-Meia", "Notícias", "R$ 13 bi previstos para 2025, pagos via Fipem.", "Média"),
]
TENTATIVAS += [
    ("Benefício médio do Bolsa Família em 2016 e 2019", "MDS (páginas antigas), imprensa", "Somente resumos secundários divergentes; não registrados."),
    ("Pé-de-Meia pago em 2025", "MEC, TCU, imprensa", "Localizada só a previsão anual (R$ 13 bi)."),
    ("Outras ações no Portal (ex.: BPC idoso 2025, Auxílio Gás por ação)", "Portal da Transparência",
     "Consulta bloqueada por verificação humana (CAPTCHA), que não foi contornada; usaram-se RTN e notícias oficiais."),
    ("ProUni (renúncia tributária) por ano", "Receita Federal (DGT), Portal da Transparência – Renúncias",
     "Não incluído: valores anuais comparáveis não localizados na busca."),
]

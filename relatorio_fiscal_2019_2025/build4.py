# -*- coding: utf-8 -*-
"""Relatório econômico-fiscal Brasil 2016 × 2019 × 2022 × 2025 (xlsx).
Reaproveita os dados 2019/2025 de build.py e acrescenta 2016 e 2022."""
import sys, re
BASE = open(sys.argv[3], encoding="utf-8").read().split("# ---------------------------------------------------------------- workbook")[0]
exec(BASE)

YEARS = [2016, 2019, 2022, 2025]
YCOL = {2016: "F", 2019: "G", 2022: "H", 2025: "I"}
IPCA = {2016: 4775.70, 2019: 5320.25, 2022: 6474.09, 2025: 7403.29}
PIB = {2016: 6269.327, 2019: 7389.131, 2022: 10079.676, 2025: 12738.566}
PTAX = {
 2016: [4.0524, 3.9737, 3.7039, 3.5658, 3.5393, 3.4245, 3.2756, 3.2097, 3.2564, 3.1858, 3.3420, 3.3523],
 2019: PTAX19,
 2022: [5.5341, 5.1966, 4.9684, 4.7580, 4.9551, 5.0492, 5.3681, 5.1433, 5.2370, 5.2503, 5.2747, 5.2424],
 2025: PTAX25,
}

# ---------------------------------------------------------------- novas fontes
FONTES += [
 ("S29", "Arrecadação federal 2016 (R$ 1,289 tri) e 2022 (R$ 2,218 tri)", "Receita Federal (via Agência Brasil / gov.br)", "https://www.gov.br/receitafederal/pt-br/assuntos/noticias/2023/janeiro/arrecadacao-federal-alcanca-mais-de-r-2-21-trilhoes-no-acumulado-de-janeiro-a-dezembro-de-2022", "01/2017 e 01/2023", "2016 e 2022", "Arrecadação das receitas federais", "Nota de arrecadação", "", "Alta"),
 ("S30", "DPF encerra 2016 em R$ 3,113 tri; DPF fecha 2022 em R$ 5,951 tri", "Tesouro Nacional (via Agência Brasil / InfoMoney)", "https://agenciabrasil.ebc.com.br/economia/noticia/2017-01/divida-publica-federal-encerra-2016-em-r-3113-trilhoes", "01/2017 e 01/2023", "2016 e 2022", "Estoque da DPF e DPMFi", "RMD", "DPMFi: R$ 2,986 tri (2016) e R$ 5,698 tri (2022).", "Alta"),
 ("S31", "Setor público: déficit primário de R$ 155,791 bi em 2016; superávit de R$ 126 bi em 2022", "BCB (via MEON/Estadão e CNN Brasil/Monitor Mercantil)", "https://www.cnnbrasil.com.br/economia/seu-bolso/meu-dinheiro/setor-publico-consolidado-registra-superavit-de-r-126-bi-em-2022-aponta-bc/", "01/2017 e 01/2023", "2016 e 2022", "Primário e juros nominais do setor público consolidado", "Notícias com dados BCB", "Juros: R$ 407,024 bi (6,46% PIB) em 2016; R$ 586,4 bi (5,96% PIB) em 2022.", "Alta (reproduz BCB)"),
 ("S32", "BNDES desembolsa R$ 88,3 bi em 2016; Relatório Anual 2022 (R$ 97,5 bi)", "BNDES", "https://www.bndes.gov.br/wps/portal/site/home/imprensa/noticias/conteudo/bndes-desembolsa-88-3-bilhoes-em-2016", "01/2017 e 2023", "2016 e 2022", "Desembolsos e aprovações", "Nota / Relatório Anual", "Aprovações 2016: R$ 79,2 bi. Aprovações 2022 não publicadas diretamente nas fontes acessadas; estimadas a partir das variações divulgadas pelo BNDES (2023 = R$ 175 bi, +32%; 2025 = R$ 237,9 bi, +80% sobre 2022) ⇒ ≈ R$ 132,5 bi.", "Alta / estimativa"),
 ("S33", "Caged 2016 (sistema antigo) e Novo Caged 2022", "MTb/MTE (via IstoÉ Dinheiro e Agência Brasil)", "https://agenciabrasil.ebc.com.br/economia/noticia/2023-01/dezembro-fecha-com-saldo-negativo-de-431011-empregos-diz-novo-caged", "01/2017 e 01/2023", "2016 e 2022", "Admissões, desligamentos, saldo e estoque", "Notícias com dados do Caged", "2016: saldo −1.321.994; admissões ~14,7 mi e desligamentos ~16,1 mi (arredondados). 2022: 22.648.395 admissões, 20.610.413 desligamentos, estoque dez/2022 42.716.337.", "Alta (reproduz MTE)"),
 ("S34", "PNAD Contínua – taxa média anual de desocupação 2016 (11,5%) e 2022 (9,3%)", "IBGE", "https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/36336-pnad-continua-em-2022-taxa-media-anual-de-desocupacao-foi-de-9-3-enquanto-de-taxa-de-subutilizacao-foi-de-20-8", "02/2017 e 02/2023", "2016 e 2022", "Taxa média anual de desocupação", "Release", "Desocupados 2022: 10,0 milhões.", "Alta"),
 ("S35", "Plano Agrícola e Pecuário 2016/2017 e Plano Safra 2022/2023", "MAPA / MDA (via Agrolink e Agência Brasil)", "https://agenciabrasil.ebc.com.br/economia/noticia/2022-06/plano-safra-20222023-anuncia-r-3408-bilhoes-para-agropecuaria", "05/2016 e 06/2022", "Ciclos 2016/17 e 2022/23", "Recursos anunciados", "Notícias", "2016/17: PAP R$ 202,88 bi (anúncio; ajustado depois para R$ 185 bi) + Plano Safra da Agricultura Familiar R$ 30 bi. 2022/23: R$ 340,88 bi, incluindo Pronaf R$ 53,61 bi.", "Alta (reproduz MAPA)"),
 ("S36", "Subsídios da União 2016 (Fazenda) e 2022 (OSU/MPO)", "Ministério da Fazenda (via Poder360) / MPO", "https://www.gov.br/planejamento/pt-br/assuntos/noticias/2023/junho/subsidios-concedidos-pela-uniao-atingem-r-581-49-bilhoes-em-2022", "2017 e 06/2023", "2016 e 2022", "Subsídios tributários, financeiros e creditícios", "OSU", "2016: R$ 386 bi (271 tributários + 115 financeiros/creditícios; 1ª edição, pode ter sido revisada). 2022: R$ 581,49 bi (461,05 + 120,43).", "Alta"),
 ("S37", "Investimentos privados em infraestrutura somam R$ 131 bi (2022)", "Abdib (via Diário do Comércio)", "https://diariodocomercio.com.br/economia/investimentos-privados-em-infraestrutura-somam-r-131-bi-no-pais/", "2023", "2022", "Investimento privado e público em infraestrutura", "Notícia", "2022: privado R$ 131 bi; setor público (todas as esferas) R$ 31,9 bi. 2016: 1,94% do PIB (sem valor em R$).", "Média (entidade setorial)"),
 ("S38", "Governo Central registra superávit de R$ 54,086 bi em 2022", "Tesouro (via Agência Brasil)", "https://agenciabrasil.ebc.com.br/economia/noticia/2023-01/governo-central-registra-superavit-de-r-54086-bi-em-2022", "01/2023", "2022", "Resultado primário do Governo Central (divulgação original)", "Notícia", "Série histórica atual do RTN registra R$ 46,4 bi (revisões posteriores).", "Alta (reproduz STN)"),
 ("S39", "PAC: estoque de restos a pagar supera orçamento de 2016", "Senado Federal (notícia)", "https://www2.senado.leg.br/bdsf/bitstream/handle/id/50561/noticia.htm?sequence=1&isAllowed=y", "2016", "2016", "Orçamento previsto do PAC em 2016", "Notícia", "Orçamento do PAC em 2016 ≈ R$ 42 bi (dotação, não pagamento).", "Média (imprensa)"),
]
TENTATIVAS += [
 ("Igualdade racial em 2022", "Portal da Transparência, Inesc, buscas por programa 5034 (PPA 2020–23)", "Não havia programa orçamentário específico de igualdade racial no PPA 2020–23 (ações diluídas no programa 5034 do MMFDH); não há recorte comparável."),
 ("PAC em 2022", "—", "Não se aplica: o PAC foi descontinuado após 2019 e o Novo PAC só foi lançado em 2023."),
 ("Estoque de emprego formal em dez/2016 (valor exato)", "Agência Brasil, IstoÉ Dinheiro, MTE", "Não localizado o número exato; estimado a partir do saldo de dezembro (−462.366 = −1,19% do estoque de novembro)."),
 ("Aprovações do BNDES em 2022", "Relatório Anual 2022, notícias BNDES", "Não localizado diretamente; estimado a partir das variações publicadas pelo BNDES."),
 ("Abdib por setor em 2016 e 2022; privado em 2016", "Site Abdib, Diário do Comércio, CNN", "Só foram localizados totais (2022) e % do PIB (2016)."),
 ("Desocupados (média anual) em 2016", "IBGE, imprensa", "Não localizado o número absoluto; a taxa (11,5%) foi localizada."),
]

# ---------------------------------------------------------------- 2016 e 2022
# X[id] = (v2016, v2022, fonte2016, fonte2022, obs_extra, tipo2016, tipo2022)
def X(v16, v22, f16, f22, obs="", t16=None, t22=None):
    return dict(v16=v16, v22=v22, f16=f16, f22=f22, obs=obs, t16=t16, t22=t22)
S1 = SIDRA; S4 = "STN – RTN tab. 2.1 (S04)"; S5 = "RREO Anexo 01 (S05)"; S8 = "BCB SGS (S08)"
EXT = {
 "pib": X(6269.327, 10079.676, S1, S1), "vab": X(5419.822, 8736.476, S1, S1), "imp": X(849.506, 1343.201, S1, S1),
 "agro": X(306.654, 581.343, S1, S1), "ind": X(1150.720, 2300.127, S1, S1), "extr": X(55.575, 476.676, S1, S1),
 "transf": X(676.238, 1317.826, S1, S1), "siup": X(143.720, 211.586, S1, S1), "constr": X(275.187, 294.040, S1, S1),
 "serv": X(3962.446, 5855.005, S1, S1), "com": X(699.768, 1117.748, S1, S1), "transp": X(235.979, 279.382, S1, S1),
 "info": X(179.031, 291.184, S1, S1), "fin": X(425.533, 609.376, S1, S1), "imob": X(527.006, 770.175, S1, S1),
 "outros": X(950.012, 1421.303, S1, S1), "adm": X(945.120, 1365.840, S1, S1),
 "nfin": X("={C}{serv}-{C}{fin}", "={C}{serv}-{C}{fin}", "Cálculo sobre S01", "Cálculo sobre S01"),
 "arrec": X(1289.0, 2218.0, "Receita Federal (S29)", "Receita Federal (S29)", "2016: R$ 1,289 tri; 2022: R$ 2,218 tri (publicados sem mais casas)."),
 "rfb": X(819.752, 1390.000, S4, S4), "ir": X(341.115, 667.223, S4, S4), "cofins": X(204.679, 276.748, S4, S4),
 "csll": X(68.143, 158.497, S4, S4), "iof": X(33.782, 59.091, S4, S4), "rgps": X(358.137, 535.710, S4, S4),
 "concess": X(21.908, 46.847, S4, S4, "2022 inclui privatização da Eletrobras e leilões do pré-sal."), "divid": X(2.848, 87.004, S4, S4, "2022: dividendos extraordinários da Petrobras."),
 "recnat": X(23.275, 132.482, S4, S4), "rectot": X(1315.985, 2313.305, S4, S4), "transfrep": X(226.835, 457.204, S4, S4),
 "recliq": X(1089.150, 1856.102, S4, S4),
 "gtrib": X(271.0, 461.05, "Fazenda – OSU 1ª ed. (S36)", "MPO – OSU (S36)", "2016 e 2022 são valores apurados (ex post); 2016 da 1ª edição do OSU, sujeito a revisão.", "OFICIAL", "OFICIAL"),
 "bfc": X(115.0, 120.43, "Fazenda – OSU (S36)", "MPO – OSU (S36)", "2016 e 2022 apurados; 2016 inflado por subsídios implícitos do BNDES/FIES.", "OFICIAL", "OFICIAL"),
 "subtot": X(386.0, 581.49, "S36", "S36", "", "OFICIAL", "OFICIAL"),
 "desprim": X(1250.426, 1809.693, S4, S4), "prev_rtn": X(507.871, 796.977, S4, S4), "pessoal": X(257.872, 337.942, S4, S4),
 "bpc": X(48.990, 78.827, S4, S4), "abono": X(56.014, 64.271, S4, S4), "fundeb": X(13.675, 32.882, S4, S4),
 "precat": X(10.163, 17.349, S4, S4), "discr": X(141.909, 152.143, S4, S4),
 "resprim": X(-161.276, 46.408, S4, S4, "2022: divulgação original = superávit de R$ 54,086 bi (S38); série atual = R$ 46,4 bi."),
 "jurosgc": X(318.362, 503.234, S4, S4),
 "desptot": X("={C}{desprim}+{C}{jurosgc}", "={C}{desprim}+{C}{jurosgc}", "Cálculo S04", "Cálculo S04"),
 "nomgc": X(-477.835, -448.288, S4, S4),
 "gastosu": X(1875.18, 2603.83, S5, S5), "gastosu_ref": X(2572.18, 4059.50, S5, S5), "loatot": X(2953.55, 4726.93, S5, S5),
 "dpf": X(3113.0, 5951.0, "Tesouro – RMD (S30)", "Tesouro – RMD (S30)"), "dpmfi": X(2986.0, 5698.0, "S30", "S30"),
 "dbgg": X(4378.48639, 7224.88223, S8, S8), "dbgg_pib": X(0.6984, 0.7168, S8, S8),
 "dlsp": X(2892.91346, 5658.01687, S8, S8), "dlsp_pib": X(0.4614, 0.5613, S8, S8),
 "jurosorc": X(204.89, 247.31, S5, S5), "juros_dot": X(304.10, 351.42, S5, S5),
 "jurosliq": X(407.024, 586.4, "BCB (S31)", "BCB (S31)"), "jurospib_pub": X(0.0646, 0.0596, "S31", "S31", "Percentuais publicados com a série de PIB da época."),
 "primsp": X(-155.791, 126.0, "S31", "S31"),
 "nomsp": X("={C}{primsp}-{C}{jurosliq}", "={C}{primsp}-{C}{jurosliq}", "Cálculo sobre S31", "Cálculo sobre S31", "2022 publicado: déficit nominal de R$ 460 bi."),
 "nfsp_pib": X(0.0898, 0.0457, S8, S8),
 "amort": X(271.44, 207.09, S5, S5), "refin": X(653.82, 1425.07, S5, S5), "refin_dot": X(766.75, 1838.02, S5, S5),
 "inv_rtn": X(48.051, 40.639, "STN – RTN tab. 2.3 (S04)", "S04"), "inv_rtn_tot": X(64.813, 45.055, "S04", "S04"),
 "pa_da": X(39.609, NL, "Portal – Programa 2034 (S07)", "Sem programa específico no PPA 2020–23", "", None, "NÃO LOCALIZADO"),
 "pa_emp": X(20.269, NL, "S07", "Sem programa específico no PPA 2020–23", "", None, "NÃO LOCALIZADO"),
 "pa_liq": X(9.406, NL, "S07", "Sem programa específico no PPA 2020–23", "", None, "NÃO LOCALIZADO"),
 "pa_pago": X(8.298, NL, "S07", "Sem programa específico no PPA 2020–23", "2016: RAP pagos no ano R$ 23,83 mi.", None, "NÃO LOCALIZADO"),
 "pa_mir": X(NL, NL, "MIR inexistente (SEPPIR)", "MIR inexistente", "", "NÃO LOCALIZADO", "NÃO LOCALIZADO"),
 "pa_transv": X(NL, NL, "Sem agenda transversal", "Sem agenda transversal", "", "NÃO LOCALIZADO", "NÃO LOCALIZADO"),
 "bndes_des": X(88.3, 97.5, "BNDES (S32)", "BNDES – Relatório Anual 2022 (S32)"),
 "bndes_apr": X(79.2, 132.5, "BNDES via MEON (S32)", "Estimativa a partir de variações BNDES (S32)", "2022 é estimativa (≈ 175/1,32 ≈ 237,9/1,80).", None, "ESTIMADO"),
 "bndes_gar": X(NL, NL, "—", "—", "", "NÃO LOCALIZADO", "NÃO LOCALIZADO"),
 "safra_tot": X("={C}{safra_emp}+{C}{safra_af}", 340.88, "Cálculo: PAP + PSAF (S35)", "MAPA (S35)", "2016/17 = PAP 202,88 (anúncio; ajustado para 185) + agricultura familiar 30,0. 2022/23 = 340,88 (inclui Pronaf)."),
 "safra_emp": X(202.88, "={C}{safra_tot}-{C}{safra_af}", "MAPA (S35)", "Cálculo: total − Pronaf"),
 "safra_af": X(30.0, 53.61, "MDA (S35)", "MAPA (S35)"),
 "pd_pib": X(0.0119584, 0.0118873, "MCTI via World Bank WDI (S22)", "MCTI via World Bank WDI (S22)", "2016 e 2022 são dados observados.", "OFICIAL", "OFICIAL"),
 "pd_rs": X("={C}{pd_pib}*PIB_2016", "={C}{pd_pib}*PIB_2022", "Cálculo S22 × S01", "Cálculo S22 × S01"),
 "estoque": X(38392395, 42716337, "Estimativa sobre Caged (S33)", "Novo Caged (S33)", "2016 estimado: 462.366 ÷ 1,19% − 462.366 (saldo de dezembro e variação relativa publicados).", "ESTIMADO", "OFICIAL"),
 "adm": X(14700000, 22648395, "Caged via Agência Brasil (S33)", "Novo Caged (S33)", "2016 publicado arredondado (14,7 mi).", "APROXIMAÇÃO", None),
 "desl": X(16100000, 20610413, "Caged via Agência Brasil (S33)", "Novo Caged (S33)", "2016 publicado arredondado (16,1 mi).", "APROXIMAÇÃO", None),
 "saldo": X(-1321994, "={C}{adm}-{C}{desl}", "Caged (S33)", "Novo Caged (S33)", "2016: saldo publicado (não calculado, pois admissões/desligamentos estão arredondados)."),
 "desoc": X(0.115, 0.093, "IBGE (S34)", "IBGE (S34)"),
 "desoc_sidra": X(0.116, 0.0925, "SIDRA 4099", "SIDRA 4099"),
 "desocup": X(NL, 10.0, "Não localizado", "IBGE (S34)", "", "NÃO LOCALIZADO", None),
 "exp": X(179.526129214, 334.13603822, "Comex Stat (S18)", "Comex Stat (S18)"),
 "imp": X(139.321357653, 272.610686946, "Comex Stat (S18)", "Comex Stat (S18)"),
 "saldo_bc": X("={C}{exp}-{C}{imp}", "={C}{exp}-{C}{imp}", "Cálculo S18", "Cálculo S18"),
 "corrente": X("={C}{exp}+{C}{imp}", "={C}{exp}+{C}{imp}", "Cálculo S18", "Cálculo S18"),
 "idp": X(74.2946, 75.5011, S8, S8),
 "fbcf": X(973.270, 1794.223, S1, S1),
 "nib": X(NL, NL, "Programa inexistente", "Programa inexistente", "", "NÃO LOCALIZADO", "NÃO LOCALIZADO"),
 "bndes_ind": X(NL, NL, "—", "—", "", "NÃO LOCALIZADO", "NÃO LOCALIZADO"),
 "abdib_priv": X(NL, 131.0, "—", "Abdib via Diário do Comércio (S37)", "2022: recorde da série (desde 2003).", "NÃO LOCALIZADO", None),
 "infra_fed": X(15.874, 13.376, "Cálculo RTN tab. 2.3 (S04)", "Cálculo RTN tab. 2.3 (S04)", "2016: 10,787+1,756+3,139+0,105+0,042+0,045; 2022: 7,147+0,342+5,622+0,025+0,056+0,184."),
 "pac": X(42.0, "não se aplica – PAC extinto (Novo PAC só em 2023)", "Senado (S39) – dotação aproximada", "—", "2016: orçamento previsto do PAC ≈ R$ 42 bi (imprensa).", "IMPRENSA/SETORIAL", "NÃO LOCALIZADO"),
 "inv_transp": X(10.787, 7.147, "S04", "S04"),
 "abdib_tot": X("=0.0194*PIB_2016", 162.9, "Estimativa: 1,94% × PIB (S37)", "Abdib: 131 privado + 31,9 público (S37)", "2016: só o % do PIB foi localizado; valor em R$ é estimativa.", "ESTIMADO", None),
 "abdib_transp": X(NL, NL, "—", "—", "", "NÃO LOCALIZADO", "NÃO LOCALIZADO"),
 "abdib_san": X(NL, NL, "—", "—", "", "NÃO LOCALIZADO", "NÃO LOCALIZADO"),
}
P7 = "Portal da Transparência (S07)"
# estágios: prefix -> (2016 [di,da,emp,liq,pago], 2022 [...])
SX = {
 "tot": ([2141.17, 2188.92, 1961.59, 1892.46, 1875.18], [2854.31, 3067.02, 2793.73, 2675.76, 2603.83]),
 "inv": ([45.31, 47.21, 38.08, 17.28, 16.80], [42.36, 52.07, 51.19, 19.99, 19.59]),
 "sau": ([108.006, 110.456, 106.487, 98.773, 100.191], [147.204, 153.698, 153.231, 136.174, 136.850]),
 "edu": ([91.627, 97.410, 94.546, 84.949, 95.184], [112.505, 118.572, 117.753, 104.467, 109.778]),
 "prev": ([570.877, 595.214, 594.563, 593.925, 568.387], [882.003, 897.749, 897.148, 894.750, 824.009]),
 "rgps": ([481.161, 499.745, 499.525, 499.044, None], [763.251, 776.226, 776.226, 774.211, None]),
 "rpps": ([81.316, 86.338, 86.108, 86.044, None], [112.398, 114.742, 114.257, 114.131, None]),
 "seg": ([7.032, 9.425, 8.816, 7.553, 8.423], [11.607, 13.489, 13.057, 10.982, 11.729]),
 "cid": ([1.313, 3.624, 2.324, 1.802, 1.842], [1.105, 1.003, 0.972, 0.662, 0.724]),
 "ct": ([7.258, 7.372, 6.975, 5.908, 6.126], [12.953, 11.075, 9.273, 8.112, 8.251]),
 "rod": ([6.841, 6.974, 6.088, 3.201, None], [5.711, 8.890, 8.865, 4.389, None]),
 "fer": ([1.404, 1.207, 1.036, 0.743, None], [0.428, 0.239, 0.238, 0.130, None]),
 "por": ([1.319, 0.855, 0.585, 0.302, None], [0.315, 0.198, 0.192, 0.104, None]),
 "aer": ([0.231, 0.217, 0.065, 0.020, None], [0.146, 0.121, 0.121, 0.053, None]),
 "san": ([0.636, 0.641, 0.564, 0.410, 0.409], [0.333, 0.767, 0.763, 0.317, 0.291]),
 "mob": ([1.095, 1.115, 0.834, 0.489, None], [0.343, 0.593, 0.593, 0.301, None]),
}
for pre, (a16, a22) in SX.items():
    for k, i in (("di", 0), ("da", 1), ("emp", 2), ("liq", 3), ("pago", 4)):
        rid = f"{pre}_{k}"
        if a16[i] is None:
            continue
        src = "RREO Anexo 01 (S05)" if pre in ("tot", "inv") else "RREO Anexo 02 (S06)"
        if k == "pago" and pre not in ("tot", "inv"):
            src = P7
        EXT[rid] = X(a16[i], a22[i], src, src)

ALL_LISTS = [PIB_ROWS, REC_ROWS, DESP_ROWS, DIV_ROWS, LOA_ROWS, SOC_ROWS, SEG_ROWS, BND_ROWS, EMP_ROWS, CEX_ROWS, INV_ROWS, INF_ROWS]
for lst in ALL_LISTS:
    for r in lst:
        e = EXT.get(r["id"])
        vals = {}
        # converte fórmulas 2019/2025 ("=F{x}" / "=G{x}") para o marcador de coluna
        v19 = r["v19"]; v25 = r["v25"]
        if isinstance(v19, str) and v19.startswith("="):
            v19 = re.sub(r"F\{", "{C}{", v19).replace("PIB_2019", "PIB_2019")
        if isinstance(v25, str) and v25.startswith("="):
            v25 = re.sub(r"G\{", "{C}{", v25)
        r["V"] = {2019: v19, 2025: v25}
        r["FT"] = {2019: r["f19"], 2025: r["f25"]}
        r["TY"] = {2019: None, 2025: None}
        if e:
            r["V"][2016] = e["v16"]; r["V"][2022] = e["v22"]
            r["FT"][2016] = e["f16"]; r["FT"][2022] = e["f22"]
            r["TY"][2016] = e["t16"]; r["TY"][2022] = e["t22"]
            if e["obs"]:
                r["obs"] = (r["obs"] + " " if r["obs"] else "") + "[2016/2022] " + e["obs"]
        else:
            r["V"][2016] = NL; r["V"][2022] = NL
            r["FT"][2016] = "—"; r["FT"][2022] = "—"
            r["TY"][2016] = "NÃO LOCALIZADO"; r["TY"][2022] = "NÃO LOCALIZADO"
        # 2019/2025 que eram texto 'não localizado'
        for y in (2019, 2025):
            if r["V"][y] == NL:
                r["TY"][y] = "NÃO LOCALIZADO"

MISSING = [r["id"] for lst in ALL_LISTS for r in lst if r["id"] not in EXT]
print("sem 2016/2022:", MISSING)

# ---------------------------------------------------------------- workbook
wb = Workbook()
ws0 = wb.active
ws0.title = "Resumo executivo"
SHEETS = ["Indicadores consolidados", "PIB setorial", "Receitas públicas", "Despesas públicas", "Dívida e juros",
          "LOA e execução orçamentária", "Saúde, educação e previdência", "Segurança e polít. afirmativas",
          "BNDES, Plano Safra e P&D", "Emprego", "Comércio exterior", "Invest. privados e industriais",
          "Infraestrutura federal", "Fontes e metodologia"]
for s in SHEETS:
    wb.create_sheet(s)
LOC = {}

def q(s): return "'" + s + "'"

def title(ws, t, sub):
    ws["A1"] = t; ws["A1"].font = F_TIT
    ws["A2"] = sub; ws["A2"].font = F_SUB
    ws.row_dimensions[1].height = 22

def header(ws, row, cols, widths):
    for i, (c, w) in enumerate(zip(cols, widths), start=1):
        cell = ws.cell(row=row, column=i, value=c)
        cell.font = F_HDR; cell.fill = HDR_FILL; cell.border = BORDER
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = 48

def resolve(v, col, rowmap):
    if isinstance(v, str) and v.startswith("="):
        v = v.replace("{C}", col)
        for k, r in rowmap.items():
            v = v.replace("{" + k + "}", str(r))
    return v

# colunas das abas temáticas
# A-E descr | F-I valores | J-L corrigidos | M-P variações | Q-R dif abs | S-V %PIB | W-Z fontes | AA tipo | AB obs
TH = (["Código", "Indicador", "Conceito / estágio", "Âmbito", "Unidade", "Brasil 2016", "Brasil 2019", "Brasil 2022", "Brasil 2025",
       "2016 em R$ de dez/2025", "2019 em R$ de dez/2025", "2022 em R$ de dez/2025",
       "Variação 2016→2019", "Variação 2019→2022", "Variação 2022→2025", "Variação 2016→2025",
       "Diferença absoluta 2025−2016 (nominal)", "Diferença absoluta 2025−2019 (nominal)",
       "2016 % do PIB", "2019 % do PIB", "2022 % do PIB", "2025 % do PIB",
       "Fonte 2016", "Fonte 2019", "Fonte 2022", "Fonte 2025", "Classificação do dado", "Observações metodológicas"])
THW = [7, 36, 26, 14, 8, 12, 12, 12, 12, 12, 12, 12, 11, 11, 11, 11, 13, 13, 9, 9, 9, 9, 20, 20, 20, 20, 14, 60]
PAIRS = [(2016, 2019), (2019, 2022), (2022, 2025), (2016, 2025)]
CORR = {2016: "J", 2019: "K", 2022: "L", 2025: None}

def corr_ref(y, n):
    return f"{CORR[y]}{n}" if CORR[y] else f"{YCOL[y]}{n}"

def write_row_formulas(ws, n, un):
    """Preenche J..V para a linha n conforme a unidade."""
    money = un in ("R$ bi", "R$ mi")
    div = "/1000" if un == "R$ mi" else ""
    for y in (2016, 2019, 2022):
        c = ws.cell(row=n, column=ord(CORR[y]) - 64)
        c.value = f'=IFERROR({YCOL[y]}{n}*FATOR_{y},"n.d.")' if money else "n.a."
        c.number_format = FMT["R$ bi"]
    for j, (a, b) in enumerate(PAIRS):
        c = ws.cell(row=n, column=13 + j)
        if money:
            c.value = f'=IFERROR({corr_ref(b, n)}/{corr_ref(a, n)}-1,"n.d.")'; c.number_format = PCT
        elif un in ("%", "% do PIB"):
            c.value = f'=IFERROR(({YCOL[b]}{n}-{YCOL[a]}{n})*100,"n.d.")'; c.number_format = PP
        else:
            c.value = f'=IFERROR({YCOL[b]}{n}/{YCOL[a]}{n}-1,"n.d.")'; c.number_format = PCT
    for j, a in enumerate((2016, 2019)):
        c = ws.cell(row=n, column=17 + j)
        if un in ("%", "% do PIB"):
            c.value = f'=IFERROR((I{n}-{YCOL[a]}{n})*100,"n.d.")'; c.number_format = PP
        else:
            c.value = f'=IFERROR(I{n}-{YCOL[a]}{n},"n.d.")'; c.number_format = FMT[un]
    for j, y in enumerate(YEARS):
        c = ws.cell(row=n, column=19 + j)
        if money:
            c.value = f'=IFERROR({YCOL[y]}{n}{div}/PIB_{y},"n.d.")'
        elif un == "US$ bi":
            c.value = f'=IFERROR({YCOL[y]}{n}/(PIB_{y}/PTAX_{y}),"n.d.")'
        elif un == "% do PIB":
            c.value = f'=IF(ISNUMBER({YCOL[y]}{n}),{YCOL[y]}{n},"n.d.")'
        else:
            c.value = "n.a."
        c.number_format = PCT

def footnotes(ws, row, notes):
    ws.cell(row=row, column=1, value="Notas metodológicas").font = F_BLD
    for i, t in enumerate(notes + COMMON4, 1):
        ws.cell(row=row + i, column=1, value=f"{i}. {t}").font = F_NOTE

COMMON4 = [
 "Valores nominais do próprio ano (R$ bilhões, salvo indicação). Correção para R$ de dez/2025 pelo IPCA: fator = índice dez/2025 ÷ índice de dezembro do ano (FATOR_2016, FATOR_2019, FATOR_2022 na aba 'Resumo executivo').",
 "Colunas de variação: para valores em R$ = variação REAL (IPCA); para US$ e pessoas = variação nominal; para taxas e % = diferença em pontos percentuais (p.p.).",
 "% do PIB com o PIB anual do IBGE (SIDRA 1846) de cada ano; valores em US$ usam o PIB convertido pela PTAX média anual.",
 "'n.a.' = não se aplica; 'n.d.' = não disponível (algum ano 'não localizado após busca'). Azul = dado digitado da fonte; preto = fórmula; verde = vínculo com outra aba.",
 "Cor da linha = classificação do dado em 2019/2025; células de 2016/2022 com cor própria quando a classificação difere (ex.: estimado, não localizado).",
 "Períodos 2016→2019, 2019→2022 e 2022→2025 correspondem aproximadamente aos mandatos Temer, Bolsonaro e Lula III (até 2025); 2016 inclui o governo Dilma até maio.",
]

def write_theme(sheet, ttl, sub, rows, notes, extra_usd=False, extra_rows_fn=None):
    ws = wb[sheet]
    title(ws, ttl, sub)
    cols = TH + (["2016 em R$ bi (PTAX)", "2019 em R$ bi (PTAX)", "2022 em R$ bi (PTAX)", "2025 em R$ bi (PTAX)"] if extra_usd else [])
    header(ws, 3, cols, THW + ([12] * 4 if extra_usd else []))
    start = 4
    rowmap = {r["id"]: start + i for i, r in enumerate(rows)}
    for i, r in enumerate(rows):
        n = start + i
        LOC[r["id"]] = (sheet, n)
        for c, v in enumerate([r["cod"], r["ind"], r["conc"], r["amb"], r["un"]], 1):
            ws.cell(row=n, column=c, value=v)
        for y in YEARS:
            col = YCOL[y]
            v = resolve(r["V"][y], col, rowmap)
            cell = ws[f"{col}{n}"]
            cell.value = v
            isf = isinstance(v, str) and v.startswith("=")
            cell.font = F_TXT if isf else F_INP
            if isinstance(v, (int, float)) or isf:
                cell.number_format = FMT[r["un"]]
            else:
                cell.alignment = WRAP
        write_row_formulas(ws, n, r["un"])
        for j, y in enumerate(YEARS):
            ws.cell(row=n, column=23 + j, value=r["FT"][y])
        ws.cell(row=n, column=27, value=r["tipo"])
        ws.cell(row=n, column=28, value=r["obs"] or "—")
        if extra_usd:
            for j, y in enumerate(YEARS):
                c = ws.cell(row=n, column=29 + j)
                if r["un"] == "US$ bi":
                    c.value = f'=IFERROR({YCOL[y]}{n}*PTAX_{y},"n.d.")'; c.number_format = FMT["R$ bi"]
                else:
                    c.value = "n.a."
        for c in range(1, len(cols) + 1):
            cell = ws.cell(row=n, column=c)
            cell.border = BORDER
            cell.fill = FILL[r["tipo"]]
            if c not in (6, 7, 8, 9):
                cell.font = F_TXT
            if c <= 5 or c >= 23:
                cell.alignment = WRAP
        for y in YEARS:
            t = r["TY"][y]
            if t and t != r["tipo"]:
                ws[f"{YCOL[y]}{n}"].fill = FILL[t]
    last = start + len(rows) - 1
    if extra_rows_fn:
        last = extra_rows_fn(ws, last, rowmap)
    ws.auto_filter.ref = f"A3:{get_column_letter(len(cols))}{last}"
    ws.freeze_panes = "C4"
    footnotes(ws, last + 2, notes)

def pib_shares(ws, last, rowmap):
    shares = [("sh_agro", "7a", "Participação da agropecuária", "agro"), ("sh_ind", "7b", "Participação da indústria", "ind"),
              ("sh_serv", "7c'", "Participação dos serviços (total)", "serv"),
              ("sh_fin", "7c", "Participação das atividades financeiras", "fin"), ("sh_nfin", "7d", "Participação dos serviços não financeiros", "nfin")]
    p = rowmap["pib"]; v = rowmap["vab"]
    for i, (sid, cod, nome, base) in enumerate(shares):
        n = last + 1 + i
        b = rowmap[base]
        LOC[sid] = ("PIB setorial", n)
        for c, x in enumerate([cod, nome + " no PIB", "VAB da atividade ÷ PIB a preços de mercado", "Brasil", "%"], 1):
            ws.cell(row=n, column=c, value=x)
        for y in YEARS:
            ws[f"{YCOL[y]}{n}"] = f"={YCOL[y]}{b}/{YCOL[y]}{p}"
            ws[f"{YCOL[y]}{n}"].number_format = PCT
        write_row_formulas(ws, n, "%")
        for j in range(4):
            ws.cell(row=n, column=23 + j, value="Cálculo sobre S01")
        ws.cell(row=n, column=27, value="ESTIMADO")
        vb = {x["id"]: x for x in PIB_ROWS}
        def val(k, y):
            if k == "nfin":
                return val("serv", y) - val("fin", y)
            return vb[k]["V"][y]
        txt = "Participação no VAB (critério IBGE): " + "; ".join(f"{y}: " + f"{val(base, y) / vb['vab']['V'][y] * 100:.2f}".replace(".", ",") + "%" for y in YEARS) + "."
        ws.cell(row=n, column=28, value=txt)
        for c in range(1, 29):
            cell = ws.cell(row=n, column=c); cell.border = BORDER; cell.fill = FILL["ESTIMADO"]; cell.font = F_TXT
            if c <= 5 or c >= 23:
                cell.alignment = WRAP
    return last + len(shares)

write_theme("PIB setorial", "PIB setorial – valor adicionado por atividade (valores correntes)",
            "IBGE, Contas Nacionais Trimestrais (SIDRA 1846), soma dos quatro trimestres de cada ano. Participações ao final.",
            PIB_ROWS, ["Serviços não financeiros = VAB de serviços − VAB de atividades financeiras, de seguros e serviços relacionados.",
                       "Participações sobre o PIB a preços de mercado; a observação traz a participação sobre o VAB.",
                       "Série consultada em 22/09/2026; valores podem diferir das divulgações originais de cada ano."], extra_rows_fn=pib_shares)
write_theme("Receitas públicas", "Receitas públicas – União e Governo Central",
            "Arrecadação federal (RFB), receitas do Governo Central (RTN/STN, caixa) e subsídios da União (OSU/PLOA).",
            REC_ROWS, ["Arrecadação federal (RFB) e receita total do RTN são conceitos distintos e não devem ser somados.",
                       "Gastos tributários: 2016, 2019 e 2022 apurados (OSU); 2025 é projeção oficial."])
write_theme("Despesas públicas", "Despesas públicas – Governo Central (RTN) e União (orçamento)",
            "Despesa primária pelo critério caixa (STN); juros e resultado nominal pelo critério competência (BCB); despesa orçamentária paga (RREO).",
            DESP_ROWS, ["Despesa primária (RTN, caixa) ≠ despesa orçamentária paga (RREO).",
                        "A 'despesa total do Governo Central' é aproximação (soma de critérios distintos)."])
write_theme("Dívida e juros", "Dívida pública, juros, amortização e refinanciamento",
            "Estoques em 31 de dezembro (dívida) e fluxos anuais (juros, amortização, refinanciamento).",
            DIV_ROWS, ["Estoques não são somados a fluxos.",
                       "DPF (Tesouro) ≠ DBGG (BCB) ≠ DLSP (BCB).",
                       "Juros pagos (orçamento, caixa) ≠ juros apropriados (BCB, competência). Refinanciamento = rolagem."])
write_theme("LOA e execução orçamentária", "LOA e execução orçamentária da União – despesa total e investimentos",
            "Estágios: dotação inicial → dotação atualizada → empenho → liquidação → pagamento (RREO, 6º bimestre).",
            LOA_ROWS, ["Previsão e execução nunca são somadas.",
                       "'Pago' do RREO = pagamentos do exercício; o RTN soma restos a pagar pagos (linhas 24.1 e 24.2)."])
write_theme("Saúde, educação e previdência", "Saúde, educação e previdência – LOA e execução (União)",
            "RREO Anexo 02 (funções/subfunções) para dotação, empenho e liquidação; Portal da Transparência para valor pago.",
            SOC_ROWS, ["Função orçamentária ≠ mínimos constitucionais (ASPS/MDE).",
                       "2016: vigência do teto de gastos a partir de 2017 (EC 95/2016); 2019–2022 sob teto; 2025 sob o Regime Fiscal Sustentável (LC 200/2023)."])
write_theme("Segurança e polít. afirmativas", "Segurança pública e políticas afirmativas – LOA e execução",
            "Função 06 pelo RREO; políticas afirmativas pelos programas de igualdade racial (Portal da Transparência) e dados do MIR.",
            SEG_ROWS, ["Programa 2034 (PPA 2016–19) cobre 2016 e 2019; 5804 (PPA 2024–27) cobre 2025; no PPA 2020–23 não houve programa específico.",
                       "Valores das políticas afirmativas em R$ milhões."])
write_theme("BNDES, Plano Safra e P&D", "BNDES, Plano Safra e pesquisa & desenvolvimento",
            "BNDES (desembolsos e aprovações), Plano Safra (anúncio por ciclo agrícola) e P&D (orçamento e dispêndio nacional).",
            BND_ROWS, ["Desembolsos do BNDES não são despesas da LOA.",
                       "Plano Safra por ciclo jul–jun: 2016/17, 2019/20, 2022/23 e 2025/26 (não coincidem com os anos civis).",
                       "P&D realizado: dado observado em 2016, 2019 e 2022; 2025 usa o último dado (2023)."])
write_theme("Emprego", "Emprego formal e desemprego",
            "Caged (2016 e 2019, sistema antigo), Novo Caged (2022 e 2025) e PNAD Contínua (IBGE).",
            EMP_ROWS, ["Estoque = posição em 31/dez; admissões, desligamentos e saldo = acumulado jan–dez.",
                       "Quebra de série em 2020 (Caged → Novo Caged): 2016/2019 não são diretamente comparáveis a 2022/2025 em níveis de fluxos."])
write_theme("Comércio exterior", "Comércio exterior e investimento estrangeiro direto (US$)",
            "Comex Stat/MDIC (FOB, série atual) e BCB (IDP, BPM6). Últimas colunas convertem para R$ pela PTAX média anual.",
            CEX_ROWS, ["Valores em US$ não são corrigidos pelo IPCA."], extra_usd=True)
write_theme("Invest. privados e industriais", "Investimentos privados e industriais",
            "Distinção entre investimento anunciado, aprovado/contratado e realizado.",
            INV_ROWS, ["Anunciado (NIB) ≠ aprovado (BNDES) ≠ realizado (FBCF, Abdib)."])
write_theme("Infraestrutura federal", "Infraestrutura – investimentos federais e totais",
            "Orçamento da União por subfunção (RREO), investimentos pagos por função (RTN), PAC/Novo PAC e Abdib.",
            INF_ROWS, ["Subfunções de transporte trazem a despesa total do orçamento, não só o GND 4.",
                       "PAC existia em 2016 e 2019, não em 2022; o Novo PAC começou em 2023."])

# ---------------------------------------------------------------- políticas afirmativas e apoio (nova aba)
FMT["milhões de famílias"] = '#,##0.0'
FMT["R$ por mês"] = '#,##0.00'
FMT["milhões de estudantes"] = '#,##0.0'
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
        RA("pnae_rep", "PA.10", "Alimentação escolar – PNAE: recursos federais repassados", "Repasse do FNDE às redes estaduais, distrital e municipais", "União → subnacionais", "R$ bi",
           [3.42, 3.95, 3.56, 5.5], ["FNDE – Dados físicos e financeiros do PNAE (S45)"] * 3 + ["Orçamento estimado – MEC/Agência Gov (S45)"], "OFICIAL",
           "2016–2022: valores repassados (FNDE). 2025: orçamento estimado do programa (R$ 5,5 bi), não repasse apurado; em 2023 o repasse foi R$ 5,26 bi. Exclui a rede federal (R$ 10,8 mi, 22,2 mi e 34,1 mi pagos em 2016, 2019 e 2022).",
           [None, None, None, "ESTIMADO"]),
        RA("pnae_alu", "PA.10.1", "Alimentação escolar – PNAE: estudantes atendidos", "Alunos atendidos no ano", "Brasil", "milhões de estudantes",
           [40.3, 40.2, 39.58, NL], ["FNDE (S45)"] * 3 + ["—"], "OFICIAL",
           "2025 não localizado (o FNDE informa 'cerca de 40 milhões')."),
        RA("fies_prim", "PA.11", "Fies – impacto primário no resultado do Governo Central", "RTN, linha 4.3.18 (caixa)", "Governo Central", "R$ bi",
           [7.020, 1.942, 0.726, 2.190], ["STN – RTN tab. 2.1 (S04)"] * 4, "OFICIAL",
           "Não é o valor financiado: mede só o efeito primário (subsídio implícito/risco). A concessão de financiamentos (ação 00IG, inversão financeira) não pôde ser obtida no Portal (verificação humana). "
           "Nota Técnica Conof/CD 26/2021 (S46): concessão de financiamentos paga, incl. restos a pagar, em R$ de 2021 = 23,8 bi (2016) e 9,7 bi (2019)."),
        RA("fies_cred", "PA.11.1", "Fies – benefício creditício (subsídio implícito)", "Orçamento de Subsídios da União", "União", "R$ bi",
           [NL, NL, 41.4, NL], ["—", "—", "MPO – OSU (S36)", "—"], "OFICIAL",
           "2022 elevado pelos juros altos (em 2021: R$ 15 bi; em 2023: cerca de R$ 22 bi). Valores anuais de 2016, 2019 e 2025 não localizados nas fontes acessadas."),
        RA("prouni", "PA.12", "ProUni – gasto tributário (renúncia de IRPJ, CSLL, PIS e Cofins)", "Demonstrativo de Gastos Tributários – bases efetivas", "União", "R$ bi",
           [2.170886, 2.195672, 2.827438, 3.621780],
           ["RFB – DGT Bases Efetivas 2016 (S47)", "RFB – DGT Bases Efetivas 2019 (S47)", "RFB – DGT Bases Efetivas 2022 (S47)", "RFB – projeção no DGT Bases Efetivas 2022 (S47)"],
           "OFICIAL", "Renúncia (não é despesa orçamentária). 2025 é projeção da Receita Federal, não valor apurado.", [None, None, None, "ESTIMADO"]),
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
FONTES += [
    ("S45", "PNAE – Dados físicos e financeiros; orçamento 2025", "FNDE / MEC (via Agência Gov e CNM)",
     "https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/programas/pnae/consultas/pnae-dados-fisicos-e-financeiros-do-pnae",
     "Consulta 22/09/2026", "2016–2023; 2025 (orçamento)", "Recursos repassados e alunos atendidos", "Quadros 1 e 2",
     "2016: R$ 3,42 bi / 40,3 mi alunos; 2019: R$ 3,95 bi / 40,2 mi; 2022: R$ 3,56 bi / 39,58 mi; 2023: R$ 5,26 bi; 2025: orçamento estimado R$ 5,5 bi.", "Alta"),
    ("S46", "Nota Técnica Conof/CD nº 26/2021 – séries do Fies e do Prouni", "Câmara dos Deputados",
     "https://www2.camara.leg.br/orcamento-da-uniao/estudos/2021/NT26_2021PSOLUniversidadesFieseProuni.pdf", "2021", "1999–2020",
     "Fies: autorizado e pago (em R$ de 2021)", "Gráficos 17 a 19", "Valores em preços de 2021; citados só como referência.", "Alta"),
    ("S47", "Demonstrativo de Gastos Tributários – Bases Efetivas (2016, 2019 e 2022)", "Receita Federal",
     "https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/relatorios/renuncia/gastos-tributarios-bases-efetivas",
     "2019, 2022 e 2025", "2016, 2019, 2022 (efetivos) e 2025 (projeção)", "ProUni – total de IRPJ, CSLL, PIS e Cofins", "Quadros III, X e XXVI–XXXII",
     "ProUni: 2,1709 bi (2016); 2,1957 bi (2019); 2,8274 bi (2022); 3,6218 bi (projeção 2025).", "Alta"),
]
TENTATIVAS += [
    ("Fies – concessão de financiamentos (ação 00IG) e PNAE por ação orçamentária", "Portal da Transparência (bloqueado por CAPTCHA), FNDE, Câmara",
     "Usados: impacto primário (RTN), repasses do PNAE (FNDE) e NT Conof 26/2021 como referência em preços de 2021."),
    ("Fies – novos contratos por ano", "MEC, FNDE, imprensa", "Série anual comparável não localizada."),
    ("Benefício médio do Bolsa Família em 2016 e 2019", "MDS (páginas antigas), imprensa", "Somente resumos secundários divergentes; não registrados."),
    ("Pé-de-Meia pago em 2025", "MEC, TCU, imprensa", "Localizada só a previsão anual (R$ 13 bi)."),
    ("Outras ações no Portal (ex.: BPC idoso 2025, Auxílio Gás por ação)", "Portal da Transparência",
     "Consulta bloqueada por verificação humana (CAPTCHA), que não foi contornada; usaram-se RTN e notícias oficiais."),
    ("ProUni (renúncia tributária) por ano", "Receita Federal (DGT), Portal da Transparência – Renúncias",
     "Não incluído: valores anuais comparáveis não localizados na busca."),
]

write_theme("Políticas afirmativas e apoio", "Políticas afirmativas e de apoio social – transferência de renda, assistência estudantil e igualdade racial",
            "Subdivisões: PA.1 transferência de renda; PA.2 BPC; PA.3–PA.5 assistência estudantil; PA.6 igualdade racial; PA.7–PA.8 outros apoios; PA.9 subtotal pago; PA.10 PNAE; PA.11 Fies; PA.12 ProUni.",
            AFF_ROWS, ["Agrupamento definido para a análise da dissertação: programas de transferência de renda e de permanência estudantil ao lado das ações de igualdade racial.",
                       "Fontes com critérios distintos (Portal = pago do exercício por ação; RTN = caixa) não são somadas; o subtotal PA.9 usa só o Portal.",
                       "Unidades: transferência de renda, BPC, Auxílio Gás e Pé-de-Meia em R$ bilhões; assistência estudantil e igualdade racial em R$ milhões.",
                       "PNAE (repasse), Fies (impacto primário e subsídio creditício) e ProUni (renúncia tributária) têm conceitos distintos entre si e não entram no subtotal PA.9.",
                       "Mandatos: 2016 (Dilma/Temer), 2019 e 2022 (Bolsonaro), 2025 (Lula III)."])

_i = [c[0] for c in CONS].index("34b") + 1
CONS[_i:_i] = [("34c", "Transferência de renda – Bolsa Família/Auxílio Brasil (pago)", "bf_pago"), ("34d", "BPC/LOAS (pago, RTN)", "bpc_aff"),
               ("34e", "Assistência estudantil – PNAES (pago)", "pnaes_pago"), ("34f", "Políticas afirmativas e de apoio – subtotal pago", "aff_sub"), ("34g", "Alimentação escolar – PNAE (repasse)", "pnae_rep"), ("34h", "Fies – impacto primário", "fies_prim"), ("34i", "ProUni – renúncia tributária", "prouni")]
# ---------------------------------------------------------------- consolidado
wc = wb["Indicadores consolidados"]
title(wc, "Indicadores consolidados – Brasil 2016 × 2019 × 2022 × 2025",
      "Valores vinculados às abas temáticas (texto verde). R$ bilhões correntes salvo indicação; correção pelo IPCA até dez/2025.")
CC = ["Código", "Indicador", "Conceito", "Âmbito", "Unidade", "Brasil 2016", "Brasil 2019", "Brasil 2022", "Brasil 2025",
      "2016 corrigido para preços de 2025", "2019 corrigido para preços de 2025", "2022 corrigido para preços de 2025",
      "Variação nominal 2019→2025", "Variação real 2016→2025", "Variação real 2019→2025", "Variação real 2022→2025",
      "2016 como % do PIB", "2019 como % do PIB", "2022 como % do PIB", "2025 como % do PIB",
      "Fonte 2016", "Fonte 2019", "Fonte 2022", "Fonte 2025", "Data de acesso", "Observações metodológicas"]
header(wc, 3, CC, [7, 36, 28, 14, 8, 12, 12, 12, 12, 12, 12, 12, 11, 11, 11, 11, 9, 9, 9, 9, 20, 20, 20, 20, 10, 60])
ALLR = {r["id"]: r for lst in ALL_LISTS + [AFF_ROWS] for r in lst}
for i, (cod, nome, rid) in enumerate(CONS):
    n = 4 + i
    sh, sr = LOC[rid]
    src = ALLR.get(rid)
    if src is None:
        un, conc, amb, tipo = "%", "VAB da atividade ÷ PIB", "Brasil", "ESTIMADO"
        fts = {y: "Cálculo sobre S01" for y in YEARS}; tys = {y: None for y in YEARS}
        obs = f"={q(sh)}!AB{sr}"
    else:
        un, conc, amb, tipo, obs = src["un"], src["conc"], src["amb"], src["tipo"], (src["obs"] or "—")
        fts = src["FT"]; tys = src["TY"]
        if conc in ("Dotação inicial (LOA)", "Empenhado", "Pago", "Liquidado", "Dotação atualizada"):
            conc = conc + " – " + src["ind"]
    for c, v in enumerate([cod, nome, conc, amb, un], 1):
        wc.cell(row=n, column=c, value=v)
    for y in YEARS:
        cell = wc[f"{YCOL[y]}{n}"]
        cell.value = f"={q(sh)}!{YCOL[y]}{sr}"; cell.font = F_LNK; cell.number_format = FMT.get(un, "#,##0.00")
    money = un in ("R$ bi", "R$ mi"); div = "/1000" if un == "R$ mi" else ""
    for y, col in ((2016, "J"), (2019, "K"), (2022, "L")):
        wc[f"{col}{n}"] = f'=IFERROR({YCOL[y]}{n}*FATOR_{y},"n.d.")' if money else ("n.a. (US$)" if un == "US$ bi" else "n.a.")
        wc[f"{col}{n}"].number_format = FMT["R$ bi"]
    if un in ("%", "% do PIB"):
        wc[f"M{n}"] = f'=IFERROR((I{n}-G{n})*100,"n.d.")'; wc[f"M{n}"].number_format = PP
    else:
        wc[f"M{n}"] = f'=IFERROR(I{n}/G{n}-1,"n.d.")'; wc[f"M{n}"].number_format = PCT
    for col, base in (("N", "J"), ("O", "K"), ("P", "L")):
        wc[f"{col}{n}"] = f'=IFERROR(I{n}/{base}{n}-1,"n.d.")' if money else "n.a."
        wc[f"{col}{n}"].number_format = PCT
    for j, y in enumerate(YEARS):
        col = get_column_letter(17 + j)
        if money:
            f = f'=IFERROR({YCOL[y]}{n}{div}/PIB_{y},"n.d.")'
        elif un == "US$ bi":
            f = f'=IFERROR({YCOL[y]}{n}/(PIB_{y}/PTAX_{y}),"n.d.")'
        elif un == "% do PIB":
            f = f'=IF(ISNUMBER({YCOL[y]}{n}),{YCOL[y]}{n},"n.d.")'
        else:
            f = "n.a."
        wc[f"{col}{n}"] = f; wc[f"{col}{n}"].number_format = PCT
    for j, y in enumerate(YEARS):
        wc.cell(row=n, column=21 + j, value=fts[y])
    wc.cell(row=n, column=25, value=ACESSO)
    wc.cell(row=n, column=26, value=(f"[{tipo}] " + obs) if not obs.startswith("=") else f'="[{tipo}] "&{obs[1:]}')
    for c in range(1, 27):
        cell = wc.cell(row=n, column=c)
        cell.border = BORDER; cell.fill = FILL[tipo]
        if c not in (6, 7, 8, 9):
            cell.font = F_TXT
        if c in (2, 3, 4) or c >= 21:
            cell.alignment = WRAP
    for y in YEARS:
        if tys[y] and tys[y] != tipo:
            wc[f"{YCOL[y]}{n}"].fill = FILL[tys[y]]
last_c = 4 + len(CONS) - 1
wc.auto_filter.ref = f"A3:Z{last_c}"
wc.freeze_panes = "C4"
footnotes(wc, last_c + 2, ["'Variação nominal 2019→2025' para taxas/percentuais = diferença em p.p.",
                           "Linhas de LOA: 'previsto' = dotação inicial; 'empenhado' e 'pago' são estágios de execução – não somar.",
                           "A classificação do dado aparece entre colchetes no início das observações e na cor da linha."])

# ---------------------------------------------------------------- resumo executivo
ws = wb["Resumo executivo"]
title(ws, "Relatório econômico-fiscal do Brasil – 2016 × 2019 × 2022 × 2025",
      f"Escopo nacional; contas públicas com prioridade à União/Governo Central. Dados acessados em {ACESSO}. Valores nominais do próprio ano; correção pelo IPCA até dez/2025.")
ws.column_dimensions["A"].width = 46
for col, w in zip("BCDEFGHI", (14, 14, 14, 14, 13, 13, 13, 44)):
    ws.column_dimensions[col].width = w
ws["A4"] = "Parâmetros de cálculo"; ws["A4"].font = F_BLD
for j, h in enumerate(["2016", "2019", "2022", "2025"]):
    c = ws.cell(row=4, column=2 + j, value=h); c.font = F_HDR; c.fill = HDR_FILL; c.alignment = Alignment(horizontal="center")
prow = [("PIB (R$ bi, IBGE SIDRA 1846)", "PIB", lambda y: PIB[y], '#,##0.0'),
        ("IPCA número-índice de dezembro (SIDRA 1737)", "IPCA_DEZ", lambda y: IPCA[y], '#,##0.00'),
        ("Fator IPCA dez/ano → dez/2025", "FATOR", lambda y: f"=IPCA_DEZ_2025/IPCA_DEZ_{y}", '0.0000'),
        ("PTAX média anual (R$/US$, média das médias mensais – BCB SGS 3698)", "PTAX", lambda y: "=AVERAGE(" + ",".join(str(x) for x in PTAX[y]) + ")", '0.0000'),
        ("PIB em US$ bi", None, lambda y: f"=PIB_{y}/PTAX_{y}", '#,##0.0')]
for i, (lab, nm, fn, fmt) in enumerate(prow):
    n = 5 + i
    ws.cell(row=n, column=1, value=lab).font = F_TXT
    ws.cell(row=n, column=1).border = BORDER
    for j, y in enumerate(YEARS):
        c = ws.cell(row=n, column=2 + j, value=fn(y))
        c.font = F_TXT if isinstance(c.value, str) else F_INP
        c.number_format = fmt; c.border = BORDER
        if nm == "FATOR":
            c.fill = PatternFill("solid", fgColor="FFFF00")
        if nm:
            name = f"{nm}_{y}"
            wb.defined_names[name] = DefinedName(name, attr_text=f"'Resumo executivo'!${get_column_letter(2 + j)}${n}")
r0 = 5 + len(prow) + 1
ws.cell(row=r0, column=1, value="Principais indicadores").font = F_BLD
hdr = ["Indicador", "2016", "2019", "2022", "2025", "Var. real 2016→2019", "Var. real 2019→2022", "Var. real 2022→2025", "Leitura"]
for i, h in enumerate(hdr, 1):
    c = ws.cell(row=r0 + 1, column=i, value=h); c.font = F_HDR; c.fill = HDR_FILL; c.border = BORDER
    c.alignment = Alignment(wrap_text=True, horizontal="center")
KEY = [
 ("PIB (R$ bi)", "pib", "Recessão 2015–16, pandemia em 2020 e recuperação desde 2021."),
 ("Participação da agropecuária no PIB", "sh_agro", "Ganho contínuo de peso relativo."),
 ("Participação da indústria no PIB", "sh_ind", "Salto em 2022 puxado pela extrativa (petróleo)."),
 ("Participação dos serviços financeiros no PIB", "sh_fin", ""),
 ("Participação dos serviços não financeiros no PIB", "sh_nfin", "Perde participação ao longo do período."),
 ("Receita líquida do Governo Central (R$ bi)", "recliq", ""),
 ("Despesa primária do Governo Central (R$ bi)", "desprim", "Teto de gastos (2017–2022) × arcabouço (2024–)."),
 ("Resultado primário do Governo Central (R$ bi)", "resprim", "Déficit em 2016 e 2019, superávit em 2022, déficit em 2025."),
 ("Juros nominais – setor público consolidado (R$ bi)", "jurosliq", "Selic: 14,25% (2016) → 4,5% (2019) → 13,75% (2022) → 15% (2025)."),
 ("Dívida Bruta do Governo Geral (% PIB, BCB)", "dbgg_pib", ""),
 ("Dívida Líquida do Setor Público (% PIB, BCB)", "dlsp_pib", ""),
 ("Investimentos federais pagos – RTN (R$ bi)", "inv_rtn", "Mínimo em 2022."),
 ("Desembolsos do BNDES (R$ bi)", "bndes_des", ""),
 ("Plano Safra (R$ bi, ciclo)", "safra_tot", "Ciclos agrícolas, não anos civis."),
 ("Saldo de empregos formais (pessoas)", "saldo", "Quebra Caged/Novo Caged em 2020."),
 ("Bolsa Família / Auxílio Brasil pago (R$ bi)", "bf_pago", "Auxílio Brasil em 2022; novo Bolsa Família em 2025."),
 ("Taxa média de desocupação", "desoc", ""),
 ("Exportações (US$ bi)", "exp", ""),
 ("Saldo comercial (US$ bi)", "saldo_bc", ""),
]
for i, (lab, rid, txt) in enumerate(KEY):
    n = r0 + 2 + i
    sh, sr = LOC[rid]
    un = ALLR[rid]["un"] if rid in ALLR else "%"
    ws.cell(row=n, column=1, value=lab)
    for j, y in enumerate(YEARS):
        c = ws.cell(row=n, column=2 + j, value=f"={q(sh)}!{YCOL[y]}{sr}")
        c.font = F_LNK
        c.number_format = PCT if un in ("%", "% do PIB") else FMT[un]
    for j, (a, b) in enumerate(PAIRS[:3]):
        ca, cb = get_column_letter(2 + YEARS.index(a)), get_column_letter(2 + YEARS.index(b))
        c = ws.cell(row=n, column=6 + j)
        if un.startswith("R$"):
            c.value = f'=IFERROR(({cb}{n}/FATOR_{b if b != 2025 else 2025})/({ca}{n}*FATOR_{a})*FATOR_{b if b != 2025 else 2025}/FATOR_{b if b != 2025 else 2025}-1,"n.d.")'
            c.value = f'=IFERROR(({cb}{n}*FATOR_{b})/({ca}{n}*FATOR_{a})-1,"n.d.")'
            c.number_format = PCT
        elif un in ("%", "% do PIB"):
            c.value = f'=IFERROR(({cb}{n}-{ca}{n})*100,"n.d.")'; c.number_format = PP
        else:
            c.value = f'=IFERROR({cb}{n}/{ca}{n}-1,"n.d.")'; c.number_format = PCT
    ws.cell(row=n, column=9, value=txt)
    for cc in range(1, 10):
        cell = ws.cell(row=n, column=cc); cell.border = BORDER
        if cc not in (2, 3, 4, 5):
            cell.font = F_TXT
        if cc in (1, 9):
            cell.alignment = WRAP
ws.cell(row=r0 + 2 + len(KEY), column=1, value="Para % e taxas, as colunas de variação trazem diferença em p.p.; para US$ e pessoas, variação nominal.").font = F_NOTE
r1 = r0 + 2 + len(KEY) + 2
ws.cell(row=r1, column=1, value="Legenda de cores (classificação do dado)").font = F_BLD
for i, (k, (col, desc)) in enumerate(TIPOS.items()):
    n = r1 + 1 + i
    c = ws.cell(row=n, column=1, value=k); c.fill = FILL[k]; c.font = F_BLD; c.border = BORDER
    ws.cell(row=n, column=2, value=desc).font = F_TXT
    ws.merge_cells(start_row=n, start_column=2, end_row=n, end_column=9)
r2 = r1 + 1 + len(TIPOS) + 1
ws.cell(row=r2, column=1, value="Síntese das principais diferenças 2016 × 2019 × 2022 × 2025").font = F_BLD
for i, t in enumerate([x for x in open(sys.argv[2], encoding="utf-8").read().strip().split("\n") if x.strip()]):
    n = r2 + 1 + i
    c = ws.cell(row=n, column=1, value=t)
    c.font = F_BLD if t.startswith("■") else F_TXT
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=n, start_column=1, end_row=n, end_column=9)
    ws.row_dimensions[n].height = 15 if t.startswith("■") else max(15, 13 * (len(t) // 170 + 1))
ws.freeze_panes = "A4"

# ---------------------------------------------------------------- fontes
wf = wb["Fontes e metodologia"]
title(wf, "Fontes e metodologia", f"Todas as fontes consultadas em {ACESSO}. Confiabilidade: Alta = fonte oficial primária ou reprodução fiel; Média = imprensa/entidade setorial ou anúncio.")
FC = ["ID", "Título da fonte", "Instituição", "URL", "Data da publicação", "Ano de referência", "Indicador utilizado", "Página ou tabela", "Observações", "Nível de confiabilidade"]
header(wf, 3, FC, [6, 40, 26, 50, 16, 14, 34, 22, 60, 16])
FONTES_ADJ = []
for row in FONTES:
    row = list(row)
    if row[0] in ("S01", "S03", "S04", "S05", "S06", "S07", "S08", "S18", "S22"):
        row[5] = row[5].replace("2019 e 2025", "2016, 2019, 2022 e 2025").replace("dez/2019 e dez/2025", "dez/2016, 2019, 2022 e 2025")
        row[3] = row[3].replace("an_exercicio=2025", "an_exercicio={ano}") if row[0] in ("S05", "S06") else row[3]
    FONTES_ADJ.append(row)
for i, row in enumerate(FONTES_ADJ):
    n = 4 + i
    for c, v in enumerate(row, 1):
        cell = wf.cell(row=n, column=c, value=v)
        cell.font = F_TXT; cell.border = BORDER; cell.alignment = WRAP
        if c == 4 and v.startswith("http"):
            cell.hyperlink = v.replace("{ano}", "2025"); cell.font = Font(name=ARIAL, size=9, color="0563C1", underline="single")
    fill = FILL["OFICIAL"] if row[9].startswith("Alta") else FILL["IMPRENSA/SETORIAL"]
    for c in range(1, 11):
        wf.cell(row=n, column=c).fill = fill
lastf = 4 + len(FONTES_ADJ) - 1
wf.auto_filter.ref = f"A3:J{lastf}"
wf.freeze_panes = "B4"
n = lastf + 2
wf.cell(row=n, column=1, value="Dados não localizados ou só aproximados – tentativas de busca").font = F_BLD
for j, h in enumerate(["Item", "Fontes tentadas", "Resultado / tratamento"]):
    c = wf.cell(row=n + 1, column=[2, 4, 9][j], value=h); c.font = F_HDR; c.fill = HDR_FILL
for i, (a, b, c_) in enumerate(TENTATIVAS):
    m = n + 2 + i
    for col, v in ((2, a), (4, b), (9, c_)):
        cell = wf.cell(row=m, column=col, value=v); cell.font = F_TXT; cell.alignment = WRAP; cell.fill = FILL["NÃO LOCALIZADO"]
n = n + 2 + len(TENTATIVAS) + 1
wf.cell(row=n, column=1, value="Regras metodológicas aplicadas").font = F_BLD
REGRAS = [
 "Fluxos anuais nunca são somados a estoques (DPF, DBGG, DLSP, estoque de emprego).",
 "Previsão orçamentária (dotação) separada da execução (empenho, liquidação, pagamento).",
 "Juros (GND 2), amortização (GND 6) e refinanciamento em linhas próprias.",
 "DPF (União) separada da DBGG (Governo Geral) e da DLSP (setor público consolidado).",
 "Desembolsos do BNDES não tratados como despesa da LOA.",
 "Investimentos privados: anunciados, aprovados e realizados em linhas distintas.",
 "Plano Safra por ciclo agrícola (jul–jun), que não coincide com o ano civil.",
 "Emprego: estoque em 31/dez; fluxos acumulados no ano; quebra Caged → Novo Caged em 2020.",
 "PIB em valores correntes e VAB por atividade; atividades financeiras separadas.",
 "Divergências entre fontes registradas nas observações (ex.: primário 2022 original × série atual; exportações 2019; IDP 2019; desocupação).",
 "IPCA dez/ano → dez/2025: 2016 ≈ 1,5502; 2019 ≈ 1,3915; 2022 ≈ 1,1435. Não se aplica a US$, pessoas ou taxas.",
 "Séries oficiais (SIDRA, RTN, RREO/Siconfi, BCB/SGS, Comex Stat) foram consultadas na versão atual (revisada), o que pode diferir das divulgações originais de 2016 e 2022.",
 "Limitação: páginas gov.br de MCTI, Casa Civil e MIR fora do ar em 22/09/2026 (legislação eleitoral).",
]
for i, t in enumerate(REGRAS, 1):
    wf.cell(row=n + i, column=1, value=f"{i}. {t}").font = F_NOTE

for w in wb.worksheets:
    w.sheet_view.zoomScale = 90
    for row in w.iter_rows():
        for cell in row:
            if type(cell).__name__ == "MergedCell":
                continue
            if cell.font is None or cell.font.name != ARIAL:
                f = cell.font
                cell.font = Font(name=ARIAL, size=f.size or 9, bold=f.bold, italic=f.italic, color=f.color)
    w.page_setup.orientation = "landscape"
    w.sheet_properties.pageSetUpPr.fitToPage = True
    w.page_setup.fitToWidth = 1
    w.page_setup.fitToHeight = 0
wb.save(OUT)
print("ok", OUT)

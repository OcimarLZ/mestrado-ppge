p = 'build4.py'
s = open(p, encoding='utf-8').read()
assert "pnae_rep" not in s
anchor = '        RA("aff_sub", "PA.9",'
assert anchor in s
new_rows = '''        RA("pnae_rep", "PA.10", "Alimentação escolar – PNAE: recursos federais repassados", "Repasse do FNDE às redes estaduais, distrital e municipais", "União → subnacionais", "R$ bi",
           [3.42, 3.95, 3.56, 5.5], ["FNDE – Dados físicos e financeiros do PNAE (S45)"] * 3 + ["Orçamento estimado – MEC/Agência Gov (S45)"], "OFICIAL",
           "2016–2022: valores repassados (FNDE). 2025: orçamento estimado do programa (R$ 5,5 bi), não repasse apurado; em 2023 o repasse foi R$ 5,26 bi. Exclui a rede federal (R$ 10,8 mi, 22,2 mi e 34,1 mi pagos em 2016, 2019 e 2022).",
           [None, None, None, "ESTIMADO"]),
        RA("pnae_alu", "PA.10.1", "Alimentação escolar – PNAE: estudantes atendidos", "Alunos atendidos no ano", "Brasil", "milhões de famílias",
           [40.3, 40.2, 39.58, NL], ["FNDE (S45)"] * 3 + ["—"], "OFICIAL",
           "Unidade: milhões de estudantes (não famílias). 2025 não localizado (o FNDE informa 'cerca de 40 milhões')."),
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
'''
s = s.replace(anchor, new_rows + anchor, 1)
old = '("34f", "Políticas afirmativas e de apoio – subtotal pago", "aff_sub")]'
assert old in s
s = s.replace(old, '("34f", "Políticas afirmativas e de apoio – subtotal pago", "aff_sub"), ("34g", "Alimentação escolar – PNAE (repasse)", "pnae_rep"), ("34h", "Fies – impacto primário", "fies_prim"), ("34i", "ProUni – renúncia tributária", "prouni")]')
old = 'TENTATIVAS += [\n    ("Benefício médio do Bolsa Família em 2016 e 2019"'
assert old in s
s = s.replace(old, '''FONTES += [
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
    ("Benefício médio do Bolsa Família em 2016 e 2019"''', 1)
open(p, 'w', encoding='utf-8').write(s)
print("ok")

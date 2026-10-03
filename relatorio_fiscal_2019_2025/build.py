# -*- coding: utf-8 -*-
"""Gera o relatório econômico-fiscal Brasil 2019 x 2025 (xlsx)."""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.utils import get_column_letter

OUT = sys.argv[1]
ACESSO = "22/09/2026"

# ---------------------------------------------------------------- parâmetros
IPCA_DEZ19, IPCA_DEZ25 = 5320.25, 7403.29          # SIDRA 1737, v2266
PTAX19 = [3.7417, 3.7236, 3.8465, 3.8962, 4.0015, 3.8588, 3.7793, 4.0200, 4.1215, 4.0870, 4.1553, 4.1096]
PTAX25 = [6.0218, 5.7656, 5.7468, 5.7837, 5.6674, 5.5471, 5.5285, 5.4469, 5.3674, 5.3855, 5.3409, 5.4531]
PIB19, PIB25 = 7389.131, 12738.566                   # R$ bi, SIDRA 1846 (soma 4 tri)

# ---------------------------------------------------------------- estilos
ARIAL = "Arial"
F_TIT = Font(name=ARIAL, size=14, bold=True, color="1F3864")
F_SUB = Font(name=ARIAL, size=9, italic=True, color="595959")
F_HDR = Font(name=ARIAL, size=9, bold=True, color="FFFFFF")
F_TXT = Font(name=ARIAL, size=9)
F_INP = Font(name=ARIAL, size=9, color="0000FF")      # dado digitado (hardcode)
F_LNK = Font(name=ARIAL, size=9, color="008000")      # link para outra aba
F_BLD = Font(name=ARIAL, size=9, bold=True)
F_NOTE = Font(name=ARIAL, size=8, italic=True, color="404040")
HDR_FILL = PatternFill("solid", fgColor="1F3864")
TIPOS = {
    "OFICIAL": ("E2EFDA", "Dado oficial publicado (IBGE, BCB, Tesouro, RFB, MTE, MDIC, BNDES, MAPA/MDA, Siconfi, Portal da Transparência, Casa Civil)"),
    "ESTIMADO": ("FFF2CC", "Estimativa/projeção oficial ou cálculo próprio a partir de dados oficiais (soma, diferença, % aplicado ao PIB)"),
    "APROXIMAÇÃO": ("DDEBF7", "Aproximação: período, conceito ou recorte diferente do solicitado (explicado na observação)"),
    "IMPRENSA/SETORIAL": ("FCE4D6", "Cifra obtida via imprensa ou entidade setorial (Abdib, Inesc etc.), sem acesso direto à base oficial"),
    "NÃO LOCALIZADO": ("D9D9D9", "Não localizado após busca — tentativas registradas na aba 'Fontes e metodologia'"),
}
FILL = {k: PatternFill("solid", fgColor=v[0]) for k, v in TIPOS.items()}
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
NL = "não localizado após busca"

FMT = {
    "R$ bi": '#,##0.00;[Red]-#,##0.00',
    "R$ mi": '#,##0.00;[Red]-#,##0.00',
    "US$ bi": '#,##0.00;[Red]-#,##0.00',
    "%": '0.00%',
    "% do PIB": '0.00%',
    "pessoas": '#,##0;[Red]-#,##0',
    "milhões de pessoas": '#,##0.0',
}
PCT = '0.00%;[Red]-0.00%'
PP = '0.00" p.p.";[Red]-0.00" p.p."'

# ---------------------------------------------------------------- fontes
# (id, título, instituição, url, data publicação, ano ref, indicador, página/tabela, observações, confiabilidade)
FONTES = [
 ("S01", "Contas Nacionais Trimestrais – Tabela 1846 (valores correntes)", "IBGE / SIDRA", "https://apisidra.ibge.gov.br/values/t/1846/n1/all/v/all/p/201901,201902,201903,201904,202501,202502,202503,202504/c11255/all", "Série consultada em 22/09/2026 (divulgação 2º tri/2026)", "2019 e 2025", "PIB, VAB por atividade, FBCF", "Tabela 1846 – soma dos 4 trimestres", "Valores anuais obtidos pela soma dos trimestres a preços correntes; série sujeita a revisão.", "Alta"),
 ("S02", "PIB cresce 2,3% em 2025 e fecha o ano em R$ 12,7 trilhões", "IBGE – Agência de Notícias", "https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/45968-pib-cresce-2-3-em-2025-e-fecha-o-ano-em-r-12-7-trilhoes", "03/2026", "2025", "PIB 2025 (divulgação original)", "Release", "Divulgação original R$ 12,7 tri; SIDRA atual = R$ 12.738,6 bi (revisão).", "Alta"),
 ("S03", "IPCA – número-índice (Tabela 1737, v. 2266)", "IBGE / SIDRA", "https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/2266/p/201912,202512", "Consulta 22/09/2026", "dez/2019 e dez/2025", "Fator de correção IPCA", "Tabela 1737", "Índice dez/2019 = 5.320,25; dez/2025 = 7.403,29.", "Alta"),
 ("S04", "Resultado do Tesouro Nacional – Séries históricas (serie_historica_dez25.xlsx)", "Tesouro Nacional (STN)", "https://www.tesourotransparente.gov.br/publicacoes/boletim-resultado-do-tesouro-nacional-rtn/2025/12", "29/01/2026", "1997–2025", "Receitas, despesas primárias, juros e resultado nominal do Governo Central; investimentos por função", "Tabelas 2.1, 2.1-A e 2.3", "Receita/despesa pelo critério caixa (acima da linha); juros e nominal apurados pelo BCB (abaixo da linha).", "Alta"),
 ("S05", "RREO da União – Anexo 01 (Balanço Orçamentário), 6º bimestre", "Tesouro Nacional – API Siconfi", "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo?an_exercicio=2025&nr_periodo=6&co_tipo_demonstrativo=RREO&no_anexo=RREO-Anexo%2001&co_esfera=U&id_ente=1", "Jan/2020 e jan/2026", "2019 e 2025", "Dotação inicial/atualizada, empenho, liquidação, pagamento por GND; refinanciamento", "RREO Anexo 01", "Orçamentos Fiscal e da Seguridade Social. 'Pago' = pagamentos do exercício (não inclui restos a pagar).", "Alta"),
 ("S06", "RREO da União – Anexo 02 (Despesa por Função/Subfunção), 6º bimestre", "Tesouro Nacional – API Siconfi", "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo?an_exercicio=2025&nr_periodo=6&co_tipo_demonstrativo=RREO&no_anexo=RREO-Anexo%2002&co_esfera=U&id_ente=1", "Jan/2020 e jan/2026", "2019 e 2025", "Saúde, educação, segurança, previdência, C&T, direitos da cidadania, transporte, saneamento, urbanismo", "RREO Anexo 02", "Anexo não traz 'pago'; pagamentos por função vêm do Portal da Transparência (S07). Exclui despesas intra-orçamentárias.", "Alta"),
 ("S07", "Portal da Transparência – Funções e Programas orçamentários", "CGU – Portal da Transparência", "https://portaldatransparencia.gov.br/funcoes/10-saude?ano=2019", "Consulta 22/09/2026", "2019 e 2025", "Valor pago por função; programas 2034 (2019) e 5804 (2025)", "Páginas /funcoes/{código}?ano= e /programas-e-acoes/programa-orcamentario/...", "'Valor pago' do Portal inclui pagamentos de restos a pagar no ano e usa base de dados própria (SIAFI), podendo divergir do RREO.", "Alta"),
 ("S08", "SGS – séries 13761/13762 (DBGG), 4478/4513 (DLSP), 5727 (NFSP nominal), 22885 (IDP), 3698 (PTAX média mensal)", "Banco Central do Brasil", "https://api.bcb.gov.br/dados/serie/bcdata.sgs.13761/dados?formato=json", "Consulta 22/09/2026", "dez/2019 e dez/2025", "Dívida bruta, dívida líquida, NFSP, IDP, câmbio", "SGS", "Estoques em dezembro; %PIB calculado pelo BCB com PIB acumulado 12 meses (valorizado).", "Alta"),
 ("S09", "Contas públicas têm déficit primário de R$ 61,872 bi em 2019", "Agência Brasil (dados BCB)", "https://agenciabrasil.ebc.com.br/economia/noticia/2020-01/contas-publicas-tem-deficit-primario-de-r-61872-bi-em-2019", "31/01/2020", "2019", "Resultado primário e juros nominais do setor público consolidado", "Notícia", "Juros 2019 = R$ 367,282 bi (5,06% do PIB pela série de PIB da época).", "Alta (reproduz BCB)"),
 ("S10", "Estatísticas fiscais – dezembro de 2025 / Juro da dívida e déficit nominal 2025", "BCB via Poder360 e CNN Brasil", "https://www.poder360.com.br/poder-economia/juro-da-divida-bate-recorde-e-deficit-nominal-supera-r-1-trilhao/", "30/01/2026", "2025", "Juros nominais e resultado nominal/primário do setor público consolidado", "Notícia + nota do BCB", "Juros 2025 = R$ 1.007,6 bi (7,91% PIB); nominal = −R$ 1.062,6 bi; primário = −R$ 55,0 bi.", "Alta (reproduz BCB)"),
 ("S11", "Dívida Pública Federal: RMD dez/2019 e dez/2025", "Tesouro Nacional (via Ministério da Economia/Fazenda)", "https://www.gov.br/fazenda/pt-br/assuntos/noticias/2026/janeiro/divida-publica-encerra-2025-em-r-8-635-trilhoes-dentro-dos-limites-projetados-aponta-tesouro", "28/01/2020 e 28/01/2026", "2019 e 2025", "Estoque da DPF e DPMFi", "Relatório Mensal da Dívida", "2019: DPF R$ 4,248 tri (Agência Brasil arredonda para 4,249); 2025: R$ 8,635 tri.", "Alta"),
 ("S12", "Arrecadação federal 2019 e 2025", "Receita Federal (via Agência Brasil / gov.br)", "https://www.gov.br/receitafederal/pt-br/assuntos/noticias/2026/janeiro/arrecadacao-de-receitas-federais-alcanca-r-2-886-trilhoes-em-2025", "23/01/2020 e 22/01/2026", "2019 e 2025", "Arrecadação das receitas federais", "Nota de arrecadação", "Total inclui receitas administradas pela RFB e por outros órgãos (royalties etc.).", "Alta"),
 ("S13", "Orçamento de Subsídios da União (OSU) – 4ª edição (ref. 2019)", "Ministério da Economia", "https://www.gov.br/economia/pt-br/assuntos/noticias/2020/julho/subsidios-concedidos-pela-uniao-atingem-r-348-3-bilhoes-em-2019", "14/07/2020", "2019", "Subsídios tributários, financeiros e creditícios", "Relatório OSU", "Total R$ 348,3 bi (4,8% PIB); 88,5% tributários, 11,5% financeiros+creditícios.", "Alta"),
 ("S14", "Nota Técnica Conjunta CONOF/CD e CONORF/SF – PLOA 2026", "Câmara dos Deputados / Senado Federal", "https://www12.senado.leg.br/orcamento/documentos/estudos/tipos-de-estudos/notas-tecnicas-e-informativos/notatecnicaconjunta_ploa-2026_.pdf", "09/2025", "2025–2026", "Gastos tributários 2025 (DGT Bases Efetivas e PLOA 2025); benefícios financeiros e creditícios 2025", "p. 11, 41–43 e 93–94", "Gastos tributários 2026 = R$ 612,8 bi, +R$ 68,4 bi sobre PLOA 2025 e +R$ 25,4 bi sobre a última projeção de 2025 (DGT Bases Efetivas) ⇒ 544,4 e 587,4. Benefícios fin./cred. 2025 estimados em R$ 172,5 bi.", "Alta (estimativas oficiais)"),
 ("S15", "Novo Caged – apresentação dez/2025 e notícia MTE", "Ministério do Trabalho e Emprego", "https://www.gov.br/trabalho-e-emprego/pt-br/noticias-e-conteudo/2026/janeiro/novo-caged-brasil-encerra-2025-com-saldo-positivo-de-1-27-milhao-de-empregos-formais", "29/01/2026", "2025", "Admissões, desligamentos, saldo e estoque", "Apresentação p. 8", "Estoque dez/2025: 48.474.348 (excl. estatutários RAIS) e 49.090.182 (total recuperado).", "Alta"),
 ("S16", "Caged 2019 (sistema antigo)", "Ministério da Economia (via Agência Brasil)", "https://agenciabrasil.ebc.com.br/economia/noticia/2020-01/caged-pais-gerou-644-mil-novas-vagas-de-trabalho-em-2019", "24/01/2020", "2019", "Admissões, desligamentos, saldo e estoque", "Notícia/sumário executivo", "Caged antigo (declaração do empregador); não é diretamente comparável ao Novo Caged (eSocial, desde 2020).", "Alta"),
 ("S17", "PNAD Contínua – taxa anual de desocupação 2019 e 2025; Tabela 4099", "IBGE", "https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/45759-pnad-continua-em-2025-taxa-anual-de-desocupacao-foi-de-5-6-enquanto-taxa-de-subutilizacao-foi-14-5", "02/2020 e 02/2026", "2019 e 2025", "Taxa média anual de desocupação", "Releases + SIDRA 4099", "Publicado: 11,9% (2019) e 5,6% (2025). Média dos 4 trimestres na série atual do SIDRA: 12,0% e 5,9%.", "Alta"),
 ("S18", "Comex Stat – API geral (FOB)", "MDIC / Secex", "https://api-comexstat.mdic.gov.br/general", "Consulta 22/09/2026", "2019 e 2025", "Exportações e importações (US$ FOB)", "Consulta geral anual", "Série revisada: 2019 exp. 221,13 / imp. 185,93. Divulgação original (jan/2020): 224,01 / 177,34.", "Alta"),
 ("S19", "Exportações brasileiras alcançam US$ 349 bi em 2025", "MDIC", "https://www.gov.br/mdic/pt-br/assuntos/noticias/2026/janeiro/exportacoes-brasileiras-alcancam-us-349-bi-em-2025-e-batem-recorde-historico", "01/2026", "2025", "Balança comercial 2025 (divulgação)", "Nota", "Divulgação: exp. 348,7; imp. 280,4; saldo 68,3 (API atual: 348,28 / 280,21).", "Alta"),
 ("S20", "BNDES – desempenho 2019 e balanço 2025", "BNDES (via Agência Brasil / Estado de Minas)", "https://agenciabrasil.ebc.com.br/economia/noticia/2026-03/injecao-do-bndes-na-economia-equivale-r-1-bilhao-por-dia-em-2025", "03/2020 e 03/2026", "2019 e 2025", "Desembolsos, aprovações, consultas, garantias", "Notícias com dados do BNDES", "2019: desembolsos 55,314; aprovações 63,077. 2025: desembolsos 169,7; aprovações 237,9; garantias 128,2.", "Alta (reproduz BNDES)"),
 ("S21", "Plano Safra 2019/2020 e 2025/2026", "MAPA / MDA", "https://www.gov.br/agricultura/pt-br/assuntos/noticias/governo-federal-lanca-plano-safra-2025-2026-com-r-516-2-bilhoes-para-impulsionar-o-agro-brasileiro", "06/2019 e 07/2025", "Ciclos 2019/20 e 2025/26", "Recursos anunciados", "Notas oficiais", "Valores anunciados (disponibilidade de crédito), não contratados. Ciclo jul–jun.", "Alta"),
 ("S22", "World Bank WDI – GB.XPD.RSDV.GD.ZS (fonte primária: MCTI/UNESCO)", "Banco Mundial / UNESCO-UIS", "https://api.worldbank.org/v2/country/BRA/indicator/GB.XPD.RSDV.GD.ZS?format=json&date=2018:2024", "Atualizado 13/07/2026", "2019 e 2023", "Dispêndio nacional em P&D (% PIB)", "WDI", "Páginas do MCTI inacessíveis (período eleitoral). 2019 = 1,151%; 2023 = 1,194% (último disponível).", "Alta (série internacional oficial)"),
 ("S23", "Novo PAC – execução orçamentária 2025", "Casa Civil (via Agência Gov)", "https://agenciagov.ebc.com.br/noticias/202601/novo-pac-alcanca-execucao-orcamentaria-total-em-2025-e-consolida-desempenho-financeiro-expressivo", "01/2026", "2025", "Dotação e empenho OGU do Novo PAC", "Notícia", "Dotação 2025 R$ 49,8 bi com 100% empenhado; pagamentos OGU 2023–2025 acumulados R$ 117,7 bi. Página hoje fora do ar (legislação eleitoral) – dado obtido do resumo do buscador.", "Média"),
 ("S24", "Abdib – investimentos em infraestrutura 2019 e 2025", "Abdib (via Conjur, CNN Brasil e site Abdib)", "https://conjur.com.br/2026-abr-05/investimento-privado-na-infraestrutura-bate-recorde-em-2025/", "12/2020 e 04/2026", "2019 e 2025", "Investimento total em infraestrutura por setor", "Livro Azul / notícias", "Entidade setorial privada; cifras de todas as esferas e do setor privado. 2019: R$ 123,9 bi; 2025: R$ 280 bi (R$ 235 bi privados).", "Média (entidade setorial)"),
 ("S25", "Relatório Inesc/MIR 2025 – orçamento da igualdade racial", "Inesc / Alma Preta", "https://almapreta.com.br/sessao/politica/governo-orcamento-igualdade-racial-monitoramento-desafio/", "2026", "2025", "Orçamento do Ministério da Igualdade Racial e agenda transversal", "Notícia", "MIR: autorizado R$ 139,32 mi, executado R$ 137,08 mi; agenda transversal R$ 674,71 mi autorizados, R$ 548,32 mi empenhados.", "Média (imprensa/ONG)"),
 ("S26", "Nova Indústria Brasil completa 1 ano com R$ 3,4 trilhões", "MDIC", "https://www.gov.br/mdic/pt-br/assuntos/noticias/2025/fevereiro/nib-completa-1-ano-com-r-3-4-trilhoes-de-investimentos-e-crescimento-industrial", "12/02/2025", "2024–2025 (anúncios plurianuais)", "Investimentos privados anunciados na indústria", "Nota", "R$ 2,2 tri anunciados pelo setor privado (horizonte plurianual) + R$ 1,2 tri federais. Não é execução anual.", "Média (anúncio)"),
 ("S27", "IDP 2019 (divulgação original) e 2025", "BCB (via IstoÉ Dinheiro e Poder360)", "https://www.poder360.com.br/poder-economia/investimento-direto-soma-us-777-bi-em-2025-maior-em-7-anos/", "01/2020 e 01/2026", "2019 e 2025", "Investimento direto no país", "Notícias", "Original 2019: US$ 78,559 bi; série atual SGS 22885: US$ 69,17 bi (revisão metodológica).", "Alta (reproduz BCB)"),
 ("S28", "Déficit primário do Governo Central de 2019 e 2025", "Agência Brasil (dados STN)", "https://agenciabrasil.ebc.com.br/economia/noticia/2026-01/deficit-primario-do-governo-central-totaliza-r-617-bilhoes-em-2025", "01/2020 e 01/2026", "2019 e 2025", "Resultado primário e compensações da meta", "Notícias", "2025: déficit R$ 61,69 bi; excluídas compensações autorizadas (R$ 48,68 bi) ⇒ R$ 13 bi (0,1% PIB).", "Alta (reproduz STN)"),
]

TENTATIVAS = [
 ("Investimentos do PAC pagos em 2019", "Boletim RTN dez/2019 (PDF thot 31547 – conteúdo não extraível), TCU Contas do Governo 2019 (página sem cifra do PAC), buscas Contas Abertas/Agência Brasil/Ipea", "Não foi localizada cifra anual oficial de PAC pago em 2019 (o PAC deixou de ter marcador próprio nas estatísticas do RTN após 2019)."),
 ("P&D realizado em 2025", "MCTI (indicadores 1.1.3 e 2.1.3 – páginas bloqueadas 'Conteúdo restrito' durante período eleitoral), Ipea/CTS, World Bank WDI", "Último dado nacional publicado = 2023 (1,19% PIB). Usado como aproximação."),
 ("Investimento privado industrial anunciado em 2019", "MDIC, Renai, CNI, imprensa", "Não há levantamento anual comparável em 2019 (a NIB e seu painel de anúncios começaram em 2024)."),
 ("Gastos tributários efetivos (realizados) de 2025", "Receita Federal – DGT Bases Efetivas (último publicado não cobre 2025 como realizado), nota técnica PLOA 2026", "Usada a última projeção oficial para 2025 (estimativa)."),
 ("Dotação inicial (LOA) do programa de igualdade racial", "Portal da Transparência (exibe apenas orçamento atualizado), Inesc", "Apresentado o orçamento atualizado como 'previsto'."),
 ("Pagamentos do Novo PAC no ano de 2025", "Casa Civil (páginas fora do ar por legislação eleitoral), Agência Gov", "Disponível apenas o acumulado 2023–2025 (R$ 117,7 bi) e a dotação/empenho de 2025."),
 ("Abdib – investimento privado em 2019 e rodovias/ferrovias/portos/aeroportos separadamente", "Site Abdib, Conjur, CNN, Exame", "Só foram localizados totais por macrossetor (transporte e logística; saneamento; energia; telecom)."),
]

# ---------------------------------------------------------------- dados (R$ bi, salvo indicação)
# campos: id, cod, indicador, conceito, ambito, unidade, v19, v25, fonte19, fonte25, tipo, obs
def R(id, cod, ind, conc, amb, un, v19, v25, f19, f25, tipo, obs):
    return dict(id=id, cod=cod, ind=ind, conc=conc, amb=amb, un=un, v19=v19, v25=v25, f19=f19, f25=f25, tipo=tipo, obs=obs)

SIDRA = "IBGE/SIDRA 1846 (S01)"
PIB_ROWS = [
 R("pib", "1", "PIB total", "PIB a preços de mercado, valores correntes (fluxo anual)", "Brasil", "R$ bi", 7389.131, 12738.566, SIDRA, SIDRA, "OFICIAL", "Soma dos 4 trimestres. Divulgação original de 2025: R$ 12,7 tri (S02); Tesouro usa R$ 12.733,6 bi (série anterior)."),
 R("vab", "1.1", "Valor adicionado bruto (VAB) a preços básicos", "Soma do VAB das atividades", "Brasil", "R$ bi", 6356.683, 10951.982, SIDRA, SIDRA, "OFICIAL", "Base para participações setoriais usadas pelo IBGE."),
 R("imp", "1.2", "Impostos líquidos sobre produtos", "PIB − VAB", "Brasil", "R$ bi", 1032.447, 1786.584, SIDRA, SIDRA, "OFICIAL", ""),
 R("agro", "2", "PIB da agropecuária (VAB)", "VAB – Agropecuária total", "Brasil", "R$ bi", 310.714, 775.297, SIDRA, SIDRA, "OFICIAL", ""),
 R("ind", "3", "PIB da indústria (VAB)", "VAB – Indústria total", "Brasil", "R$ bi", 1385.804, 2566.814, SIDRA, SIDRA, "OFICIAL", "Extrativa + transformação + eletricidade/gás/água/esgoto + construção."),
 R("extr", "3.1", "Indústrias extrativas", "VAB", "Brasil", "R$ bi", 182.817, 403.599, SIDRA, SIDRA, "OFICIAL", ""),
 R("transf", "3.2", "Indústrias de transformação", "VAB", "Brasil", "R$ bi", 763.482, 1499.618, SIDRA, SIDRA, "OFICIAL", ""),
 R("siup", "3.3", "Eletricidade e gás, água, esgoto e resíduos", "VAB", "Brasil", "R$ bi", 190.862, 260.230, SIDRA, SIDRA, "OFICIAL", ""),
 R("constr", "3.4", "Construção", "VAB", "Brasil", "R$ bi", 248.642, 403.368, SIDRA, SIDRA, "OFICIAL", ""),
 R("serv", "4", "PIB dos serviços (VAB)", "VAB – Serviços total", "Brasil", "R$ bi", 4660.166, 7609.870, SIDRA, SIDRA, "OFICIAL", ""),
 R("com", "4.1", "Comércio", "VAB", "Brasil", "R$ bi", 822.590, 1271.510, SIDRA, SIDRA, "OFICIAL", ""),
 R("transp", "4.2", "Transporte, armazenagem e correio", "VAB", "Brasil", "R$ bi", 284.471, 395.671, SIDRA, SIDRA, "OFICIAL", ""),
 R("info", "4.3", "Informação e comunicação", "VAB", "Brasil", "R$ bi", 218.876, 389.291, SIDRA, SIDRA, "OFICIAL", ""),
 R("fin", "5", "Atividades financeiras, de seguros e serviços relacionados", "VAB", "Brasil", "R$ bi", 460.292, 930.269, SIDRA, SIDRA, "OFICIAL", "Separadas dos demais serviços, conforme solicitado."),
 R("imob", "4.4", "Atividades imobiliárias", "VAB", "Brasil", "R$ bi", 619.584, 954.115, SIDRA, SIDRA, "OFICIAL", "Inclui aluguel imputado."),
 R("outros", "4.5", "Outras atividades de serviços", "VAB", "Brasil", "R$ bi", 1148.263, 1921.915, SIDRA, SIDRA, "OFICIAL", ""),
 R("adm", "4.6", "Administração, saúde e educação públicas e seguridade social", "VAB", "Brasil", "R$ bi", 1106.091, 1747.099, SIDRA, SIDRA, "OFICIAL", ""),
 R("nfin", "6", "PIB dos serviços não financeiros", "Serviços totais − atividades financeiras (cálculo)", "Brasil", "R$ bi", "=F{serv}-F{fin}", "=G{serv}-G{fin}", "Cálculo sobre S01", "Cálculo sobre S01", "ESTIMADO", "Calculado na planilha: VAB serviços − VAB financeiro (mesma fonte e conceito)."),
]
# participações (linhas especiais tratadas à parte)

REC_ROWS = [
 R("arrec", "8", "Arrecadação da União (receitas federais)", "Arrecadação total das receitas federais (RFB + outros órgãos), fluxo anual", "União", "R$ bi", 1537.0, 2886.0, "Receita Federal (S12)", "Receita Federal (S12)", "OFICIAL", "Valores publicados como R$ 1,537 tri (2019) e R$ 2,886 tri (2025), sem mais casas decimais. Conceito distinto da 'receita total' do RTN (caixa do Tesouro)."),
 R("rfb", "8.1", "Receitas administradas pela RFB (RTN)", "Caixa – Tesouro Nacional", "Governo Central", "R$ bi", 946.083, 1859.844, "STN – RTN tab. 2.1 (S04)", "STN – RTN tab. 2.1 (S04)", "OFICIAL", "Exclui arrecadação líquida do RGPS."),
 R("ir", "8.2", "Imposto de Renda", "Caixa", "Governo Central", "R$ bi", 398.370, 867.310, "S04", "S04", "OFICIAL", ""),
 R("cofins", "8.3", "Cofins", "Caixa", "Governo Central", "R$ bi", 238.700, 391.530, "S04", "S04", "OFICIAL", ""),
 R("csll", "8.4", "CSLL", "Caixa", "Governo Central", "R$ bi", 82.020, 177.800, "S04", "S04", "OFICIAL", ""),
 R("iof", "8.5", "IOF", "Caixa", "Governo Central", "R$ bi", 41.040, 86.380, "S04", "S04", "OFICIAL", "Alta de alíquotas do IOF em 2025."),
 R("rgps", "8.6", "Arrecadação líquida para o RGPS", "Caixa", "Governo Central", "R$ bi", 413.331, 709.714, "S04", "S04", "OFICIAL", ""),
 R("concess", "8.7", "Concessões e permissões", "Caixa – receita não administrada pela RFB", "Governo Central", "R$ bi", 93.280, 7.200, "S04", "S04", "OFICIAL", "2019 inclui leilão da cessão onerosa (receita extraordinária)."),
 R("divid", "8.8", "Dividendos e participações", "Caixa", "Governo Central", "R$ bi", 20.880, 49.800, "S04", "S04", "OFICIAL", ""),
 R("recnat", "8.9", "Receitas de exploração de recursos naturais", "Caixa (royalties/participação especial)", "Governo Central", "R$ bi", 64.680, 139.350, "S04", "S04", "OFICIAL", ""),
 R("rectot", "10", "Receita primária total do Governo Central", "Receita total (Tesouro + Previdência + BCB), caixa", "Governo Central", "R$ bi", 1635.608, 2902.275, "S04", "S04", "OFICIAL", ""),
 R("transfrep", "10.1", "Transferências por repartição de receita", "FPM/FPE, royalties etc.", "Governo Central → subnacionais", "R$ bi", 288.331, 569.716, "S04", "S04", "OFICIAL", ""),
 R("recliq", "10.2", "Receita líquida do Governo Central", "Receita total − transferências por repartição", "Governo Central", "R$ bi", 1347.277, 2332.558, "S04", "S04", "OFICIAL", ""),
 R("gtrib", "16", "Renúncias fiscais / gastos tributários", "2019: benefícios tributários efetivos (OSU). 2025: última projeção oficial (DGT Bases Efetivas)", "União", "R$ bi", 308.4, 587.4, "OSU 4ª ed. (S13)", "RFB via Nota Técnica PLOA 2026 (S14)", "ESTIMADO", "2025 é projeção (não realizado): 612,8 − 25,4 = 587,4 (4,40% PIB). Estimativa do PLOA 2025 = 544,4 (612,8 − 68,4). 2019 é valor efetivo. Divergência = diferença entre estimativa ex ante e apuração ex post."),
 R("bfc", "17", "Benefícios financeiros e creditícios", "Subsídios explícitos (financeiros) + implícitos (creditícios)", "União", "R$ bi", 40.05, 172.5, "OSU 4ª ed. (S13) – 11,5% × R$ 348,3 bi", "Estimativa do Executivo – PLOA 2026 (S14)", "ESTIMADO", "2019: 11,5% de R$ 348,3 bi (cálculo sobre dado oficial). 2025: estimativa do Poder Executivo, não apuração. Em 2024 (realizado, OSU 9ª ed.) financeiros+creditícios = 16,9% de R$ 678 bi ≈ R$ 114,6 bi — ordem de grandeza menor que a estimativa de 2025."),
 R("subtot", "16.1", "Subsídios da União – total (tributários + financeiros + creditícios)", "OSU", "União", "R$ bi", 348.3, "=G{gtrib}+G{bfc}", "OSU (S13)", "Soma de estimativas (S14)", "ESTIMADO", "2025 = soma das duas estimativas oficiais acima; não há OSU 2025 publicado."),
]

DESP_ROWS = [
 R("desprim", "11", "Despesa primária do Governo Central", "Despesa total primária (RTN), caixa", "Governo Central", "R$ bi", 1442.340, 2394.250, "STN – RTN tab. 2.1 (S04)", "S04", "OFICIAL", ""),
 R("prev_rtn", "11.1", "Benefícios previdenciários (RGPS)", "RTN, caixa", "Governo Central", "R$ bi", 626.510, 1026.870, "S04", "S04", "OFICIAL", ""),
 R("pessoal", "11.2", "Pessoal e encargos sociais", "RTN, caixa", "Governo Central", "R$ bi", 313.090, 402.550, "S04", "S04", "OFICIAL", ""),
 R("bpc", "11.3", "BPC/LOAS e RMV", "RTN, caixa", "Governo Central", "R$ bi", 59.730, 127.240, "S04", "S04", "OFICIAL", ""),
 R("abono", "11.4", "Abono e seguro-desemprego", "RTN, caixa", "Governo Central", "R$ bi", 55.590, 87.840, "S04", "S04", "OFICIAL", ""),
 R("fundeb", "11.5", "Complementação da União ao Fundeb", "RTN, caixa", "Governo Central", "R$ bi", 15.600, 59.730, "S04", "S04", "OFICIAL", "Novo Fundeb (EC 108/2020) ampliou a complementação."),
 R("precat", "11.6", "Sentenças judiciais e precatórios (custeio e capital)", "RTN, caixa", "Governo Central", "R$ bi", 15.480, 42.770, "S04", "S04", "OFICIAL", ""),
 R("discr", "11.7", "Despesas discricionárias do Executivo", "RTN, caixa", "Governo Central", "R$ bi", 164.420, 204.920, "S04", "S04", "OFICIAL", ""),
 R("resprim", "11.8", "Resultado primário do Governo Central", "Receita líquida − despesa primária (acima da linha)", "Governo Central", "R$ bi", -95.065, -61.690, "S04 / S28", "S04 / S28", "OFICIAL", "2025 sem as compensações autorizadas (R$ 48,68 bi); com elas o resultado para a meta foi −R$ 13 bi (0,1% PIB)."),
 R("jurosgc", "12.1", "Juros nominais do Governo Central", "Apropriados por competência (BCB, abaixo da linha)", "Governo Central", "R$ bi", 310.120, 891.880, "BCB via RTN tab. 2.1 linha 9 (S04)", "S04", "OFICIAL", ""),
 R("desptot", "12", "Despesa total do Governo Central (primária + juros nominais)", "Soma: despesa primária (caixa, STN) + juros nominais (competência, BCB)", "Governo Central", "R$ bi", "=F{desprim}+F{jurosgc}", "=G{desprim}+G{jurosgc}", "Cálculo S04", "Cálculo S04", "APROXIMAÇÃO", "Indicador sem publicação oficial única. Soma critérios diferentes (caixa × competência); usar apenas como ordem de grandeza. Ver também o déficit nominal oficial na linha seguinte."),
 R("nomgc", "12.2", "Resultado nominal do Governo Central", "BCB, abaixo da linha", "Governo Central", "R$ bi", -399.010, -950.570, "S04", "S04", "OFICIAL", ""),
 R("gastosu", "9", "Gastos da União – despesa paga (OFSS), sem refinanciamento", "Despesas pagas no exercício, exceto intra-orçamentárias; inclui juros e amortização", "União", "R$ bi", 2198.25, 3606.51, "RREO Anexo 01 (S05)", "S05", "OFICIAL", "Não inclui restos a pagar pagos nem refinanciamento da dívida."),
 R("gastosu_ref", "9.1", "Gastos da União – despesa paga com refinanciamento", "Total pago (inclui intra-orçamentárias e refinanciamento)", "União", "R$ bi", 2710.91, 5054.25, "S05", "S05", "OFICIAL", ""),
 R("loatot", "9.2", "LOA – dotação inicial total (com refinanciamento)", "Orçamentos Fiscal e da Seguridade Social", "União", "R$ bi", 3262.20, 5719.39, "S05", "S05", "OFICIAL", "Previsão ≠ execução."),
]

DIV_ROWS = [
 R("dpf", "13", "Dívida Pública Federal (DPF)", "Estoque em 31/dez (interna + externa)", "União", "R$ bi", 4248.0, 8635.0, "Tesouro – RMD (S11)", "S11", "OFICIAL", "Estoque; não somar com fluxos."),
 R("dpmfi", "13.1", "Dívida Pública Mobiliária Federal interna (DPMFi)", "Estoque em 31/dez", "União", "R$ bi", 4083.0, 8309.0, "S11", "S11", "OFICIAL", ""),
 R("dbgg", "14", "Dívida Bruta do Governo Geral (DBGG)", "Estoque em dez (União + estados + municípios; exclui BCB e estatais)", "Governo Geral", "R$ bi", 5500.10416, 10017.91914, "BCB SGS 13761 (S08)", "S08", "OFICIAL", "DBGG ≠ DPF: inclui dívida de estados/municípios e operações compromissadas do BCB; exclui títulos na carteira do BCB."),
 R("dbgg_pib", "14.1", "DBGG em % do PIB (BCB)", "Estoque/PIB 12 meses (BCB)", "Governo Geral", "% do PIB", 0.7444, 0.7864, "BCB SGS 13762 (S08)", "S08", "OFICIAL", "Imprensa arredondou 2025 para 78,7%."),
 R("dlsp", "15", "Dívida Líquida do Setor Público (DLSP)", "Estoque em dez (setor público consolidado, inclui BCB e estatais não financeiras)", "Setor público consolidado", "R$ bi", 4041.76878, 8311.08576, "BCB SGS 4478 (S08)", "S08", "OFICIAL", ""),
 R("dlsp_pib", "15.1", "DLSP em % do PIB (BCB)", "Estoque/PIB 12 meses (BCB)", "Setor público consolidado", "% do PIB", 0.5470, 0.6524, "BCB SGS 4513 (S08)", "S08", "OFICIAL", "Imprensa arredondou 2025 para 65,3%."),
 R("jurosorc", "18", "Juros nominais pagos – juros e encargos da dívida (orçamento)", "GND 2, valor pago no exercício (caixa)", "União", "R$ bi", 285.09, 363.47, "RREO Anexo 01 (S05)", "S05", "OFICIAL", "Pagamento orçamentário; difere dos juros apropriados (competência) do BCB. Não há estatística oficial de juros 'pagos' do setor público consolidado."),
 R("jurosliq", "19", "Juros nominais líquidos apropriados – setor público consolidado", "Competência, líquidos de juros ativos (BCB/NFSP)", "Setor público consolidado", "R$ bi", 367.282, 1007.6, "BCB via Agência Brasil (S09)", "BCB via Poder360 (S10)", "OFICIAL", "Governo Central (juros nominais BCB): 310,1 (2019) e 891,9 (2025) – ver aba Despesas. 2025 inclui ganho de R$ 105,9 bi com swaps cambiais (redutor)."),
 R("jurospib_pub", "19.1", "Juros nominais do setor público em % do PIB (publicado)", "BCB", "Setor público consolidado", "% do PIB", 0.0506, 0.0791, "S09", "S10", "OFICIAL", "2019 publicado com PIB anterior à revisão; com PIB atual equivale a 4,97%."),
 R("primsp", "19.2", "Resultado primário do setor público consolidado", "BCB, abaixo da linha", "Setor público consolidado", "R$ bi", -61.872, -55.021, "S09", "S10", "OFICIAL", ""),
 R("nomsp", "19.3", "Resultado nominal do setor público consolidado", "Primário − juros nominais", "Setor público consolidado", "R$ bi", "=F{primsp}-F{jurosliq}", -1062.6, "Cálculo sobre S09", "S10", "OFICIAL", "2019 calculado (primário + juros, mesmos conceitos BCB); 2025 publicado."),
 R("nfsp_pib", "19.4", "NFSP nominal em % do PIB (BCB)", "Déficit nominal acumulado 12 meses", "Setor público consolidado", "% do PIB", 0.0581, 0.0834, "BCB SGS 5727 (S08)", "S08", "OFICIAL", ""),
 R("amort", "20", "Amortizações da dívida (exceto refinanciamento)", "GND 6, pago no exercício", "União", "R$ bi", 275.69, 353.98, "RREO Anexo 01 (S05)", "S05", "OFICIAL", "Fluxo; não confundir com refinanciamento (rolagem com emissão de títulos)."),
 R("refin", "21", "Refinanciamento da dívida", "Amortização paga com recursos de emissão de títulos (rolagem)", "União", "R$ bi", 476.78, 1417.64, "RREO Anexo 01 (S05)", "S05", "OFICIAL", "Dotação inicial: 714,09 (2019) e 1.655,91 (2025)."),
 R("refin_dot", "21.1", "Refinanciamento – dotação inicial na LOA", "Previsão orçamentária", "União", "R$ bi", 714.09, 1655.91, "S05", "S05", "OFICIAL", "Previsão ≠ execução."),
 R("juros_dot", "18.1", "Juros e encargos – dotação inicial na LOA", "Previsão orçamentária", "União", "R$ bi", 378.90, 480.01, "S05", "S05", "OFICIAL", ""),
]

def stages(prefix, cod, nome, amb, di, da, emp, liq, pago, fonte_pago, obs_pago, tipo_pago="OFICIAL", conc_extra=""):
    """Linhas LOA: dotação inicial, atualizada, empenhado, liquidado, pago."""
    rows = []
    lab = [("di", "Dotação inicial (LOA)"), ("da", "Dotação atualizada"), ("emp", "Empenhado"), ("liq", "Liquidado")]
    vals = [di, da, emp, liq]
    for (k, l), v in zip(lab, vals):
        rows.append(R(f"{prefix}_{k}", cod, nome, l + conc_extra, amb, "R$ bi", v[0], v[1], "RREO Anexo 02 (S06)" if prefix not in ("inv", "tot") else "RREO Anexo 01 (S05)", "RREO Anexo 02 (S06)" if prefix not in ("inv", "tot") else "RREO Anexo 01 (S05)", "OFICIAL", "Exclui intra-orçamentárias." if k == "di" else ""))
    if pago is not None:
        rows.append(R(f"{prefix}_pago", cod, nome, "Pago", amb, "R$ bi", pago[0], pago[1], fonte_pago, fonte_pago, tipo_pago, obs_pago))
    return rows

PORTAL_OBS = "Pago segundo o Portal da Transparência: inclui restos a pagar pagos no ano e classificação por função do Portal; pode divergir do RREO (critérios distintos)."

LOA_ROWS = (
 stages("tot", "9.3", "Despesa total da União (exceto intra-orçamentárias)", "União", (2504.68, 4028.70), (2556.50, 4144.73), (2331.13, 3901.65), (2255.45, 3705.42), (2198.25, 3606.51), "RREO Anexo 01 (S05)", "Pago no exercício; não inclui refinanciamento.") +
 stages("inv", "22–24", "Investimentos (GND 4)", "União", (36.12, 80.28), (45.44, 74.36), (42.44, 72.11), (16.61, 38.62), (16.37, 37.81), "RREO Anexo 01 (S05)", "Pago do exercício (sem RAP).") +
 [R("inv_rtn", "24.1", "Investimentos (GND 4)", "Pago total no ano, inclui restos a pagar (RTN)", "Governo Central", "R$ bi", 37.820, 69.923, "STN – RTN tab. 2.3 (S04)", "S04", "OFICIAL", "Conceito mais usado no debate fiscal: inclui pagamentos de RAP de anos anteriores."),
  R("inv_rtn_tot", "24.2", "Investimento total (GND 4 + inversões financeiras)", "Pago total no ano (RTN)", "Governo Central", "R$ bi", 56.593, 83.406, "S04", "S04", "OFICIAL", "")]
)

SOC_ROWS = (
 stages("sau", "25–26", "Saúde (função 10)", "União", (120.56, 232.87), (125.01, 239.62), (124.11, 238.64), (113.91, 217.07), (114.182, 234.280), "Portal da Transparência (S07)", PORTAL_OBS) +
 stages("edu", "27–28", "Educação (função 12)", "União", (103.03, 163.10), (104.57, 176.86), (101.30, 176.01), (88.22, 156.97), (94.474, 174.587), "Portal da Transparência (S07)", PORTAL_OBS) +
 stages("prev", "31–32", "Previdência Social (função 09)", "União", (733.92, 1085.59), (727.78, 1103.83), (726.13, 1103.11), (725.89, 1101.48), (668.956, 1126.374), "Portal da Transparência (S07)", PORTAL_OBS + " Em 2019 o pago do Portal (668,96) fica abaixo do liquidado do RREO (725,89): o Portal reclassifica parte dos benefícios; prefira o liquidado/RTN para comparação.") +
 stages("rgps", "31.1", "Previdência básica – RGPS (subfunção 271)", "União", (624.29, 980.82), (611.87, 991.36), (611.36, 991.34), (611.28, 990.18), None, "", "") +
 stages("rpps", "31.2", "Previdência do regime estatutário – RPPS (subfunção 272)", "União", (101.99, 97.86), (109.37, 105.21), (108.51, 104.61), (108.46, 104.50), None, "", "")
)

SEG_ROWS = (
 stages("seg", "29–30", "Segurança pública (função 06)", "União", (10.37, 15.62), (10.51, 16.88), (10.23, 16.58), (8.45, 13.89), (9.018, 15.410), "Portal da Transparência (S07)", PORTAL_OBS) +
 [R("pa_da", "33", "Políticas afirmativas – programa de igualdade racial", "Orçamento atualizado (proxy de 'previsto')", "União", "R$ mi", 12.908, 78.020, "Portal – Programa 2034 (S07)", "Portal – Programa 5804 (S07)", "APROXIMAÇÃO", "Programa 2034 'Promoção da Igualdade Racial e Superação do Racismo' (PPA 2016–19) × 5804 'Promoção da Igualdade Étnico-Racial, Combate e Superação do Racismo' (PPA 2024–27). Programas diferentes; dotação inicial não localizada."),
  R("pa_emp", "34a", "Políticas afirmativas – programa de igualdade racial", "Empenhado", "União", "R$ mi", 12.458, 77.486, "S07", "S07", "APROXIMAÇÃO", "Mesmo recorte da linha acima."),
  R("pa_liq", "34b", "Políticas afirmativas – programa de igualdade racial", "Liquidado", "União", "R$ mi", 5.937, 60.634, "S07", "S07", "APROXIMAÇÃO", ""),
  R("pa_pago", "34c", "Políticas afirmativas – programa de igualdade racial", "Pago no exercício (sem RAP)", "União", "R$ mi", 5.880, 58.026, "S07", "S07", "APROXIMAÇÃO", "RAP pagos no ano: 9,25 (2019) e 22,73 (2025)."),
  R("pa_mir", "34.1", "Ministério da Igualdade Racial – orçamento executado", "Executado (órgão)", "União", "R$ mi", NL, 137.08, "Órgão inexistente em 2019 (MIR criado em 2023)", "Inesc/Alma Preta (S25)", "IMPRENSA/SETORIAL", "Autorizado 2025: R$ 139,32 mi. 2019: não há órgão equivalente (SEPPIR estava no MMFDH)."),
  R("pa_transv", "34.2", "Agenda transversal de igualdade racial – empenhado", "63 ações em vários órgãos", "União", "R$ mi", NL, 548.32, "Sem agenda transversal marcada no PPA 2016–19", "Inesc/Alma Preta (S25)", "IMPRENSA/SETORIAL", "Autorizado 2025: R$ 674,71 mi."),
 ] +
 stages("cid", "33.1", "Direitos da cidadania (função 14) – recorte amplo", "União", (2.00, 2.79), (2.69, 2.33), (2.30, 2.26), (0.83, 1.35), (0.892, 1.486), "Portal da Transparência (S07)", PORTAL_OBS + " Função ampla: inclui povos indígenas, custódia (2019) e direitos individuais.")
)

BND_ROWS = [
 R("bndes_des", "35", "Desembolsos anuais do BNDES", "Fluxo de desembolsos do Sistema BNDES", "BNDES (fora da LOA)", "R$ bi", 55.314, 169.7, "BNDES via Estado de Minas/Agência Brasil (S20)", "BNDES via Agência Brasil (S20)", "OFICIAL", "Desembolsos do BNDES não são despesa da LOA (funding próprio, FAT, Tesouro)."),
 R("bndes_apr", "36", "Aprovações anuais do BNDES", "Operações de crédito aprovadas", "BNDES", "R$ bi", 63.077, 237.9, "S20", "S20", "OFICIAL", "2025 por setor (aprovações): infraestrutura 71,4; indústria 71,0; agropecuária 54,3; comércio e serviços 41,2."),
 R("bndes_gar", "36.1", "Garantias concedidas pelo BNDES", "Garantias", "BNDES", "R$ bi", NL, 128.2, "Não divulgado no balanço 2019 consultado", "S20", "OFICIAL", "O 'impacto total' de R$ 366 bi de 2025 = aprovações + garantias; não é desembolso."),
 R("safra_tot", "39", "Plano Safra – valor total anunciado", "Ciclo 2019/20 (jul/2019–jun/2020) × ciclo 2025/26 (jul/2025–jun/2026)", "União (crédito rural)", "R$ bi", 225.59, "=G{safra_emp}+G{safra_af}", "MAPA (S21)", "MAPA + MDA (S21)", "APROXIMAÇÃO", "Ano-safra não coincide com o ano civil. Valores anunciados (disponibilidade), não contratados. 2025/26 = empresarial 516,2 + agricultura familiar 89,0."),
 R("safra_emp", "39.1", "Plano Safra – agricultura empresarial (inclui Pronamp)", "Anunciado", "União", "R$ bi", "=F{safra_tot}-F{safra_af}", 516.2, "Cálculo: total − Pronaf", "MAPA (S21)", "ESTIMADO", "2019/20 calculado por diferença (inclui subvenção ao seguro e apoio à comercialização)."),
 R("safra_af", "39.2", "Plano Safra – agricultura familiar (Pronaf em 2019/20; total MDA em 2025/26)", "Anunciado", "União", "R$ bi", 31.22, 89.0, "MAPA (S21)", "MDA (S21)", "APROXIMAÇÃO", "2025/26: Pronaf = R$ 78,2 bi dentro dos R$ 89 bi do Plano Safra da Agricultura Familiar."),
] + stages("ct", "37", "P&D no orçamento federal – função Ciência e Tecnologia (19)", "União", (7.38, 19.03), (7.09, 35.09), (6.95, 35.01), (6.28, 19.21), (6.371, 23.768), "Portal da Transparência (S07)", PORTAL_OBS + " 2025 inclui operações reembolsáveis do FNDCT (subfunção desenvolvimento tecnológico: R$ 28,9 bi empenhados), o que infla a comparação.") + [
 R("pd_pib", "38", "P&D realizado – dispêndio nacional (% do PIB)", "Governo + empresas + ESFL", "Brasil", "%", 0.0115115, 0.0119380, "MCTI via World Bank WDI (S22)", "Último dado: 2023 (S22)", "APROXIMAÇÃO", "Não há dado para 2025; a coluna 2025 traz o valor de 2023."),
 R("pd_rs", "38.1", "P&D realizado – dispêndio nacional (R$ bi, estimado)", "% do PIB × PIB do ano", "Brasil", "R$ bi", "=F{pd_pib}*PIB_2019", "=G{pd_pib}*PIB_2025", "Cálculo S22 × S01", "Cálculo (2023 % × PIB 2025)", "ESTIMADO", "2025 é hipótese: supõe a mesma intensidade de P&D de 2023."),
]

EMP_ROWS = [
 R("estoque", "40", "Estoque de empregos formais", "Estoque em 31/dez (vínculos celetistas)", "Brasil", "pessoas", 39054507, 48474348, "Caged antigo (S16)", "Novo Caged (S15)", "APROXIMAÇÃO", "Quebra metodológica: Caged antigo (2019) × Novo Caged/eSocial (2025). 2025: 48.474.348 exclui estatutários da RAIS; 'estoque total recuperado' = 49.090.182."),
 R("adm", "41", "Admissões formais", "Fluxo anual (jan–dez)", "Brasil", "pessoas", 16197094, 26599777, "S16", "S15", "APROXIMAÇÃO", "Novo Caged capta mais movimentações (temporários, intermitentes) – níveis de admissões/desligamentos não são comparáveis diretamente."),
 R("desl", "42", "Desligamentos formais", "Fluxo anual (jan–dez)", "Brasil", "pessoas", 15553015, 25320279, "S16", "S15", "APROXIMAÇÃO", "Idem."),
 R("saldo", "43", "Saldo anual de empregos formais", "Admissões − desligamentos (saldo acumulado no ano)", "Brasil", "pessoas", "=F{adm}-F{desl}", "=G{adm}-G{desl}", "S16", "S15", "OFICIAL", "Calculado na planilha e idêntico ao publicado (644.079 e 1.279.498)."),
 R("desoc", "44", "Taxa média anual de desemprego (desocupação)", "PNAD Contínua – média anual", "Brasil", "%", 0.119, 0.056, "IBGE (S17)", "IBGE (S17)", "OFICIAL", "Publicado. Série atual do SIDRA 4099 (média dos 4 trimestres, após reponderação): 12,0% (2019) e 5,9% (2025)."),
 R("desoc_sidra", "44.1", "Taxa de desocupação – média simples dos 4 trimestres (série atual)", "SIDRA 4099", "Brasil", "%", 0.11975, 0.05875, "SIDRA 4099 (S17)", "SIDRA 4099 (S17)", "ESTIMADO", "Cálculo próprio para mostrar a divergência com a taxa anual divulgada."),
 R("desocup", "44.2", "População desocupada – média anual", "PNAD Contínua", "Brasil", "milhões de pessoas", 12.6, 6.2, "S17", "S17", "OFICIAL", ""),
]

CEX_ROWS = [
 R("exp", "47", "Exportações", "FOB, fluxo anual", "Brasil", "US$ bi", 221.126807647, 348.2784625, "Comex Stat – série revisada (S18)", "Comex Stat (S18)", "OFICIAL", "Divulgação original 2019: US$ 224,01 bi. Revisão posterior da Secex (ajustes de registros, ex.: plataformas de petróleo/Repetro)."),
 R("imp", "48", "Importações", "FOB, fluxo anual", "Brasil", "US$ bi", 185.92796758, 280.208433825, "S18", "S18", "OFICIAL", "Divulgação original 2019: US$ 177,34 bi; 2025 divulgado US$ 280,4 bi."),
 R("saldo_bc", "49", "Saldo da balança comercial", "Exportações − importações", "Brasil", "US$ bi", "=F{exp}-F{imp}", "=G{exp}-G{imp}", "Cálculo S18", "Cálculo S18", "OFICIAL", "Original 2019: US$ 46,7 bi; revisado: US$ 35,2 bi. 2025 divulgado: US$ 68,3 bi."),
 R("corrente", "49.1", "Corrente de comércio", "Exportações + importações", "Brasil", "US$ bi", "=F{exp}+F{imp}", "=G{exp}+G{imp}", "Cálculo S18", "Cálculo S18", "OFICIAL", ""),
 R("idp", "46", "Investimento estrangeiro direto (IDP)", "Ingressos líquidos, BPM6, fluxo anual", "Brasil", "US$ bi", 69.1744, 77.6761, "BCB SGS 22885 (S08)", "S08", "OFICIAL", "2019 divulgado originalmente: US$ 78,559 bi (S27); série atual revisada: 69,17. 2025: 3,41% do PIB segundo o BCB."),
]

INV_ROWS = [
 R("fbcf", "45", "Formação bruta de capital fixo (investimento realizado – toda a economia)", "Contas Nacionais, valores correntes", "Brasil (público + privado)", "R$ bi", 1143.186, 2145.050, SIDRA, SIDRA, "OFICIAL", "Investimento efetivamente realizado; inclui governo e estatais – o IBGE não separa FBCF privada na série trimestral."),
 R("nib", "45.1", "Investimentos privados anunciados na indústria (Nova Indústria Brasil)", "Anúncios plurianuais", "Setor privado", "R$ bi", NL, 2200.0, "Sem programa/painel equivalente em 2019", "MDIC (S26)", "APROXIMAÇÃO", "Anúncio ≠ contratado ≠ realizado. Valor acumulado de anúncios de 2024 até fev/2025 para vários anos; não é fluxo de 2025."),
 R("bndes_ind", "45.2", "BNDES – indústria (contratado/aprovado)", "2019: desembolsos à indústria; 2025: aprovações à indústria", "BNDES", "R$ bi", 8.816, 71.0, "BNDES via Estado de Minas (S20)", "BNDES via Agência Brasil (S20)", "APROXIMAÇÃO", "Estágios diferentes (desembolso × aprovação) – não calcular variação como se fosse o mesmo conceito."),
 R("abdib_priv", "45.3", "Investimento privado em infraestrutura (realizado)", "Abdib", "Setor privado", "R$ bi", NL, 235.0, "Não localizado para 2019", "Abdib via Conjur (S24)", "IMPRENSA/SETORIAL", "84% do total de R$ 280 bi em 2025."),
]

INF_ROWS = [
 R("infra_fed", "50", "Investimentos federais em infraestrutura (GND 4 pagos)", "Soma das funções Transporte, Saneamento, Urbanismo, Habitação, Energia e Comunicações – pago total no ano (RTN)", "Governo Central", "R$ bi", 12.364, 20.816, "Cálculo STN – RTN tab. 2.3 (S04)", "S04", "ESTIMADO", "Agregação própria (mesma fonte e conceito). 2019: 7,834+1,157+3,176+0,047+0,062+0,089; 2025: 13,607+0,612+5,965+0,552+0,030+0,049."),
 R("pac", "51", "Investimentos do PAC / Novo PAC (orçamento federal)", "2025: dotação OGU do Novo PAC (100% empenhada)", "União", "R$ bi", NL, 49.8, "Ver tentativas na aba 'Fontes e metodologia'", "Casa Civil via Agência Gov (S23)", "APROXIMAÇÃO", "2025 é dotação/empenho, não pagamento. Novo PAC (todas as fontes, inclusive privadas e estatais) somou R$ 944,8 bi executados de 2023 a ago/2025."),
 R("inv_transp", "50.1", "Investimentos (GND 4) na função Transporte – pago total", "RTN", "Governo Central", "R$ bi", 7.834, 13.607, "S04", "S04", "OFICIAL", ""),
] + stages("rod", "52", "Rodovias – subfunção Transporte Rodoviário (782)", "União", (7.04, 11.66), (6.32, 12.69), (6.31, 12.65), (4.25, 9.69), None, "", "", conc_extra="") + \
    stages("fer", "53", "Ferrovias – subfunção Transporte Ferroviário (783)", "União", (0.57, 0.46), (0.51, 0.06), (0.51, 0.06), (0.36, 0.02), None, "", "") + \
    stages("por", "54", "Portos – subfunção Transporte Hidroviário/Aquaviário (784)", "União", (0.60, 0.85), (0.87, 0.58), (0.87, 0.45), (0.19, 0.24), None, "", "") + \
    stages("aer", "55", "Aeroportos – subfunção Transporte Aéreo (781)", "União", (0.31, 0.25), (0.16, 0.20), (0.16, 0.19), (0.04, 0.08), None, "", "") + \
    stages("san", "56a", "Saneamento (função 17)", "União", (0.45, 1.74), (0.52, 0.98), (0.51, 0.79), (0.45, 0.26), (0.451, 0.284), "Portal da Transparência (S07)", PORTAL_OBS) + \
    stages("mob", "56b", "Mobilidade – subfunção Transportes Coletivos Urbanos (453)", "União", (0.70, 1.04), (0.61, 0.89), (0.58, 0.86), (0.44, 0.74), None, "", "") + [
 R("abdib_tot", "56.1", "Investimento total em infraestrutura (todas as fontes)", "Abdib – energia, transportes/logística, saneamento, telecom", "Brasil (público + privado)", "R$ bi", 123.9, 280.0, "Abdib (S24)", "Abdib (S24)", "IMPRENSA/SETORIAL", "Entidade setorial. 2019 = 1,71% do PIB (PIB antigo)."),
 R("abdib_transp", "56.2", "Investimento em transportes e logística (todas as fontes)", "Abdib", "Brasil", "R$ bi", 25.0, 76.5, "S24", "S24", "IMPRENSA/SETORIAL", "Rodovias, ferrovias, hidrovias, portos, aeroportos e mobilidade urbana somados; a abertura por modal não foi localizada."),
 R("abdib_san", "56.3", "Investimento em saneamento", "2019: total; 2025: somente capital privado", "Brasil", "R$ bi", 14.4, 30.0, "S24", "S24", "IMPRENSA/SETORIAL", "Conceitos diferentes (total × privado) – variação não deve ser interpretada literalmente."),
]
for r in INF_ROWS:
    if r["id"].split("_")[0] in ("rod", "fer", "por", "aer", "mob") and r["id"].endswith("_di"):
        r["obs"] = "Despesa total da subfunção (todos os GND), não só investimento; exclui concessões, estatais e setor privado. 2025: subfunção renomeada 'Transporte Aquaviário'." if r["id"].startswith("por") else "Despesa total da subfunção (todos os GND), não só investimento; exclui concessões, estatais e setor privado."

# ---------------------------------------------------------------- consolidado (código, indicador, id da linha, conceito curto)
CONS = [
 ("1", "PIB total do Brasil", "pib"), ("2", "PIB da agropecuária", "agro"), ("3", "PIB da indústria", "ind"),
 ("4", "PIB dos serviços", "serv"), ("5", "PIB das atividades financeiras, de seguros e serviços relacionados", "fin"),
 ("6", "PIB dos serviços não financeiros", "nfin"),
 ("7a", "Participação da agropecuária no PIB", "sh_agro"), ("7b", "Participação da indústria no PIB", "sh_ind"),
 ("7c", "Participação dos serviços financeiros no PIB", "sh_fin"), ("7d", "Participação dos serviços não financeiros no PIB", "sh_nfin"),
 ("8", "Arrecadação da União", "arrec"), ("9", "Gastos da União", "gastosu"),
 ("10", "Receita primária do Governo Central", "rectot"), ("10b", "Receita líquida do Governo Central", "recliq"),
 ("11", "Despesa primária do Governo Central", "desprim"), ("12", "Despesa total do Governo Central", "desptot"),
 ("13", "Dívida Pública Federal", "dpf"), ("14", "Dívida Bruta do Governo Geral", "dbgg"), ("15", "Dívida Líquida do Setor Público", "dlsp"),
 ("16", "Renúncias fiscais e gastos tributários", "gtrib"), ("17", "Benefícios financeiros e creditícios", "bfc"),
 ("18", "Juros nominais pagos (União, orçamento)", "jurosorc"), ("19", "Juros nominais líquidos (setor público consolidado)", "jurosliq"),
 ("20", "Amortizações da dívida", "amort"), ("21", "Refinanciamento da dívida", "refin"),
 ("22", "Investimentos previstos na LOA", "inv_di"), ("23", "Investimentos empenhados", "inv_emp"), ("24", "Investimentos pagos", "inv_pago"),
 ("25", "Saúde prevista na LOA", "sau_di"), ("26a", "Saúde empenhada", "sau_emp"), ("26b", "Saúde paga", "sau_pago"),
 ("27", "Educação prevista na LOA", "edu_di"), ("28a", "Educação empenhada", "edu_emp"), ("28b", "Educação paga", "edu_pago"),
 ("29", "Segurança pública prevista na LOA", "seg_di"), ("30a", "Segurança pública empenhada", "seg_emp"), ("30b", "Segurança pública paga", "seg_pago"),
 ("31", "Previdência prevista na LOA", "prev_di"), ("32a", "Previdência empenhada", "prev_emp"), ("32b", "Previdência paga", "prev_pago"),
 ("33", "Políticas afirmativas previstas (orçamento atualizado)", "pa_da"), ("34a", "Políticas afirmativas empenhadas", "pa_emp"), ("34b", "Políticas afirmativas pagas", "pa_pago"),
 ("35", "Desembolsos anuais do BNDES", "bndes_des"), ("36", "Aprovações anuais do BNDES", "bndes_apr"),
 ("37", "P&D no orçamento federal (função C&T, empenhado)", "ct_emp"), ("38", "P&D realizado (dispêndio nacional, % PIB)", "pd_pib"),
 ("39", "Valor total do Plano Safra", "safra_tot"),
 ("40", "Estoque de empregos formais", "estoque"), ("41", "Admissões formais", "adm"), ("42", "Desligamentos formais", "desl"),
 ("43", "Saldo anual de empregos formais", "saldo"), ("44", "Taxa média anual de desemprego", "desoc"),
 ("45", "Investimentos privados/industriais (anunciados – NIB)", "nib"), ("45b", "Investimento realizado – FBCF", "fbcf"),
 ("46", "Investimento estrangeiro direto", "idp"), ("47", "Exportações", "exp"), ("48", "Importações", "imp"), ("49", "Saldo da balança comercial", "saldo_bc"),
 ("50", "Investimentos federais em infraestrutura", "infra_fed"), ("51", "Investimentos do PAC", "pac"),
 ("52", "Investimentos em rodovias (empenhado)", "rod_emp"), ("53", "Investimentos em ferrovias (empenhado)", "fer_emp"),
 ("54", "Investimentos em portos (empenhado)", "por_emp"), ("55", "Investimentos em aeroportos (empenhado)", "aer_emp"),
 ("56a", "Saneamento (empenhado)", "san_emp"), ("56b", "Mobilidade urbana (empenhado)", "mob_emp"),
]

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

LOC = {}  # id -> (sheet, row)

def q(sheet):
    return "'" + sheet + "'"

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
    ws.row_dimensions[row].height = 36

def resolve(v, rowmap):
    if isinstance(v, str) and v.startswith("="):
        for k, r in rowmap.items():
            v = v.replace("{" + k + "}", str(r))
    return v

def calc_formulas(un, r):
    """Fórmulas H..M (2019 corrigido, dif abs, dif %, var real, %PIB19, %PIB25)."""
    F, G = f"F{r}", f"G{r}"
    na = '"n.a."'
    if un in ("R$ bi", "R$ mi"):
        div = "" if un == "R$ bi" else "/1000"
        H = f'=IFERROR({F}*FATOR_IPCA,"n.d.")'
        I = f'=IFERROR({G}-{F},"n.d.")'
        J = f'=IFERROR({G}/{F}-1,"n.d.")'
        K = f'=IFERROR({G}/H{r}-1,"n.d.")'
        L = f'=IFERROR({F}{div}/PIB_2019,"n.d.")'
        M = f'=IFERROR({G}{div}/PIB_2025,"n.d.")'
    elif un == "US$ bi":
        H = f"={na}"
        I = f'=IFERROR({G}-{F},"n.d.")'
        J = f'=IFERROR({G}/{F}-1,"n.d.")'
        K = f"={na}"
        L = f'=IFERROR({F}/(PIB_2019/PTAX_2019),"n.d.")'
        M = f'=IFERROR({G}/(PIB_2025/PTAX_2025),"n.d.")'
    elif un in ("%", "% do PIB"):
        H = f"={na}"
        I = f'=IFERROR(({G}-{F})*100,"n.d.")'
        J = f'=IFERROR({G}/{F}-1,"n.d.")'
        K = f"={na}"
        L = f'=IF(ISNUMBER({F}),{F},"n.d.")' if un == "% do PIB" else f"={na}"
        M = f'=IF(ISNUMBER({G}),{G},"n.d.")' if un == "% do PIB" else f"={na}"
    else:
        H = f"={na}"
        I = f'=IFERROR({G}-{F},"n.d.")'
        J = f'=IFERROR({G}/{F}-1,"n.d.")'
        K = f"={na}"
        L = f"={na}"; M = f"={na}"
    return H, I, J, K, L, M

THEM_COLS = ["Código", "Indicador", "Conceito / estágio", "Âmbito", "Unidade", "Brasil 2019", "Brasil 2025",
             "2019 em R$ de dez/2025 (IPCA)", "Diferença absoluta (2025−2019)", "Diferença % nominal", "Variação real (IPCA)",
             "2019 % do PIB", "2025 % do PIB", "Fonte 2019", "Fonte 2025", "Classificação do dado", "Observações metodológicas"]
THEM_W = [7, 38, 30, 16, 9, 13, 13, 14, 14, 11, 11, 10, 10, 26, 26, 15, 60]

def write_theme(sheet, ttl, sub, rows, notes, extra_usd=False):
    ws = wb[sheet]
    title(ws, ttl, sub)
    cols = THEM_COLS + (["2019 em R$ bi (PTAX média)", "2025 em R$ bi (PTAX média)"] if extra_usd else [])
    header(ws, 3, cols, THEM_W + ([14, 14] if extra_usd else []))
    rowmap = {}
    start = 4
    for i, r in enumerate(rows):
        rowmap[r["id"]] = start + i
    for i, r in enumerate(rows):
        n = start + i
        LOC[r["id"]] = (sheet, n)
        vals = [r["cod"], r["ind"], r["conc"], r["amb"], r["un"]]
        for c, v in enumerate(vals, 1):
            ws.cell(row=n, column=c, value=v)
        for c, v in ((6, r["v19"]), (7, r["v25"])):
            v = resolve(v, rowmap)
            cell = ws.cell(row=n, column=c, value=v)
            cell.font = F_TXT if (isinstance(v, str) and v.startswith("=")) else F_INP
            if isinstance(v, (int, float)) or (isinstance(v, str) and v.startswith("=")):
                cell.number_format = FMT[r["un"]]
            if isinstance(v, str) and not v.startswith("="):
                cell.alignment = WRAP
        H, I, J, K, L, M = calc_formulas(r["un"], n)
        for c, f in zip(range(8, 14), (H, I, J, K, L, M)):
            cell = ws.cell(row=n, column=c, value=f)
            cell.font = F_TXT
        ws.cell(row=n, column=8).number_format = FMT.get(r["un"], "#,##0.00") if r["un"].startswith("R$") else "@"
        ws.cell(row=n, column=9).number_format = PP if r["un"] in ("%", "% do PIB") else FMT[r["un"]]
        for c in (10, 11, 12, 13):
            ws.cell(row=n, column=c).number_format = PCT
        for c, v in ((14, r["f19"]), (15, r["f25"]), (16, r["tipo"]), (17, r["obs"] or "—")):
            ws.cell(row=n, column=c, value=v).alignment = WRAP
        if extra_usd:
            if r["un"] == "US$ bi":
                ws.cell(row=n, column=18, value=f'=IFERROR(F{n}*PTAX_2019,"n.d.")').number_format = FMT["R$ bi"]
                ws.cell(row=n, column=19, value=f'=IFERROR(G{n}*PTAX_2025,"n.d.")').number_format = FMT["R$ bi"]
            else:
                ws.cell(row=n, column=18, value="n.a."); ws.cell(row=n, column=19, value="n.a.")
        for c in range(1, len(cols) + 1):
            cell = ws.cell(row=n, column=c)
            cell.border = BORDER
            cell.fill = FILL[r["tipo"]]
            if cell.font != F_INP and c not in (6, 7):
                cell.font = F_TXT
            if c <= 5:
                cell.alignment = WRAP
    last = start + len(rows) - 1
    ws.auto_filter.ref = f"A3:{get_column_letter(len(cols))}{last}"
    ws.freeze_panes = "C4"
    footnotes(ws, last + 2, notes)
    return rowmap, last

COMMON_NOTES = [
 "Valores nominais do próprio ano, em R$ bilhões (salvo indicação). Correção de 2019 para R$ de dez/2025 pelo IPCA: fator = índice dez/2025 ÷ índice dez/2019 (célula FATOR_IPCA na aba 'Resumo executivo').",
 "Variação real = valor 2025 ÷ valor 2019 corrigido − 1. % do PIB calculado com o PIB anual do IBGE (SIDRA 1846) de cada ano. Para % e taxas, a 'diferença absoluta' está em pontos percentuais (p.p.).",
 "'n.a.' = não se aplica (unidade não monetária ou em US$); 'n.d.' = não disponível porque um dos anos foi 'não localizado após busca'. Texto em azul = dado digitado da fonte; preto = fórmula; verde = vínculo com outra aba.",
 "Cores das linhas: verde = oficial; amarelo = estimado/cálculo próprio; azul-claro = aproximação; laranja = imprensa/entidade setorial; cinza = não localizado.",
]

def footnotes(ws, row, notes):
    ws.cell(row=row, column=1, value="Notas metodológicas").font = F_BLD
    for i, t in enumerate(notes + COMMON_NOTES, 1):
        c = ws.cell(row=row + i, column=1, value=f"{i}. {t}")
        c.font = F_NOTE

# --- abas temáticas
write_theme("PIB setorial", "PIB setorial – valor adicionado por atividade (valores correntes)",
            "Fonte: IBGE, Contas Nacionais Trimestrais (SIDRA 1846), soma dos quatro trimestres. Participações ao final.",
            PIB_ROWS, ["Participações calculadas sobre o PIB a preços de mercado e, entre parênteses nas linhas 7, sobre o VAB (critério usual do IBGE).",
                       "Serviços não financeiros = VAB de serviços − VAB de atividades financeiras, de seguros e serviços relacionados.",
                       "Valores de 2025 refletem a série consultada em 22/09/2026 e podem diferir da divulgação de março/2026."])
# linhas de participação no PIB setorial
ws = wb["PIB setorial"]
sh_start = LOC["nfin"][1] + 1
shares = [("sh_agro", "7a", "Participação da agropecuária", "agro"), ("sh_ind", "7b", "Participação da indústria", "ind"),
          ("sh_serv", "7c'", "Participação dos serviços (total)", "serv"),
          ("sh_fin", "7c", "Participação das atividades financeiras", "fin"), ("sh_nfin", "7d", "Participação dos serviços não financeiros", "nfin")]
# desloca notas: reescreve a partir de sh_start (as notas foram escritas depois; apagamos e reescrevemos)
for rr in range(sh_start, sh_start + 20):
    for cc in range(1, 18):
        ws.cell(row=rr, column=cc).value = None
for i, (sid, cod, nome, base) in enumerate(shares):
    n = sh_start + i
    LOC[sid] = ("PIB setorial", n)
    b = LOC[base][1]; p = LOC["pib"][1]; v = LOC["vab"][1]
    vals = [cod, nome + " no PIB", f"VAB da atividade ÷ PIB (VAB: 2019 = ver obs.)", "Brasil", "%"]
    for c, x in enumerate(vals, 1):
        ws.cell(row=n, column=c, value=x)
    ws.cell(row=n, column=6, value=f"=F{b}/F{p}").number_format = PCT
    ws.cell(row=n, column=7, value=f"=G{b}/G{p}").number_format = PCT
    ws.cell(row=n, column=8, value="n.a.")
    ws.cell(row=n, column=9, value=f"=(G{n}-F{n})*100").number_format = PP
    ws.cell(row=n, column=10, value=f"=G{n}/F{n}-1").number_format = PCT
    ws.cell(row=n, column=11, value="n.a."); ws.cell(row=n, column=12, value="n.a."); ws.cell(row=n, column=13, value="n.a.")
    ws.cell(row=n, column=14, value="Cálculo sobre S01"); ws.cell(row=n, column=15, value="Cálculo sobre S01")
    ws.cell(row=n, column=16, value="ESTIMADO")
    vb = {x["id"]: x for x in PIB_ROWS}
    def _v(k, col):
        if k == "nfin":
            return vb["serv"][col] - vb["fin"][col]
        return vb[k][col]
    t19 = _v(base, "v19") / vb["vab"]["v19"] * 100; t25 = _v(base, "v25") / vb["vab"]["v25"] * 100
    ws.cell(row=n, column=17, value=("Participação no VAB (critério IBGE): " + f"{t19:.2f}".replace(".", ",") + "% (2019) e " + f"{t25:.2f}".replace(".", ",") + "% (2025)."))
    for c in range(1, 18):
        cell = ws.cell(row=n, column=c); cell.border = BORDER; cell.fill = FILL["ESTIMADO"]; cell.font = F_TXT; cell.alignment = WRAP
ws.auto_filter.ref = f"A3:Q{sh_start + len(shares) - 1}"
footnotes(ws, sh_start + len(shares) + 1,
          ["Participações calculadas sobre o PIB a preços de mercado (inclui impostos); a observação traz a participação sobre o VAB (critério usual do IBGE).",
           "Serviços não financeiros = VAB de serviços − VAB de atividades financeiras, de seguros e serviços relacionados.",
           "Valores de 2025 refletem a série consultada em 22/09/2026 e podem diferir da divulgação de março/2026 (R$ 12,7 tri)."])

write_theme("Receitas públicas", "Receitas públicas – União e Governo Central",
            "Arrecadação federal (RFB), receitas do Governo Central (RTN/STN, caixa) e subsídios da União (OSU/PLOA).",
            REC_ROWS, ["Arrecadação federal (RFB) e receita total do RTN são conceitos distintos e não devem ser somados.",
                       "Gastos tributários e benefícios financeiros/creditícios de 2025 são estimativas oficiais ex ante; 2019 são apurações ex post (OSU)."])
write_theme("Despesas públicas", "Despesas públicas – Governo Central (RTN) e União (orçamento)",
            "Despesa primária pelo critério caixa (STN); juros e resultado nominal pelo critério competência (BCB); despesa orçamentária paga (RREO).",
            DESP_ROWS, ["Despesa primária do RTN (caixa) ≠ despesa orçamentária paga do RREO (inclui juros, amortização e demais despesas financeiras).",
                        "A 'despesa total do Governo Central' é aproximação (soma de critérios distintos) e está sinalizada como tal."])
write_theme("Dívida e juros", "Dívida pública, juros, amortização e refinanciamento",
            "Estoques em 31 de dezembro (dívida) e fluxos anuais (juros, amortização, refinanciamento).",
            DIV_ROWS, ["Estoques (DPF, DBGG, DLSP) não devem ser somados a fluxos (juros, amortização).",
                       "DPF (Tesouro) ≠ DBGG (BCB): a DBGG inclui estados e municípios e as operações compromissadas do BCB e exclui títulos em carteira do BCB.",
                       "Juros pagos (orçamento, caixa) ≠ juros apropriados (BCB, competência, líquidos de juros ativos). Refinanciamento é rolagem da dívida, não gasto primário."])
write_theme("LOA e execução orçamentária", "LOA e execução orçamentária da União – despesa total e investimentos",
            "Estágios: dotação inicial → dotação atualizada → empenho → liquidação → pagamento (RREO, 6º bimestre).",
            LOA_ROWS, ["Previsão (dotação) e execução (empenho, liquidação, pagamento) nunca são somadas.",
                       "'Pago' no RREO = pagamentos do orçamento do próprio exercício; o RTN soma também restos a pagar pagos no ano (linhas 24.1 e 24.2)."])
write_theme("Saúde, educação e previdência", "Saúde, educação e previdência – LOA e execução (União)",
            "RREO Anexo 02 (funções/subfunções) para dotação, empenho e liquidação; Portal da Transparência para valor pago.",
            SOC_ROWS, ["Função orçamentária ≠ mínimo constitucional de saúde/educação (ASPS e MDE têm regras próprias de cômputo).",
                       "Previdência (função 09) inclui RGPS, RPPS da União e militares inativos; a linha 11.1 (aba Despesas) traz o RGPS pelo RTN."])
write_theme("Segurança e polít. afirmativas", "Segurança pública e políticas afirmativas – LOA e execução",
            "Função 06 (segurança) pelo RREO; políticas afirmativas pelos programas de igualdade racial (Portal da Transparência) e dados do MIR.",
            SEG_ROWS, ["Não existe classificação orçamentária única de 'políticas afirmativas'; usou-se o programa federal de igualdade racial de cada PPA (2034 e 5804) como recorte comparável, mais o MIR e a agenda transversal como complemento.",
                       "Valores das políticas afirmativas em R$ milhões."])
write_theme("BNDES, Plano Safra e P&D", "BNDES, Plano Safra e pesquisa & desenvolvimento",
            "BNDES (desembolsos e aprovações), Plano Safra (anúncio por ciclo agrícola) e P&D (orçamento federal e dispêndio nacional).",
            BND_ROWS, ["Desembolsos do BNDES não são despesas da LOA.",
                       "Plano Safra: o ciclo 2019/2020 vai de jul/2019 a jun/2020 e o ciclo 2025/2026 de jul/2025 a jun/2026 – não coincidem com os anos civis.",
                       "P&D realizado para 2025 não existe ainda; usou-se o último dado (2023) como aproximação."])
write_theme("Emprego", "Emprego formal e desemprego",
            "Caged (2019, sistema antigo) e Novo Caged (2025); PNAD Contínua (IBGE).",
            EMP_ROWS, ["Estoque = posição em 31 de dezembro; admissões, desligamentos e saldo = acumulado jan–dez.",
                       "Quebra de série: o Novo Caged (eSocial) substituiu o Caged em 2020 – comparações de nível entre 2019 e 2025 são aproximações."])
write_theme("Comércio exterior", "Comércio exterior e investimento estrangeiro direto (US$)",
            "Comex Stat/MDIC (FOB) e BCB (IDP). Valores mantidos em US$; colunas R e S convertem para R$ pela PTAX média anual.",
            CEX_ROWS, ["% do PIB calculado com o PIB convertido para US$ pela PTAX média anual (BCB SGS 3698).",
                       "Não há correção pelo IPCA de valores em US$ (índice de preços brasileiro não se aplica a moeda estrangeira)."], extra_usd=True)
write_theme("Invest. privados e industriais", "Invest. privados e industriais",
            "Distinção entre investimento anunciado, contratado/aprovado e efetivamente realizado.",
            INV_ROWS, ["Anunciado (NIB) ≠ contratado/aprovado (BNDES) ≠ realizado (FBCF/IBGE, Abdib).",
                       "Não há estatística oficial anual de investimento privado industrial realizado para 2025 (PIA/IBGE tem defasagem de 2 anos)."])
write_theme("Infraestrutura federal", "Infraestrutura – investimentos federais e totais",
            "Orçamento da União por subfunção (RREO), investimentos pagos por função (RTN), Novo PAC e estimativas Abdib (todas as fontes).",
            INF_ROWS, ["Subfunções de transporte trazem a despesa total (todos os grupos), não apenas o GND 4; concessões privadas e estatais estão fora do orçamento.",
                       "Abdib é entidade setorial privada; seus números incluem investimentos privados e de todas as esferas e não são comparáveis ao orçamento federal."])

# --- Indicadores consolidados
wc = wb["Indicadores consolidados"]
title(wc, "Indicadores consolidados – Brasil 2019 × 2025",
      "Valores vinculados às abas temáticas (texto verde). R$ bilhões correntes salvo indicação; variação real e correção pelo IPCA dez/2019→dez/2025.")
CCOLS = ["Código", "Indicador", "Conceito", "Âmbito", "Unidade", "Brasil 2019", "Brasil 2025", "2019 corrigido para preços de 2025",
         "Variação nominal", "Variação real", "2019 como percentual do PIB", "2025 como percentual do PIB", "Fonte 2019", "Fonte 2025",
         "Data de acesso", "Observações metodológicas"]
header(wc, 3, CCOLS, [7, 40, 32, 16, 9, 13, 13, 14, 11, 11, 11, 11, 26, 26, 11, 60])
ALLROWS = {r["id"]: r for r in PIB_ROWS + REC_ROWS + DESP_ROWS + DIV_ROWS + LOA_ROWS + SOC_ROWS + SEG_ROWS + BND_ROWS + EMP_ROWS + CEX_ROWS + INV_ROWS + INF_ROWS}
for i, (cod, nome, rid) in enumerate(CONS):
    n = 4 + i
    sh, sr = LOC[rid]
    src = ALLROWS.get(rid)
    if src is None:  # participações
        un, conc, amb, f19, f25, tipo = "%", "VAB da atividade ÷ PIB", "Brasil", "Cálculo sobre S01", "Cálculo sobre S01", "ESTIMADO"
        obs = f"={q(sh)}!Q{sr}"
    else:
        un, conc, amb, f19, f25, tipo, obs = src["un"], src["conc"], src["amb"], src["f19"], src["f25"], src["tipo"], (src["obs"] or "—")
    stage = ""
    if src is not None and src["conc"] in ("Dotação inicial (LOA)", "Empenhado", "Pago", "Liquidado", "Dotação atualizada"):
        conc = src["conc"] + " – " + src["ind"]
    vals = [cod, nome, conc, amb, un]
    for c, v in enumerate(vals, 1):
        wc.cell(row=n, column=c, value=v)
    for c, col in ((6, "F"), (7, "G")):
        cell = wc.cell(row=n, column=c, value=f"={q(sh)}!{col}{sr}")
        cell.font = F_LNK
        cell.number_format = FMT.get(un, "#,##0.00")
    Fc, Gc = f"F{n}", f"G{n}"
    if un in ("R$ bi", "R$ mi"):
        div = "" if un == "R$ bi" else "/1000"
        H = f'=IFERROR({Fc}*FATOR_IPCA,"n.d.")'; I = f'=IFERROR({Gc}/{Fc}-1,"n.d.")'; J = f'=IFERROR({Gc}/H{n}-1,"n.d.")'
        K = f'=IFERROR({Fc}{div}/PIB_2019,"n.d.")'; L = f'=IFERROR({Gc}{div}/PIB_2025,"n.d.")'
    elif un == "US$ bi":
        H = '="n.a. (US$)"'; I = f'=IFERROR({Gc}/{Fc}-1,"n.d.")'; J = '="n.a. (US$)"'
        K = f'=IFERROR({Fc}/(PIB_2019/PTAX_2019),"n.d.")'; L = f'=IFERROR({Gc}/(PIB_2025/PTAX_2025),"n.d.")'
    elif un in ("%", "% do PIB"):
        H = '="n.a."'; I = f'=IFERROR(({Gc}-{Fc})*100,"n.d.")'; J = '="n.a."'
        K = f'=IF(ISNUMBER({Fc}),{Fc},"n.d.")' if un == "% do PIB" else '="n.a."'
        L = f'=IF(ISNUMBER({Gc}),{Gc},"n.d.")' if un == "% do PIB" else '="n.a."'
    else:
        H = '="n.a."'; I = f'=IFERROR({Gc}/{Fc}-1,"n.d.")'; J = '="n.a."'; K = '="n.a."'; L = '="n.a."'
    for c, f in zip(range(8, 13), (H, I, J, K, L)):
        wc.cell(row=n, column=c, value=f)
    wc.cell(row=n, column=8).number_format = FMT["R$ bi"]
    wc.cell(row=n, column=9).number_format = PP if un in ("%", "% do PIB") else PCT
    for c in (10, 11, 12):
        wc.cell(row=n, column=c).number_format = PCT
    wc.cell(row=n, column=13, value=f19); wc.cell(row=n, column=14, value=f25)
    wc.cell(row=n, column=15, value=ACESSO)
    wc.cell(row=n, column=16, value=(f"[{tipo}] " + obs) if not obs.startswith("=") else f'="[{tipo}] "&{obs[1:]}')
    for c in range(1, 17):
        cell = wc.cell(row=n, column=c)
        cell.border = BORDER; cell.fill = FILL[tipo]
        if c not in (6, 7):
            cell.font = F_TXT
        if c in (2, 3, 4, 13, 14, 16):
            cell.alignment = WRAP
last_c = 4 + len(CONS) - 1
wc.auto_filter.ref = f"A3:P{last_c}"
wc.freeze_panes = "C4"
footnotes(wc, last_c + 2, [
 "Para percentuais e taxas, a coluna 'Variação nominal' mostra a diferença em pontos percentuais (p.p.).",
 "Para valores em US$, não há correção pelo IPCA; % do PIB usa o PIB convertido pela PTAX média anual.",
 "Linhas de LOA (22–34, 37, 52–56): 'previsto' = dotação inicial da LOA; 'empenhado' e 'pago' são estágios de execução – não somar entre si.",
 "A classificação do dado aparece entre colchetes no início das observações e na cor da linha."])

# --- Resumo executivo
ws = wb["Resumo executivo"]
title(ws, "Relatório econômico-fiscal do Brasil – 2019 × 2025",
      f"Escopo nacional; contas públicas com prioridade à União/Governo Central. Dados acessados em {ACESSO}. Valores nominais do próprio ano, 2019 corrigido pelo IPCA até dez/2025.")
ws.column_dimensions["A"].width = 46
for col, w in zip("BCDEFG", (16, 16, 16, 14, 14, 40)):
    ws.column_dimensions[col].width = w
ws["A4"] = "Parâmetros de cálculo"; ws["A4"].font = F_BLD
params = [
 ("PIB 2019 (R$ bi, IBGE SIDRA 1846)", PIB19, "PIB_2019", '#,##0.0'),
 ("PIB 2025 (R$ bi, IBGE SIDRA 1846)", PIB25, "PIB_2025", '#,##0.0'),
 ("IPCA número-índice dez/2019", IPCA_DEZ19, "IPCA_DEZ19", '#,##0.00'),
 ("IPCA número-índice dez/2025", IPCA_DEZ25, "IPCA_DEZ25", '#,##0.00'),
 ("Fator IPCA dez/2019 → dez/2025", "=IPCA_DEZ25/IPCA_DEZ19", "FATOR_IPCA", '0.0000'),
 ("PTAX média anual 2019 (R$/US$, média das médias mensais – BCB SGS 3698)", "=AVERAGE(" + ",".join(str(x) for x in PTAX19) + ")", "PTAX_2019", '0.0000'),
 ("PTAX média anual 2025 (R$/US$, média das médias mensais – BCB SGS 3698)", "=AVERAGE(" + ",".join(str(x) for x in PTAX25) + ")", "PTAX_2025", '0.0000'),
 ("PIB 2019 em US$ bi", "=PIB_2019/PTAX_2019", None, '#,##0.0'),
 ("PIB 2025 em US$ bi", "=PIB_2025/PTAX_2025", None, '#,##0.0'),
]
for i, (lab, val, name, fmt) in enumerate(params):
    n = 5 + i
    ws.cell(row=n, column=1, value=lab).font = F_TXT
    c = ws.cell(row=n, column=2, value=val)
    c.font = F_INP if not (isinstance(val, str) and val.startswith("=")) else F_TXT
    c.number_format = fmt
    c.fill = PatternFill("solid", fgColor="FFFF00") if name == "FATOR_IPCA" else PatternFill()
    for cc in (1, 2):
        ws.cell(row=n, column=cc).border = BORDER
    if name:
        wb.defined_names[name] = DefinedName(name, attr_text=f"'Resumo executivo'!$B${n}")

r0 = 5 + len(params) + 1
ws.cell(row=r0, column=1, value="Principais indicadores").font = F_BLD
hdr = ["Indicador", "2019", "2025", "2019 em R$ de 2025", "Variação real", "Var. nominal / p.p.", "Leitura"]
for i, h in enumerate(hdr, 1):
    c = ws.cell(row=r0 + 1, column=i, value=h); c.font = F_HDR; c.fill = HDR_FILL; c.border = BORDER
    c.alignment = Alignment(wrap_text=True, horizontal="center")
KEY = [
 ("PIB (R$ bi)", "pib", "Crescimento real acumulado de ~24% se deflacionado pelo IPCA (o deflator do PIB difere)."),
 ("Participação da agropecuária no PIB", "sh_agro", "Agro ganhou peso relativo (preços de commodities e safras recordes)."),
 ("Participação da indústria no PIB", "sh_ind", "Indústria total ganha participação, puxada por extrativa e transformação."),
 ("Participação dos serviços financeiros no PIB", "sh_fin", "Setor financeiro cresce acima da média."),
 ("Participação dos serviços não financeiros no PIB", "sh_nfin", "Demais serviços perdem participação relativa."),
 ("Receita líquida do Governo Central (R$ bi)", "recliq", "Estável como % do PIB (~18,2–18,3%)."),
 ("Despesa primária do Governo Central (R$ bi)", "desprim", "Cai como % do PIB, mas cresce em termos reais."),
 ("Resultado primário do Governo Central (R$ bi)", "resprim", "Déficit menor em 2025."),
 ("Juros nominais – setor público consolidado (R$ bi)", "jurosliq", "Juros sobem de ~5% para ~7,9% do PIB (Selic média 14,3% em 2025)."),
 ("Dívida Bruta do Governo Geral (R$ bi)", "dbgg", "DBGG sobe de 74,4% para 78,6% do PIB."),
 ("Dívida Líquida do Setor Público (R$ bi)", "dlsp", "DLSP sobe ~10,5 p.p. do PIB."),
 ("Investimentos federais pagos – RTN (R$ bi)", "inv_rtn", "Investimento federal cresce em termos reais."),
 ("Desembolsos do BNDES (R$ bi)", "bndes_des", "Desembolsos triplicam em termos nominais."),
 ("Plano Safra (R$ bi, ciclo)", "safra_tot", "Ciclos agrícolas, não anos civis."),
 ("Saldo de empregos formais (pessoas)", "saldo", "Quebra Caged/Novo Caged."),
 ("Taxa média de desocupação", "desoc", "Menor taxa da série da PNAD Contínua em 2025."),
 ("Exportações (US$ bi)", "exp", "Recorde em 2025."),
 ("Saldo comercial (US$ bi)", "saldo_bc", ""),
]
for i, (lab, rid, txt) in enumerate(KEY):
    n = r0 + 2 + i
    sh, sr = LOC[rid]
    un = ALLROWS[rid]["un"] if rid in ALLROWS else "%"
    ws.cell(row=n, column=1, value=lab)
    ws.cell(row=n, column=2, value=f"={q(sh)}!F{sr}").font = F_LNK
    ws.cell(row=n, column=3, value=f"={q(sh)}!G{sr}").font = F_LNK
    if un.startswith("R$"):
        ws.cell(row=n, column=4, value=f"=B{n}*FATOR_IPCA")
        ws.cell(row=n, column=5, value=f"=C{n}/D{n}-1")
        ws.cell(row=n, column=6, value=f"=C{n}/B{n}-1")
        fmt = FMT["R$ bi"]
        ws.cell(row=n, column=6).number_format = PCT
    elif un in ("%", "% do PIB"):
        ws.cell(row=n, column=4, value="n.a."); ws.cell(row=n, column=5, value="n.a.")
        ws.cell(row=n, column=6, value=f"=(C{n}-B{n})*100"); ws.cell(row=n, column=6).number_format = PP
        fmt = PCT
    else:
        ws.cell(row=n, column=4, value="n.a."); ws.cell(row=n, column=5, value="n.a.")
        ws.cell(row=n, column=6, value=f"=C{n}/B{n}-1"); ws.cell(row=n, column=6).number_format = PCT
        fmt = FMT[un]
    for cc in (2, 3, 4):
        ws.cell(row=n, column=cc).number_format = fmt
    ws.cell(row=n, column=5).number_format = PCT
    ws.cell(row=n, column=7, value=txt)
    for cc in range(1, 8):
        cell = ws.cell(row=n, column=cc); cell.border = BORDER
        if cc not in (2, 3):
            cell.font = F_TXT
        if cc in (1, 7):
            cell.alignment = WRAP

r1 = r0 + 2 + len(KEY) + 1
ws.cell(row=r1, column=1, value="Legenda de cores (classificação do dado)").font = F_BLD
for i, (k, (col, desc)) in enumerate(TIPOS.items()):
    n = r1 + 1 + i
    c = ws.cell(row=n, column=1, value=k); c.fill = FILL[k]; c.font = F_BLD; c.border = BORDER
    d = ws.cell(row=n, column=2, value=desc); d.font = F_TXT
    ws.merge_cells(start_row=n, start_column=2, end_row=n, end_column=7)

r2 = r1 + 1 + len(TIPOS) + 1
ws.cell(row=r2, column=1, value="Síntese das principais diferenças 2019 × 2025").font = F_BLD
SINTESE = open(sys.argv[2], encoding="utf-8").read().strip().split("\n")
for i, t in enumerate([x for x in SINTESE if x.strip()]):
    n = r2 + 1 + i
    c = ws.cell(row=n, column=1, value=t)
    c.font = F_BLD if t.startswith("■") else F_TXT
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=n, start_column=1, end_row=n, end_column=7)
    ws.row_dimensions[n].height = 15 if t.startswith("■") else max(15, 13 * (len(t) // 150 + 1))
ws.freeze_panes = "A4"

# --- Fontes e metodologia
wf = wb["Fontes e metodologia"]
title(wf, "Fontes e metodologia", f"Todas as fontes consultadas em {ACESSO}. Confiabilidade: Alta = fonte oficial primária ou reprodução fiel; Média = imprensa/entidade setorial ou anúncio.")
FC = ["ID", "Título da fonte", "Instituição", "URL", "Data da publicação", "Ano de referência", "Indicador utilizado", "Página ou tabela", "Observações", "Nível de confiabilidade"]
header(wf, 3, FC, [6, 40, 26, 50, 16, 14, 34, 22, 60, 16])
for i, row in enumerate(FONTES):
    n = 4 + i
    for c, v in enumerate(row, 1):
        cell = wf.cell(row=n, column=c, value=v)
        cell.font = F_TXT; cell.border = BORDER; cell.alignment = WRAP
        if c == 4:
            cell.hyperlink = v; cell.font = Font(name=ARIAL, size=9, color="0563C1", underline="single")
    conf = row[9]
    fill = FILL["OFICIAL"] if conf.startswith("Alta") else FILL["IMPRENSA/SETORIAL"]
    for c in range(1, 11):
        wf.cell(row=n, column=c).fill = fill
lastf = 4 + len(FONTES) - 1
wf.auto_filter.ref = f"A3:J{lastf}"
wf.freeze_panes = "B4"
n = lastf + 2
wf.cell(row=n, column=1, value="Dados não localizados ou só aproximados – tentativas de busca").font = F_BLD
for j, h in enumerate(["Item", "Fontes tentadas", "Resultado / tratamento"], 1):
    c = wf.cell(row=n + 1, column=[2, 4, 9][j - 1], value=h); c.font = F_HDR; c.fill = HDR_FILL
for i, (a, b, c_) in enumerate(TENTATIVAS):
    m = n + 2 + i
    for col, v in ((2, a), (4, b), (9, c_)):
        cell = wf.cell(row=m, column=col, value=v); cell.font = F_TXT; cell.alignment = WRAP; cell.fill = FILL["NÃO LOCALIZADO"]
n = n + 2 + len(TENTATIVAS) + 1
wf.cell(row=n, column=1, value="Regras metodológicas aplicadas").font = F_BLD
REGRAS = [
 "Fluxos anuais (PIB, receitas, despesas, juros, desembolsos, comércio) nunca são somados a estoques (DPF, DBGG, DLSP, estoque de emprego).",
 "Previsão orçamentária (dotação inicial/atualizada) é apresentada separada da execução (empenho, liquidação, pagamento).",
 "Juros (GND 2), amortização (GND 6) e refinanciamento (rolagem) aparecem em linhas próprias.",
 "DPF (Tesouro, União) apresentada separadamente da DBGG (BCB, Governo Geral) e da DLSP (setor público consolidado).",
 "Desembolsos do BNDES não são tratados como despesa da LOA.",
 "Investimentos privados: anunciados (NIB), aprovados/contratados (BNDES) e realizados (FBCF, Abdib) em linhas distintas.",
 "Plano Safra: ciclos jul–jun (2019/20 e 2025/26) não coincidem com os anos civis de 2019 e 2025.",
 "Emprego: estoque em 31/dez; admissões, desligamentos e saldo acumulados no ano; quebra Caged → Novo Caged sinalizada.",
 "PIB: valores correntes e VAB por atividade; atividades financeiras separadas dos demais serviços.",
 "Divergências entre fontes estão registradas nas observações (ex.: PIB 2025, balança 2019, IDP 2019, taxa de desocupação, estoque de emprego, DBGG/DLSP arredondadas).",
 "Correção monetária: IPCA dez/2019→dez/2025 (fator ≈ 1,3915). Não se aplica a valores em US$, pessoas ou taxas.",
 "Limitação: páginas gov.br de MCTI, Casa Civil e MIR estavam fora do ar em 22/09/2026 (restrição da legislação eleitoral); usaram-se séries equivalentes (World Bank/UNESCO, Agência Gov, Inesc).",
]
for i, t in enumerate(REGRAS, 1):
    c = wf.cell(row=n + i, column=1, value=f"{i}. {t}"); c.font = F_NOTE

# fontes/estilo padrão Arial em todas as células sem fonte explícita
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
    w.page_setup.fitToWidth = 1
    w.sheet_properties.pageSetUpPr.fitToPage = True
    w.page_setup.fitToHeight = 0

wb.save(OUT)
print("ok", OUT)

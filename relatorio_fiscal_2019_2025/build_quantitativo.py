# -*- coding: utf-8 -*-
"""Tabela complementar - Brasil 2016 x 2019 x 2022 x 2025 (xlsx).

Indicadores NAO monetarios (numeros/estatisticas) que nao cabem no
Relatorio_economico_fiscal_Brasil_2016_2019_2022_2025.xlsx (esse so tem R$/%PIB):
  a) LOA detalhada por orgao/GND (aqui SIM e monetario, mas em granularidade
     diferente da aba "LOA e execucao orcamentaria" do workbook fiscal, que e
     por funcao; por isso os valores ficam nominais, sem deflacao/%PIB).
  b) Seguranca publica - estatisticas (mortes, efetivo, ocorrencias).
  c) Pacto federativo - repasses da Uniao a estados/municipios por area.
  d) Educacao - matriculas, rendimento, Enem e Sisu (numeros, nao R$).

Mesma convencao visual do build.py/build4.py (fontes, cores por classificacao
do dado, aba "Fontes e metodologia"), adaptada para indicadores nao-monetarios.
"""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = sys.argv[1] if len(sys.argv) > 1 else "Relatorio_quantitativo_2016_2019_2022_2025.xlsx"
ACESSO = "23/09/2026"

# ---------------------------------------------------------------- estilos (iguais ao build.py)
ARIAL = "Arial"
F_TIT = Font(name=ARIAL, size=14, bold=True, color="1F3864")
F_SUB = Font(name=ARIAL, size=9, italic=True, color="595959")
F_HDR = Font(name=ARIAL, size=9, bold=True, color="FFFFFF")
F_TXT = Font(name=ARIAL, size=9)
F_INP = Font(name=ARIAL, size=9, color="0000FF")      # dado digitado (hardcode)
F_BLD = Font(name=ARIAL, size=9, bold=True)
F_NOTE = Font(name=ARIAL, size=8, italic=True, color="404040")
HDR_FILL = PatternFill("solid", fgColor="1F3864")
TIPOS = {
    "OFICIAL": ("E2EFDA", "Dado oficial publicado"),
    "ESTIMADO": ("FFF2CC", "Estimativa/calculo proprio a partir de dados oficiais"),
    "APROXIMAÇÃO": ("DDEBF7", "Aproximacao: periodo, conceito ou recorte diferente do solicitado"),
    "IMPRENSA/SETORIAL": ("FCE4D6", "Cifra obtida via imprensa ou entidade setorial, sem acesso direto a base oficial"),
    "NÃO LOCALIZADO": ("D9D9D9", "Nao localizado apos busca - tentativas registradas na aba 'Fontes e metodologia'"),
}
FILL = {k: PatternFill("solid", fgColor=v[0]) for k, v in TIPOS.items()}
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
NL = "não localizado após busca"

FMT_NUM = '#,##0;[Red]-#,##0'
FMT_DEC = '#,##0.0;[Red]-#,##0.0'
PCT = '0.00%;[Red]-0.00%'
PP = '0.00" p.p.";[Red]-0.00" p.p."'
# Valores de unidade "%" são guardados como número percentual "cru" (94.3 = 94,3%), não como
# fração (0.943) — por isso usamos um formato literal com "%" anexado, sem a multiplicação por
# 100 que o formato percentual nativo do Excel ('0.00%') aplicaria a um valor já em escala 0-100.
PCT_LIT = '0.00"%";[Red]-0.00"%"'
FMT = {
    "número": FMT_NUM,
    "milhões": FMT_DEC,
    "%": PCT_LIT,
    "por 100 mil hab.": FMT_DEC,
    "R$ bi": '#,##0.00;[Red]-#,##0.00',
    "R$ mi": '#,##0.00;[Red]-#,##0.00',
}

YEARS = [2016, 2019, 2022, 2025]
YCOL = {2016: "F", 2019: "G", 2022: "H", 2025: "I"}
PAIRS = [(2016, 2019), (2019, 2022), (2022, 2025), (2016, 2025)]

# ---------------------------------------------------------------- fontes
# (id, título, instituição, url, data publicação, ano ref, indicador, página/tabela, observações, confiabilidade)
FONTES = [
 ("Q01", "Orçamento da União em Foco, Ano 4, nº 1", "Consultoria de Orçamento da Câmara dos Deputados (CONOF)", "https://www2.camara.leg.br/orcamento-da-uniao/orcamento-da-uniao-em-foco/web_orcamento_uniao_em_foco_ano-2017", "09/2017", "2016", "Execução por órgão (autorizado/pago) e por GND", "Tabelas 10 e 18", "Valores de execução do exercício (autorizado = dotação após créditos adicionais; pago = executado).", "Alta"),
 ("Q02", "Raio X do Orçamento 2019 – Autógrafo", "Consultoria de Orçamento da Câmara dos Deputados (CONOF)", "https://www2.camara.leg.br/orcamento-da-uniao/raio-x-do-orcamento/2019/raio-x-do-orcamento-2019-autografo", "21/03/2019", "2019", "LOA aprovada (autógrafo) por GND e top-10 órgãos", "Painel Raio X 2019", "Órgão apenas parcial nesta fonte (top-10 + 'demais'); GND completo.", "Alta"),
 ("Q03", "Raio X do Orçamento 2022 – Autógrafo", "Consultoria de Orçamento da Câmara dos Deputados (CONOF)", "https://www2.camara.leg.br/orcamento-da-uniao/raio-x-do-orcamento/2022/raio-x-do-orcamento-2022-autografo-v1", "01/2022", "2022", "LOA aprovada (autógrafo) por órgão (despesas primárias) e itens da despesa total", "Painel Raio X 2022", "'Total' por órgão exclui serviço da dívida (juros/amortização/rolagem) e investimento das estatais.", "Alta"),
 ("Q04", "Raio X do Orçamento 2025 – Pós-Vetos", "Consultoria de Orçamento da Câmara dos Deputados (CONOF)", "https://www2.camara.leg.br/orcamento-da-uniao/raio-x-do-orcamento/2025/raio-x-do-orcamento-2025-pos-vetos", "04/2025", "2025", "LOA aprovada (pós-vetos) por órgão (despesas primárias) e itens da despesa total", "Painel Raio X 2025", "Mesmo escopo/limitação de Q03.", "Alta"),
 ("Q05", "Lei nº 13.255, de 14/01/2016 (LOA 2016)", "Presidência da República", "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2016/lei/L13255.htm", "14/01/2016", "2016", "Total da LOA aprovada", "Texto da lei", "Total Orç. Fiscal+Seguridade R$ 2.953,5 bi; incl. investimento das estatais R$ 3.050,6 bi.", "Alta"),
 ("Q06", "Lei nº 13.808, de 15/01/2019 (LOA 2019)", "Presidência da República", "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2019/Lei/L13808.htm", "15/01/2019", "2019", "Total da LOA aprovada", "Texto da lei", "Total Orç. Fiscal+Seguridade R$ 3.262,2 bi; incl. investimento das estatais R$ 3.382,2 bi.", "Alta"),
 ("Q07", "Lei nº 14.303, de 21/01/2022 (LOA 2022)", "Presidência da República", "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14303.htm", "21/01/2022", "2022", "Total da LOA aprovada", "Texto da lei", "Total Orç. Fiscal+Seguridade R$ 4.730,0 bi; incl. investimento das estatais R$ 4.826,5 bi.", "Alta"),
 ("Q08", "Lei nº 15.121, de 10/04/2025 (LOA 2025)", "Presidência da República (espelho: modeloinicial.com.br)", "https://modeloinicial.com.br/lei/L-15121-2025", "10/04/2025", "2025", "Total da LOA aprovada", "Texto da lei", "Total Orç. Fiscal+Seguridade R$ 5.722,4 bi; incl. investimento das estatais R$ 5.886,0 bi. Consultado via espelho porque o texto integral não foi facilmente localizado direto no Planalto.", "Média (espelho de fonte oficial)"),
 ("Q09", "Infográfico Censo Escolar 2019", "Inep", "https://download.inep.gov.br/educacao_basica/censo_escolar/download/2019/infografico_censo_2019.pdf", "01/2020", "2019", "Matrículas e nº de escolas – educação básica", "Infográfico", "", "Alta"),
 ("Q10", "Apresentação coletiva – Censo Escolar 2022", "Inep", "https://download.inep.gov.br/censo_escolar/resultados/2022/apresentacao_coletiva.pdf", "02/2023", "2022", "Matrículas e nº de escolas – educação básica", "Apresentação", "", "Alta"),
 ("Q11", "Censo registra queda de 1 milhão de matrículas na educação básica", "Agência Brasil (dados Inep)", "https://agenciabrasil.ebc.com.br/educacao/noticia/2026-02/censo-registra-queda-de-1-milhao-de-matriculas-na-educacao-basica", "02/2026", "2024 e 2025", "Matrículas e nº de escolas – educação básica", "Notícia", "2025: 46.018 mil matrículas (dado já fechado); 2024: 47.088.922 (base de comparação).", "Alta (reproduz Inep)"),
 ("Q12", "Censo Escolar 2025: Ensino Fundamental na rede pública tem avanço histórico", "Inep/MEC", "https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/censo-escolar/censo-escolar-2025-ensino-fundamental-na-rede-publica-tem-avanco-historico", "2026", "2025", "Taxas de rendimento (aprovação/reprovação/abandono), rede pública", "Notícia oficial", "Fundamental rede pública: aprovação ~97%, reprovação 2,4%, abandono 0,6%.", "Alta"),
 ("Q13", "Taxas de rendimento escolar 2022 (fund./médio, pública/privada)", "Inep", "https://convivaeducacao.org.br/fique_atento/5591", "19/05/2023", "2022", "Taxas de rendimento por rede e etapa", "Notícia (dados Inep)", "Aprovação fund. anos iniciais: pública 95,3%/privada 99,1%. Reprovação fund. anos finais: pública 6,8%/privada 1,7%. Abandono médio: pública 6,5%/privada 0,7%.", "Alta (reproduz Inep)"),
 ("Q14", "Notas sobre o Censo da Educação Superior 2016", "Inep/MEC", "https://download.inep.gov.br/educacao_superior/censo_superior/documentos/2016/notas_sobre_o_censo_da_educacao_superior_2016.pdf", "08/2017", "2016", "Matrículas graduação (total, presencial/EAD)", "Notas estatísticas", "8.052.254 matrículas; presencial 81,4%/EAD 18,6%.", "Alta"),
 ("Q15", "Inep divulga Censo da Educação Superior 2019", "Semesp (dados Inep)", "https://www.semesp.org.br/politicas-publicas/2020/10/23/inep-divulga-censo-da-educacao-superior-2019/", "10/2020", "2019", "Matrículas graduação (total, pública/privada, presencial/EAD)", "Notícia (dados Inep)", "8,6 milhões; pública 24,2%/privada 75,8%; presencial 71,5%/EAD 28,5%.", "Alta (reproduz Inep)"),
 ("Q16", "Apresentação Censo da Educação Superior 2022", "Inep", "https://download.inep.gov.br/educacao_superior/censo_superior/documentos/2022/apresentacao_censo_da_educacao_superior_2022.pdf", "2023", "2022", "Matrículas graduação (total, pública/privada)", "Apresentação", "9.443.597 matrículas; pública 22,0%/privada 78,0%.", "Alta"),
 ("Q17", "Censo da Educação Superior 2024 mostra que matrículas na EAD são maioria", "Jeduca (dados Inep)", "https://jeduca.org.br/noticia/censo-da-educacao-superior-2024-mostra-que-pela-primeira-vez-matriculas-na-ead-sao-maioria", "17/09/2025", "2024", "Matrículas graduação (total, pública/privada, EAD)", "Notícia (dados Inep)", "10.226.873 matrículas (privada 8.162.039 + pública 2.064.834); EAD = 50,7% do total. Censo 2025 ainda não divulgado (coleta em 2026).", "Alta (reproduz Inep)"),
 ("Q18", "Dados de abstenção e eliminação – Enem 2016", "Inep/MEC", "https://download.inep.gov.br/imprensa/2016/dados_de_abstencao_e_eliminacao_enem_2016.pdf", "2016", "2016", "Inscritos, presentes e abstenção – Enem", "Relatório oficial", "Inscritos regulares 8.630.306; presentes 5.848.619; abstenção 30,0%.", "Alta"),
 ("Q19", "Enem termina com 27,19% de ausentes, menor taxa desde 2009", "Agência Brasil (dados Inep)", "https://agenciabrasil.ebc.com.br/educacao/noticia/2019-11/enem-termina-com-2719-de-ausentes-menor-taxa-desde-2009", "11/2019", "2019", "Inscritos e presentes – Enem", "Notícia (dados Inep)", "Inscritos ≈5,1 milhões; presentes (2º dia) 3.935.237 (77,23%).", "Alta (reproduz Inep)"),
 ("Q20", "Enem 2024 tem 4,3 milhões de inscritos confirmados", "Inep", "https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/enem/enem-2024-tem-4-3-milhoes-de-inscritos-confirmados", "10/2024", "2024", "Inscritos confirmados – Enem", "Notícia oficial", "4.325.960 inscritos confirmados.", "Alta"),
 ("Q21", "Participantes podem consultar as notas do Enem 2025", "Inep", "https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/enem/participantes-podem-consultar-as-notas-do-enem-2025", "16/01/2026", "2025", "Inscritos e resultado – Enem", "Notícia oficial", "≈4,8 milhões de inscritos; resultado já divulgado.", "Alta"),
 ("Q28", "Enem 2025 teve participação de 70% dos inscritos; gabaritos serão divulgados no dia 20", "Agência Gov", "https://agenciagov.ebc.com.br/noticias/202511/enem-2025-teve-participacao-de-70-dos-inscritos-gabaritos-serao-divulgados-no-dia-20", "11/2025", "2025", "Presença (%) – Enem", "Notícia oficial", "72% de presença entre os inscritos (título da notícia arredonda para 70%).", "Alta"),
 ("Q22", "Sisu tem 1,8 milhão de estudantes inscritos", "Agência Brasil (dados MEC)", "https://agenciabrasil.ebc.com.br/educacao/noticia/2019-01/sisu-tem-18-milhao-de-estudantes-inscritos", "01/2019", "2019 (edição 2019.1)", "Inscritos e vagas – Sisu", "Notícia (dados MEC)", "1.823.871 pessoas inscritas (3.492.751 inscrições, com 2 opções); 235.476 vagas ofertadas.", "Alta (reproduz MEC)"),
 ("Q23", "Tudo sobre o Sisu 2025: vagas, datas e como aplicar", "CNN Brasil (dados MEC/dadosabertos.mec.gov.br)", "https://www.cnnbrasil.com.br/educacao/tudo-sobre-o-sisu-2025-vagas-datas-e-como-aplicar/", "01/2025", "2025 (edição 2025.1)", "Inscrições e vagas – Sisu", "Notícia (dados MEC)", "2.505.979 inscrições (com 2 opções); 261.779 vagas ofertadas (124 instituições, 6.851 cursos); 254.899 convocados.", "Alta (reproduz MEC)"),
 ("Q24", "Censo Escolar 2017: cai o número de matrículas", "Conviva Educação (dados Inep)", "https://convivaeducacao.org.br/fique_atento/497", "2017", "2016", "Matrículas – educação básica", "Notícia (dados Inep)", "≈48,8 milhões; divergência com outra nota do Inep (que cita 37,9 mi para um recorte diferente de etapas) não resolvida nesta busca.", "Média (fonte secundária, divergência não resolvida)"),
 ("Q25", "Censo Escolar: as escolas que os brasileiros frequentam", "Nova Escola (dados Inep)", "https://novaescola.org.br/conteudo/9953", "2016", "2016", "Número de escolas – educação básica", "Notícia (dados Inep)", "≈184,1 mil; ano exato do dado não confirmado na fonte.", "Baixa (ano exato incerto)"),
 ("Q26", "Censo Escolar 2022: como foram as matrículas nas escolas do país", "FRM (dados Inep)", "https://www.frm.org.br/conteudo/educacao-basica/noticia/censo-escolar-2022-como-foram-matriculas-nas-escolas-do-pais", "02/2023", "2022", "Número de escolas – educação básica", "Notícia (dados Inep)", "178.346 escolas.", "Alta (reproduz Inep)"),
 ("Q27", "Reprovação cai 62% no ensino médio público entre 2022 e 2025", "Jornal de Brasília (dados MEC/Inep)", "https://www.jb.com.br/brasil/educacao/2026/06/1060095-reprovacao-cai-62-no-ensino-medio-publico-entre-2022-e-2025.html", "06/2026", "2022 e 2025", "Variação da reprovação e do abandono – ensino médio, rede pública", "Notícia (dados MEC/Inep)", "Reprovação médio público caiu 62% e abandono caiu 61% entre 2022 e 2025 (valores absolutos de 2025 não vieram na cobertura).", "Alta (reproduz Inep, mas só variação %)"),
 ("SP01", "20º Anuário Brasileiro de Segurança Pública", "Fórum Brasileiro de Segurança Pública (FBSP)", "https://forumseguranca.org.br/wp-content/uploads/2026/07/anuario-2026.pdf", "07/2026", "2025 (com série histórica revisada 2016-2025)", "MVI, homicídio doloso, feminicídio, latrocínio, letalidade policial, roubos, estupro", "Tabelas 02-04, 15, 29", "Traz série histórica revisada retroativamente (mesma metodologia) para os 4 anos, além dos dados fechados de 2025.", "Alta"),
 ("SP02", "11º Anuário Brasileiro de Segurança Pública", "Fórum Brasileiro de Segurança Pública (FBSP)", "https://forumseguranca.org.br/wp-content/uploads/2018/10/ANUARIO_11_2017.pdf", "2017", "2016", "MVI, homicídio doloso, latrocínio, letalidade policial, roubos, estupro, feminicídio", "Tabelas 01, 05, 13, 17", "Valores publicados originalmente à época, antes das revisões retroativas do FBSP.", "Alta"),
 ("SP03", "14º Anuário Brasileiro de Segurança Pública", "Fórum Brasileiro de Segurança Pública (FBSP)", "https://static.poder360.com.br/2020/11/Anuario-Brasileiro-de-Seguranca-Publica-2020.pdf", "2020", "2019", "MVI, homicídio doloso, latrocínio, letalidade policial, feminicídio, estupro", "Tabelas 19, 21, 22, 37, 41", "", "Alta"),
 ("SP04", "17º Anuário Brasileiro de Segurança Pública", "Fórum Brasileiro de Segurança Pública (FBSP)", "https://static.poder360.com.br/2023/07/Anuario-Brasileiro-de-Seguranca-Publica-2023-Forum-Brasileiro-de-Seguranca-Publica.pdf", "2023", "2022", "MVI, homicídio doloso, latrocínio, letalidade policial, feminicídio", "Tabela 01 e texto sobre feminicídios", "", "Alta"),
 ("SP05", "Mortes violentas caem 8,2% no Brasil em 2025; sete estados registram alta", "CNN Brasil (dados FBSP)", "https://www.cnnbrasil.com.br/nacional/brasil/mortes-violentas-caem-82-no-brasil-em-2025-sete-estados-registram-alta/", "07/2026", "2025", "MVI", "Notícia (dados FBSP)", "Confirma o dado do 20º Anuário (SP01).", "Alta (reproduz FBSP)"),
 ("SP06", "Mortes violentas intencionais no Brasil em 2025: entre avanços históricos e desafios persistentes", "Fonte Segura / FBSP", "https://fontesegura.forumseguranca.org.br/mortes-violentas-intencionais-no-brasil-em-2025-entre-avancos-historicos-e-desafios-persistentes/", "2026", "2025", "Homicídio doloso (nº e taxa)", "Artigo do blog do FBSP", "", "Alta"),
 ("SP07", "Estupro bate recorde e chega a quase 75 mil casos em 2022, segundo Anuário de Segurança Pública", "Adusp (dados FBSP)", "https://adusp.org.br/violencia/75mil-estupros/", "2023", "2022", "Estupro (registros)", "Notícia (dados do 17º Anuário)", "74.930 registros, recorde da série histórica até então; taxa nacional exata não veio na cobertura.", "Média (imprensa sindical reproduzindo FBSP)"),
 ("F01", "Transferências Constitucionais por Tipo de Transferência – série histórica (planilhas FPE.xls e FPM.xls)", "Tesouro Nacional / Tesouro Transparente", "https://www.tesourotransparente.gov.br/publicacoes/transferencias-constitucionais-por-tipo-de-transferencia-serie-historica/2020/26", "Consulta 23/09/2026", "2016, 2019, 2022 e 2025", "FPE e FPM – valor pago no ano", "Abas 'FPEAnual' e 'FPM{ano}'", "Valores líquidos da retenção de 20% destinada ao Fundeb. Não têm classificação por área/finalidade (partilha de receita).", "Alta"),
 ("F02", "Consulta Consolidada Fundo a Fundo", "Ministério da Saúde / Fundo Nacional de Saúde (FNS)", "https://consultafns.saude.gov.br", "Consulta 23/09/2026", "2016, 2019, 2022 e 2025", "Repasses do SUS (fundo a fundo) a estados e municípios", "Filtro Ano/Estado=Todos/Tipo=Todos", "Valor líquido = bruto menos descontos/glosas (principalmente no bloco de Média e Alta Complexidade).", "Alta"),
 ("F03", "Nota Técnica nº 46 (Disoc)", "Ipea", "https://repositorio.ipea.gov.br/items/5274f0d9-9e2a-43e1-9c76-3dc3b3407abf", "01/2018", "2016", "Repasses do SUS fundo a fundo (conferência)", "Nota técnica", "R$ 66,83 bi para 2016 — próximo do valor da consulta FNS (F02), usado como conferência de ordem de grandeza.", "Alta"),
 ("F04", "Transferências ao Fundo de Manutenção e Desenvolvimento da Educação Básica (Fundeb) – 2022", "Tesouro Nacional / Tesouro Transparente", "https://www.tesourotransparente.gov.br/publicacoes/transferencias-ao-fundo-de-manutencao-e-desenvolvimento-da-educacao-basica-fundeb/2022/114-2", "2023", "2022", "Complementação da União ao Fundeb (VAAF + VAAT)", "Aba Resumo, acumulado no ano", "R$ 32,88 bi (VAAF R$ 22,67 bi + VAAT R$ 10,21 bi).", "Alta"),
 ("F05", "Transferências ao Fundo de Manutenção e Desenvolvimento da Educação Básica (Fundeb) – 2025", "Tesouro Nacional / Tesouro Transparente", "https://www.tesourotransparente.gov.br/publicacoes/transferencias-ao-fundo-de-manutencao-e-desenvolvimento-da-educacao-basica-fundeb/2025/114", "2026", "2025", "Complementação da União ao Fundeb (VAAF + VAAT + VAAR + FTI)", "Aba Resumo, acumulado no ano", "R$ 59,73 bi (VAAF R$ 27,57 bi + VAAT R$ 24,51 bi + VAAR R$ 5,06 bi + FTI R$ 2,60 bi).", "Alta"),
 ("F06", "Dados Físicos e Financeiros do PNAE (tabela 1995–2023)", "Fundo Nacional de Desenvolvimento da Educação (FNDE)", "https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/programas/pnae/consultas/pnae-dados-fisicos-e-financeiros-do-pnae", "Consulta 23/09/2026", "2016, 2019 e 2022", "PNAE – repasse pago (redes estadual+distrital+municipal)", "Tabela histórica", "Tabela oficial só vai até 2023; 2025 não localizado como valor pago.", "Alta"),
 ("F07", "Complementação da União ao Fundeb 2019 (estimativa por diferença)", "Wikipédia, citando FNDE (fonte terciária)", "https://pt.wikipedia.org/wiki/Fundeb", "Consulta 23/09/2026", "2019", "Complementação da União ao Fundeb", "Cálculo: Fundeb total 2019 (R$166,3bi) − parcela dos entes (≈R$151,3bi)", "Estimativa por diferença, não é uma linha de relatório oficial. Ver F10 (RTN) para o valor oficial usado nesta planilha.", "Baixa (fonte terciária, cálculo indireto)"),
 ("F08", "Notícias sobre Fundeb 2017/2018 (complementação da União)", "Jornal da Nova (imprensa)", "https://jornaldanova.com.br", "2017-2018", "2016 (aproximação)", "Complementação da União ao Fundeb", "Notícia", "Não é um valor de 2016 propriamente dito; usado apenas como ordem de grandeza antes de adotar o valor oficial do RTN (F10) nesta planilha.", "Baixa (imprensa, ano aproximado)"),
 ("F09", "Orçamento do PNATE para 2022 (notícia)", "Imprensa / FNDE", "https://www.fnde.gov.br/programas/pnate", "2022", "2022", "PNATE – orçamento (não é valor pago)", "Notícia/portal do programa", "≈R$0,77 bi orçado (LOA), não confirmado como valor efetivamente pago.", "Baixa (orçado, não execução)"),
 ("F10", "Resultado do Tesouro Nacional – Séries históricas (RTN, tabela 2.1)", "Tesouro Nacional (STN)", "https://www.tesourotransparente.gov.br/publicacoes/boletim-resultado-do-tesouro-nacional-rtn/2025/12", "Consulta 23/09/2026", "2016, 2019, 2022 e 2025", "Complementação da União ao Fundeb (despesa do Governo Central)", "Tabela 2.1", "Mesma fonte/linha já usada na aba 'Despesas públicas' do Relatorio_economico_fiscal_Brasil_2016_2019_2022_2025.xlsx (valores: 13,675 / 15,600 / 32,882 / 59,730 R$ bi) — praticamente idênticos aos valores de 2022/2025 obtidos via F04/F05, o que confirma a consistência entre as duas fontes.", "Alta"),
]

TENTATIVAS = [
 ("LOA 2019 por órgão (Judiciário, Legislativo, Fazenda, Justiça isolados)", "Orçamento da União em Foco (edição ~2020, não localizada com PDF direto), Raio X 2019", "Fonte disponível só trouxe top-10 órgãos + 'demais' agregados; valores individuais não localizados para 2019."),
 ("LOA 2022/2025 por GND clássico completo (Outras Despesas Correntes, Inversões Financeiras isoladas)", "Raio X do Orçamento 2022 e 2025", "Essas edições do Raio X substituíram o detalhamento clássico por GND por uma tabela de 'itens da despesa total' (transferências constitucionais, rolagem, amortização, juros); os dois GNDs específicos não aparecem isolados."),
 ("Consulta direta ao SIGA Brasil (Senado)", "www12.senado.leg.br/orcamento/sigabrasil", "Ferramenta interativa (Business Objects), não acessível via busca/fetch simples; substituída pelos boletins CONOF/Câmara."),
 ("Taxas de rendimento escolar nacionais únicas (não fatiadas por rede) para os 4 anos", "Inep – notícias e apresentações dos Censos Escolares 2016/2019/2022/2025", "As divulgações acessadas trazem taxas separadas por rede pública/privada e por etapa; não foi localizada uma taxa 'Brasil' única e consolidada por ano nesta busca (recomenda-se baixar a planilha de Taxas de Rendimento Escolar direto do Inep)."),
 ("Censo da Educação Superior 2025", "Inep, cronograma oficial (Portaria 771/2025)", "Ainda não existe: a coleta ocorre em 2026, com divulgação prevista para set-out/2026 em diante."),
 ("Concluintes graduação 2024 (número total exato) e médias do Enem 2022 por área", "Inep – Resumo Técnico Censo Superior 2024; apresentações de resultado Enem 2022", "Não localizados nesta busca; recomenda-se checar os PDFs oficiais diretamente."),
 ("Sisu – matriculados/convocados finais em 2016, 2019 e 2022", "Notícias sobre cada edição do Sisu; dadosabertos.mec.gov.br/sisu", "Só foram localizados inscritos e vagas ofertadas para esses anos; o número de matriculados/convocados finais não apareceu nas fontes consultadas."),
 ("Total geral de transferências da União a estados e municípios (todos os tipos), por ano", "Painel das Transferências Intergovernamentais (Tesouro Transparente) — painel interativo, não retornou valores em texto simples nas consultas; fontes secundárias divergentes (ex.: R$595,7 bi vs R$761 bi para 2024, sem reconciliação de metodologia)", "Não incluído na planilha para evitar publicar um número não reconciliado; recomenda-se extrair diretamente do painel interativo do Tesouro Transparente."),
 ("Repasses do FNAS/SUAS (assistência social) a estados e municípios, série 2016-2025", "Painel 'Repasses Fundo a Fundo' do MDS (paineis.mds.gov.br/public/extensions/RFF/RFF.html) — dashboard interativo, não extraível via busca; só fragmentos de programas específicos (ex. PROCADSUAS+IGDBPF+Primeira Infância no SUAS) foram localizados, sem série completa", "Não localizado um total FNAS/SUAS comparável para os 4 anos; recomenda-se extrair diretamente do painel do MDS."),
 ("PNATE (transporte escolar) — série paga 2016-2025", "FNDE (portal do programa), imprensa", "Só foi localizado um valor orçado (não pago) para 2022; sem série completa e confiável."),
]

def R(id, cod, ind, conc, amb, un, v16, v19, v22, v25, f16, f19, f22, f25, tipo, obs):
    return dict(id=id, cod=cod, ind=ind, conc=conc, amb=amb, un=un,
                V={2016: v16, 2019: v19, 2022: v22, 2025: v25},
                FT={2016: f16, 2019: f19, 2022: f22, 2025: f25},
                tipo=tipo, obs=obs)

# ---------------------------------------------------------------- dados por aba
# Preencher cada lista com R(...) conforme os agentes de pesquisa retornarem
# os numeros reais (ver "Fontes e metodologia" para os codigos Sxx).

LOA_ROWS = [   # a) LOA detalhada por orgao / GND (R$ bi nominais)
 R("loa_total", "0", "Total da LOA aprovada (Orç. Fiscal + Seguridade Social)", "Dotação aprovada na lei sancionada, antes de créditos adicionais no curso do exercício", "União", "R$ bi",
   2953.5, 3262.2, 4730.0, 5722.4, "Lei 13.255/2016 (Q05)", "Lei 13.808/2019 (Q06)", "Lei 14.303/2022 (Q07)", "Lei 15.121/2025 (Q08)",
   "OFICIAL", "Não inclui investimento das estatais (ver linha 0.1)."),
 R("loa_total_estatais", "0.1", "Total da LOA incl. investimento das estatais", "Dotação aprovada", "União", "R$ bi",
   3050.6, 3382.2, 4826.5, 5886.0, "Q05", "Q06", "Q07", "Q08", "OFICIAL", ""),
 R("loa_estatais_inv", "0.2", "Investimento das estatais (fora do Orç. Fiscal+Seguridade)", "Diferença entre 0.1 e 0", "União", "R$ bi",
   97.1, 120.0, 96.5, 166.6, "Cálculo Q05/Q05 (0.1−0)", "Raio X 2019 (Q02)", "Raio X 2022 (Q03)", "Raio X 2025 (Q04)",
   "ESTIMADO", "2016 calculado por diferença entre os dois totais oficiais da LOA; 2019/2022/2025 vêm diretamente do Raio X do Orçamento."),
 R("loa_saude", "1", "Ministério da Saúde", "2016 = pago no exercício; 2019 = autógrafo aprovado; 2022/2025 = despesas primárias (Raio X, exclui serviço da dívida)", "União", "R$ bi",
   108.7, 132.8, 159.3, 245.5, "Orçamento da União em Foco 2017 (Q01)", "Raio X 2019 (Q02)", "Raio X 2022 (Q03)", "Raio X 2025 (Q04)",
   "APROXIMAÇÃO", "Bases diferentes por ano — não tratar a variação como real sem ajustar a base. Para série homogênea (função 10, RREO), ver a aba 'Saúde, educação e previdência' do relatório fiscal principal."),
 R("loa_educ", "2", "Ministério da Educação", "Mesma ressalva de base da linha 'Saúde'", "União", "R$ bi",
   90.7, 123.0, 129.3, 187.2, "Q01", "Q02", "Q03", "Q04", "APROXIMAÇÃO",
   "Para série homogênea (função 12, RREO), ver a aba 'Saúde, educação e previdência' do relatório fiscal principal."),
 R("loa_defesa", "3", "Ministério da Defesa", "Mesma ressalva de base da linha 'Saúde'", "União", "R$ bi",
   79.7, 107.7, 112.7, 128.1, "Q01", "Q02", "Q03", "Q04", "APROXIMAÇÃO", ""),
 R("loa_prev_assist", "4", "Previdência / Assistência Social (órgão responsável variou por governo)", "2016 = 'Trabalho e Previdência Social' (fusão administrativa); 2019 = 'Desenvolvimento Social' (inclui benefícios RGPS pós-reforma); 2022 = 'Trabalho e Previdência'; 2025 = 'Previdência Social'", "União", "R$ bi",
   588.6, 508.3, 864.5, 1036.4, "Q01", "Q02", "Q03", "Q04", "APROXIMAÇÃO",
   "Nome e composição do órgão mudaram em cada governo (reformas administrativas); série não reflete estrutura estável — usar com cautela."),
 R("loa_seg_justica", "5", "Justiça e Segurança Pública (órgão)", "2016 = 'Ministério da Justiça' (pago); 2022/2025 = 'Justiça e Segurança Pública' (despesas primárias)", "União", "R$ bi",
   12.0, NL, 16.4, 20.7, "Q01", "—", "Q03", "Q04", "APROXIMAÇÃO", "2019 não localizado isolado nesta fonte (agregado em 'demais órgãos')."),
 R("loa_judiciario", "6", "Judiciário + Ministério Público + Defensoria", "Despesas primárias (Raio X)", "União", "R$ bi",
   NL, NL, 57.0, 70.1, "—", "—", "Q03", "Q04", "APROXIMAÇÃO", "2016/2019 não localizados isolados nas fontes consultadas (agregados em 'demais órgãos')."),
 R("loa_legislativo", "7", "Legislativo + TCU", "Despesas primárias (Raio X)", "União", "R$ bi",
   NL, NL, 13.9, 17.4, "—", "—", "Q03", "Q04", "APROXIMAÇÃO", "2016/2019 não localizados isolados nas fontes consultadas."),
 R("loa_ct", "8", "Ciência, Tecnologia e Inovação (MCTI)", "Despesas primárias (Raio X)", "União", "R$ bi",
   NL, NL, 9.9, 13.4, "—", "—", "Q03", "Q04", "APROXIMAÇÃO", "2016/2019 não localizados isolados nas fontes consultadas."),
 R("loa_pessoal", "9", "Pessoal e encargos sociais (todos os poderes)", "2016 = pago (GND1); 2019 = autógrafo (GND1); 2022/2025 = item 'Pessoal' do total da despesa", "União", "R$ bi",
   276.0, 350.4, 362.5, 443.1, "Q01", "Q02", "Q03", "Q04", "APROXIMAÇÃO", ""),
 R("loa_juros", "10", "Juros e encargos da dívida", "2016 = pago (GND2); 2019 = autógrafo (GND2); 2022/2025 = item do total da despesa", "União", "R$ bi",
   204.9, 378.9, 351.4, 480.0, "Q01", "Q02", "Q03", "Q04", "APROXIMAÇÃO", "Comparar com a aba 'Dívida e juros' do relatório fiscal principal (série mais robusta, com BCB/SGS)."),
 R("loa_amortizacao", "11", "Amortização da dívida", "2016 estimado por diferença (GND6 pago − refinanciamento pago); 2022/2025 = item do total da despesa", "União", "R$ bi",
   274.7, NL, 235.3, 393.1, "Cálculo sobre Q01", "—", "Q03", "Q04", "ESTIMADO", "2019 não localizado isolado (GND6 do Raio X 2019 não segrega amortização de refinanciamento nesta fonte)."),
 R("loa_refinanciamento", "12", "Rolagem / refinanciamento da dívida mobiliária federal", "2016 = pago; 2022/2025 = item do total da despesa", "União", "R$ bi",
   650.6, NL, 1884.9, 1655.8, "Q01", "—", "Q03", "Q04", "APROXIMAÇÃO", "2019 não localizado isolado nesta fonte."),
 R("loa_invest_gnd4", "13", "Investimentos (GND4, piso constitucional)", "2016 = pago; 2019 = autógrafo; 2022/2025 = soma dos investimentos por órgão (Raio X)", "União", "R$ bi",
   16.8, 36.2, 43.5, 80.3, "Q01", "Q02", "Q03", "Q04", "APROXIMAÇÃO", "Comparar com a linha 'Investimentos (GND 4)' da aba 'LOA e execução orçamentária' do relatório fiscal principal (RREO, conceito de execução paga)."),
 R("loa_transf_estados", "14", "Transferências a estados, DF e municípios (via LOA)", "2016 = pago (linha própria); 2022/2025 = 'Transferências Constitucionais' (item do total da despesa)", "União", "R$ bi",
   237.2, NL, 377.7, 555.6, "Q01", "—", "Q03", "Q04", "APROXIMAÇÃO", "2019 não localizado isolado nesta fonte. Ver também a aba 'Pacto federativo', que detalha esses repasses por área (saúde, educação, assistência social) e separa FPE/FPM."),
]
SEG_ROWS = [   # b) Seguranca publica - estatisticas
 R("seg_mvi_abs", "1", "Mortes Violentas Intencionais (MVI) – nº absoluto", "Homicídio doloso + feminicídio + latrocínio + lesão corporal seguida de morte + mortes por intervenção policial", "Brasil", "número",
   61600, 47765, 47963, 40775, "SP01", "SP01", "SP01", "SP01", "OFICIAL",
   "Série revisada retroativamente pelo FBSP (mesma edição/metodologia para os 4 anos). Valores publicados originalmente à época: 2016=61.283 (SP02); 2019=47.773 (SP03); 2022=47.508 (SP04)."),
 R("seg_mvi_taxa", "1.1", "Mortes Violentas Intencionais (MVI) – taxa", "Por 100 mil habitantes, série revisada", "Brasil", "por 100 mil hab.",
   30.2, 23.0, 22.7, 19.1, "SP01", "SP01", "SP01", "SP01", "OFICIAL",
   "Taxas publicadas originalmente à época: 2016=29,7; 2019=22,7; 2022=23,4."),
 R("seg_hom_abs", "2", "Homicídio doloso – nº absoluto", "", "Brasil", "número",
   54053, 39561, 39629, 32914, "SP02", "SP03", "SP04", "SP01/SP06", "OFICIAL", ""),
 R("seg_hom_taxa", "2.1", "Homicídio doloso – taxa", "Por 100 mil habitantes", "Brasil", "por 100 mil hab.",
   NL, 18.8, NL, 15.4, "—", "SP03", "—", "SP06", "APROXIMAÇÃO", "2016 e 2022 não localizados nas subtabelas consultadas (só trouxeram nº absoluto)."),
 R("seg_feminicidio", "3", "Feminicídio – nº absoluto", "Lei do Feminicídio (Lei 13.104/2015)", "Brasil", "número",
   621, 1326, 1437, 1571, "SP02", "SP03", "SP04", "SP01", "APROXIMAÇÃO",
   "2016 é o primeiro ano de vigência da lei, com classificação/registro ainda incipiente nas polícias estaduais — número provavelmente subnotificado e não totalmente comparável com os anos seguintes."),
 R("seg_latrocinio_abs", "4", "Latrocínio (roubo seguido de morte) – nº absoluto", "", "Brasil", "número",
   2666, 1577, 1229, 807, "SP02", "SP03", "SP04", "SP01", "OFICIAL", ""),
 R("seg_latrocinio_taxa", "4.1", "Latrocínio – taxa", "Por 100 mil habitantes", "Brasil", "por 100 mil hab.",
   NL, 0.8, NL, 0.4, "—", "SP03", "—", "SP01", "APROXIMAÇÃO", "2016 e 2022 não localizados nas subtabelas consultadas."),
 R("seg_mdip", "5", "Mortes decorrentes de intervenção policial (MDIP)", "Letalidade policial", "Brasil", "número",
   4223, 6357, 6430, 6602, "SP02", "SP03", "SP04", "SP01", "OFICIAL", ""),
 R("seg_policiais_mortos", "6", "Policiais civis e militares mortos (violência letal)", "2016 segrega serviço/fora de serviço (118+335); demais anos não segregam nesta fonte", "Brasil", "número",
   453, 172, 173, 139, "SP02", "SP03", "SP04", "SP01", "APROXIMAÇÃO",
   "2016: 118 mortos em serviço + 335 fora de serviço. Segregação não localizada para 2019/2022/2025 nesta fonte."),
 R("seg_efetivo", "7", "Efetivo policial (civil + militar)", "Total nacional", "Brasil", "número",
   NL, NL, NL, NL, "—", "—", "—", "—", "NÃO LOCALIZADO",
   "Tabelas de efetivo dos Anuários do FBSP vieram com extração de texto corrompida/desalinhada nesta busca. Pontos soltos fora dos anos pedidos: ≈544 mil policiais (PM+PC+bombeiros) em 2020 (Agência Brasil); ≈406.384 PMs estaduais em 2021 (17º Anuário). Recomenda-se extrair manualmente a tabela 'Efetivo das Forças Policiais' dos PDFs oficiais (SP01-SP04)."),
 R("seg_roubos_abs", "8", "Roubos (total de ocorrências) – nº absoluto", "", "Brasil", "número",
   1726757, 1314472, NL, 610959, "SP02", "SP03", "—", "SP01", "APROXIMAÇÃO",
   "2022 não localizado: a tabela correspondente do 17º Anuário não foi extraída com texto legível nesta busca (possível página em formato de imagem)."),
 R("seg_roubos_taxa", "8.1", "Roubos (total) – taxa", "Por 100 mil habitantes", "Brasil", "por 100 mil hab.",
   837.9, 625.5, NL, 286.3, "SP02", "SP03", "—", "SP01", "APROXIMAÇÃO", "2022 não localizado (mesma limitação da linha acima)."),
 R("seg_estupro_abs", "9", "Estupro – registros (nº absoluto)", "2016 = categoria 'estupro' isolada; 2019 em diante = 'estupro' + 'estupro de vulnerável' combinados", "Brasil", "número",
   49497, 66123, 74930, 84388, "SP02", "SP03", "SP07", "SP01", "APROXIMAÇÃO",
   "2016 não é diretamente comparável aos demais anos por mudança de categoria/metodologia de registro."),
 R("seg_estupro_taxa", "9.1", "Estupro – taxa", "Por 100 mil habitantes", "Brasil", "por 100 mil hab.",
   24.0, 31.5, NL, 39.5, "SP02", "SP03", "—", "SP01", "APROXIMAÇÃO", "2022: taxa nacional exata não localizada nesta busca (só o nº absoluto, via fonte secundária SP07)."),
]
FED_ROWS = [   # c) Pacto federativo - repasses por area
 R("fed_fpe", "1", "FPE – Fundo de Participação dos Estados", "Transferência constitucional, valor pago no ano, líquido da retenção de 20% ao Fundeb", "União → Estados/DF", "R$ bi",
   69.91, 77.95, 125.34, 163.97, "F01", "F01", "F01", "F01", "OFICIAL",
   "Sem classificação por área/finalidade — é partilha de receita, não repasse por política pública. Não somar com as linhas de transferências por área abaixo."),
 R("fed_fpm", "2", "FPM – Fundo de Participação dos Municípios", "Transferência constitucional, valor pago no ano, líquido da retenção de 20% ao Fundeb", "União → Municípios", "R$ bi",
   79.91, 90.41, 146.33, 198.04, "F01", "F01", "F01", "F01", "OFICIAL",
   "Mesma ressalva da linha 'FPE': sem classificação por área."),
 R("fed_fpe_fpm_tot", "2.1", "FPE + FPM (total de transferências constitucionais)", "Soma das duas linhas acima", "União → Estados/DF/Municípios", "R$ bi",
   149.82, 168.36, 271.67, 362.01, "F01", "F01", "F01", "F01", "OFICIAL", "Linha de referência apenas — não é comparável às transferências por área (linhas 3+), que têm outra natureza (transferências legais/específicas)."),
 R("fed_sus_bruto", "3", "Repasses do SUS (fundo a fundo) a estados e municípios – valor bruto", "Saúde", "União → Estados/DF/Municípios", "R$ bi",
   67.04, 84.60, 101.11, 169.99, "F02", "F02", "F02", "F02", "OFICIAL",
   "Conferência independente para 2016: Nota Técnica Ipea nº 46 (F03) aponta R$ 66,83 bi, muito próximo do valor da consulta FNS."),
 R("fed_sus_liquido", "3.1", "Repasses do SUS (fundo a fundo) – valor líquido (após glosas)", "Saúde; líquido = bruto − descontos/glosas, principalmente no bloco de Média e Alta Complexidade", "União → Estados/DF/Municípios", "R$ bi",
   64.24, 80.36, 97.25, 164.73, "F02", "F02", "F02", "F02", "APROXIMAÇÃO",
   "Valores de 2019/2022/2025 são aproximados (a fonte primária os apresenta com o prefixo '~'); apenas 2016 veio como número exato."),
 R("fed_fundeb", "4", "Complementação da União ao Fundeb", "Educação", "União → Estados/DF/Municípios", "R$ bi",
   13.675, 15.600, 32.882, 59.730, "F10", "F10", "F10", "F10", "OFICIAL",
   "Valores oficiais do RTN (mesma fonte/linha já usada na aba 'Despesas públicas' do relatório fiscal principal). Para 2022 e 2025 esse número bate quase exatamente com a publicação específica do Fundeb do Tesouro Transparente (F04/F05: R$32,88 bi e R$59,73 bi) — boa conferência cruzada."),
 R("fed_pnae", "5", "PNAE – repasse pago (alimentação escolar)", "Educação; redes estadual + distrital + municipal", "União → Estados/DF/Municípios", "R$ bi",
   3.42, 3.95, 3.56, NL, "F06", "F06", "F06", "—", "APROXIMAÇÃO",
   "2025 não localizado como valor pago (a tabela oficial do FNDE consultada só vai até 2023). Ordem de grandeza compatível com os valores deflacionados já citados na síntese do relatório fiscal principal (R$5,3 bi/R$4,1 bi em R$ de 2025)."),
 R("fed_pnate", "5.1", "PNATE – repasse (transporte escolar)", "Educação", "União → Estados/DF/Municípios", "R$ bi",
   NL, NL, 0.77, NL, "—", "—", "F09", "—", "NÃO LOCALIZADO",
   "Categoria de menor materialidade. Único valor encontrado (2022) é orçamento (LOA), não confirmado como pago; 2016/2019/2025 não localizados."),
 R("fed_fnas", "6", "Repasses do FNAS/SUAS a estados e municípios", "Assistência social", "União → Estados/DF/Municípios", "R$ bi",
   NL, NL, NL, NL, "—", "—", "—", "—", "NÃO LOCALIZADO",
   "Painel 'Repasses Fundo a Fundo' do MDS é um dashboard interativo, não extraível via busca nesta pesquisa. Só foram localizados fragmentos de programas específicos, sem série comparável para os 4 anos."),
 R("fed_transf_total", "7", "Total geral de transferências da União a estados e municípios (todos os tipos)", "Constitucionais + legais + voluntárias + específicas", "União → Estados/DF/Municípios", "R$ bi",
   NL, NL, NL, NL, "—", "—", "—", "—", "NÃO LOCALIZADO",
   "Não reconciliado nesta pesquisa: fontes secundárias divergem (ex.: R$595,7 bi vs R$761 bi para 2024). Recomenda-se extrair diretamente do Painel das Transferências Intergovernamentais (Tesouro Transparente), que é interativo e não retornou valores em texto simples."),
]
EDU_ROWS = [   # d) Educacao - matriculas e rendimento
 R("edu_matriculas_basica", "1", "Matrículas – educação básica (total)", "Censo Escolar", "Brasil", "número",
   48800000, 47900000, 47400000, 46018000, "Q24", "Q09", "Q10", "Q11", "APROXIMAÇÃO",
   "2016 vem de fonte secundária de confiança média (ver Q24); 2019/2022/2025 são divulgações diretas do Inep. 2025 já é dado fechado (Censo Escolar 2025, divulgado fev/2026); 2024 = 47.088.922 (base de comparação do próprio Inep)."),
 R("edu_escolas", "2", "Número de escolas – educação básica", "Censo Escolar", "Brasil", "número",
   184100, 180600, 178346, 178760, "Q25", "Q09", "Q26", "Q11", "APROXIMAÇÃO",
   "2016: ano exato do dado não confirmado na fonte (baixa confiança); demais anos são divulgações diretas do Inep."),
 R("edu_aprovacao_fund", "3", "Taxa de aprovação – ensino fundamental, rede pública", "Etapa/recorte varia por ano conforme o que foi divulgado", "Brasil", "%",
   NL, 94.3, 95.3, 97.0, "—", "Q13", "Q13", "Q12", "APROXIMAÇÃO",
   "2019 = anos iniciais; 2022 = anos iniciais; 2025 = fundamental geral (rede pública, valor divulgado como '~97%'). Não é uma série estritamente homogênea entre etapas — ver observação de cada fonte."),
 R("edu_reprovacao_fund", "4", "Taxa de reprovação – ensino fundamental, rede pública", "Etapa/recorte varia por ano", "Brasil", "%",
   NL, NL, 6.8, 2.4, "—", "—", "Q13", "Q12", "APROXIMAÇÃO",
   "2022 = anos finais; 2025 = fundamental geral. 2016/2019 não localizados nesta busca para o recorte de rede pública."),
 R("edu_abandono_medio", "5", "Taxa de abandono – ensino médio, rede pública", "", "Brasil", "%",
   NL, NL, 6.5, 2.5, "—", "—", "Q13", "Cálculo sobre Q27", "ESTIMADO",
   "2025 estimado a partir da variação divulgada (queda de 61% frente a 2022, Q27); valor absoluto de 2025 não veio na cobertura consultada. 2016/2019 não localizados."),
 R("edu_matriculas_superior", "6", "Matrículas – graduação (total)", "Censo da Educação Superior", "Brasil", "número",
   8052254, 8600000, 9443597, 10226873, "Q14", "Q15", "Q16", "Q17", "OFICIAL",
   "2025 ainda não existe: a coleta do Censo da Educação Superior 2025 ocorre em 2026, com divulgação prevista para set-out/2026 em diante — o valor de 2025 usado aqui é na verdade o do Censo 2024 (mais recente disponível em 23/09/2026)."),
 R("edu_superior_publica_pct", "6.1", "Matrículas – graduação, participação da rede pública", "% do total de matrículas", "Brasil", "%",
   NL, 24.2, 22.0, 20.2, "—", "Q15", "Q16", "Q17", "APROXIMAÇÃO", "2016 não localizado nesta busca; 2025 = dado do Censo 2024 (ver observação da linha 6)."),
 R("edu_superior_ead_pct", "6.2", "Matrículas – graduação, participação do EAD", "% do total de matrículas", "Brasil", "%",
   18.6, 28.5, NL, 50.7, "Q14", "Q15", "—", "Q17", "APROXIMAÇÃO",
   "2022 não localizado nesta busca. 2024/2025: primeira vez que o EAD é maioria das matrículas de graduação. 2025 = dado do Censo 2024 (ver observação da linha 6)."),
 R("edu_ingressantes_superior", "7", "Ingressantes – graduação", "Censo da Educação Superior", "Brasil", "número",
   NL, 3600000, 4700000, 5010433, "—", "Q15", "Q16", "Q17", "APROXIMAÇÃO",
   "2016 não localizado em número absoluto (só variação percentual vs 2015). 2025 = dado do Censo 2024."),
 R("edu_concluintes_superior", "8", "Concluintes – graduação", "Censo da Educação Superior", "Brasil", "número",
   1100000, 1250076, 1300000, NL, "Q14", "Q15", "Q16", "—", "APROXIMAÇÃO",
   "2024/2025 não localizado como número total exato nesta busca (recomenda-se o Resumo Técnico do Censo Superior 2024). 2016/2022 são ordens de grandeza ('>1,1 milhão'/'~1,3 milhão')."),
]
ENEM_ROWS = [  # d) Enem e Sisu
 R("enem_inscritos", "1", "Enem – inscritos", "2016 = inscritos regulares (exclui PPL); demais anos = inscritos confirmados", "Brasil", "número",
   8630306, 5100000, 3476226, 4800000, "Q18", "Q19", "—", "Q21", "OFICIAL",
   "2019 é valor arredondado divulgado pela imprensa a partir do Inep. 2025 já é dado fechado (resultado divulgado 16/01/2026)."),
 R("enem_presentes", "2", "Enem – presentes (participantes efetivos)", "", "Brasil", "número",
   5848619, 3935237, NL, NL, "Q18", "Q19", "—", "—", "APROXIMAÇÃO",
   "2022: não localizado número absoluto de presentes nesta busca (só percentuais por dia de prova: 73,3% e 67,64%). 2025: só percentual de presença (72%) foi localizado, não o número absoluto."),
 R("enem_abstencao", "3", "Enem – taxa de abstenção", "", "Brasil", "%",
   30.0, 22.77, NL, 28.0, "Q18", "Q19", "—", "Cálculo sobre Q28", "APROXIMAÇÃO",
   "2022 não localizado diretamente (só presença por dia, não abstenção do exame como um todo). 2025 = complemento da presença de 72% divulgada (Agência Gov, Q28)."),
 R("sisu_inscricoes", "4", "Sisu – inscrições (contagem por opção de curso, 1ª edição do ano)", "Uma pessoa pode gerar até 2 inscrições (2 opções de curso)", "Brasil", "número",
   NL, 3492751, 2062815, 2505979, "—", "Q22", "—", "Q23", "APROXIMAÇÃO", "2016 não localizado nesta busca."),
 R("sisu_inscritos_pessoas", "4.1", "Sisu – inscritos (pessoas únicas, 1ª edição do ano)", "", "Brasil", "número",
   NL, 1823871, 1054474, NL, "—", "Q22", "—", "—", "APROXIMAÇÃO",
   "2016 e 2025 não localizados como pessoas únicas nesta busca (só a contagem de inscrições, ver linha 4)."),
 R("sisu_vagas", "5", "Sisu – vagas ofertadas (1ª edição do ano)", "", "Brasil", "número",
   228000, 235476, 222000, 261779, "—", "Q22", "—", "Q23", "OFICIAL", ""),
 R("sisu_convocados", "6", "Sisu – convocados/matriculados (1ª edição do ano)", "", "Brasil", "número",
   NL, NL, NL, 254899, "—", "—", "—", "Q23", "NÃO LOCALIZADO",
   "Só foi localizado o número de convocados para 2025; para 2016/2019/2022 as fontes consultadas trouxeram apenas inscritos e vagas ofertadas."),
]

# ---------------------------------------------------------------- workbook
wb = Workbook()
ws0 = wb.active
ws0.title = "Resumo executivo"
SHEETS = ["LOA detalhada (órgão, GND)", "Segurança pública", "Pacto federativo",
          "Educação - matrículas", "Enem e Sisu", "Fontes e metodologia"]
for s in SHEETS:
    wb.create_sheet(s)


def title(ws, t, sub):
    ws["A1"] = t
    ws["A1"].font = F_TIT
    ws["A2"] = sub
    ws["A2"].font = F_SUB
    ws.row_dimensions[1].height = 22


def header(ws, row, cols, widths):
    for i, (c, w) in enumerate(zip(cols, widths), start=1):
        cell = ws.cell(row=row, column=i, value=c)
        cell.font = F_HDR
        cell.fill = HDR_FILL
        cell.border = BORDER
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = 48


def footnotes(ws, row, notes):
    ws.cell(row=row, column=1, value="Notas metodológicas").font = F_BLD
    for i, t in enumerate(notes + COMMON, 1):
        ws.cell(row=row + i, column=1, value=f"{i}. {t}").font = F_NOTE


COMMON = [
    "Valores nominais do próprio ano (sem correção monetária), salvo indicação em contrário — este workbook é"
    " complementar ao Relatorio_economico_fiscal_Brasil_2016_2019_2022_2025.xlsx, que já traz os valores em R$"
    " deflacionados e como % do PIB para as rubricas orçamentárias por função.",
    "Colunas de variação: para indicadores em número/milhões/por 100 mil hab. = variação percentual nominal;"
    " para indicadores em % = diferença em pontos percentuais (p.p.).",
    "'n.d.' = não disponível (dado 'não localizado após busca' para aquele ano, ver aba 'Fontes e metodologia').",
    "Cor da linha = classificação do dado predominante; células individuais têm cor própria quando a"
    " classificação daquele ano específico diverge (ex.: estimado, não localizado).",
    "Períodos 2016→2019, 2019→2022 e 2022→2025 correspondem aproximadamente aos mandatos Temer, Bolsonaro e"
    " Lula III (até 2025); 2016 inclui o governo Dilma até maio.",
]

TH = (["Código", "Indicador", "Conceito / detalhe", "Âmbito", "Unidade",
       "Brasil 2016", "Brasil 2019", "Brasil 2022", "Brasil 2025",
       "Variação 2016→2019", "Variação 2019→2022", "Variação 2022→2025", "Variação 2016→2025",
       "Fonte 2016", "Fonte 2019", "Fonte 2022", "Fonte 2025",
       "Classificação do dado", "Observações metodológicas"])
THW = [7, 34, 30, 16, 14, 12, 12, 12, 12, 12, 12, 12, 12, 20, 20, 20, 20, 14, 60]


def write_theme(sheet, ttl, sub, rows, notes):
    ws = wb[sheet]
    title(ws, ttl, sub)
    header(ws, 3, TH, THW)
    start = 4
    for i, r in enumerate(rows):
        n = start + i
        un = r["un"]
        for c, v in enumerate([r["cod"], r["ind"], r["conc"], r["amb"], un], 1):
            ws.cell(row=n, column=c, value=v)
        for y in YEARS:
            col = YCOL[y]
            v = r["V"][y]
            cell = ws[f"{col}{n}"]
            cell.value = v
            cell.font = F_INP
            if isinstance(v, (int, float)):
                cell.number_format = FMT.get(un, FMT_NUM)
            else:
                cell.alignment = WRAP
        for j, (a, b) in enumerate(PAIRS):
            c = ws.cell(row=n, column=10 + j)
            ca, cb = f"{YCOL[a]}{n}", f"{YCOL[b]}{n}"
            if un == "%":
                c.value = f'=IFERROR({cb}-{ca},"n.d.")'
                c.number_format = PP
            else:
                c.value = f'=IFERROR({cb}/{ca}-1,"n.d.")'
                c.number_format = PCT
        for j, y in enumerate(YEARS):
            ws.cell(row=n, column=14 + j, value=r["FT"][y])
        ws.cell(row=n, column=18, value=r["tipo"])
        ws.cell(row=n, column=19, value=r["obs"] or "—")
        for c in range(1, len(TH) + 1):
            cell = ws.cell(row=n, column=c)
            cell.border = BORDER
            cell.fill = FILL[r["tipo"]]
            if c not in (6, 7, 8, 9):
                cell.font = F_TXT
            if c <= 5 or c >= 14:
                cell.alignment = WRAP
    last = start + len(rows) - 1
    if rows:
        ws.auto_filter.ref = f"A3:{get_column_letter(len(TH))}{last}"
    ws.freeze_panes = "C4"
    footnotes(ws, last + 2, notes)


write_theme("LOA detalhada (órgão, GND)",
            "LOA e execução orçamentária da União – detalhamento por órgão e por grupo de natureza de despesa",
            "Complementa a aba 'LOA e execução orçamentária' do relatório fiscal (que é só por função) com o recorte por órgão/Poder e por GND (pessoal, juros, custeio, investimentos, inversões, amortização).",
            LOA_ROWS,
            ["Fonte preferencial: SIGA Brasil (Senado) e SIOP; na falta de exportação direta, notas técnicas do Congresso sobre a LOA de cada ano."])

write_theme("Segurança pública",
            "Segurança pública – estatísticas (não monetárias)",
            "Mortes violentas intencionais, letalidade policial, efetivo policial e ocorrências, com base no Anuário Brasileiro de Segurança Pública (FBSP/Sinesp).",
            SEG_ROWS,
            ["MVI (mortes violentas intencionais) engloba homicídio doloso, feminicídio, latrocínio, lesão corporal seguida de morte e mortes por intervenção policial."])

write_theme("Pacto federativo",
            "Pacto federativo – repasses da União a estados e municípios por grande área",
            "Transferências constitucionais (FPE/FPM, sem classificação por área) apresentadas à parte das transferências legais/específicas por finalidade (saúde – SUS fundo a fundo; educação – FNDE/Fundeb; assistência social – FNAS/SUAS).",
            FED_ROWS,
            ["FPE e FPM são partilha de receita e não têm classificação por área/finalidade — tratados em linha própria, não somados às transferências por área."])

write_theme("Educação - matrículas",
            "Educação – matrículas e taxas de rendimento (números, não R$)",
            "Censo Escolar da Educação Básica e Censo da Educação Superior (Inep): matrículas, escolas, aprovação/reprovação/abandono, ingressantes e concluintes.",
            EDU_ROWS,
            ["Dados de 2025 do Censo Escolar/Educação Superior costumam ser divulgados só no início do ano seguinte; quando não disponíveis, ver observação da linha."])

write_theme("Enem e Sisu",
            "Enem e Sisu – inscritos, participantes e vagas",
            "Número de inscritos e participantes efetivos no Enem; inscritos, vagas ofertadas e matriculados via Sisu, por edição.",
            ENEM_ROWS,
            ["Resultados/notas do Enem de um ano costumam sair só no início do ano seguinte; inscrições, por serem anteriores à prova, já ficam disponíveis no próprio ano."])

# ---------------------------------------------------------------- resumo executivo
ws = wb["Resumo executivo"]
title(ws, "Tabela complementar – Brasil 2016 × 2019 × 2022 × 2025",
      "Indicadores não monetários (e a LOA em granularidade de órgão/GND) que complementam o "
      "Relatorio_economico_fiscal_Brasil_2016_2019_2022_2025.xlsx.")
ws["A4"] = ("Este workbook não repete os valores em R$ já cobertos pelo relatório fiscal principal; "
            "ele adiciona: (a) a LOA detalhada por órgão e grupo de natureza de despesa; (b) estatísticas de "
            "segurança pública; (c) repasses da União a estados/municípios por grande área (pacto federativo); "
            "e (d) números de matrículas, rendimento escolar, Enem e Sisu.")
ws["A4"].font = F_TXT
ws["A4"].alignment = WRAP
ws.column_dimensions["A"].width = 110
ws.row_dimensions[4].height = 60

# ---------------------------------------------------------------- fontes e metodologia
wf = wb["Fontes e metodologia"]
title(wf, "Fontes e metodologia",
      f"Todas as fontes consultadas em {ACESSO}. Confiabilidade: Alta = fonte oficial primária; "
      "Média = imprensa/entidade setorial ou anúncio.")
FC = ["ID", "Título da fonte", "Instituição", "URL", "Data da publicação", "Ano de referência",
      "Indicador utilizado", "Página ou tabela", "Observações", "Nível de confiabilidade"]
header(wf, 3, FC, [6, 40, 26, 50, 16, 14, 34, 22, 60, 16])
for i, row in enumerate(FONTES):
    n = 4 + i
    for c, v in enumerate(row, 1):
        cell = wf.cell(row=n, column=c, value=v)
        cell.font = F_TXT
        cell.border = BORDER
        cell.alignment = WRAP
        if c == 4 and isinstance(v, str) and v.startswith("http"):
            cell.hyperlink = v
            cell.font = Font(name=ARIAL, size=9, color="0563C1", underline="single")
    fill = FILL["OFICIAL"] if row[9].startswith("Alta") else FILL["IMPRENSA/SETORIAL"]
    for c in range(1, 11):
        wf.cell(row=n, column=c).fill = fill
lastf = 4 + len(FONTES) - 1 if FONTES else 3
if FONTES:
    wf.auto_filter.ref = f"A3:J{lastf}"
wf.freeze_panes = "B4"
n = lastf + 2
wf.cell(row=n, column=1, value="Dados não localizados ou só aproximados – tentativas de busca").font = F_BLD
for j, h in enumerate(["Item", "Fontes tentadas", "Resultado / tratamento"]):
    c = wf.cell(row=n + 1, column=[2, 4, 9][j], value=h)
    c.font = F_HDR
    c.fill = HDR_FILL
for i, (a, b, c_) in enumerate(TENTATIVAS):
    m = n + 2 + i
    for col, v in ((2, a), (4, b), (9, c_)):
        cell = wf.cell(row=m, column=col, value=v)
        cell.font = F_TXT
        cell.alignment = WRAP
        cell.fill = FILL["NÃO LOCALIZADO"]

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

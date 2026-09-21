// Conteudo da secao "Pesquisa": achados e indicadores dos capitulos 3-6 e das
// Considerações Finais, em formato de cards -- reaproveita o texto e as figuras reais
// ja extraidas da dissertacao (ver web_app/content_export/). Nao substitui a leitura
// integral (isso e o papel de "Dissertação"); e um resumo navegavel dos achados.

export interface PesquisaCard {
  value: string;
  label: string;
}

export interface PesquisaImage {
  file: string;
  caption: string;
}

export interface PesquisaTema {
  slug: string;
  icon: string;
  title: string;
  summary: string;
  intro: string[];
  cards: PesquisaCard[];
  images: PesquisaImage[];
  chapterSlug: string;
  chapterLabel: string;
}

const temas: PesquisaTema[] = [
  {
    slug: 'o-estado-como-arquiteto-do-mercado',
    icon: 'Landmark',
    title: 'O Estado como arquiteto do mercado',
    summary: 'Como metas sem recursos, flexibilização regulatória e austeridade fiscal fabricaram a hegemonia privada na EaD.',
    intro: [
      'A hegemonia privada na EaD não resultou de competição aberta entre setores público e privado. Foi fabricada por mecanismos convergentes: metas ambiciosas sem os recursos públicos necessários para sua execução, sucessivas ondas de flexibilização regulatória e o congelamento dos gastos federais justamente quando a expansão era exigida do setor público.',
      'Sob a perspectiva de Bourdieu, toda política é efeito das forças que disputam sua direção. O Plano Nacional de Educação (2014-2024) precisa ser lido, como propõe Ball, como texto e processo: seus efeitos não decorrem apenas do que está escrito, mas do que é operacionalmente possível diante da austeridade fiscal e da captura regulatória.',
    ],
    cards: [
      { value: 'Metas 12, 15 e 16', label: 'Do PNE 2014-2024, estabelecidas sem alocação dos recursos públicos necessários à sua execução' },
      { value: '3 ondas', label: 'De flexibilização regulatória da EaD entre 1996 e 2024' },
      { value: 'Decretos 9.057/2017 e 9.235/2017', label: 'Eliminam limites de polos EaD e simplificam a acreditação de instituições privadas' },
      { value: 'EC nº 95/2016', label: 'Congela os gastos federais por vinte anos, asfixiando as Universidades Federais' },
    ],
    images: [
      { file: 'grafico_02', caption: 'Orçamento destinado à educação superior (em bilhões de R$), 2006-2024' },
    ],
    chapterSlug: 'as-politicas-de-ead-e-a-reconfiguracao-da-educacao-superior-brasileira',
    chapterLabel: 'Capítulo 4 — As Políticas de EaD e a Reconfiguração da Educação Superior Brasileira',
  },
  {
    slug: 'a-explosao-da-ead-privada',
    icon: 'TrendingUp',
    title: 'A explosão da EaD privada',
    summary: 'A magnitude da inversão entre matrículas presenciais e a distância no Brasil, geral e nas licenciaturas.',
    intro: [
      'Os dados do Censo da Educação Superior (INEP), processados por meio de um Data Warehouse próprio, revelam a magnitude da transformação: entre 2014 e 2024, a modalidade a distância deixou de ser marginal para se tornar o principal vetor de acesso à educação superior no Brasil — e, de forma ainda mais acentuada, à formação de professores.',
      'A inversão no campo específico das licenciaturas seguiu o mesmo padrão, com os ingressantes em EaD ultrapassando 80% do total a partir de 2022.',
    ],
    cards: [
      { value: '+286,73%', label: 'Matrículas EaD no Brasil: de 1.341.876 (2014) para 5.189.376 (2024)' },
      { value: '-22,47%', label: 'Matrículas presenciais no Brasil: de 6.497.889 (2014) para 5.037.875 (2024)' },
      { value: '+117,74%', label: 'Matrículas EaD em licenciaturas: de 540.693 (2014) para 1.177.315 (2024)' },
      { value: '-41,54%', label: 'Matrículas presenciais em licenciaturas: de 925.855 (2014) para 541.262 (2024)' },
      { value: '80%+', label: 'Dos ingressantes em licenciaturas via EaD a partir de 2022' },
    ],
    images: [
      { file: 'grafico_10', caption: 'Evolução das matrículas por modalidade de ensino no Brasil (2014-2024)' },
      { file: 'grafico_11', caption: 'Evolução das matrículas por tipo de rede e modalidade de ensino (2014-2024)' },
    ],
    chapterSlug: 'as-politicas-de-ead-e-a-reconfiguracao-da-educacao-superior-brasileira',
    chapterLabel: 'Capítulo 4 — O Plano Nacional de Educação (2014-2024) e a formação de professores',
  },
  {
    slug: 'os-grandes-conglomerados-educacionais',
    icon: 'Building2',
    title: 'Os grandes conglomerados educacionais',
    summary: 'Cinco grupos privados concentraram a expansão da EaD no Brasil, com estratégias e modelos de negócio distintos.',
    intro: [
      'A consolidação da hegemonia privada não foi um fenômeno monolítico, mas um campo disputado por diferentes teses de investimento. Entre 2005 e 2024, cinco grupos se destacaram como arquitetos centrais da reconfiguração do campo: Cogna, YDUQS, Ser Educacional, Vitru e Ânima.',
      'Observam-se dois grandes eixos estratégicos de expansão: o modelo tradicional de aquisição de ativos físicos (campi presenciais) e o modelo contemporâneo de expansão em rede digital-híbrida (asset-light), focado na capilaridade de polos de EaD.',
    ],
    cards: [
      { value: 'Cogna Educação', label: 'Megafusões presenciais e pivô para EaD, com padronização curricular' },
      { value: 'Vitru Educação', label: 'Modelo asset-light: desmaterialização do campus e logística educacional em rede' },
      { value: 'YDUQS', label: 'Hibridização premium e expansão metropolitana da EaD' },
      { value: 'Ânima Educação', label: 'Aquisições seletivas com foco em prestígio e portfólio de marcas' },
      { value: 'Ser Educacional', label: 'Dominação regional e interiorização, com foco de baixo custo' },
    ],
    images: [
      { file: 'quadro_02', caption: 'Estratégias, capitais dos conglomerados e efeitos estruturais produzidos' },
      { file: 'figura_05', caption: 'Evolução da capilaridade dos polos EaD da Cogna Educação (2005-2014-2024)' },
    ],
    chapterSlug: 'as-politicas-de-ead-e-a-reconfiguracao-da-educacao-superior-brasileira',
    chapterLabel: 'Capítulo 4 — Os principais grupos empresariais da educação superior brasileira',
  },
  {
    slug: 'as-universidades-federais-em-retracao',
    icon: 'Building',
    title: 'As Universidades Federais em retração',
    summary: 'Enquanto o setor privado se expande, as UFs mantêm trajetória de estabilidade, leve retração e evasão crescente.',
    intro: [
      'Em contraste com a rápida expansão do setor privado, as Universidades Federais mantiveram trajetória marcada por estabilidade, leve retração e ausência de movimentos expansivos significativos nas licenciaturas entre 2014 e 2024.',
      'O EaD federal próprio não conseguiu estabelecer presença territorial estável, permanecendo estruturalmente dependente do sistema UAB. A retração dos campi, a dependência da UAB e a heterogeneidade das estratégias institucionais produziram impactos diretos sobre a capacidade do sistema federal de formar professores, atrair novos estudantes e reter aqueles que ingressam.',
    ],
    cards: [
      { value: 'Estabilidade e leve retração', label: 'Na oferta presencial de cursos de licenciatura nas UFs (2014-2024)' },
      { value: 'Dependência estrutural da UAB', label: 'Único vetor de expansão territorial da EaD pública nas licenciaturas' },
      { value: 'Evasão crescente', label: 'Desligados, transferidos e trancados aumentam ao longo da década' },
      { value: 'Setor privado absorve em massa', label: 'Os ingressantes e concluintes que as UFs não retêm' },
    ],
    images: [
      { file: 'grafico_40', caption: 'Evolução das matrículas nas licenciaturas das UFs por modalidade (2014-2024)' },
      { file: 'grafico_44', caption: 'Evasão total nos cursos de licenciatura nas UFs (2014-2024)' },
    ],
    chapterSlug: 'a-modalidade-ead-nas-universidades-publicas-federais-analise-dos-indicadores-dos-cursos-de-licenciaturas-2014-2024',
    chapterLabel: 'Capítulo 5 — A Modalidade EaD nas Universidades Públicas Federais',
  },
  {
    slug: 'politicas-e-estrategias-institucionais-das-ufs',
    icon: 'Users',
    title: 'Políticas e estratégias institucionais das UFs',
    summary: 'Da resistência à omissão estratégica: como as federais responderam (ou não) à concorrência do setor privado.',
    intro: [
      'Diante da hegemonia privada na EaD, a resposta institucional das Universidades Federais foi heterogênea — combinando ações reais de ampliação, ausências estratégicas, tensões internas e, em muitos casos, uma retração que redefine o próprio papel público da instituição.',
    ],
    cards: [
      { value: 'Ações reais de ampliação e resistência', label: 'Iniciativas institucionais que buscaram enfrentar a concorrência privada' },
      { value: 'Ausências estratégicas', label: 'O "não agir" como posição de campo diante da expansão privada' },
      { value: 'Tensões internas', label: 'Corpo docente, gestão e estudantes em disputa sobre os rumos da EaD pública' },
      { value: 'A retração estrutural', label: 'Como redefinição do papel público das UFs no campo da formação docente' },
      { value: 'A fragilidade institucional da EaD pública', label: 'Como evidência da retração estatal no financiamento e na regulação' },
      { value: 'A bifurcação formativa', label: 'E o risco de um apartheid educacional entre formação pública e privada' },
    ],
    images: [
      { file: 'tabela_21', caption: 'Tipologias institucionais das UFs diante do EaD em 2024' },
    ],
    chapterSlug: 'as-universidades-federais-e-a-ead-politicas-e-estrategias-institucionais',
    chapterLabel: 'Capítulo 6 — As Universidades Federais e a EaD: Políticas e Estratégias Institucionais',
  },
  {
    slug: 'sintese-dos-achados',
    icon: 'Flag',
    title: 'Síntese: Considerações Finais',
    summary: 'Os quatro núcleos de evidência que sintetizam a pesquisa e os números que marcam a virada histórica de 2014-2024.',
    intro: [
      'A pesquisa articulou três planos analíticos — teórico (Cap. 3), político-estrutural (Cap. 4) e institucional (Cap. 5 e 6) — cuja integração permite uma síntese em quatro núcleos de evidência: a arquitetura política da assimetria, a reconfiguração estrutural do campo, o papel das Universidades Federais e a bifurcação formativa resultante.',
      'O Estado não foi árbitro neutro nesse processo: foi arquiteto do mercado. A universidade pública federal, historicamente protagonista da formação docente, tornou-se agente residual em um campo que ela mesma ajudou a construir.',
    ],
    cards: [
      { value: '+286,73%', label: 'Matrículas EaD no Brasil (2014-2024)' },
      { value: '-22,47%', label: 'Matrículas presenciais no Brasil (2014-2024)' },
      { value: '+117,74%', label: 'Matrículas EaD em licenciaturas (2014-2024)' },
      { value: '-41,54%', label: 'Matrículas presenciais em licenciaturas (2014-2024)' },
      { value: '80%+', label: 'Dos ingressantes em licenciaturas via EaD em 2024' },
      { value: '~70%', label: 'Das matrículas em formação docente em IES privadas com fins lucrativos' },
    ],
    images: [],
    chapterSlug: 'consideracoes-finais',
    chapterLabel: 'Considerações Finais',
  },
];

export default temas;

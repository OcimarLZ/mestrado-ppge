// Conteudo da apresentacao de defesa (28 slides), escrito a partir do conteudo real
// da dissertacao (nao e uma copia dos slides de qualificacao, que traziam resultados
// preliminares e secoes "a definir"). Ver web_app/content_export/ para a extracao
// original dos textos e figuras usados aqui.

export type SlideImage = { file: string; caption?: string };
// "icon" usa um icone Lucide; "label" usa um selo de texto curto (ex: "Q1", "i") --
// so um dos dois costuma ser usado por item.
export type IconItem = { icon?: string; label?: string; text: string };
export type CardItem = { icon?: string; title: string; text: string };
export type Column = { icon?: string; title: string; items: string[] };

export type ComparisonImage = { before: SlideImage; after: SlideImage; beforeLabel: string; afterLabel: string };
export type SlideLink = { label: string; to: string };
// Variante do slide 'stats' em que os cards sao agrupados sob um card maior por grupo
// (ex: um grupo por Meta do PNE, com os indicadores daquela meta como sub-cards).
export type StatGroup = { title: string; stats: { value: string; label: string }[] };

export interface Slide {
  kind: 'cover' | 'section' | 'text' | 'icons' | 'image' | 'images' | 'comparison' | 'stats' | 'cards' | 'columns' | 'closing';
  title: string;
  subtitle?: string;
  bullets?: string[];
  items?: IconItem[];
  cards?: CardItem[];
  columns?: Column[];
  image?: SlideImage;
  images?: SlideImage[];
  comparison?: ComparisonImage;
  stats?: { value: string; label: string }[];
  statGroups?: StatGroup[];
  note?: string;
  showLogos?: boolean;
  footerNote?: string;
  backgroundImage?: string;
  centerBullets?: boolean;
  centerContent?: boolean;
  raiseContent?: boolean;
  wideItems?: boolean;
  largeText?: boolean;
  cardsRowsOf3?: boolean;
  sideBullets?: boolean;
  links?: SlideLink[];
  imageMaxHeight?: string;
  secondaryImage?: SlideImage;
}

const slides: Slide[] = [
  {
    kind: 'cover',
    title: 'Educação a Distância no Brasil',
    subtitle: 'O público e o privado na formação de professores (2014-2024)',
    bullets: [
      'Ocimar Luis Zolin',
      'Orientador: Prof. Dr. Joviles Vitório Trevisol',
      'Programa de Pós-Graduação em Educação — UFFS',
    ],
    showLogos: true,
    backgroundImage: 'foto_campus_uffs_chapeco',
    footerNote: 'Chapecó, 23 de outubro de 2026',
  },
  {
    kind: 'text',
    title: '',
    bullets: [
      '"Ninguém educa ninguém, ninguém educa a si mesmo, os homens se educam entre si, mediatizados pelo mundo."',
      '— Paulo Freire, 1987',
    ],
  },
  {
    kind: 'image',
    title: '',
    image: {
      file: 'mapa_municipios_ead_2006_2014_2024',
      caption: 'Municípios brasileiros com presença de polos EaD — 2006, 2014 e 2024',
    },
    bullets: [
      'O impacto da Educação a Distância (EaD) nos cursos de licenciatura no Brasil',
      'Análise das políticas e dinâmicas que transformaram a formação de professores no período do PNE 2014-2024',
      'Estratégias adotadas pelas Universidades Federais perante a massificação da EaD privada',
    ],
    centerBullets: true,
  },
  {
    kind: 'icons',
    title: 'Justificativa: uma mercantilização inesperada',
    items: [
      { icon: 'AlertTriangle', text: 'Transformação estrutural da formação docente sem precedentes durante a vigência do PNE (2014-2024)' },
      { icon: 'Landmark', text: 'A EaD foi fomentada pelo Estado para reduzir o déficit de professores sem diplomação adequada' },
      { icon: 'TrendingUp', text: 'Mas os dados mais recentes mostram as IES privadas com fins lucrativos dominando esse campo' },
      { icon: 'Scale', text: 'Inversão dos indicadores: matrículas privadas em EaD explodem enquanto as IES públicas presenciais estagnam e evadem' },
      { icon: 'ShieldAlert', text: 'Grande preocupação dos intelectuais e profissionais da educação quanto ao risco da precarização na formação docente' },
    ],
    centerContent: true,
    raiseContent: true,
  },
  {
    kind: 'icons',
    title: 'Relevância da pesquisa',
    items: [
      { icon: 'Database', text: 'Intersecção entre pesquisa educacional e Ciência de Dados: Data Warehouse próprio e ETL sobre dezenas de milhões de registros do Censo da Educação Superior' },
      { icon: 'CalendarClock', text: 'Realizada no término do PNE 2014-2024, oferecendo subsídios baseados em evidências para o próximo ciclo de planejamento educacional' },
      { icon: 'Building2', text: 'Relevância institucional para a UFFS: articula a linha de Políticas Educacionais do PPGE com a atuação técnica do autor na Secretaria de Tecnologia da Informação (SETI)' },
    ],
    centerContent: true,
    raiseContent: true,
  },
  {
    kind: 'icons',
    title: 'Questões de pesquisa',
    items: [
      { label: 'Q1', text: 'Como a flexibilização regulatória e as políticas neoliberais de educação superior impulsionaram a modalidade EaD no período do PNE (2014-2024)?' },
      { label: 'Q2', text: 'De que maneira as tensões entre o interesse público e o mercado moldaram os instrumentos de regulação e avaliação do MEC/INEP, permitindo que a massificação da EaD se sobrepusesse a um projeto crítico de formação de professores?' },
      { label: 'Q3', text: 'Como os microdados da educação superior entre 2014 e 2024 evidenciam a reconfiguração da oferta de licenciaturas, considerando o comportamento das Universidades Federais frente ao crescimento exponencial das instituições privadas na EaD?' },
      { label: 'Q4', text: 'Quais foram as estratégias institucionais (ou a ausência delas) adotadas pelas Universidades Federais para enfrentar a concorrência do mercado privado e preservar a qualidade e a natureza pública da formação docente?' },
    ],
    centerContent: true,
    raiseContent: true,
    wideItems: true,
  },
  {
    kind: 'icons',
    title: 'Objetivo geral',
    items: [
      { icon: 'Target', text: 'Compreender e analisar as reações e estratégias das Universidades Federais frente ao avanço e à consolidação da hegemonia das instituições privadas na oferta de cursos de licenciatura a distância, em um contexto de precarização da formação docente impulsionado pelas políticas educacionais vigentes durante o PNE (2014-2024)' },
    ],
    centerContent: true,
    wideItems: true,
    largeText: true,
  },
  {
    kind: 'icons',
    title: 'Objetivos específicos',
    items: [
      { label: 'O1', text: 'Analisar o impacto da flexibilização regulatória e das políticas educacionais neoliberais na expansão da EaD no período do PNE (2014-2024)' },
      { label: 'O2', text: 'Examinar como as tensões entre interesse público e lógica de mercado moldaram os instrumentos de regulação e avaliação do MEC/INEP, favorecendo a massificação da EaD em detrimento de um projeto crítico de formação de professores' },
      { label: 'O3', text: 'Analisar a reconfiguração da oferta de licenciaturas (2014-2024), contrastando o crescimento exponencial do EaD privado com o comportamento institucional das Universidades Federais, a partir dos microdados de cursos, ingressos, concluintes e evasão' },
      { label: 'O4', text: 'Investigar as estratégias institucionais — ou a ausência destas — adotadas pelas Universidades Federais para enfrentar a concorrência do mercado privado e preservar a natureza pública e a qualidade da formação docente' },
    ],
    centerContent: true,
    raiseContent: true,
    wideItems: true,
  },
  {
    kind: 'columns',
    title: 'Percurso metodológico',
    centerContent: true,
    raiseContent: true,
    columns: [
      {
        icon: 'FlaskConical',
        title: 'Tipo de pesquisa',
        items: [
          'Pesquisa quantitativa, documental e ex-post-facto, sobre registros e microdados já consolidados',
          'Recorte 2014-2024 (vigência do PNE), com contextualização histórica desde 2005',
          'Interpretação teórico-sociológica a partir de Stephen Ball e Pierre Bourdieu',
        ],
      },
      {
        icon: 'ListChecks',
        title: 'Passos da pesquisa',
        items: [
          'Estado do conhecimento: revisão em BDTD, CAPES, SciELO e RD/UFFS (de ~394 mil ocorrências a 109 obras selecionadas)',
          'Análise documental da legislação e das políticas regulatórias da EaD',
          'Coleta e ETL dos microdados (INEP, IBGE, IPEA, CVM) num Data Warehouse dimensional',
          'Estatística descritiva e comparativa (público × privado, presencial × EaD, regiões)',
        ],
      },
      {
        icon: 'Wrench',
        title: 'Ferramentas utilizadas e construídas',
        items: [
          'SQLite (Data Warehouse) e DBeaver para administração e consultas SQL',
          'Python (Pandas, NumPy, SQLAlchemy) nos processos de ETL; Power BI, Matplotlib e Seaborn nas visualizações',
          'Collaboratio: aplicação web autoral (Python/FastAPI) para gestão e rastreabilidade da pesquisa',
          'Zotero para gestão bibliográfica',
        ],
      },
    ],
  },
  {
    kind: 'image',
    title: 'Arquitetura de dados da pesquisa',
    centerContent: true,
    sideBullets: true,
    image: { file: 'figura_18', caption: 'Modelo de dicionário de dados do Data Warehouse projetado' },
    bullets: [
      'Consolidação de múltiplas fontes oficiais num único modelo fato/dimensão',
      'Mais de uma década de séries históricas (Censo da Educação Superior, 2014-2024)',
    ],
    links: [
      { label: 'Visualizar o Apêndice I', to: '/capitulo/apendice-i' },
      { label: 'Painéis Interativos', to: '/paineis-interativos' },
    ],
  },
  {
    kind: 'cards',
    title: 'Referencial teórico: uma arquitetura conceitual',
    subtitle: 'Cinco pilares que se articulam numa progressão, do político ao econômico',
    cards: [
      { icon: 'FileText', title: 'Stephen Ball', text: 'Políticas educacionais como campo de disputas: textos e discursos ambíguos e disputáveis' },
      { icon: 'Layers', title: 'Pierre Bourdieu', text: 'Teoria dos campos: capitais, hegemonia simbólica e agentes em disputa' },
      { icon: 'Landmark', title: 'Raymundo Faoro', text: 'Estamento e patrimonialismo: a porosidade histórica entre público e privado no Estado brasileiro' },
      { icon: 'Cog', title: 'Dardot e Laval', text: 'Neoliberalismo como racionalidade política, não apenas um programa econômico' },
      { icon: 'CircleDollarSign', title: 'Sguissardi, Amaral, Chaves', text: 'Mercantilização e financeirização: a universidade como ativo financeiro' },
    ],
    centerContent: true,
    raiseContent: true,
    largeText: true,
    cardsRowsOf3: true,
  },
  {
    kind: 'icons',
    title: 'Ball: políticas educacionais como campo de disputas',
    items: [
      { icon: 'FileText', text: 'As políticas educacionais são "textos e discursos" produzidos em arenas permeadas por conflitos, interesses econômicos e disputas por interpretação' },
      { icon: 'AlertTriangle', text: 'A expansão da EaD não decorre de escolhas pedagógicas, mas de escolhas regulatórias que favoreceram grandes grupos privados' },
      { icon: 'FileSearch', text: 'Políticas são "ambíguas e disputáveis": conglomerados privados exploram as lacunas dos marcos regulatórios para flexibilizar credenciamentos e reduzir exigências acadêmicas' },
    ],
    centerContent: true,
    raiseContent: true,
  },
  {
    kind: 'icons',
    title: 'Bourdieu: a disputa por hegemonia no campo educacional',
    items: [
      { icon: 'Layers', text: 'A teoria dos campos: a educação superior como espaço social estruturado de posições em confronto' },
      { icon: 'Users', text: 'Estado, conglomerados privados, universidades públicas e organismos multilaterais disputam a autoridade legítima de definir o que é educação superior' },
      { icon: 'Swords', text: 'A reconfiguração do ensino superior é uma disputa estruturada de poder — não uma questão meramente pedagógica ou tecnológica' },
    ],
    centerContent: true,
    raiseContent: true,
  },
  {
    kind: 'icons',
    title: 'Faoro: estamento e patrimonialismo no Estado brasileiro',
    items: [
      { icon: 'Landmark', text: 'Estamento e patrimonialismo mobilizados como pressupostos teórico-contextuais, não como objeto central de investigação' },
      { icon: 'Shuffle', text: 'Descrevem a porosidade histórica entre as esferas pública e privada, nunca plenamente separadas na formação do Estado brasileiro' },
      { icon: 'Handshake', text: 'Essa porosidade torna inteligíveis as trocas de favores e os acordos regulatórios entre governantes e o setor econômico educacional' },
    ],
    centerContent: true,
    raiseContent: true,
  },
  {
    kind: 'icons',
    title: 'Neoliberalismo, escalabilidade e performatividade (Dardot, Laval e Ball)',
    items: [
      { icon: 'Cog', text: 'Neoliberalismo não como um conjunto de políticas econômicas, mas como uma racionalidade política — uma forma específica de governar' },
      { icon: 'Building2', text: 'Introduz a lógica da concorrência e da gestão empresarial em esferas antes regidas por outros princípios, incluindo a educação pública' },
      { icon: 'Zap', text: 'A EaD é sua materialização mais acabada: escalabilidade, padronização curricular e gestão algorítmica construídas para uma economia educacional orientada por desempenho e retorno sobre investimento' },
      { icon: 'ClipboardCheck', text: 'Performatividade (Ball): ENADE, Conceito Institucional e IGC funcionam como selos de mercado que legitimam modelos de baixo custo e alta escala, substituindo a garantia de qualidade pública pela produção de hegemonia privada' },
    ],
    centerContent: true,
    raiseContent: true,
    wideItems: true,
  },
  {
    kind: 'icons',
    title: 'Mercantilização e financeirização (Sguissardi, Amaral, Chaves)',
    items: [
      { icon: 'CircleDollarSign', text: 'A educação superior se converte em ativo financeiro: fusões, aquisições, abertura de capital (IPOs) e instrumentos do capitalismo financeiro' },
      { icon: 'ArrowRightLeft', text: 'O valor econômico, e não o valor formativo, torna-se o eixo organizador das decisões acadêmicas' },
      { icon: 'Gauge', text: 'A EaD é o modelo ideal para essa lógica: maximiza a relação aluno/docente e viabiliza margens de lucro em escala nacional' },
    ],
    centerContent: true,
    raiseContent: true,
  },
  {
    kind: 'image',
    title: 'Orçamento da educação superior brasileira (2006-2024)',
    centerContent: true,
    centerBullets: true,
    sideBullets: true,
    image: { file: 'grafico_02', caption: 'Orçamento destinado à educação superior (em bilhões de R$), 2006-2024' },
    secondaryImage: { file: 'tabela_03', caption: 'Tabela 3 — Orçamento destinado à educação superior (em bilhões de R$): 2006-2024' },
    bullets: [
      'O PIB brasileiro cresce <span class="slide-pos">112,72%</span> entre 2006 e 2024, mas o orçamento da educação superior avança apenas <span class="slide-pos">49,93%</span> — e os investimentos do MEC recuam <span class="slide-neg">48,71%</span>',
      'Emenda Constitucional nº 95/2016 congela os gastos federais por vinte anos: asfixia orçamentária das Universidades Federais justamente quando o PNE demandava expansão',
      'A partir de 2011, a expansão da EBSERH desloca parte da força de trabalho dos hospitais universitários do regime estatutário para contratos celetistas sob métricas empresariais — mesma racionalidade gerencial que atinge o restante da rede federal',
    ],
  },
  {
    kind: 'icons',
    title: 'Flexibilização regulatória: o Estado como arquiteto do mercado',
    items: [
      { icon: 'FileSignature', text: 'Sucessivas mudanças normativas, sobretudo a partir de 2017, flexibilizam credenciamento, autorização e oferta de polos EaD, reduzindo exigências antes aplicadas ao presencial' },
      { icon: 'TrendingUp', text: 'A proporção de matrículas privadas financiadas por FIES e ProUni salta de <span class="slide-pos">6,39%</span> (2006) para <span class="slide-pos">33,06%</span> (2014) — o Estado cria dependência sistêmica entre mantenedoras privadas e financiamento público' },
      { icon: 'TrendingDown', text: 'A crise fiscal pós-2015 inverte o mecanismo: os contratos do FIES caem de <span class="slide-neg">1,34 milhão</span> (2015) para <span class="slide-neg">155.560</span> (2024) — queda de <span class="slide-neg">88,4%</span>' },
      { icon: 'ArrowRightLeft', text: 'Sem financiamento presencial, a EaD privada — sem exigência de polo físico consolidado — torna-se a rota de expansão de menor custo e maior margem' },
    ],
    centerContent: true,
    raiseContent: true,
  },
  {
    kind: 'image',
    title: 'Evolução das matrículas por modalidade de ensino',
    centerContent: true,
    centerBullets: true,
    raiseContent: true,
    image: { file: 'grafico_10', caption: 'Evolução das matrículas por modalidade de ensino no Brasil (2014-2024)' },
    bullets: [
      'EaD: de <span class="slide-pos">1.341.876</span> (2014) para <span class="slide-pos">5.189.376</span> (2024) — alta de <span class="slide-pos">286,73%</span>',
      'Presencial: de <span class="slide-neg">6.497.889</span> (2014) para <span class="slide-neg">5.037.875</span> (2024) — retração de <span class="slide-neg">22,47%</span>',
    ],
  },
  {
    kind: 'image',
    title: 'Matrículas por tipo de rede e modalidade',
    centerContent: true,
    centerBullets: true,
    raiseContent: true,
    image: { file: 'grafico_11', caption: 'Evolução das matrículas por tipo de rede e modalidade de ensino (2014-2024)' },
    bullets: [
      'Em 2014, o presencial tinha <span class="slide-pos">2.386.758</span> ingressantes contra <span class="slide-pos">727.752</span> na EaD — proporção de mais de 3 para 1; a EaD ultrapassa o presencial de forma definitiva em 2020',
      'A expansão da EaD é liderada quase integralmente pelo setor privado; o setor público (presencial + EaD) mantém trajetória estável, sem acompanhar a curva privada',
    ],
  },
  {
    kind: 'image',
    title: 'O colapso do FIES presencial',
    centerContent: true,
    centerBullets: true,
    raiseContent: true,
    image: { file: 'grafico_20', caption: 'Retração do FIES e explosão da EaD privada (2014-2024)' },
    bullets: [
      'De <span class="slide-neg">1,34 milhão</span> de contratos ativos (2015) para <span class="slide-neg">155.560</span> (2024) — queda de <span class="slide-neg">88,4%</span>',
      'A retração do financiamento presencial coincide, ano a ano, com a explosão das matrículas EaD privadas',
    ],
  },
  {
    kind: 'stats',
    title: 'As Metas 12, 15 e 16 do PNE: cumprimento formal, não material',
    centerContent: true,
    raiseContent: true,
    statGroups: [
      {
        title: 'Meta 12 — Expansão da educação superior',
        stats: [
          { value: '<span class="slide-pos">31% → 48%</span>', label: 'Taxa bruta de matrícula (meta: 50%)' },
          { value: '<span class="slide-pos">17% → 21%</span>', label: 'Taxa líquida de matrícula (meta: 33%)' },
          { value: '<span class="slide-neg">13%</span>', label: 'Participação do setor público no total de matrículas (meta: 40%)' },
        ],
      },
      {
        title: 'Meta 15 — Formação inicial de professores',
        stats: [
          { value: '<span class="slide-pos">68%+</span>', label: 'Das matrículas em licenciaturas são EaD (2024)' },
          { value: '<span class="slide-pos">~90%</span>', label: 'Dessa EaD em licenciaturas é privada com fins lucrativos' },
          { value: '<span class="slide-neg">-41,54%</span>', label: 'Matrículas presenciais em licenciaturas (2014-2024)' },
        ],
      },
      {
        title: 'Meta 16 — Pós-graduação de professores',
        stats: [
          { value: '<span class="slide-pos">31,4% → 48%</span>', label: 'Docentes com pós-graduação (2014-2024)' },
          { value: '43,5%', label: 'Com especialização lato sensu (majoritariamente EaD privada)' },
          { value: '3,4%', label: 'Com mestrado' },
          { value: '1,1%', label: 'Com doutorado' },
        ],
      },
    ],
  },
  {
    kind: 'cards',
    title: 'Os grandes grupos educacionais',
    subtitle: 'Cinco conglomerados — receitas combinadas superiores a R$ 14 bilhões/ano — concentram a expansão da EaD privada, hoje presente em mais de 3.300 municípios',
    centerContent: true,
    centerBullets: true,
    raiseContent: true,
    cards: [
      { title: 'Cogna Educação', text: 'Megafusões presenciais e pivô para EaD, com padronização curricular' },
      { title: 'Vitru Educação', text: 'Modelo asset-light: desmaterialização do campus e logística em rede' },
      { title: 'YDUQS', text: 'Hibridização premium e expansão metropolitana da EaD' },
      { title: 'Ânima Educação', text: 'Aquisições seletivas com foco em prestígio e portfólio de marcas' },
      { title: 'Ser Educacional', text: 'Dominação regional e interiorização, com foco de baixo custo' },
    ],
    image: { file: 'quadro_02', caption: 'Estratégias, capitais dos conglomerados e efeitos estruturais produzidos' },
    bullets: [
      'Síntese comparativa dos cinco grupos sob a lente de Bourdieu e Ball',
      'Efeito comum: hegemonia empresarial e pressão competitiva sobre as instituições federais',
    ],
  },
  {
    kind: 'images',
    title: 'Cogna Educação',
    centerContent: true,
    centerBullets: true,
    images: [
      { file: 'figura_05', caption: 'Evolução da capilaridade dos polos EaD da Cogna Educação (2005-2014-2024)' },
      { file: 'grafico_22', caption: 'Evolução da receita líquida e da EBITDA da Cogna Educação (2018-2024)' },
    ],
    bullets: [
      'Pioneira na oligopolização do setor via megafusões e financeirização',
      'Em 2024: receita líquida de <span class="slide-pos">R$ 6,42 bilhões</span> e EBITDA de <span class="slide-pos">R$ 2,31 bilhões</span>',
    ],
  },
  {
    kind: 'images',
    title: 'Vitru Educação',
    centerContent: true,
    centerBullets: true,
    images: [
      { file: 'figura_06', caption: 'Evolução da capilaridade dos polos EaD da Vitru Educação (2005-2014-2024)' },
      { file: 'grafico_23', caption: 'Evolução da receita líquida e da EBITDA da Vitru Educação (2018-2024)' },
    ],
    bullets: [
      'Modelo asset-light: desmaterialização do campus e logística educacional em rede',
      'Em 2024: receita líquida de <span class="slide-pos">R$ 2,14 bilhões</span> — alta de <span class="slide-pos">459%</span> desde 2018 — e EBITDA de <span class="slide-pos">R$ 483,7 milhões</span>',
    ],
  },
  {
    kind: 'images',
    title: 'YDUQS',
    centerContent: true,
    centerBullets: true,
    images: [
      { file: 'figura_07', caption: 'Evolução da capilaridade dos polos EaD da YDUQS (2005-2014-2024)' },
      { file: 'grafico_24', caption: 'Evolução da receita líquida e da EBITDA da YDUQS (2018-2024)' },
    ],
    bullets: [
      'Dualidade estratégica entre EaD de massa e ensino presencial premium',
      'Em 2024: receita líquida de <span class="slide-pos">R$ 5,35 bilhões</span> — alta de <span class="slide-pos">56%</span> desde 2018 — e EBITDA ajustado de <span class="slide-pos">R$ 1,82 bilhão</span>',
    ],
  },
  {
    kind: 'images',
    title: 'Ânima Educação',
    centerContent: true,
    centerBullets: true,
    images: [
      { file: 'figura_08', caption: 'Evolução da capilaridade dos polos EaD da Ânima Educação (2005-2014-2024)' },
      { file: 'grafico_25', caption: 'Evolução da receita líquida e da EBITDA da Ânima Educação (2018-2024)' },
    ],
    bullets: [
      'Captura de capital simbólico via marcas tradicionais e portfólio segmentado (Inspirali, Ânima Core, Ensino Digital)',
      'Em 2024: receita líquida consolidada de <span class="slide-pos">R$ 3,8 bilhões</span> e margem EBITDA ajustada de <span class="slide-pos">34,5%</span>',
    ],
  },
  {
    kind: 'images',
    title: 'Ser Educacional',
    centerContent: true,
    centerBullets: true,
    images: [
      { file: 'figura_09', caption: 'Evolução da capilaridade dos polos EaD da Ser Educacional (2005-2014-2024)' },
      { file: 'grafico_26', caption: 'Evolução da receita líquida e da EBITDA da Ser Educacional (2018-2024)' },
    ],
    bullets: [
      'Monopólio regional e interiorização, com foco em baixo custo e modelo asset-light',
      'Em 2024: receita líquida consolidada de <span class="slide-pos">R$ 1,98 bilhão</span> e EBITDA de <span class="slide-pos">R$ 461,4 milhões</span>',
    ],
  },
  {
    kind: 'image',
    title: 'Síntese do capítulo 4: reconfiguração e mercantilização da EaD',
    centerContent: true,
    centerBullets: true,
    raiseContent: true,
    imageMaxHeight: '38vh',
    image: {
      file: 'diagrama_ishikawa_reconfiguracao_ead',
      caption: 'Diagrama de causa-efeito (elaborado pelo autor) — três eixos convergindo para a reconfiguração da EaD',
    },
    bullets: [
      'Três eixos convergem para a reconfiguração da EaD: legislação e regulação, financiamento público (FIES/ProUni) e financeirização de mercado (IPOs) — contrapostos pelo ajuste fiscal (EC 95/2016), pelo planejamento estatal (PNE) e por uma fase corretiva (2023-2024)',
      'O eixo "novas diretrizes curriculares" refere-se à Resolução CNE/CP nº 4/2024 e às Portarias nº 2.041/2023 e 158/2024 — a "fase corretiva das autorizações" (Sguissardi, 2015b), não à BNC-Formação',
    ],
  },
  {
    kind: 'image',
    title: 'A trajetória das Universidades Federais',
    image: { file: 'grafico_27', caption: 'Evolução da criação de UFs por década (1920-2019)' },
    bullets: [
      'Rede federal expandida em duas grandes ondas: 1960-1969 e 2000-2009',
      'Instituições historicamente ancoradas no modelo presencial e na indissociabilidade ensino-pesquisa-extensão',
    ],
  },
  {
    kind: 'image',
    title: 'Licenciaturas nas UFs: presencial, EaD e UAB',
    image: { file: 'grafico_40', caption: 'Evolução das matrículas nas licenciaturas das UFs por modalidade (2014-2024)' },
    bullets: [
      'Trajetória de estabilidade e leve retração, sem movimentos expansivos significativos',
      'EaD federal próprio não consolida presença territorial estável — depende estruturalmente da UAB',
    ],
  },
  {
    kind: 'image',
    title: 'Ingressos nas licenciaturas das UFs',
    image: { file: 'grafico_42', caption: 'Dinâmica dos ingressantes nos cursos de licenciatura nas UFs por modalidade de ensino (2014-2024)' },
    bullets: [
      'Capacidade de atração das licenciaturas federais analisada ao longo da década',
      'Contraste direto com o crescimento exponencial de ingressantes no setor privado',
    ],
  },
  {
    kind: 'image',
    title: 'Evasão nas licenciaturas das UFs',
    image: { file: 'grafico_44', caption: 'Evasão total (desligados, transferidos e trancados) nos cursos de licenciatura nas UFs (2014-2024)' },
    bullets: [
      'A evasão expõe fragilidades estruturais do campo público diante das transformações do período',
      'Efeito direto da retração dos campi e do colapso do EaD próprio federal',
    ],
  },
  {
    kind: 'stats',
    title: 'A retração das Universidades Federais em números',
    stats: [
      { value: '<span class="slide-neg">-10,4%</span>', label: 'Matrículas em licenciaturas (<span class="slide-neg">290.966 → 260.741</span>)' },
      { value: '<span class="slide-neg">24,9% → 18,2%</span>', label: 'Participação das UFs no total de matrículas' },
      { value: '<span class="slide-neg">-89%</span>', label: 'Matrículas em EaD própria (<span class="slide-neg">4.333 → 472</span>)' },
      { value: '<span class="slide-neg">-66,7%</span>', label: 'Polos de EaD própria' },
      { value: '<span class="slide-neg">-26,1%</span>', label: 'Matrículas via sistema UAB (<span class="slide-neg">60.026 → 44.339</span>)' },
      { value: '<span class="slide-neg">-18,3%</span> / <span class="slide-neg">-6,2%</span>', label: 'Ingressos / concluintes em licenciaturas' },
    ],
    bullets: [
      'A EaD própria federal entra em colapso justamente no período em que a EaD privada se torna hegemônica',
      'O sistema UAB — única via relevante de EaD pública federal — também recua, sob extrema volatilidade orçamentária e dependência de editais pontuais',
    ],
  },
  {
    kind: 'icons',
    title: 'Cinco tipologias institucionais das UFs diante do EaD',
    items: [
      { label: '14', text: 'Resistência total: licenciaturas integralmente presenciais, sem EaD própria nem via UAB — legitimidade acadêmica associada à presencialidade' },
      { label: '23', text: 'Dependência estrutural da UAB: um terço das UFs concentra 20% ou mais das matrículas de licenciatura no sistema federal de polos UAB' },
      { label: '24', text: 'Presencialidade dominante com EaD complementar via UAB: modalidade a distância incorporada sem deslocar a centralidade do presencial' },
      { label: '6', text: 'EaD própria residual — UFGD, UFPEL, UFPR, UFRN, UFSC e UNIVASF — mas mesmo aí as matrículas variam de apenas 0,3% a 6,2% do total institucional' },
      { label: '2', text: 'Experiências abandonadas: UNIFAL (EaD própria até 2022, UAB até 2013) e UFV (EaD própria até 2016) desistiram da modalidade' },
    ],
  },
  {
    kind: 'images',
    title: 'UFs × setor privado — comparativo direto',
    images: [
      { file: 'grafico_49', caption: 'Matrículas em licenciaturas: UFs × privadas com e sem fins lucrativos (2014-2024)' },
      { file: 'tabela_21', caption: 'Tipologias institucionais das UFs diante do EaD em 2024' },
    ],
    bullets: [
      'Em 2014, o mercado era relativamente equilibrado: privadas com fins lucrativos 40,7%, sem fins lucrativos 30,1%, UFs 23,5%, demais IES públicas 5,8%',
      'Em 2024: privadas com fins lucrativos controlam <span class="slide-pos">66,2%</span> do mercado, as UFs encolhem para <span class="slide-neg">17,3%</span>',
    ],
  },
  {
    kind: 'icons',
    title: 'Ações reais e ausências estratégicas das UFs',
    items: [
      { icon: 'CheckCircle2', text: 'Ações efetivamente implementadas: políticas de permanência estudantil (PNAES) — ainda que limitadas e descontinuadas — e iniciativas pontuais e fragmentadas de EaD própria' },
      { icon: 'XCircle', text: 'Ausência 1: nenhuma UF construiu um sistema federal coordenado de EaD própria em escala' },
      { icon: 'XCircle', text: 'Ausência 2: nenhuma UF liderou uma expansão agressiva do sistema UAB' },
      { icon: 'XCircle', text: 'Ausência 3: políticas sistemáticas de permanência e combate à evasão não se consolidaram' },
      { icon: 'XCircle', text: 'Ausência 4: nenhuma UF disputou competitivamente o espaço ocupado pela EaD privada' },
    ],
  },
  {
    kind: 'stats',
    title: 'Bifurcação formativa: dois circuitos, um só sistema',
    stats: [
      { value: '3,5 : 1', label: 'Evadidos por concluinte nas UFs (2024)' },
      { value: '5,7 : 1', label: 'Evadidos por concluinte no setor privado lucrativo' },
      { value: '2,9 : 1', label: 'Evadidos por concluinte nas demais IES públicas' },
      { value: '3,4 : 1', label: 'Evadidos por concluinte nas privadas sem fins lucrativos' },
    ],
    bullets: [
      'O setor privado lucrativo evade em massa, mas forma uma fração que, dada a escala colossal, ainda supera a produção pública em volume absoluto',
      'Risco de um apartheid educacional: um circuito público de formação mais seletiva e um circuito privado de massa, de menor custo por matrícula e maior evasão relativa',
    ],
  },
  {
    kind: 'stats',
    title: 'Síntese dos achados',
    stats: [
      { value: '<span class="slide-pos">+286,73%</span>', label: 'Matrículas EaD (Brasil, 2014-2024)' },
      { value: '<span class="slide-neg">-22,47%</span>', label: 'Matrículas presenciais (Brasil, 2014-2024)' },
      { value: '<span class="slide-pos">+117,74%</span>', label: 'Matrículas EaD em licenciaturas (2014-2024)' },
      { value: '<span class="slide-neg">-41,54%</span>', label: 'Matrículas presenciais em licenciaturas (2014-2024)' },
      { value: '<span class="slide-pos">80%+</span>', label: 'Dos ingressantes em licenciaturas via EaD em 2024' },
      { value: '<span class="slide-pos">66,2%</span>', label: 'Das matrículas em formação docente em IES privadas com fins lucrativos' },
    ],
    bullets: [
      'O Estado não foi árbitro neutro: foi arquiteto do mercado — metas do PNE sem recursos, flexibilização regulatória, EC 95/2016',
      'A universidade pública federal, historicamente protagonista da formação docente, tornou-se agente residual em um campo que ela mesma ajudou a construir',
    ],
  },
  {
    kind: 'icons',
    title: 'Recomendações para o próximo ciclo de política educacional',
    items: [
      { icon: 'Landmark', text: 'Reconstruir a UAB como política de Estado permanente, não como programa sujeito a editais e descontinuidades orçamentárias' },
      { icon: 'Banknote', text: 'Recompor o orçamento das Universidades Federais para infraestrutura própria de EaD e permanência estudantil' },
      { icon: 'ClipboardCheck', text: 'Redefinir os critérios de avaliação do SINAES, distinguindo formação universitária de mera entrega instrucional' },
      { icon: 'FileSignature', text: 'Regulamentar exigências de qualidade para o EaD em licenciaturas (Decreto nº 12.456/2025)' },
      { icon: 'HandCoins', text: 'Fortalecer políticas de permanência no presencial, como o Programa Pé-de-Meia Licenciaturas (R$ 1.050,00 mensais)' },
    ],
  },
  {
    kind: 'icons',
    title: 'Contribuições da pesquisa',
    items: [
      { icon: 'FlaskConical', text: 'Empírica: mapeamento inédito da expansão privada da EaD nas licenciaturas e do recuo presencial, especialmente nas federais' },
      { icon: 'Cpu', text: 'Metodológica: integração de políticas públicas, microdados em larga escala e Data Warehouse próprio, reprodutível por código' },
      { icon: 'Landmark', text: 'Para políticas públicas: subsídios para o próximo ciclo de planejamento educacional decidir entre aprofundar a bifurcação formativa ou reconstruir o pacto estatal pela formação de professores' },
    ],
  },
  {
    kind: 'closing',
    title: 'Obrigado',
    subtitle: 'Educação a Distância no Brasil: o público e o privado na formação de professores (2014-2024)',
    bullets: [
      'Ocimar Luis Zolin',
      'Orientador: Prof. Dr. Joviles Vitório Trevisol',
      'Banca: Prof. Dr. Jaime Giolo (UFFS) · Prof. Dr. Lucídio Bianchetti (UFSC) · Prof. Dr. Derlan Trombeta (UFFS)',
      'Programa de Pós-Graduação em Educação — UFFS',
    ],
    showLogos: true,
  },
];

export default slides;

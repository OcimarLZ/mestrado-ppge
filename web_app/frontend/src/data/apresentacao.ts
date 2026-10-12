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
// Tabela HTML (nao imagem) para dados que nao existem como figura/tabela numerada na
// dissertacao -- renderizada no lugar da imagem nos slides kind:'image' com sideBullets.
export type SlideTable = { headers: string[]; rows: string[][] };

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
  table?: SlideTable;
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
  secondaryImages?: SlideImage[];
  secondaryImageMaxHeight?: string;
  contactInfo?: string[];
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
    secondaryImages: [
      { file: 'tabela_03', caption: 'Tabela 3 — Orçamento destinado à educação superior (em bilhões de R$): 2006-2024' },
      { file: 'tabela_04', caption: 'Tabela 4 — Orçamento das maiores UFs brasileiras (em bilhões de R$): 2006-2024' },
    ],
    bullets: [
      'O PIB brasileiro cresce <span class="slide-pos">112,72%</span> entre 2006 e 2024, mas o orçamento da educação superior avança apenas <span class="slide-pos">49,93%</span> — e os investimentos do MEC recuam <span class="slide-neg">48,71%</span>, considerando o orçamento de 2024 e 2014',
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
          { value: '<span class="slide-neg">31% → 48%</span>', label: 'Taxa bruta de matrícula (meta: 50%)' },
          { value: '<span class="slide-red">17% → 21%</span>', label: 'Taxa líquida de matrícula (meta: 33%)' },
          { value: '<span class="slide-red">13%</span>', label: 'Participação do setor público no total de matrículas (meta: 40%)' },
        ],
      },
      {
        title: 'Meta 15 — Formação inicial de professores',
        stats: [
          { value: '<span class="slide-red">68%+</span>', label: 'Das matrículas em licenciaturas são EaD (2024)' },
          { value: '<span class="slide-red">~90%</span>', label: 'Dessa EaD em licenciaturas é privada com fins lucrativos' },
          { value: '<span class="slide-red">-41,54%</span>', label: 'Matrículas presenciais em licenciaturas (2014-2024)' },
        ],
      },
      {
        title: 'Meta 16 — Pós-graduação de professores',
        stats: [
          { value: '<span class="slide-pos">31,4% → 48%</span>', label: 'Docentes com pós-graduação (2014-2024)' },
          { value: '<span class="slide-neg">43,5%</span>', label: 'Com especialização lato sensu (majoritariamente EaD privada)' },
          { value: '<span class="slide-red">3,4%</span>', label: 'Com mestrado' },
          { value: '<span class="slide-red">1,1%</span>', label: 'Com doutorado' },
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
    centerContent: true,
    centerBullets: true,
    raiseContent: true,
    image: { file: 'grafico_27', caption: 'Evolução da criação de UFs por década (1920-2019)' },
    bullets: [
      'Rede federal expandida em duas grandes ondas: 1960-1969 e 2000-2009',
      'Instituições historicamente ancoradas no modelo presencial e na indissociabilidade ensino-pesquisa-extensão',
    ],
  },
  {
    kind: 'image',
    title: 'Expansão institucional das Universidades Federais',
    centerContent: true,
    centerBullets: true,
    raiseContent: true,
    image: { file: 'figura_10', caption: 'Municípios com campus federal ofertando licenciaturas (2014×2024)' },
    bullets: [
      'Municípios com campus federal: <span class="slide-pos">580 → 673</span> (+16%) — a rede federal se torna mais capilar como instituição',
    ],
  },
  {
    kind: 'image',
    title: 'A retração da licenciatura presencial no território',
    centerContent: true,
    centerBullets: true,
    raiseContent: true,
    image: { file: 'figura_11', caption: 'Municípios com oferta presencial de licenciaturas nas UFs (2014×2024)' },
    bullets: [
      'Municípios com licenciatura presencial: <span class="slide-neg">223 → 206</span> (-7,6%) — o campus continua, a formação presencial recua',
    ],
  },
  {
    kind: 'images',
    title: 'A instabilidade territorial do EaD público (UAB)',
    centerContent: true,
    centerBullets: true,
    raiseContent: true,
    imageMaxHeight: '32vh',
    images: [
      { file: 'tabela_19', caption: 'Tabela 19 — Evolução territorial das UFs e dos polos UAB com cursos de licenciaturas (2014-2024)' },
      { file: 'grafico_oscilacao_polos_uab', caption: 'Elaborado pelo autor a partir da Tabela 19 — oscilação dos municípios com polos UAB (2014-2024)' },
    ],
    bullets: [
      'Municípios com polos UAB (geral): <span class="slide-green">354</span> (2014) → <span class="slide-pos">494</span> (2024), oscilando entre um mínimo de <span class="slide-neg">121 (2016)</span> e um máximo de <span class="slide-pos">589</span> (2023)',
      'Municípios com polos UAB vinculados às UFs: <span class="slide-green">275</span> → <span class="slide-green">320</span>, com quedas para <span class="slide-neg">68 (2015)</span> e saltos para <span class="slide-green">368</span> (2017) — oscilação ano a ano, sem padrão',
    ],
  },
  {
    kind: 'image',
    title: 'Licenciaturas nas UFs: presencial, EaD e UAB',
    centerContent: true,
    centerBullets: true,
    raiseContent: true,
    image: { file: 'grafico_40', caption: 'Evolução das matrículas nas licenciaturas das UFs por modalidade (2014-2024)' },
    bullets: [
      'Trajetória de estabilidade e leve retração, sem movimentos expansivos significativos',
      'EaD federal próprio não consolida presença territorial estável — depende estruturalmente da UAB',
    ],
  },
  {
    kind: 'images',
    title: 'Retração seletiva dos cursos presenciais: o Sul na contramão',
    centerContent: true,
    centerBullets: true,
    raiseContent: true,
    imageMaxHeight: '34vh',
    images: [
      { file: 'grafico_30', caption: 'Evolução dos cursos de licenciaturas presenciais nas UFs (2014-2024)' },
      { file: 'grafico_31', caption: 'Evolução dos cursos de licenciaturas presenciais por região nas UFs (2014-2024)' },
    ],
    bullets: [
      'Cursos presenciais no Brasil: <span class="slide-neg">1.538 → 1.420</span> (-7,7%); Nordeste -56 cursos (-12,2%), Norte -38 (-12,0%), Sudeste -30 (-8,4%)',
      'O Sul é a única região que cresce: <span class="slide-pos">211 → 224</span> cursos (+6,2%) — na contramão de todas as demais',
    ],
  },
  {
    kind: 'image',
    title: 'Nas UFs, o presencial não recua — cresce',
    centerContent: true,
    centerBullets: true,
    raiseContent: true,
    imageMaxHeight: '38vh',
    image: { file: 'grafico_35', caption: 'Evolução dos percentuais das matrículas nas UFs por modalidade (2014-2024)' },
    bullets: [
      'Participação do presencial nas matrículas das UFs: <span class="slide-pos">77,9% → 82,8%</span> — cresce, no sentido oposto do que ocorre no Brasil como um todo',
      'EaD próprio entra em colapso (<span class="slide-neg">1,5% → 0,2%</span>) e a UAB recua (<span class="slide-neg">20,6% → 17,0%</span>) da participação total',
    ],
  },
  {
    kind: 'image',
    title: 'Cinco tipologias institucionais das UFs diante do EaD',
    centerContent: true,
    centerBullets: true,
    sideBullets: true,
    table: {
      headers: ['Grupo', 'Qtd', 'Característica predominante'],
      rows: [
        ['Resistência', '14', 'Ausência de EaD próprio e UAB; presencialidade integral'],
        ['Alta dependência da UAB', '23', 'Participação da UAB ≥ 20% das matrículas em licenciaturas'],
        ['Presencial dominante + EaD via UAB', '29', 'Participação da UAB entre 0% e 20%, sem EaD próprio'],
        ['EaD próprio', '6', 'EaD próprio presente, entre 0,3% e 6,2% das matrículas'],
        ['Experiências abandonadas', '2', 'Ofertaram EaD próprio e/ou UAB, mas não mais em 2024'],
      ],
    },
    bullets: [
      '<span class="slide-neg">14</span> — Resistência total: licenciaturas integralmente presenciais, sem EaD própria nem via UAB<br/><br/><span class="slide-neg">23</span> — Dependência estrutural da UAB: um terço das UFs concentra 20% ou mais das matrículas via UAB',
      '<span class="slide-neg">29</span> — Presencialidade dominante com EaD complementar via UAB: a distância incorporada sem deslocar a centralidade do presencial<br/><br/><span class="slide-neg">6</span> — EaD própria residual (UFGD, UFPEL, UFPR, UFRN, UFSC e UNIVASF), com apenas 0,3% a 6,2% das matrículas',
      '<span class="slide-neg">2</span> — Experiências abandonadas: UNIFAL (EaD própria até 2022, UAB até 2013) e UFV (EaD própria até 2016) desistiram da modalidade',
    ],
  },
  {
    kind: 'stats',
    title: 'A retração das Universidades Federais nas Licenciaturas',
    centerContent: true,
    centerBullets: true,
    raiseContent: true,
    stats: [
      { value: '<span class="slide-neg">-10,4%</span>', label: 'Matrículas em licenciaturas (<span class="slide-neg">290.966 → 260.741</span>)' },
      { value: '<span class="slide-neg">-4,7%</span>', label: 'Matrículas presenciais (<span class="slide-neg">226.607 → 215.930</span>)' },
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
    kind: 'image',
    title: 'Matrículas presenciais: Norte em colapso, Sudeste em alta',
    centerContent: true,
    centerBullets: true,
    raiseContent: true,
    imageMaxHeight: '24vh',
    image: { file: 'grafico_39', caption: 'Evolução das matrículas presenciais em licenciaturas por região nas UFs (2014-2024)' },
    secondaryImages: [
      { file: 'tabela_22', caption: 'Tabela 22 — Matrículas presenciais em licenciaturas, população regional e densidade territorial (2022)' },
    ],
    bullets: [
      'Norte: <span class="slide-neg">60.462 → 42.985</span> matrículas (-28,9%) — a maior queda entre as regiões',
      'Sudeste cresce (<span class="slide-pos">43.946 → 50.682</span>) e o Nordeste se mantém estável e líder em volume absoluto (<span class="slide-pos">75.548 → 78.094</span>)',
      'Mesmo com menos matrículas, o Norte tem a maior proporção por habitante (<span class="slide-pos">288,94</span>/100 mil hab. em 2022, contra 60,02 no Sudeste) — mas a menor densidade territorial (13,15/1000 km²)',
    ],
  },
  {
    kind: 'image',
    title: 'Ingressos nas licenciaturas das UFs',
    centerContent: true,
    centerBullets: true,
    raiseContent: true,
    image: { file: 'grafico_42', caption: 'Dinâmica dos ingressantes nos cursos de licenciatura nas UFs por modalidade de ensino (2014-2024)' },
    bullets: [
      'Capacidade de atração das licenciaturas federais analisada ao longo da década',
      'Contraste direto com o crescimento exponencial de ingressantes no setor privado',
    ],
  },
  {
    kind: 'image',
    title: 'Concluintes: a baixíssima eficiência formativa',
    centerContent: true,
    centerBullets: true,
    raiseContent: true,
    sideBullets: true,
    imageMaxHeight: '18vh',
    secondaryImageMaxHeight: '19vh',
    image: { file: 'grafico_43', caption: 'Evolução dos concluintes nas licenciaturas das UFs por modalidade de ensino (2014-2024)' },
    secondaryImages: [
      { file: 'tabela_23', caption: 'Tabela 23 — taxa de conclusão implícita, presencial (2018-2024)' },
      { file: 'tabela_24', caption: 'Tabela 24 — taxa de conclusão implícita, UAB (2018-2024)' },
      { file: 'tabela_25', caption: 'Tabela 25 — taxa de conclusão implícita, EaD própria (2018-2024)' },
    ],
    bullets: [
      'Concluintes: <span class="slide-neg">33.148 → 31.094</span> (<span class="slide-neg">-6,2%</span>) — presencial estável (<span class="slide-neg">-1,2%</span>), UAB recua <span class="slide-neg">21,5%</span>, EaD própria colapsa <span class="slide-neg">95,6%</span>',
      'Taxa de conclusão implícita (ingressante → concluinte no prazo): apenas <span class="slide-neg">11,4%</span> no presencial, <span class="slide-neg">9,4%</span> na UAB e <span class="slide-neg">4,5%</span> no EaD próprio',
    ],
  },
  {
    kind: 'images',
    title: 'Evasão: do abandono para a suspensão que não retorna',
    centerContent: true,
    centerBullets: true,
    raiseContent: true,
    imageMaxHeight: '34vh',
    images: [
      { file: 'grafico_44', caption: 'Evasão total por modalidade nas licenciaturas das UFs (2014-2024)' },
      { file: 'grafico_45', caption: 'Evasão por tipo — desvinculados, trancados e transferidos (2014-2024)' },
    ],
    bullets: [
      'Em 2024, a evasão (<span class="slide-neg">109.834</span>) supera os ingressantes (<span class="slide-neg">71.248</span>) em mais de <span class="slide-neg">50%</span> — esvaziamento líquido do sistema',
      'A evasão mudou de forma, não de volume: desvinculados caem <span class="slide-neg">-10,6%</span>, mas trancamentos saltam <span class="slide-neg">+30,8%</span> — e o pico não foi na pandemia (<span class="slide-neg">2020</span>), foi em <span class="slide-neg">2022</span>, com trancados represados que nunca voltaram',
    ],
  },
  {
    kind: 'images',
    title: 'UFs × setor privado — comparativo direto',
    centerContent: true,
    centerBullets: true,
    raiseContent: true,
    imageMaxHeight: '32vh',
    images: [
      { file: 'grafico_49', caption: 'Matrículas em licenciaturas: UFs × privadas com e sem fins lucrativos (2014-2024)' },
      { file: 'tabela_26', caption: 'Tabela 26 — Síntese comparativa: matrículas, ingressos EaD, concluintes e evasão por categoria (2014-2024)' },
    ],
    bullets: [
      'Em 2014, o mercado era relativamente equilibrado: privadas com fins lucrativos <span class="slide-neg">40,7%</span>, sem fins lucrativos <span class="slide-neg">30,1%</span>, UFs <span class="slide-neg">23,5%</span>, demais IES públicas <span class="slide-neg">5,8%</span>',
      'Em 2024: privadas com fins lucrativos controlam <span class="slide-neg">66,2%</span> do mercado, as UFs encolhem para <span class="slide-neg">17,3%</span>',
      'Nos ingressos em EaD especificamente, o monopólio é ainda maior: <span class="slide-neg">88%</span> vão para as privadas com fins lucrativos, e as UFs caem de <span class="slide-neg">9,1%</span> para apenas <span class="slide-neg">2,7%</span>',
    ],
  },
  {
    kind: 'icons',
    title: 'Ações reais e ausências estratégicas das UFs',
    centerContent: true,
    raiseContent: true,
    items: [
      { icon: 'CheckCircle2', text: 'Ações efetivamente implementadas: políticas de permanência estudantil (PNAES) — ainda que limitadas e descontinuadas — e iniciativas pontuais e fragmentadas de EaD própria' },
      { icon: 'XCircle', text: 'Ausência 1: nenhuma UF construiu um sistema federal coordenado de EaD própria em escala' },
      { icon: 'XCircle', text: 'Ausência 2: nenhuma UF liderou uma expansão agressiva do sistema UAB' },
      { icon: 'XCircle', text: 'Ausência 3: políticas sistemáticas de permanência e combate à evasão não se consolidaram' },
      { icon: 'XCircle', text: 'Ausência 4: nenhuma UF disputou competitivamente o espaço ocupado pela EaD privada' },
    ],
  },
  {
    kind: 'icons',
    title: 'A "triangulação da inércia": corpo docente, gestão e estudantes',
    centerContent: true,
    raiseContent: true,
    wideItems: true,
    items: [
      { icon: 'BookUser', text: 'Corpo docente: maior capital simbólico do campo, vê a EaD como "degradação" formativa — mas o próprio presencial forma mal (taxa de conclusão de apenas <span class="slide-neg">8,7% a 13,6%</span>). Comparando público × privado: as UFs (majoritariamente presenciais) têm <span class="slide-pos">3,5</span> evadidos por concluinte, contra <span class="slide-pos">5,7</span> nas privadas com fins lucrativos (majoritariamente EaD) — que, mesmo assim, formam mais: <span class="slide-pos">116.068</span> concluintes contra <span class="slide-pos">31.094</span> das UFs (<span class="slide-pos">56,4%</span> de todos os diplomas de licenciatura do país)' },
      { icon: 'Building2', text: 'Gestão universitária: sabe que a EaD seria vantajosa, mas trava entre a resistência docente, a infraestrutura insuficiente e o orçamento congelado pela EC 95/2016 — com incentivo à opacidade sobre a evasão' },
      { icon: 'Users', text: 'Estudantes: posição mais subordinada do campo; pedem flexibilidade por sobrevivência acadêmica (conciliar trabalho e família), não por preferência pedagógica — demanda real que o setor privado capturou' },
      { icon: 'CircleOff', text: 'O resultado não é consenso, é paralisia: cada grupo trava a mudança por um motivo diferente, e a EC 95/2016 transforma a falta de recursos em justificativa institucional para a inércia' },
    ],
  },
  {
    kind: 'icons',
    title: 'Da retração à desuniversitarização: a redistribuição dos capitais no campo',
    centerContent: true,
    raiseContent: true,
    wideItems: true,
    items: [
      { icon: 'TrendingDown', text: 'Retração estrutural = perda de posição no campo (Bourdieu): as UFs perdem <span class="slide-red">6,7 pontos percentuais</span> de participação enquanto o setor privado lucrativo ganha <span class="slide-red">26,8 pontos</span> (<span class="slide-red">43,2%</span> → <span class="slide-red">70,0%</span>)' },
      { icon: 'ShieldOff', text: '"Resistência sem apropriação": apenas <span class="slide-red">6 das 69</span> UFs tentaram EaD própria — e mesmo essas colapsam <span class="slide-red">89%</span> nas matrículas' },
      { icon: 'Unplug', text: 'Fragilidade institucional = descapitalização seletiva do Estado: polos próprios caem de <span class="slide-red">117</span> para <span class="slide-red">39 (-66,7%)</span>; conclusão de apenas <span class="slide-red">9,4%</span> (UAB) e <span class="slide-red">4,5%</span> (EaD própria)' },
      { icon: 'GraduationCap', text: '"Desuniversitarização" (Termo definido pelo autor a partir das ideias defendidas por Giolo; Bianchetti e Sguissardi): mais de <span class="slide-red">70%</span> dos futuros professores do Brasil já se formam fora do ambiente universitário' },
    ],
  },
  {
    kind: 'stats',
    title: 'Bifurcação formativa: dois circuitos, um só sistema',
    centerContent: true,
    centerBullets: true,
    raiseContent: true,
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
    kind: 'icons',
    title: 'Respostas às questões de pesquisa',
    centerContent: true,
    raiseContent: true,
    wideItems: true,
    items: [
      { label: 'Q1', text: 'O domínio privado na EaD não foi evolução espontânea do mercado, mas engenharia política: três ondas de flexibilização regulatória (1996-2004, 2005-2013, 2014-2024), a EC 95/2016 asfixiando o orçamento público e o FIES/ProUni subsidiando a demanda privada' },
      { label: 'Q2', text: 'O SINAES foi capturado pela performatividade (Ball) e passou a premiar escala, não qualidade; os Decretos 9.057/2017 e 9.235/2017 foram redigidos com participação do setor privado — a massificação ocorreu por meio da regulação, com sua chancela' },
      { label: 'Q3', text: 'Os microdados confirmam uma reconfiguração estrutural e irreversível: UFs <span class="slide-neg">-10,4%</span> nas matrículas contra <span class="slide-pos">+98,3%</span> das privadas com fins lucrativos; mais de <span class="slide-pos">80%</span> dos ingressantes em licenciatura já entram pela EaD; apenas <span class="slide-neg">6 das 69</span> UFs têm EaD próprio' },
      { label: 'Q4', text: 'As UFs praticaram uma "abstenção estratégica": cinco tipologias institucionais, quatro ausências estratégicas e a "triangulação da inércia" (corpo docente, gestão, estudantes) bloquearam qualquer resposta competitiva à expansão privada' },
    ],
  },
  {
    kind: 'stats',
    title: 'Síntese dos achados',
    centerContent: true,
    centerBullets: true,
    raiseContent: true,
    stats: [
      { value: '<span class="slide-red">+286,73%</span>', label: 'Matrículas EaD (Brasil, 2014-2024)' },
      { value: '<span class="slide-neg">-22,47%</span>', label: 'Matrículas presenciais (Brasil, 2014-2024)' },
      { value: '<span class="slide-red">+117,74%</span>', label: 'Matrículas EaD em licenciaturas (2014-2024)' },
      { value: '<span class="slide-neg">-41,54%</span>', label: 'Matrículas presenciais em licenciaturas (2014-2024)' },
      { value: '<span class="slide-red">80%+</span>', label: 'Dos ingressantes em licenciaturas via EaD em 2024' },
      { value: '<span class="slide-red">66,2%</span>', label: 'Das matrículas em formação docente em IES privadas com fins lucrativos' },
    ],
    bullets: [
      'O Estado não foi árbitro neutro: foi arquiteto do mercado — metas do PNE sem recursos, flexibilização regulatória, EC 95/2016',
      'A universidade pública federal, historicamente protagonista da formação docente, tornou-se agente residual em um campo que ela mesma ajudou a construir',
    ],
  },
  {
    kind: 'icons',
    title: 'Recomendações para o próximo ciclo de política educacional',
    centerContent: true,
    raiseContent: true,
    wideItems: true,
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
    centerContent: true,
    raiseContent: true,
    wideItems: true,
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
      'Programa de Pós-Graduação em Educação — UFFS',
    ],
    showLogos: true,
    links: [
      { label: 'Visualizar as Referências Bibliográficas', to: '/capitulo/referencias' },
      { label: 'Conhecer os dados da pesquisa', to: '/pesquisa' },
      { label: 'Explorar os Painéis Interativos', to: '/paineis-interativos' },
      { label: 'Ver o Apêndice I — ferramentas da pesquisa', to: '/capitulo/apendice-i' },
    ],
    contactInfo: [
      'ocimar.zolin@gmail.com',
      'ocimar.zolin@uffs.edu.br',
      'ocimar.zolin@estudante.uffs.edu.br',
      '(49) 98855-8025',
    ],
  },
];

export default slides;

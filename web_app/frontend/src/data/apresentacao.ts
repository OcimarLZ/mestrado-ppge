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

export interface Slide {
  kind: 'cover' | 'section' | 'text' | 'icons' | 'image' | 'images' | 'stats' | 'cards' | 'columns' | 'closing';
  title: string;
  subtitle?: string;
  bullets?: string[];
  items?: IconItem[];
  cards?: CardItem[];
  columns?: Column[];
  image?: SlideImage;
  images?: SlideImage[];
  stats?: { value: string; label: string }[];
  note?: string;
  showLogos?: boolean;
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
  },
  {
    kind: 'text',
    title: 'Epígrafe',
    bullets: [
      '"Ninguém educa ninguém, ninguém educa a si mesmo, os homens se educam entre si, mediatizados pelo mundo."',
      '— Paulo Freire, 1987',
    ],
  },
  {
    kind: 'image',
    title: 'Tema e contexto',
    image: { file: 'figura_01', caption: 'Municípios brasileiros com polos EaD em 2006 e 2024' },
    bullets: [
      'Recorte temporal: 2014-2024, período de vigência do Plano Nacional de Educação (PNE)',
      'Entre 2014 e 2024, o eixo presencial/universitário deixa de ser dominante na formação docente',
      'A formação de professores passa a ser majoritariamente EaD privada com fins lucrativos',
    ],
  },
  {
    kind: 'icons',
    title: 'Justificativa: uma mercantilização inesperada',
    items: [
      { icon: 'AlertTriangle', text: 'Transformação estrutural da formação docente sem precedentes durante a vigência do PNE (2014-2024)' },
      { icon: 'Landmark', text: 'A EaD foi fomentada pelo Estado para reduzir o déficit de professores sem diplomação adequada' },
      { icon: 'TrendingUp', text: 'Mas os dados mais recentes mostram as IES privadas com fins lucrativos dominando esse campo' },
      { icon: 'Scale', text: 'Inversão dos indicadores: matrículas privadas em EaD explodem enquanto as IES públicas presenciais estagnam e evadem' },
    ],
  },
  {
    kind: 'icons',
    title: 'Relevância da pesquisa',
    items: [
      { icon: 'Database', text: 'Intersecção entre pesquisa educacional e Ciência de Dados: Data Warehouse próprio e ETL sobre dezenas de milhões de registros do Censo da Educação Superior' },
      { icon: 'CalendarClock', text: 'Realizada no término do PNE 2014-2024, oferecendo subsídios baseados em evidências para o próximo ciclo de planejamento educacional' },
      { icon: 'Building2', text: 'Relevância institucional para a UFFS: articula a linha de Políticas Educacionais do PPGE com a atuação técnica do autor na Secretaria de Tecnologia da Informação (SETI)' },
    ],
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
  },
  {
    kind: 'icons',
    title: 'Objetivo geral',
    items: [
      { icon: 'Target', text: 'Compreender e analisar as reações e estratégias das Universidades Federais frente ao avanço e à consolidação da hegemonia das instituições privadas na oferta de cursos de licenciatura a distância, em um contexto de precarização da formação docente impulsionado pelas políticas educacionais vigentes durante o PNE (2014-2024)' },
    ],
  },
  {
    kind: 'icons',
    title: 'Objetivos específicos',
    items: [
      { label: 'i', text: 'Analisar o impacto da flexibilização regulatória e das políticas educacionais neoliberais na expansão da EaD no período do PNE (2014-2024)' },
      { label: 'ii', text: 'Examinar como as tensões entre interesse público e lógica de mercado moldaram os instrumentos de regulação e avaliação do MEC/INEP, favorecendo a massificação da EaD em detrimento de um projeto crítico de formação de professores' },
      { label: 'iii', text: 'Analisar a reconfiguração da oferta de licenciaturas (2014-2024), contrastando o crescimento exponencial do EaD privado com o comportamento institucional das Universidades Federais, a partir dos microdados de cursos, ingressos, concluintes e evasão' },
      { label: 'iv', text: 'Investigar as estratégias institucionais — ou a ausência destas — adotadas pelas Universidades Federais para enfrentar a concorrência do mercado privado e preservar a natureza pública e a qualidade da formação docente' },
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
  },
  {
    kind: 'icons',
    title: 'Ball: políticas educacionais como campo de disputas',
    items: [
      { icon: 'FileText', text: 'As políticas educacionais são "textos e discursos" produzidos em arenas permeadas por conflitos, interesses econômicos e disputas por interpretação' },
      { icon: 'AlertTriangle', text: 'A expansão da EaD não decorre de escolhas pedagógicas, mas de escolhas regulatórias que favoreceram grandes grupos privados' },
      { icon: 'FileSearch', text: 'Políticas são "ambíguas e disputáveis": conglomerados privados exploram as lacunas dos marcos regulatórios para flexibilizar credenciamentos e reduzir exigências acadêmicas' },
    ],
  },
  {
    kind: 'icons',
    title: 'Bourdieu: a disputa por hegemonia no campo educacional',
    items: [
      { icon: 'Layers', text: 'A teoria dos campos: a educação superior como espaço social estruturado de posições em confronto' },
      { icon: 'Users', text: 'Estado, conglomerados privados, universidades públicas e organismos multilaterais disputam a autoridade legítima de definir o que é educação superior' },
      { icon: 'Swords', text: 'A reconfiguração do ensino superior é uma disputa estruturada de poder — não uma questão meramente pedagógica ou tecnológica' },
    ],
  },
  {
    kind: 'icons',
    title: 'Faoro: estamento e patrimonialismo no Estado brasileiro',
    items: [
      { icon: 'Landmark', text: 'Estamento e patrimonialismo mobilizados como pressupostos teórico-contextuais, não como objeto central de investigação' },
      { icon: 'Shuffle', text: 'Descrevem a porosidade histórica entre as esferas pública e privada, nunca plenamente separadas na formação do Estado brasileiro' },
      { icon: 'Handshake', text: 'Essa porosidade torna inteligíveis as trocas de favores e os acordos regulatórios entre governantes e o setor econômico educacional' },
    ],
  },
  {
    kind: 'icons',
    title: 'Neoliberalismo como racionalidade política (Dardot e Laval)',
    items: [
      { icon: 'Cog', text: 'Neoliberalismo não como um conjunto de políticas econômicas, mas como uma racionalidade política — uma forma específica de governar' },
      { icon: 'Building2', text: 'Introduz a lógica da concorrência e da gestão empresarial em esferas antes regidas por outros princípios, incluindo a educação pública' },
      { icon: 'Zap', text: 'A EaD é sua materialização mais acabada: escalabilidade, padronização curricular e gestão algorítmica construídas para uma economia educacional orientada por desempenho e retorno sobre investimento' },
    ],
  },
  {
    kind: 'icons',
    title: 'Mercantilização e financeirização (Sguissardi, Amaral, Chaves)',
    items: [
      { icon: 'CircleDollarSign', text: 'A educação superior se converte em ativo financeiro: fusões, aquisições, abertura de capital (IPOs) e instrumentos do capitalismo financeiro' },
      { icon: 'ArrowRightLeft', text: 'O valor econômico, e não o valor formativo, torna-se o eixo organizador das decisões acadêmicas' },
      { icon: 'Gauge', text: 'A EaD é o modelo ideal para essa lógica: maximiza a relação aluno/docente e viabiliza margens de lucro em escala nacional' },
    ],
  },
  {
    kind: 'icons',
    title: 'Percurso metodológico',
    items: [
      { icon: 'Database', text: 'Data Warehouse próprio, construído a partir dos microdados do INEP, CAPES e IBGE' },
      { icon: 'GitBranch', text: 'Processos de ETL (Extract, Transform, Load) integralmente reproduzíveis por código' },
      { icon: 'Code2', text: 'Consultas parametrizadas, rotinas automatizadas e visualizações geradas programaticamente' },
      { icon: 'FileSearch', text: 'Análise documental complementar (legislação, decretos, demonstrações financeiras)' },
    ],
  },
  {
    kind: 'image',
    title: 'Arquitetura de dados da pesquisa',
    image: { file: 'figura_18', caption: 'Modelo de dicionário de dados do Data Warehouse projetado' },
    bullets: [
      'Consolidação de múltiplas fontes oficiais num único modelo fato/dimensão',
      'Mais de uma década de séries históricas (Censo da Educação Superior, 2014-2024)',
    ],
  },
  {
    kind: 'image',
    title: 'Orçamento da educação superior brasileira (2006-2024)',
    image: { file: 'grafico_02', caption: 'Orçamento destinado à educação superior (em bilhões de R$), 2006-2024' },
    bullets: [
      'Emenda Constitucional nº 95/2016 congela os gastos federais por vinte anos',
      'Asfixia orçamentária das Universidades Federais justamente quando o PNE demandava expansão',
    ],
  },
  {
    kind: 'image',
    title: 'Evolução das matrículas por modalidade de ensino',
    image: { file: 'grafico_10', caption: 'Evolução das matrículas por modalidade de ensino no Brasil (2014-2024)' },
    bullets: [
      'EaD: de 1.341.876 (2014) para 5.189.376 (2024) — alta de 286,73%',
      'Presencial: de 6.497.889 (2014) para 5.037.875 (2024) — retração de 22,47%',
    ],
  },
  {
    kind: 'image',
    title: 'Matrículas por tipo de rede e modalidade',
    image: { file: 'grafico_11', caption: 'Evolução das matrículas por tipo de rede e modalidade de ensino (2014-2024)' },
    bullets: [
      'A expansão da EaD é liderada quase integralmente pelo setor privado',
      'O setor público (presencial + EaD) mantém trajetória estável, sem acompanhar a curva privada',
    ],
  },
  {
    kind: 'image',
    title: 'Dinheiro público para o setor privado',
    image: { file: 'grafico_20', caption: 'Retração do FIES e explosão da EaD privada (2014-2024)' },
    bullets: [
      'FIES e ProUni: instrumentos de financiamento público historicamente direcionados ao setor privado',
      'A retração do FIES presencial coincide com a explosão das matrículas EaD privadas',
    ],
  },
  {
    kind: 'cards',
    title: 'Os grandes grupos educacionais',
    subtitle: 'Cinco conglomerados concentram a expansão da EaD privada no Brasil',
    cards: [
      { title: 'Cogna Educação', text: 'Megafusões presenciais e pivô para EaD, com padronização curricular' },
      { title: 'Vitru Educação', text: 'Modelo asset-light: desmaterialização do campus e logística em rede' },
      { title: 'YDUQS', text: 'Hibridização premium e expansão metropolitana da EaD' },
      { title: 'Ânima Educação', text: 'Aquisições seletivas com foco em prestígio e portfólio de marcas' },
      { title: 'Ser Educacional', text: 'Dominação regional e interiorização, com foco de baixo custo' },
    ],
  },
  {
    kind: 'image',
    title: 'Cogna Educação',
    image: { file: 'figura_05', caption: 'Evolução da capilaridade dos polos EaD da Cogna Educação (2005-2014-2024)' },
    bullets: ['Pioneira na oligopolização do setor via megafusões e financeirização'],
  },
  {
    kind: 'image',
    title: 'Vitru Educação',
    image: { file: 'figura_06', caption: 'Evolução da capilaridade dos polos EaD da Vitru Educação (2005-2014-2024)' },
    bullets: ['Modelo asset-light: desmaterialização do campus e logística educacional em rede'],
  },
  {
    kind: 'image',
    title: 'YDUQS',
    image: { file: 'figura_07', caption: 'Evolução da capilaridade dos polos EaD da YDUQS (2005-2014-2024)' },
    bullets: ['Dualidade estratégica entre EaD de massa e ensino presencial premium'],
  },
  {
    kind: 'images',
    title: 'Ânima Educação e Ser Educacional',
    images: [
      { file: 'figura_08', caption: 'Ânima Educação (2005-2014-2024)' },
      { file: 'figura_09', caption: 'Ser Educacional (2005-2014-2024)' },
    ],
    bullets: ['Captura de capital simbólico via marcas tradicionais e monopólio regional na EaD'],
  },
  {
    kind: 'image',
    title: 'Estratégias e capitais mobilizados pelos conglomerados',
    image: { file: 'quadro_02', caption: 'Estratégias, capitais dos conglomerados e efeitos estruturais produzidos' },
    bullets: [
      'Síntese comparativa dos cinco grupos sob a lente de Bourdieu e Ball',
      'Efeito comum: hegemonia empresarial e pressão competitiva sobre as instituições federais',
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
    kind: 'images',
    title: 'UFs × setor privado — comparativo direto',
    images: [
      { file: 'grafico_49', caption: 'Matrículas em licenciaturas: UFs × privadas com e sem fins lucrativos (2014-2024)' },
      { file: 'tabela_21', caption: 'Tipologias institucionais das UFs diante do EaD em 2024' },
    ],
    bullets: [
      'Se as UFs encolheram, o setor privado cresceu exponencialmente e absorveu em massa os ingressantes',
      'Resposta institucional das UFs foi heterogênea: da resistência à omissão estratégica',
    ],
  },
  {
    kind: 'stats',
    title: 'Síntese dos achados',
    stats: [
      { value: '+286,73%', label: 'Matrículas EaD (Brasil, 2014-2024)' },
      { value: '-22,47%', label: 'Matrículas presenciais (Brasil, 2014-2024)' },
      { value: '+117,74%', label: 'Matrículas EaD em licenciaturas (2014-2024)' },
      { value: '-41,54%', label: 'Matrículas presenciais em licenciaturas (2014-2024)' },
      { value: '80%+', label: 'Dos ingressantes em licenciaturas via EaD em 2024' },
      { value: '~70%', label: 'Das matrículas em formação docente em IES privadas com fins lucrativos' },
    ],
    bullets: [
      'O Estado não foi árbitro neutro: foi arquiteto do mercado — metas do PNE sem recursos, flexibilização regulatória em três ondas, EC 95/2016',
      'A universidade pública federal, historicamente protagonista da formação docente, tornou-se agente residual em um campo que ela mesma ajudou a construir',
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

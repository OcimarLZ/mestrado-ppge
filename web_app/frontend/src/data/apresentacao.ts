// Conteudo da apresentacao de defesa (28 slides), escrito a partir do conteudo real
// da dissertacao (nao e uma copia dos slides de qualificacao, que traziam resultados
// preliminares e secoes "a definir"). Ver web_app/content_export/ para a extracao
// original dos textos e figuras usados aqui.

export type SlideImage = { file: string; caption?: string };
export type IconItem = { icon: string; text: string };
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
    title: 'Justificativa',
    items: [
      { icon: 'AlertTriangle', text: 'Transformação estrutural da formação docente sem precedentes no período' },
      { icon: 'TrendingUp', text: 'Expansão inédita da EaD privada nas licenciaturas' },
      { icon: 'TrendingDown', text: 'Recuo da oferta presencial, especialmente nas Universidades Federais' },
      { icon: 'SearchX', text: 'Lacuna analítica: poucos estudos integram políticas públicas, microdados e a escala nacional do fenômeno' },
    ],
  },
  {
    kind: 'icons',
    title: 'Problemática e questões de pesquisa',
    items: [
      { icon: 'HelpCircle', text: 'Como a flexibilização regulatória e as políticas neoliberais impulsionaram a EaD no período do PNE?' },
      { icon: 'HelpCircle', text: 'Como as tensões entre interesse público e mercado moldaram a regulação do MEC/INEP?' },
      { icon: 'HelpCircle', text: 'Como os microdados evidenciam a reconfiguração da oferta de licenciaturas nas UFs frente ao crescimento privado?' },
      { icon: 'HelpCircle', text: 'Quais estratégias (ou ausência delas) as UFs adotaram diante da concorrência do mercado privado?' },
    ],
  },
  {
    kind: 'icons',
    title: 'Objetivos',
    items: [
      { icon: 'Target', text: 'Geral: analisar a disputa de campo e os impactos da mercantilização na expansão da oferta de licenciaturas em EaD no Brasil (2014-2024)' },
      { icon: 'Building2', text: 'Investigar a dinâmica de participação e os limites de atuação das Universidades Federais nesse processo' },
      { icon: 'Scale', text: 'Analisar o impacto da flexibilização regulatória neoliberal na precarização da formação docente' },
    ],
  },
  {
    kind: 'columns',
    title: 'Referencial teórico',
    columns: [
      {
        icon: 'Layers',
        title: 'Pierre Bourdieu',
        items: ['Ensino superior como campo', 'Capitais e habitus', 'Disputas por hegemonia simbólica', 'EaD como redistribuição de capitais'],
      },
      {
        icon: 'Network',
        title: 'Stephen Ball',
        items: ['Políticas como mercado', 'Performatividade', 'Redes políticas', 'Currículo neoliberal global'],
      },
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

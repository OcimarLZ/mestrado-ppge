export interface ForumTopico {
  slug: string;
  title: string;
  description: string;
  icon: string;
}

// Tópicos do Fórum de Discussões -- curados pelo pesquisador (não vêm do CMS). Para
// adicionar, remover ou editar um tópico, basta editar este array; cada slug define a URL
// (/forum/:slug) e também o identificador da thread de comentários no Cusdis.
const topicos: ForumTopico[] = [
  {
    slug: 'ead-e-qualidade-da-formacao',
    title: 'EaD e qualidade da formação docente',
    description:
      'A expansão acelerada da Educação a Distância muda a qualidade da formação de professores? ' +
      'Compartilhe experiências, dúvidas ou críticas sobre esse debate.',
    icon: 'GraduationCap',
  },
  {
    slug: 'publico-x-privado-na-educacao-superior',
    title: 'O público e o privado na educação superior',
    description:
      'Um espaço para discutir a relação entre a expansão do setor privado e a estagnação do ' +
      'setor público na oferta de cursos de licenciatura.',
    icon: 'Building2',
  },
  {
    slug: 'duvidas-sobre-a-pesquisa',
    title: 'Dúvidas sobre a pesquisa e os dados',
    description:
      'Perguntas sobre a metodologia, as fontes de dados (Censo da Educação Superior/INEP) ou ' +
      'qualquer achado apresentado no site podem ser feitas aqui.',
    icon: 'HelpCircle',
  },
];

export default topicos;

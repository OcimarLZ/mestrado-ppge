export interface ThemeColors {
  bg: string;
  card: string;
  text: string;
  textSecondary: string;
  accent: string;
  sidebar: string;
  hero_glow: string;
  font: string;
}

export interface Theme {
  name: string;
  label: string;
  description: string;
  colors: ThemeColors;
}

const themes: Theme[] = [
  {
    name: 'dark-slate',
    label: 'Dark Slate',
    description: 'Escuro com verde esmeralda',
    colors: {
      bg: '#0f172a',
      card: 'rgba(30, 41, 59, 0.7)',
      text: '#f8fafc',
      textSecondary: '#94a3b8',
      accent: '#10b981',
      sidebar: '#0f172a',
      hero_glow: 'rgba(16,185,129,0.1)',
      font: "'Inter', system-ui, -apple-system, sans-serif",
    },
  },
  {
    name: 'ocean-blue',
    label: 'Ocean Blue',
    description: 'Azul oceano com ciano',
    colors: {
      bg: '#0c1929',
      card: 'rgba(20, 50, 80, 0.7)',
      text: '#e0f2fe',
      textSecondary: '#7ba3c7',
      accent: '#22d3ee',
      sidebar: '#0c1929',
      hero_glow: 'rgba(34, 211, 238, 0.1)',
      font: "'Inter', system-ui, -apple-system, sans-serif",
    },
  },
  {
    name: 'midnight-purple',
    label: 'Midnight Purple',
    description: 'Roxo escuro com magenta',
    colors: {
      bg: '#1a1025',
      card: 'rgba(45, 25, 65, 0.7)',
      text: '#f3e8ff',
      textSecondary: '#a686c4',
      accent: '#c084fc',
      sidebar: '#1a1025',
      hero_glow: 'rgba(192, 132, 252, 0.12)',
      font: "'Inter', system-ui, -apple-system, sans-serif",
    },
  },
  {
    name: 'forest-green',
    label: 'Forest Green',
    description: 'Verde floresta com lima',
    colors: {
      bg: '#0a1a0f',
      card: 'rgba(20, 50, 30, 0.7)',
      text: '#ecfdf5',
      textSecondary: '#6ea882',
      accent: '#4ade80',
      sidebar: '#0a1a0f',
      hero_glow: 'rgba(74, 222, 128, 0.1)',
      font: "'Inter', system-ui, -apple-system, sans-serif",
    },
  },
  {
    name: 'sunset-amber',
    label: 'Sunset Amber',
    description: 'Laranja escuro com âmbar',
    colors: {
      bg: '#1c1307',
      card: 'rgba(50, 35, 15, 0.7)',
      text: '#fffbeb',
      textSecondary: '#c4a87c',
      accent: '#fbbf24',
      sidebar: '#1c1307',
      hero_glow: 'rgba(251, 191, 36, 0.12)',
      font: "'Inter', system-ui, -apple-system, sans-serif",
    },
  },
  {
    name: 'crimson-night',
    label: 'Crimson Night',
    description: 'Vermelho escuro com rosa',
    colors: {
      bg: '#1a0a0a',
      card: 'rgba(50, 18, 18, 0.7)',
      text: '#fef2f2',
      textSecondary: '#c48a8a',
      accent: '#fb7185',
      sidebar: '#1a0a0a',
      hero_glow: 'rgba(251, 113, 133, 0.12)',
      font: "'Inter', system-ui, -apple-system, sans-serif",
    },
  },
  {
    name: 'light-clean',
    label: 'Light Clean',
    description: 'Inspirado no VS Code Light+',
    colors: {
      bg: '#ffffff',
      card: 'rgba(243, 244, 246, 0.9)',
      text: '#1e293b',
      textSecondary: '#64748b',
      accent: '#2563eb',
      sidebar: '#f8fafc',
      hero_glow: 'rgba(37, 99, 235, 0.06)',
      font: "'Inter', system-ui, -apple-system, sans-serif",
    },
  },
  {
    name: 'light-soft',
    label: 'Light Soft',
    description: 'Claro suave com tom quente',
    colors: {
      bg: '#fefcf8',
      card: 'rgba(255, 247, 237, 0.9)',
      text: '#292524',
      textSecondary: '#78716c',
      accent: '#d97706',
      sidebar: '#fefcf8',
      hero_glow: 'rgba(217, 119, 6, 0.06)',
      font: "'Inter', system-ui, -apple-system, sans-serif",
    },
  },
  {
    name: 'light-ayu',
    label: 'Light Ayu',
    description: 'Inspirado no Ayu Light',
    colors: {
      bg: '#fafafa',
      card: 'rgba(255, 255, 255, 0.85)',
      text: '#1a1a2e',
      textSecondary: '#6b6b82',
      accent: '#e68a2e',
      sidebar: '#f5f5f5',
      hero_glow: 'rgba(230, 138, 46, 0.07)',
      font: "'Inter', system-ui, -apple-system, sans-serif",
    },
  },
  {
    name: 'coffee-warm',
    label: 'Coffee Warm',
    description: 'Marrom quente acolhedor',
    colors: {
      bg: '#1a1410',
      card: 'rgba(45, 35, 28, 0.7)',
      text: '#fef7ee',
      textSecondary: '#b8a088',
      accent: '#d97706',
      sidebar: '#1a1410',
      hero_glow: 'rgba(217, 119, 6, 0.12)',
      font: "'Inter', system-ui, -apple-system, sans-serif",
    },
  },
];

export default themes;

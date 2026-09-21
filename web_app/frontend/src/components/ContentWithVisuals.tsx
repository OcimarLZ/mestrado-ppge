import React from 'react';
import VisualElement from './VisualElement';
import type { VisualData } from './DynamicSection';

interface ContentWithVisualsProps {
  html: string;
  visuals?: VisualData[];
  className?: string;
}

// Renderiza um bloco de HTML (conteudo de capitulo ou de secao) resolvendo os
// marcadores [v:ID] embutidos no texto para o elemento visual correspondente,
// no lugar exato onde aparecem -- usado tanto pelo texto de abertura do capitulo
// (GenericChapterPage) quanto pelo conteudo de cada secao (DynamicSection).
const ContentWithVisuals: React.FC<ContentWithVisualsProps> = ({ html, visuals, className = 'text-content' }) => {
  if (!visuals || visuals.length === 0) {
    return <div className={className} dangerouslySetInnerHTML={{ __html: html }} />;
  }

  const parts = html.split(/(\[v:\d+\])/g);
  return (
    <div className={className}>
      {parts.map((part, idx) => {
        const match = part.match(/^\[v:(\d+)\]$/);
        if (match) {
          const visualId = parseInt(match[1]);
          const visual = visuals.find(v => v.id === visualId);
          if (visual) {
            return <VisualElement key={idx} visual={visual} />;
          }
          return <p key={idx} style={{ color: '#ef4444', fontSize: '0.85rem' }}>[v:{visualId} — elemento não encontrado]</p>;
        }
        return <span key={idx} dangerouslySetInnerHTML={{ __html: part }} />;
      })}
    </div>
  );
};

export default ContentWithVisuals;

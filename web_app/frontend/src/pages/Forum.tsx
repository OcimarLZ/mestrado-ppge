import React from 'react';
import { Link } from 'react-router-dom';
import * as LucideIcons from 'lucide-react';
import { ArrowRight, MessagesSquare } from 'lucide-react';
import topicos from '../data/forumTopicos';

const Forum: React.FC = () => {
  return (
    <div className="container" style={{ marginTop: '2rem', paddingBottom: '4rem' }}>
      <div className="chapter-header">
        <h1><MessagesSquare size={28} style={{ marginRight: '0.5rem', verticalAlign: 'middle', color: 'var(--accent-primary)' }} />Fórum de Discussões</h1>
        <p className="lead" style={{ color: 'var(--text-secondary)' }}>
          Um espaço de diálogo sobre os temas desta pesquisa. Escolha um tópico, faça uma
          pergunta ou responda a quem já perguntou — não é necessário criar conta, basta um
          nome para comentar.
        </p>
      </div>

      <div className="grid-3">
        {topicos.map((topico) => {
          // @ts-ignore
          const Icon = LucideIcons[topico.icon] || MessagesSquare;
          return (
            <Link key={topico.slug} to={`/forum/${topico.slug}`} className="glass-panel pesquisa-index-card">
              <Icon color="var(--accent-primary)" size={32} />
              <h3 style={{ margin: '1rem 0 0.5rem 0' }}>{topico.title}</h3>
              <p style={{ fontSize: '0.9rem', flex: 1 }}>{topico.description}</p>
              <span className="pesquisa-index-card-link">
                Participar <ArrowRight size={16} />
              </span>
            </Link>
          );
        })}
      </div>
    </div>
  );
};

export default Forum;

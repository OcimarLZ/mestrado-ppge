import React from 'react';
import { Construction } from 'lucide-react';

const PaineisInterativos: React.FC = () => {
  return (
    <div className="container" style={{ marginTop: '2rem', paddingBottom: '4rem' }}>
      <div className="chapter-header">
        <h1><Construction size={28} style={{ marginRight: '0.5rem', verticalAlign: 'middle', color: 'var(--accent-primary)' }} />Painéis Interativos</h1>
      </div>

      <div className="glass-panel" style={{ textAlign: 'center', padding: '3rem 2rem' }}>
        <Construction size={40} color="var(--accent-primary)" style={{ marginBottom: '1rem' }} />
        <h2 style={{ marginBottom: '0.5rem' }}>Em Construção...</h2>
        <p style={{ color: 'var(--text-secondary)', maxWidth: 480, margin: '0 auto' }}>
          Esta seção vai reunir painéis interativos com consultas ao vivo sobre os dados da
          pesquisa. Em breve.
        </p>
      </div>
    </div>
  );
};

export default PaineisInterativos;

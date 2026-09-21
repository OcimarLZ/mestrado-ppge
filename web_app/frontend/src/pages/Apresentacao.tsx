import React from 'react';
import { Presentation } from 'lucide-react';

// TODO: substituir por um visualizador de slides navegavel (setas/teclado) assim que o
// roteiro da apresentacao de defesa for aprovado.
const Apresentacao: React.FC = () => {
  return (
    <div className="container" style={{ marginTop: '2rem', paddingBottom: '4rem' }}>
      <div className="chapter-header">
        <h1>Apresentação</h1>
        <p className="lead" style={{ color: 'var(--text-secondary)' }}>
          Slides para a defesa da dissertação.
        </p>
      </div>
      <div className="glass-panel" style={{ minHeight: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px dashed var(--accent-secondary)' }}>
        <div className="text-center">
          <Presentation size={64} color="var(--text-secondary)" style={{ opacity: 0.5, marginBottom: '1rem' }} />
          <h3 style={{ color: 'var(--text-secondary)' }}>Em construção</h3>
          <p>A apresentação navegável ficará disponível aqui em breve.</p>
        </div>
      </div>
    </div>
  );
};

export default Apresentacao;

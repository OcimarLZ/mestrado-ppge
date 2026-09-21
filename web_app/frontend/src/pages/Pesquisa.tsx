import React from 'react';
import { BarChart3 } from 'lucide-react';

// TODO: substituir por paginas com os principais achados/indicadores dos capitulos
// 3-6 e das consideracoes finais, em formato de cards, assim que a curadoria for
// definida com o autor.
const Pesquisa: React.FC = () => {
  return (
    <div className="container" style={{ marginTop: '2rem', paddingBottom: '4rem' }}>
      <div className="chapter-header">
        <h1>Pesquisa</h1>
        <p className="lead" style={{ color: 'var(--text-secondary)' }}>
          Os principais achados e indicadores da pesquisa.
        </p>
      </div>
      <div className="glass-panel" style={{ minHeight: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px dashed var(--accent-secondary)' }}>
        <div className="text-center">
          <BarChart3 size={64} color="var(--text-secondary)" style={{ opacity: 0.5, marginBottom: '1rem' }} />
          <h3 style={{ color: 'var(--text-secondary)' }}>Em construção</h3>
          <p>Os cards com os principais achados da pesquisa ficarão disponíveis aqui em breve.</p>
        </div>
      </div>
    </div>
  );
};

export default Pesquisa;

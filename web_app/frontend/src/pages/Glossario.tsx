import React, { useMemo, useState } from 'react';
import { BookOpenText, Search } from 'lucide-react';
import glossario from '../data/glossario';

const Glossario: React.FC = () => {
  const [busca, setBusca] = useState('');

  const filtrados = useMemo(() => {
    const termo = busca.trim().toLowerCase();
    if (!termo) return glossario;
    return glossario.filter((g) => g.termo.toLowerCase().includes(termo) || g.definicao.toLowerCase().includes(termo));
  }, [busca]);

  return (
    <div className="container" style={{ marginTop: '2rem', paddingBottom: '4rem' }}>
      <div className="chapter-header">
        <h1><BookOpenText size={28} style={{ marginRight: '0.5rem', verticalAlign: 'middle', color: 'var(--accent-primary)' }} />Glossário</h1>
        <p className="lead" style={{ color: 'var(--text-secondary)' }}>
          Termos e conceitos utilizados na dissertação, conforme o glossário original (p. 19-22).
        </p>
      </div>

      <div className="data-table-toolbar glass-panel">
        <div className="data-table-search">
          <Search size={16} />
          <input
            type="text"
            placeholder="Buscar termo ou definição..."
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
          />
        </div>
        <span className="data-table-count">{filtrados.length} de {glossario.length} termos</span>
      </div>

      <div className="data-table-wrapper glass-panel">
        <div className="data-table-scroll">
          <table className="data-table">
            <thead>
              <tr>
                <th className="is-sticky">Termo</th>
                <th>Definição</th>
              </tr>
            </thead>
            <tbody>
              {filtrados.map((g) => (
                <tr key={g.termo}>
                  <td className="is-sticky"><strong>{g.termo}</strong></td>
                  <td>{g.definicao}</td>
                </tr>
              ))}
              {filtrados.length === 0 && (
                <tr><td colSpan={2} className="data-table-empty">Nenhum termo encontrado.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Glossario;

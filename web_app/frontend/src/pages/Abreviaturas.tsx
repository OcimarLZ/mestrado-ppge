import React, { useMemo, useState } from 'react';
import { ListOrdered, Search } from 'lucide-react';
import abreviaturas from '../data/abreviaturas';

const Abreviaturas: React.FC = () => {
  const [busca, setBusca] = useState('');

  const filtrados = useMemo(() => {
    const termo = busca.trim().toLowerCase();
    if (!termo) return abreviaturas;
    return abreviaturas.filter((a) => a.sigla.toLowerCase().includes(termo) || a.significado.toLowerCase().includes(termo));
  }, [busca]);

  return (
    <div className="container" style={{ marginTop: '2rem', paddingBottom: '4rem' }}>
      <div className="chapter-header">
        <h1><ListOrdered size={28} style={{ marginRight: '0.5rem', verticalAlign: 'middle', color: 'var(--accent-primary)' }} />Lista de Abreviaturas e Siglas</h1>
        <p className="lead" style={{ color: 'var(--text-secondary)' }}>
          Abreviaturas e siglas utilizadas na dissertação, conforme a lista original (p. 23-27).
        </p>
      </div>

      <div className="data-table-toolbar glass-panel">
        <div className="data-table-search">
          <Search size={16} />
          <input
            type="text"
            placeholder="Buscar sigla ou significado..."
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
          />
        </div>
        <span className="data-table-count">{filtrados.length} de {abreviaturas.length} siglas</span>
      </div>

      <div className="data-table-wrapper glass-panel">
        <div className="data-table-scroll">
          <table className="data-table">
            <thead>
              <tr>
                <th className="is-sticky">Sigla</th>
                <th>Significado</th>
              </tr>
            </thead>
            <tbody>
              {filtrados.map((a) => (
                <tr key={a.sigla}>
                  <td className="is-sticky"><strong>{a.sigla}</strong></td>
                  <td>{a.significado}</td>
                </tr>
              ))}
              {filtrados.length === 0 && (
                <tr><td colSpan={2} className="data-table-empty">Nenhuma sigla encontrada.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Abreviaturas;

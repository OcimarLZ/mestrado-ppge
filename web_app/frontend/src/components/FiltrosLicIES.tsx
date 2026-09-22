import React, { useMemo } from 'react';
import { Search } from 'lucide-react';
import type { AnoCenso, LicIesRegistro } from '../lib/licIesData';

interface Props {
  registros: LicIesRegistro[];
  totalFiltrado: number;
  busca: string;
  onBuscaChange: (v: string) => void;
  uf: string;
  onUfChange: (v: string) => void;
  ano: AnoCenso;
  onAnoChange: (v: AnoCenso) => void;
  anos: AnoCenso[];
}

// Filtros de ano/busca/UF, elevados para a pagina (Pesquisa > Explorar dados) para que
// indicadores, graficos e tabela reajam todos ao mesmo filtro.
const FiltrosLicIES: React.FC<Props> = ({ registros, totalFiltrado, busca, onBuscaChange, uf, onUfChange, ano, onAnoChange, anos }) => {
  const ufs = useMemo(() => Array.from(new Set(registros.map((r) => r.estado))).sort(), [registros]);

  return (
    <div className="data-table-toolbar glass-panel">
      <div className="data-table-ano-toggle" role="group" aria-label="Ano do censo">
        {anos.map((a) => (
          <button
            key={a}
            type="button"
            className={a === ano ? 'is-active' : ''}
            onClick={() => onAnoChange(a)}
          >
            {a}
          </button>
        ))}
      </div>
      <div className="data-table-search">
        <Search size={16} />
        <input
          type="text"
          placeholder="Buscar por nome ou sigla..."
          value={busca}
          onChange={(e) => onBuscaChange(e.target.value)}
        />
      </div>
      <select value={uf} onChange={(e) => onUfChange(e.target.value)} className="data-table-uf-select">
        <option value="">Todas as UFs</option>
        {ufs.map((u) => <option key={u} value={u}>{u}</option>)}
      </select>
      <span className="data-table-count">{totalFiltrado} de {registros.length} instituições</span>
    </div>
  );
};

export default FiltrosLicIES;

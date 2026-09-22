import React, { useMemo } from 'react';
import { Search } from 'lucide-react';
import type { LicIesRegistro } from '../lib/licIesData';

interface Props {
  registros: LicIesRegistro[];
  totalFiltrado: number;
  busca: string;
  onBuscaChange: (v: string) => void;
  uf: string;
  onUfChange: (v: string) => void;
}

// Filtros de busca/UF, elevados para a pagina (Pesquisa > Explorar dados) para que
// indicadores, graficos e tabela reajam todos ao mesmo filtro.
const FiltrosLicIES: React.FC<Props> = ({ registros, totalFiltrado, busca, onBuscaChange, uf, onUfChange }) => {
  const ufs = useMemo(() => Array.from(new Set(registros.map((r) => r.estado))).sort(), [registros]);

  return (
    <div className="data-table-toolbar glass-panel">
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

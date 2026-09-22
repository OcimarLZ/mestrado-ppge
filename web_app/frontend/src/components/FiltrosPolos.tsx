import React, { useMemo } from 'react';
import { Search } from 'lucide-react';
import type { AnoCenso } from '../lib/licIesData';
import type { LicPoloRegistro, TipoPolo } from '../lib/licPolosData';

interface Props {
  registros: LicPoloRegistro[];
  totalFiltrado: number;
  busca: string;
  onBuscaChange: (v: string) => void;
  uf: string;
  onUfChange: (v: string) => void;
  tipo: TipoPolo | '';
  onTipoChange: (v: TipoPolo | '') => void;
  ano: AnoCenso;
  onAnoChange: (v: AnoCenso) => void;
  anos: AnoCenso[];
}

const TIPOS: TipoPolo[] = ['Presencial', 'EaD próprio', 'UAB'];

const FiltrosPolos: React.FC<Props> = ({ registros, totalFiltrado, busca, onBuscaChange, uf, onUfChange, tipo, onTipoChange, ano, onAnoChange, anos }) => {
  const ufs = useMemo(() => Array.from(new Set(registros.map((r) => r.ies_uf))).sort(), [registros]);

  return (
    <div className="data-table-toolbar glass-panel">
      <div className="data-table-ano-toggle" role="group" aria-label="Ano do censo">
        {anos.map((a) => (
          <button key={a} type="button" className={a === ano ? 'is-active' : ''} onClick={() => onAnoChange(a)}>
            {a}
          </button>
        ))}
      </div>
      <div className="data-table-search">
        <Search size={16} />
        <input
          type="text"
          placeholder="Buscar por IES, sigla ou município..."
          value={busca}
          onChange={(e) => onBuscaChange(e.target.value)}
        />
      </div>
      <select value={uf} onChange={(e) => onUfChange(e.target.value)} className="data-table-uf-select">
        <option value="">Todas as UFs (sede)</option>
        {ufs.map((u) => <option key={u} value={u}>{u}</option>)}
      </select>
      <select value={tipo} onChange={(e) => onTipoChange(e.target.value as TipoPolo | '')} className="data-table-uf-select">
        <option value="">Todos os tipos</option>
        {TIPOS.map((t) => <option key={t} value={t}>{t}</option>)}
      </select>
      <span className="data-table-count">{totalFiltrado} de {registros.length} polos/campus</span>
    </div>
  );
};

export default FiltrosPolos;

import React, { useMemo } from 'react';
import { Search } from 'lucide-react';
import type { ApendicePerfilRegistro } from '../lib/apendicePerfilData';

interface Props {
  registros: ApendicePerfilRegistro[];
  busca: string;
  onBuscaChange: (v: string) => void;
  selecionado: string;
  onSelecionadoChange: (nomeIes: string) => void;
}

const SeletorPerfilInstitucional: React.FC<Props> = ({ registros, busca, onBuscaChange, selecionado, onSelecionadoChange }) => {
  const filtrados = useMemo(() => {
    const termo = busca.trim().toLowerCase();
    if (!termo) return registros;
    return registros.filter((r) =>
      r.nome_ies.toLowerCase().includes(termo) || (r.sigla ?? '').toLowerCase().includes(termo)
    );
  }, [registros, busca]);

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
      <select
        value={selecionado}
        onChange={(e) => onSelecionadoChange(e.target.value)}
        className="data-table-uf-select perfil-ies-select"
      >
        {filtrados.map((r) => (
          <option key={r.nome_ies} value={r.nome_ies}>
            {r.sigla ? `${r.sigla} — ${r.nome_ies}` : r.nome_ies}
          </option>
        ))}
      </select>
      <span className="data-table-count">{filtrados.length} de {registros.length} instituições</span>
    </div>
  );
};

export default SeletorPerfilInstitucional;

import React, { useMemo, useState } from 'react';
import { ArrowUpDown, ArrowUp, ArrowDown, Search } from 'lucide-react';
import { getLicIesRegistros, type LicIesRegistro } from '../lib/licIesData';

type ColKey = keyof LicIesRegistro;

interface ColDef {
  key: ColKey;
  label: string;
  title: string;
  group: string;
  numeric?: boolean;
  format?: (v: LicIesRegistro[ColKey]) => string;
}

const anoFmt = (v: LicIesRegistro[ColKey]) => (v === null || v === undefined ? '—' : String(v));
const pctFmt = (v: LicIesRegistro[ColKey]) => `${Number(v).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}%`;
const intFmt = (v: LicIesRegistro[ColKey]) => Number(v).toLocaleString('pt-BR');

const COLUMNS: ColDef[] = [
  { key: 'ies_nome', label: 'IES', title: 'Instituição de ensino superior', group: 'Identificação' },
  { key: 'sigla', label: 'Sigla', title: 'Sigla da instituição', group: 'Identificação' },
  { key: 'estado', label: 'UF', title: 'Unidade da federação', group: 'Identificação' },
  { key: 'a_ultimo_ano_presencial', label: 'Últ. ano', title: 'Último ano do censo com oferta presencial de licenciatura', group: 'Presencial', numeric: true, format: anoFmt },
  { key: 'b_qtd_mun_presencial', label: 'Municípios', title: 'Municípios com oferta presencial de licenciatura no último ano ofertado', group: 'Presencial', numeric: true, format: intFmt },
  { key: 'b_qtd_cursos_presencial', label: 'Cursos', title: 'Cursos de licenciatura presencial no último ano ofertado', group: 'Presencial', numeric: true, format: intFmt },
  { key: 'c_ultimo_ano_ead', label: 'Últ. ano', title: 'Último ano do censo com oferta EaD de licenciatura', group: 'EaD', numeric: true, format: anoFmt },
  { key: 'd_qtd_mun_ead', label: 'Municípios', title: 'Municípios com oferta EaD de licenciatura no último ano ofertado', group: 'EaD', numeric: true, format: intFmt },
  { key: 'd_qtd_cursos_ead', label: 'Cursos', title: 'Cursos de licenciatura EaD no último ano ofertado', group: 'EaD', numeric: true, format: intFmt },
  { key: 'e_ultimo_ano_uab', label: 'Últ. ano', title: 'Último ano do censo com polo UAB ativo de licenciatura', group: 'UAB', numeric: true, format: anoFmt },
  { key: 'f_qtd_polos_uab', label: 'Polos', title: 'Polos UAB ativos de licenciatura no último ano ofertado', group: 'UAB', numeric: true, format: intFmt },
  { key: 'f_qtd_cursos_uab', label: 'Cursos', title: 'Cursos de licenciatura via UAB no último ano ofertado', group: 'UAB', numeric: true, format: intFmt },
  { key: 'g_total_matriculas_2024', label: 'Total IES', title: 'Total de matrículas da instituição em todos os cursos (2024)', group: 'Matrículas (2024)', numeric: true, format: intFmt },
  { key: 'h_total_matriculas_lic_2024', label: 'Licenciatura', title: 'Total de matrículas em licenciatura (2024)', group: 'Matrículas (2024)', numeric: true, format: intFmt },
  { key: 'k_perc_licenciatura', label: '% Lic.', title: 'Percentual de matrículas em licenciatura sobre o total da instituição', group: 'Matrículas (2024)', numeric: true, format: pctFmt },
  { key: 'i_mat_lic_ead_proprios', label: 'EaD próprio', title: 'Matrículas de licenciatura em EaD com polo próprio da instituição (2024)', group: 'Matrículas (2024)', numeric: true, format: intFmt },
  { key: 'j_mat_lic_ead_uab', label: 'EaD UAB', title: 'Matrículas de licenciatura em EaD via polo UAB (2024)', group: 'Matrículas (2024)', numeric: true, format: intFmt },
  { key: 'l_perc_ead_proprios', label: '% EaD próprio', title: 'Percentual das matrículas de licenciatura em EaD com polo próprio', group: 'Matrículas (2024)', numeric: true, format: pctFmt },
  { key: 'm_perc_ead_uab', label: '% EaD UAB', title: 'Percentual das matrículas de licenciatura em EaD via UAB', group: 'Matrículas (2024)', numeric: true, format: pctFmt },
];

// Agrupa colunas adjacentes com o mesmo "group" para o cabeçalho de duas linhas
const GROUPS = COLUMNS.reduce<{ group: string; span: number }[]>((acc, col) => {
  const last = acc[acc.length - 1];
  if (last && last.group === col.group) last.span += 1;
  else acc.push({ group: col.group, span: 1 });
  return acc;
}, []);

type SortDir = 'asc' | 'desc';

const DataTableLicIES: React.FC = () => {
  const registros = useMemo(() => getLicIesRegistros(), []);
  const [busca, setBusca] = useState('');
  const [uf, setUf] = useState('');
  const [sortKey, setSortKey] = useState<ColKey>('ies_nome');
  const [sortDir, setSortDir] = useState<SortDir>('asc');

  const ufs = useMemo(() => Array.from(new Set(registros.map((r) => r.estado))).sort(), [registros]);

  const filtrados = useMemo(() => {
    const termo = busca.trim().toLowerCase();
    return registros.filter((r) => {
      if (uf && r.estado !== uf) return false;
      if (!termo) return true;
      return r.ies_nome.toLowerCase().includes(termo) || r.sigla.toLowerCase().includes(termo);
    });
  }, [registros, busca, uf]);

  const ordenados = useMemo(() => {
    const copia = [...filtrados];
    copia.sort((a, b) => {
      const va = a[sortKey];
      const vb = b[sortKey];
      let cmp: number;
      if (va === null || va === undefined) cmp = -1;
      else if (vb === null || vb === undefined) cmp = 1;
      else if (typeof va === 'number' && typeof vb === 'number') cmp = va - vb;
      else cmp = String(va).localeCompare(String(vb), 'pt-BR');
      return sortDir === 'asc' ? cmp : -cmp;
    });
    return copia;
  }, [filtrados, sortKey, sortDir]);

  const toggleSort = (key: ColKey) => {
    if (key === sortKey) {
      setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortKey(key);
      setSortDir(key === 'ies_nome' || key === 'sigla' || key === 'estado' ? 'asc' : 'desc');
    }
  };

  return (
    <div className="data-table-wrapper glass-panel">
      <div className="data-table-toolbar">
        <div className="data-table-search">
          <Search size={16} />
          <input
            type="text"
            placeholder="Buscar por nome ou sigla..."
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
          />
        </div>
        <select value={uf} onChange={(e) => setUf(e.target.value)} className="data-table-uf-select">
          <option value="">Todas as UFs</option>
          {ufs.map((u) => <option key={u} value={u}>{u}</option>)}
        </select>
        <span className="data-table-count">{ordenados.length} de {registros.length} instituições</span>
      </div>

      <div className="data-table-scroll">
        <table className="data-table">
          <thead>
            <tr>
              {GROUPS.map((g, i) => (
                <th key={i} colSpan={g.span} className="data-table-group-header">{g.group}</th>
              ))}
            </tr>
            <tr>
              {COLUMNS.map((col) => (
                <th
                  key={col.key}
                  title={col.title}
                  className={`${col.numeric ? 'is-numeric' : ''} ${col.key === 'ies_nome' ? 'is-sticky' : ''}`}
                  onClick={() => toggleSort(col.key)}
                >
                  <span className="data-table-th-inner">
                    {col.label}
                    {sortKey === col.key ? (
                      sortDir === 'asc' ? <ArrowUp size={12} /> : <ArrowDown size={12} />
                    ) : (
                      <ArrowUpDown size={12} className="data-table-sort-idle" />
                    )}
                  </span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {ordenados.map((r) => (
              <tr key={r.ies_nome + r.sigla}>
                {COLUMNS.map((col) => (
                  <td key={col.key} className={`${col.numeric ? 'is-numeric' : ''} ${col.key === 'ies_nome' ? 'is-sticky' : ''}`}>
                    {col.format ? col.format(r[col.key]) : String(r[col.key])}
                  </td>
                ))}
              </tr>
            ))}
            {ordenados.length === 0 && (
              <tr><td colSpan={COLUMNS.length} className="data-table-empty">Nenhuma instituição encontrada para este filtro.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DataTableLicIES;

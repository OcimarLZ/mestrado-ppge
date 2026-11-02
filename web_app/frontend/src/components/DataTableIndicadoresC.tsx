import React, { useMemo, useState } from 'react';
import { ArrowUpDown, ArrowUp, ArrowDown } from 'lucide-react';
import type { ApendiceCRegistro } from '../lib/apendiceCData';

type ColKey = keyof ApendiceCRegistro;

interface ColDef {
  key: ColKey;
  label: string;
  title: string;
  group: string;
  numeric?: boolean;
  format?: (v: ApendiceCRegistro[ColKey]) => string;
}

const simNaoFmt = (v: ApendiceCRegistro[ColKey]) => (v ? 'Sim' : 'Não');
const intFmt = (v: ApendiceCRegistro[ColKey]) => Number(v).toLocaleString('pt-BR');
const pctFmt = (v: ApendiceCRegistro[ColKey]) => `${(Number(v) * 100).toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%`;

const COLUMNS: ColDef[] = [
  { key: 'sigla', label: 'IES', title: 'Sigla da instituição', group: 'Identificação' },
  { key: 'estado', label: 'UF', title: 'Unidade da federação', group: 'Identificação' },
  { key: 'num_campus_presencial_licenciatura', label: 'Campus', title: 'Municípios com licenciatura presencial em 2024', group: 'Oferta', numeric: true, format: intFmt },
  { key: 'ead_propria_oferece', label: 'Oferece', title: 'Oferece licenciatura em EaD própria (fora da UAB) em 2024', group: 'EaD Própria', format: simNaoFmt },
  { key: 'ead_propria_num_polos', label: 'Polos', title: 'Polos de EaD própria em 2024', group: 'EaD Própria', numeric: true, format: intFmt },
  { key: 'ead_propria_num_cursos', label: 'Cursos', title: 'Cursos de licenciatura em EaD própria em 2024', group: 'EaD Própria', numeric: true, format: intFmt },
  { key: 'uab_oferece', label: 'Oferece', title: 'Oferece licenciatura via UAB em 2024', group: 'UAB', format: simNaoFmt },
  { key: 'uab_num_polos', label: 'Polos', title: 'Polos UAB em 2024', group: 'UAB', numeric: true, format: intFmt },
  { key: 'uab_num_cursos', label: 'Cursos', title: 'Cursos de licenciatura via UAB em 2024', group: 'UAB', numeric: true, format: intFmt },
  { key: 'matriculas_total_ies', label: 'Total IES', title: 'Total de matrículas da instituição em todos os cursos (2024)', group: 'Matrículas', numeric: true, format: intFmt },
  { key: 'matriculas_licenciatura', label: 'Licenciatura', title: 'Total de matrículas em licenciatura (2024)', group: 'Matrículas', numeric: true, format: intFmt },
  { key: 'perc_licenciatura_no_total', label: '% Lic./Total', title: 'Percentual de matrículas em licenciatura sobre o total da instituição', group: 'Matrículas', numeric: true, format: pctFmt },
  { key: 'perc_ead_propria_na_lic', label: '% EaD própria', title: 'Percentual das matrículas de licenciatura em EaD própria sobre o total em licenciatura', group: 'Matrículas', numeric: true, format: pctFmt },
  { key: 'perc_uab_na_lic', label: '% UAB', title: 'Percentual das matrículas de licenciatura via UAB sobre o total em licenciatura', group: 'Matrículas', numeric: true, format: pctFmt },
  { key: 'perc_presencial_na_lic', label: '% Presencial', title: 'Percentual das matrículas de licenciatura presencial sobre o total em licenciatura', group: 'Matrículas', numeric: true, format: pctFmt },
];

const GROUPS = COLUMNS.reduce<{ group: string; span: number }[]>((acc, col) => {
  const last = acc[acc.length - 1];
  if (last && last.group === col.group) last.span += 1;
  else acc.push({ group: col.group, span: 1 });
  return acc;
}, []);

type SortDir = 'asc' | 'desc';

const DataTableIndicadoresC: React.FC<{ registros: ApendiceCRegistro[] }> = ({ registros }) => {
  const [sortKey, setSortKey] = useState<ColKey>('sigla');
  const [sortDir, setSortDir] = useState<SortDir>('asc');

  const ordenados = useMemo(() => {
    const copia = [...registros];
    copia.sort((a, b) => {
      const va = a[sortKey];
      const vb = b[sortKey];
      let cmp: number;
      if (va === null || va === undefined) cmp = -1;
      else if (vb === null || vb === undefined) cmp = 1;
      else if (typeof va === 'number' && typeof vb === 'number') cmp = va - vb;
      else if (typeof va === 'boolean' && typeof vb === 'boolean') cmp = Number(va) - Number(vb);
      else cmp = String(va).localeCompare(String(vb), 'pt-BR');
      return sortDir === 'asc' ? cmp : -cmp;
    });
    return copia;
  }, [registros, sortKey, sortDir]);

  const toggleSort = (key: ColKey) => {
    if (key === sortKey) {
      setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortKey(key);
      setSortDir(key === 'sigla' || key === 'estado' ? 'asc' : 'desc');
    }
  };

  return (
    <div className="data-table-wrapper glass-panel">
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
                  className={`${col.numeric ? 'is-numeric' : ''} ${col.key === 'sigla' ? 'is-sticky' : ''}`}
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
              <tr key={r.sigla}>
                {COLUMNS.map((col) => (
                  <td key={col.key} className={`${col.numeric ? 'is-numeric' : ''} ${col.key === 'sigla' ? 'is-sticky' : ''}`}>
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

export default DataTableIndicadoresC;

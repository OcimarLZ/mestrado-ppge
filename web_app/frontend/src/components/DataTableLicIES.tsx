import React, { useMemo, useState } from 'react';
import { ArrowUpDown, ArrowUp, ArrowDown } from 'lucide-react';
import type { LicIesRegistro } from '../lib/licIesData';

type ColKey = keyof LicIesRegistro;

interface ColDef {
  key: ColKey;
  label: string;
  title: string;
  group: string;
  numeric?: boolean;
  format?: (v: LicIesRegistro[ColKey]) => string;
}

const pctFmt = (v: LicIesRegistro[ColKey]) => `${Number(v).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}%`;
const intFmt = (v: LicIesRegistro[ColKey]) => Number(v).toLocaleString('pt-BR');

const COLUMNS: ColDef[] = [
  { key: 'ies_nome', label: 'IES', title: 'Instituição de ensino superior', group: 'Identificação' },
  { key: 'sigla', label: 'Sigla', title: 'Sigla da instituição', group: 'Identificação' },
  { key: 'estado', label: 'UF', title: 'Unidade da federação', group: 'Identificação' },
  { key: 'num_cursos_lic', label: 'Cursos', title: 'Cursos de licenciatura no ano selecionado', group: 'Oferta', numeric: true, format: intFmt },
  { key: 'num_campus_presencial', label: 'Campus', title: 'Municípios com licenciatura presencial no ano selecionado', group: 'Oferta', numeric: true, format: intFmt },
  { key: 'num_polos_ead_proprio', label: 'Polos EaD próprio', title: 'Municípios com licenciatura EaD própria (fora da UAB) no ano selecionado', group: 'Oferta', numeric: true, format: intFmt },
  { key: 'num_polos_uab', label: 'Polos UAB', title: 'Municípios com licenciatura via UAB no ano selecionado', group: 'Oferta', numeric: true, format: intFmt },
  { key: 'total_matriculas', label: 'Total IES', title: 'Total de matrículas da instituição em todos os cursos', group: 'Matrículas', numeric: true, format: intFmt },
  { key: 'total_matriculas_lic', label: 'Licenciatura', title: 'Total de matrículas em licenciatura', group: 'Matrículas', numeric: true, format: intFmt },
  { key: 'perc_licenciatura', label: '% Lic.', title: 'Percentual de matrículas em licenciatura sobre o total da instituição', group: 'Matrículas', numeric: true, format: pctFmt },
  { key: 'mat_lic_presencial', label: 'Presencial', title: 'Matrículas de licenciatura presencial', group: 'Matrículas', numeric: true, format: intFmt },
  { key: 'mat_lic_ead_proprio', label: 'EaD próprio', title: 'Matrículas de licenciatura em EaD própria (fora da UAB)', group: 'Matrículas', numeric: true, format: intFmt },
  { key: 'mat_lic_uab', label: 'EaD UAB', title: 'Matrículas de licenciatura via UAB', group: 'Matrículas', numeric: true, format: intFmt },
  { key: 'perc_lic_ead_proprio', label: '% EaD próprio', title: 'Percentual das matrículas de licenciatura em EaD própria sobre o total em licenciatura', group: 'Matrículas', numeric: true, format: pctFmt },
  { key: 'perc_lic_uab', label: '% EaD UAB', title: 'Percentual das matrículas de licenciatura via UAB sobre o total em licenciatura', group: 'Matrículas', numeric: true, format: pctFmt },
];

// Agrupa colunas adjacentes com o mesmo "group" para o cabeçalho de duas linhas
const GROUPS = COLUMNS.reduce<{ group: string; span: number }[]>((acc, col) => {
  const last = acc[acc.length - 1];
  if (last && last.group === col.group) last.span += 1;
  else acc.push({ group: col.group, span: 1 });
  return acc;
}, []);

type SortDir = 'asc' | 'desc';

const DataTableLicIES: React.FC<{ registros: LicIesRegistro[] }> = ({ registros }) => {
  const [sortKey, setSortKey] = useState<ColKey>('ies_nome');
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
      setSortDir(key === 'ies_nome' || key === 'sigla' || key === 'estado' ? 'asc' : 'desc');
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

import React, { useMemo, useState } from 'react';
import { ArrowUpDown, ArrowUp, ArrowDown } from 'lucide-react';
import type { LicPoloRegistro } from '../lib/licPolosData';

type ColKey = keyof LicPoloRegistro;

interface ColDef {
  key: ColKey;
  label: string;
  title: string;
  numeric?: boolean;
  format?: (v: LicPoloRegistro[ColKey]) => string;
}

const intFmt = (v: LicPoloRegistro[ColKey]) => Number(v).toLocaleString('pt-BR');

const COLUMNS: ColDef[] = [
  { key: 'ies_nome', label: 'IES', title: 'Instituição de ensino superior' },
  { key: 'sigla', label: 'Sigla', title: 'Sigla da instituição' },
  { key: 'ies_uf', label: 'UF sede', title: 'UF da sede da instituição' },
  { key: 'municipio', label: 'Município do polo', title: 'Município onde o curso é ofertado' },
  { key: 'municipio_uf', label: 'UF polo', title: 'UF do município do polo' },
  { key: 'tipo_polo', label: 'Tipo', title: 'Presencial, EaD próprio ou via UAB' },
  { key: 'num_cursos', label: 'Cursos', title: 'Cursos de licenciatura ofertados neste polo', numeric: true, format: intFmt },
  { key: 'matriculas', label: 'Matrículas', title: 'Total de matrículas em licenciatura neste polo', numeric: true, format: intFmt },
];

type SortDir = 'asc' | 'desc';

const DataTablePolos: React.FC<{ registros: LicPoloRegistro[] }> = ({ registros }) => {
  const [sortKey, setSortKey] = useState<ColKey>('matriculas');
  const [sortDir, setSortDir] = useState<SortDir>('desc');

  const ordenados = useMemo(() => {
    const copia = [...registros];
    copia.sort((a, b) => {
      const va = a[sortKey];
      const vb = b[sortKey];
      let cmp: number;
      if (typeof va === 'number' && typeof vb === 'number') cmp = va - vb;
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
      setSortDir(key === 'matriculas' || key === 'num_cursos' ? 'desc' : 'asc');
    }
  };

  return (
    <div className="data-table-wrapper glass-panel">
      <div className="data-table-scroll">
        <table className="data-table">
          <thead>
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
            {ordenados.map((r, i) => (
              <tr key={`${r.sigla}-${r.municipio}-${r.tipo_polo}-${i}`}>
                {COLUMNS.map((col) => (
                  <td key={col.key} className={`${col.numeric ? 'is-numeric' : ''} ${col.key === 'ies_nome' ? 'is-sticky' : ''}`}>
                    {col.format ? col.format(r[col.key]) : String(r[col.key])}
                  </td>
                ))}
              </tr>
            ))}
            {ordenados.length === 0 && (
              <tr><td colSpan={COLUMNS.length} className="data-table-empty">Nenhum polo encontrado para este filtro.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DataTablePolos;

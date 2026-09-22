import React, { useEffect, useMemo, useState } from 'react';
import { ArrowUpDown, ArrowUp, ArrowDown, ChevronRight, ChevronDown } from 'lucide-react';
import type { LicPoloRegistro } from '../lib/licPolosData';
import { getCursosDoPolo, type LicPoloCursoRegistro } from '../lib/licPolosCursosData';

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

const TOTAL_COLS = COLUMNS.length + 1; // +1 pela coluna do chevron de expandir

type SortDir = 'asc' | 'desc';

const chaveLinha = (r: LicPoloRegistro) => `${r.sigla}|${r.ano_censo}|${r.municipio}|${r.tipo_polo}`;

const DataTablePolos: React.FC<{ registros: LicPoloRegistro[] }> = ({ registros }) => {
  const [sortKey, setSortKey] = useState<ColKey>('matriculas');
  const [sortDir, setSortDir] = useState<SortDir>('desc');
  const [expandidos, setExpandidos] = useState<Set<string>>(new Set());

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

  const toggleExpandido = (k: string) => {
    setExpandidos((prev) => {
      const novo = new Set(prev);
      if (novo.has(k)) novo.delete(k);
      else novo.add(k);
      return novo;
    });
  };

  return (
    <div className="data-table-wrapper glass-panel">
      <p className="data-table-hint">Clique numa linha para ver os cursos ofertados naquele polo/campus.</p>
      <div className="data-table-scroll">
        <table className="data-table">
          <thead>
            <tr>
              <th className="data-table-expand-col" />
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
            {ordenados.map((r, i) => {
              const k = chaveLinha(r);
              const aberto = expandidos.has(k);
              return (
                <React.Fragment key={`${k}-${i}`}>
                  <tr className="data-table-row-expandable" onClick={() => toggleExpandido(k)}>
                    <td className="data-table-expand-col">
                      {aberto ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                    </td>
                    {COLUMNS.map((col) => (
                      <td key={col.key} className={`${col.numeric ? 'is-numeric' : ''} ${col.key === 'ies_nome' ? 'is-sticky' : ''}`}>
                        {col.format ? col.format(r[col.key]) : String(r[col.key])}
                      </td>
                    ))}
                  </tr>
                  {aberto && (
                    <tr className="data-table-subrow">
                      <td colSpan={TOTAL_COLS}>
                        <CursosDoPolo registro={r} />
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              );
            })}
            {ordenados.length === 0 && (
              <tr><td colSpan={TOTAL_COLS} className="data-table-empty">Nenhum polo encontrado para este filtro.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

const CursosDoPolo: React.FC<{ registro: LicPoloRegistro }> = ({ registro }) => {
  const [cursos, setCursos] = useState<LicPoloCursoRegistro[] | null>(null);

  useEffect(() => {
    let ativo = true;
    setCursos(null);
    getCursosDoPolo(registro.sigla, registro.ano_censo, registro.municipio, registro.tipo_polo).then((lista) => {
      if (ativo) setCursos(lista);
    });
    return () => { ativo = false; };
  }, [registro]);

  if (cursos === null) {
    return <div className="data-subtable-empty">Carregando cursos...</div>;
  }

  if (cursos.length === 0) {
    return <div className="data-subtable-empty">Nenhum curso com matrícula registrada neste polo/ano.</div>;
  }

  return (
    <table className="data-subtable">
      <thead>
        <tr>
          <th>Curso</th>
          <th className="is-numeric">Matrículas</th>
        </tr>
      </thead>
      <tbody>
        {cursos.map((c) => (
          <tr key={c.curso}>
            <td>{c.curso}</td>
            <td className="is-numeric">{c.matriculas.toLocaleString('pt-BR')}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default DataTablePolos;

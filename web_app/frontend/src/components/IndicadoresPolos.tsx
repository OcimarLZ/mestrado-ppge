import React, { useMemo } from 'react';
import type { LicPoloRegistro } from '../lib/licPolosData';
import { calcularIndicadoresPolos } from '../lib/licPolosAgregados';

const intFmt = (v: number) => Math.round(v).toLocaleString('pt-BR');
const pctFmt = (v: number) => `${v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%`;

const IndicadoresPolos: React.FC<{ registros: LicPoloRegistro[]; totalGeral: number }> = ({ registros, totalGeral }) => {
  const ind = useMemo(() => calcularIndicadoresPolos(registros), [registros]);

  const tiles = [
    { label: 'Polos/campus no filtro', value: `${ind.totalPolos} de ${totalGeral}` },
    { label: 'Municípios atendidos', value: intFmt(ind.totalMunicipios) },
    { label: 'Instituições no filtro', value: intFmt(ind.totalIes) },
    { label: 'Matrículas totais', value: intFmt(ind.totalMatriculas) },
    { label: 'Matrículas por polo (média)', value: intFmt(ind.mediaMatriculasPorPolo) },
    { label: '% de polos via UAB', value: pctFmt(ind.percUab) },
  ];

  return (
    <div className="data-indicators-grid">
      {tiles.map((t) => (
        <div key={t.label} className="data-indicator-tile">
          <div className="data-indicator-value">{t.value}</div>
          <div className="data-indicator-label">{t.label}</div>
        </div>
      ))}
    </div>
  );
};

export default IndicadoresPolos;

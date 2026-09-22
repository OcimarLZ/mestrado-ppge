import React, { useMemo } from 'react';
import type { LicIesRegistro } from '../lib/licIesData';
import { calcularIndicadores } from '../lib/licIesAgregados';

const intFmt = (v: number) => Math.round(v).toLocaleString('pt-BR');
const pctFmt = (v: number) => `${v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%`;

const IndicadoresLicIES: React.FC<{ registros: LicIesRegistro[]; totalGeral: number }> = ({ registros, totalGeral }) => {
  const ind = useMemo(() => calcularIndicadores(registros), [registros]);

  const tiles = [
    { label: 'Instituições no filtro', value: `${ind.totalIes} de ${totalGeral}` },
    { label: 'Matrículas totais (2024)', value: intFmt(ind.totalMatriculas) },
    { label: 'Matrículas em licenciatura (2024)', value: intFmt(ind.totalMatriculasLic) },
    { label: '% licenciatura via UAB', value: pctFmt(ind.percLicUab) },
    { label: 'Polos UAB ativos (licenciatura)', value: intFmt(ind.totalPolosUab) },
    { label: 'Municípios com licenciatura presencial', value: intFmt(ind.totalMunPresencial) },
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

export default IndicadoresLicIES;
